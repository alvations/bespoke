"""Strategy combination backtester — backtest weighted blends of strategies.

Usage:
    from bespoke.core.combiner import backtest_combination

    result = backtest_combination(
        strategies={"spy_buy_and_hold": 0.60, "three_fund_passive": 0.40},
        start="2020-01-01", end="2025-12-31",
        initial_cash=10000,
    )
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import pandas as pd

from bespoke.core.metrics import compute_metrics
from bespoke.core.portfolio import Portfolio
from bespoke.data.fetcher import fetch_ohlcv, add_indicators
from bespoke.strategies.registry import get_strategy


def backtest_combination(
    strategies: Dict[str, float],
    start: str = "2020-01-01",
    end: Optional[str] = None,
    initial_cash: float = 100_000,
    benchmark: str = "SPY",
    rebalance_frequency: str = "monthly",
    slippage_pct: float = 0.0005,
) -> Dict[str, Any]:
    """Backtest a weighted combination of strategies as one portfolio.

    Args:
        strategies: {strategy_name: allocation_weight} e.g. {"spy_buy_and_hold": 0.60}
        start: Backtest start date
        end: Backtest end date (default: today)
        initial_cash: Starting capital
        benchmark: Benchmark symbol for comparison
        rebalance_frequency: "daily", "weekly", or "monthly"
        slippage_pct: Slippage per trade

    Returns:
        Dict with metrics, equity_curve, per-strategy contribution, etc.
    """
    # Validate weights
    total_weight = sum(strategies.values())
    if abs(total_weight - 1.0) > 0.01:
        # Normalize
        strategies = {k: v / total_weight for k, v in strategies.items()}

    # Load strategy instances
    strat_instances = {}
    all_symbols = set()
    for name in strategies:
        strat = get_strategy(name)
        strat_instances[name] = strat
        all_symbols.update(strat.universe)
    all_symbols.add(benchmark)

    # Pre-load data
    warmup_start = str(pd.Timestamp(start) - pd.DateOffset(years=1))[:10]
    data: Dict[str, pd.DataFrame] = {}
    for sym in all_symbols:
        df = fetch_ohlcv(sym, start=warmup_start, end=end)
        if df is not None and not df.empty:
            if "Adj Close" in df.columns and df["Adj Close"].notna().any():
                df["Close_Raw"] = df["Close"]
                df["Close"] = df["Adj Close"]
            df = add_indicators(df)
            data[sym] = df

    if not data:
        return _empty_result(strategies, "No data loaded")

    # Setup portfolio
    portfolio = Portfolio(initial_cash=initial_cash, slippage_pct=slippage_pct)

    # Get trading dates
    ref_sym = benchmark if benchmark in data else next(iter(data))
    ref_df = data[ref_sym]
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end) if end else ref_df.index[-1]
    trading_dates = ref_df.loc[start_ts:end_ts].index

    equity_curve = []
    contributions: Dict[str, List[float]] = {name: [] for name in strategies}
    last_rebal = None

    for date in trading_dates:
        # Get current prices
        prices = {}
        for sym, df in data.items():
            if date in df.index:
                prices[sym] = float(df.loc[date, "Close"])

        if not prices:
            continue

        # Check rebalance
        should_rebal = False
        if last_rebal is None:
            should_rebal = True
        elif rebalance_frequency == "daily":
            should_rebal = True
        elif rebalance_frequency == "weekly":
            should_rebal = (date - last_rebal).days >= 5
        elif rebalance_frequency == "monthly":
            should_rebal = date.month != last_rebal.month or date.year != last_rebal.year

        if should_rebal:
            # Combine signals from all strategies weighted by allocation
            combined_signals: Dict[str, float] = {}
            for name, alloc in strategies.items():
                strat = strat_instances[name]
                signals = strat(date, prices, portfolio.final_positions(), data)
                if signals:
                    for sym, weight in signals.items():
                        combined_signals[sym] = combined_signals.get(sym, 0) + weight * alloc

            if combined_signals:
                _rebalance(portfolio, combined_signals, prices)
                last_rebal = date

        # Record equity
        total = portfolio.total_value(prices)
        equity_curve.append({"date": date, "value": total})

        # Track per-strategy contribution (by allocation weight)
        for name, alloc in strategies.items():
            contributions[name].append(total * alloc)

    if not equity_curve:
        return _empty_result(strategies, "No trading days")

    # Build equity series
    eq_series = pd.Series(
        [e["value"] for e in equity_curve],
        index=pd.DatetimeIndex([e["date"] for e in equity_curve]),
    )

    # Benchmark
    bench_series = None
    if benchmark in data:
        bench_df = data[benchmark].loc[start_ts:end_ts]
        if not bench_df.empty:
            bench_series = bench_df["Close"] / bench_df["Close"].iloc[0] * initial_cash

    # Compute metrics
    metrics = compute_metrics(eq_series, bench_series)

    # Per-strategy contribution summary
    contrib_summary = {}
    for name, alloc in strategies.items():
        contrib_summary[name] = {
            "allocation": alloc,
            "contribution_to_final": alloc * eq_series.iloc[-1],
        }

    return {
        "strategies": dict(strategies),
        "start": start,
        "end": end or str(end_ts.date()),
        "initial_cash": initial_cash,
        "final_value": eq_series.iloc[-1],
        "metrics": metrics,
        "equity_curve": eq_series,
        "contributions": contrib_summary,
        "final_positions": portfolio.final_positions(),
        "num_trades": len(portfolio.trades),
        "benchmark": benchmark,
    }


def _rebalance(portfolio: Portfolio, signals: Dict[str, float], prices: Dict[str, float]):
    """Rebalance portfolio to match combined target signals."""
    total_value = portfolio.total_value(prices)
    if total_value <= 0:
        return

    # Normalize signals
    total_signal = sum(abs(v) for v in signals.values())
    if total_signal == 0:
        return
    weights = {sym: v / total_signal for sym, v in signals.items() if v > 0}

    # Sell positions not in target
    for sym in list(portfolio.positions.keys()):
        if sym not in weights and sym in prices:
            portfolio.sell(sym, portfolio.positions[sym].quantity, prices[sym])

    # Adjust existing and buy new
    for sym, target_w in weights.items():
        if sym not in prices:
            continue
        target_value = total_value * target_w
        current_value = 0
        if sym in portfolio.positions:
            current_value = portfolio.positions[sym].market_value(prices[sym])

        diff = target_value - current_value
        if abs(diff) < total_value * 0.01:
            continue

        if diff > 0:
            qty = diff / prices[sym]
            portfolio.buy(sym, qty, prices[sym])
        elif diff < 0 and sym in portfolio.positions:
            qty = min(abs(diff) / prices[sym], portfolio.positions[sym].quantity)
            portfolio.sell(sym, qty, prices[sym])


def _empty_result(strategies: Dict[str, float], reason: str) -> Dict[str, Any]:
    return {
        "strategies": dict(strategies),
        "error": reason,
        "metrics": {"total_return": 0, "sharpe_ratio": 0, "max_drawdown": 0},
        "final_positions": {},
        "num_trades": 0,
        "contributions": {},
    }
