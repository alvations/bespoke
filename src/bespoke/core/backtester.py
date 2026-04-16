"""Backtester — runs a strategy against historical data."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from bespoke.core.metrics import compute_metrics
from bespoke.core.portfolio import Portfolio
from bespoke.data.fetcher import fetch_ohlcv, add_indicators
from bespoke.strategies.base import BaseStrategy


class Backtester:
    """Run a strategy against historical data and produce results.

    Usage:
        from bespoke import Backtester
        from bespoke.strategies import get_strategy

        strategy = get_strategy("momentum")
        bt = Backtester(strategy, start="2020-01-01", end="2025-12-31")
        result = bt.run()
        print(result["metrics"]["sharpe_ratio"])
        bt.save("results/momentum_backtest.json")
    """

    def __init__(
        self,
        strategy: BaseStrategy,
        start: str = "2020-01-01",
        end: Optional[str] = None,
        initial_cash: float = 100_000,
        benchmark: str = "SPY",
        slippage_pct: float = 0.0005,
    ):
        self.strategy = strategy
        self.start = start
        self.end = end
        self.initial_cash = initial_cash
        self.benchmark = benchmark
        self.slippage_pct = slippage_pct
        self._result = None

    def _load_data(self) -> Dict[str, pd.DataFrame]:
        """Load OHLCV data for all symbols + benchmark."""
        symbols = list(set(self.strategy.universe + [self.benchmark]))
        # Pre-load 1 year before start for indicator warmup
        warmup_start = str(
            pd.Timestamp(self.start) - pd.DateOffset(years=1)
        )[:10]

        data = {}
        for sym in symbols:
            df = fetch_ohlcv(sym, start=warmup_start, end=self.end)
            if df is not None and not df.empty:
                # Use Adj Close for dividend-adjusted returns
                if "Adj Close" in df.columns and df["Adj Close"].notna().any():
                    df["Close_Raw"] = df["Close"]
                    df["Close"] = df["Adj Close"]
                df = add_indicators(df)
                data[sym] = df
        return data

    def run(self) -> Dict[str, Any]:
        """Run the backtest and return results."""
        data = self._load_data()
        if not data:
            return self._empty_result("No data loaded")

        portfolio = Portfolio(
            initial_cash=self.initial_cash,
            slippage_pct=self.slippage_pct,
        )

        # Get trading dates from benchmark or first available symbol
        ref_sym = self.benchmark if self.benchmark in data else next(iter(data))
        ref_df = data[ref_sym]
        start_ts = pd.Timestamp(self.start)
        end_ts = pd.Timestamp(self.end) if self.end else ref_df.index[-1]
        trading_dates = ref_df.loc[start_ts:end_ts].index

        rebal_freq = self.strategy.config.rebalance_frequency
        equity_curve = []
        last_rebal = None

        for date in trading_dates:
            # Get current prices
            prices = {}
            for sym, df in data.items():
                if date in df.index:
                    prices[sym] = float(df.loc[date, "Close"])

            if not prices:
                continue

            # Check if we should rebalance
            should_rebal = False
            if last_rebal is None:
                should_rebal = True
            elif rebal_freq == "daily":
                should_rebal = True
            elif rebal_freq == "weekly":
                should_rebal = (date - last_rebal).days >= 5
            elif rebal_freq == "monthly":
                should_rebal = date.month != last_rebal.month or date.year != last_rebal.year

            if should_rebal:
                # Get strategy signals
                signals = self.strategy(date, prices, portfolio.final_positions(), data)

                if signals:
                    self._rebalance(portfolio, signals, prices)
                    last_rebal = date

            # Record equity
            total = portfolio.total_value(prices)
            equity_curve.append({"date": date, "value": total})

        if not equity_curve:
            return self._empty_result("No trading days")

        # Build equity series
        eq_series = pd.Series(
            [e["value"] for e in equity_curve],
            index=pd.DatetimeIndex([e["date"] for e in equity_curve]),
        )

        # Benchmark
        bench_series = None
        if self.benchmark in data:
            bench_df = data[self.benchmark].loc[start_ts:end_ts]
            if not bench_df.empty:
                bench_series = bench_df["Close"] / bench_df["Close"].iloc[0] * self.initial_cash

        # Compute metrics
        metrics = compute_metrics(eq_series, bench_series)

        self._result = {
            "strategy": self.strategy.name,
            "start": self.start,
            "end": self.end or str(end_ts.date()),
            "initial_cash": self.initial_cash,
            "final_value": eq_series.iloc[-1],
            "metrics": metrics,
            "final_positions": portfolio.final_positions(),
            "num_trades": len(portfolio.trades),
            "equity_curve": eq_series,
            "benchmark": self.benchmark,
        }
        return self._result

    def _rebalance(self, portfolio: Portfolio, signals: Dict[str, float], prices: Dict[str, float]):
        """Rebalance portfolio to match target signals."""
        total_value = portfolio.total_value(prices)
        if total_value <= 0:
            return

        # Normalize signals to weights
        total_signal = sum(abs(v) for v in signals.values())
        if total_signal == 0:
            return
        weights = {sym: v / total_signal for sym, v in signals.items() if v > 0}

        # Cap individual positions
        max_w = self.strategy.config.max_position_size
        for sym in weights:
            weights[sym] = min(weights[sym], max_w)

        # Re-normalize after capping
        total_w = sum(weights.values())
        if total_w > 1:
            weights = {sym: w / total_w for sym, w in weights.items()}

        # Sell positions not in target
        for sym in list(portfolio.positions.keys()):
            if sym not in weights and sym in prices:
                portfolio.sell(sym, portfolio.positions[sym].quantity, prices[sym])

        # Adjust existing positions and buy new ones
        for sym, target_w in weights.items():
            if sym not in prices:
                continue
            target_value = total_value * target_w
            current_value = 0
            if sym in portfolio.positions:
                current_value = portfolio.positions[sym].market_value(prices[sym])

            diff = target_value - current_value
            if abs(diff) < total_value * 0.01:  # Skip small rebalances
                continue

            if diff > 0:
                qty = diff / prices[sym]
                portfolio.buy(sym, qty, prices[sym])
            elif diff < 0 and sym in portfolio.positions:
                qty = min(abs(diff) / prices[sym], portfolio.positions[sym].quantity)
                portfolio.sell(sym, qty, prices[sym])

    def save(self, path: str) -> Path:
        """Save backtest results to JSON."""
        if self._result is None:
            raise RuntimeError("Run the backtest first")

        result = {k: v for k, v in self._result.items() if k != "equity_curve"}
        # Convert non-serializable types
        result["final_positions"] = {
            sym: {k: round(v, 4) if isinstance(v, float) else v for k, v in pos.items()}
            for sym, pos in result["final_positions"].items()
        }

        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(result, indent=2, default=str))
        return p

    def _empty_result(self, reason: str) -> Dict[str, Any]:
        return {
            "strategy": self.strategy.name,
            "start": self.start,
            "end": self.end,
            "error": reason,
            "metrics": {
                "total_return": 0, "sharpe_ratio": 0, "max_drawdown": 0,
            },
            "final_positions": {},
            "num_trades": 0,
        }
