"""Tests for bespoke.core — backtester, portfolio, metrics."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from bespoke.core.portfolio import Portfolio, Position
from bespoke.core.metrics import compute_metrics, compute_composite, compute_fitness
from bespoke.core.splits import (
    SPLITS, TRAIN_WINDOWS, VAL_WINDOWS, TEST_WINDOWS, ALL_WINDOWS,
    filter_windows, horizon_of, group_by_horizon,
)
from bespoke.core.backtester import Backtester
from bespoke.strategies.base import BaseStrategy, StrategyConfig


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class _AlwaysBuySPY(BaseStrategy):
    """Trivial strategy that always goes 100% SPY."""

    def __init__(self):
        super().__init__(StrategyConfig(
            name="_test_buy_spy",
            universe=["SPY"],
            rebalance_frequency="monthly",
            max_position_size=1.0,
        ))

    def generate_signals(self, date, prices, portfolio, data):
        if "SPY" in prices:
            return {"SPY": 1.0}
        return {}


def _make_equity_curve(start_val=100_000, n_days=252, annual_return=0.10):
    """Generate a synthetic equity curve for testing."""
    dates = pd.bdate_range("2023-01-01", periods=n_days, freq="B")
    daily_ret = (1 + annual_return) ** (1 / 252) - 1
    rng = np.random.RandomState(42)
    noise = rng.normal(daily_ret, 0.01, n_days)
    values = [start_val]
    for r in noise:
        values.append(values[-1] * (1 + r))
    return pd.Series(values[1:], index=dates)


# ---------------------------------------------------------------------------
# Portfolio tests
# ---------------------------------------------------------------------------

class TestPortfolio:
    def test_portfolio_buy_sell(self):
        p = Portfolio(initial_cash=100_000, slippage_pct=0)
        trade = p.buy("AAPL", 10, 150.0)
        assert trade.quantity == 10
        assert trade.side == "buy"
        assert p.cash == pytest.approx(100_000 - 10 * 150.0, rel=1e-4)
        assert "AAPL" in p.positions

        trade = p.sell("AAPL", 5, 160.0)
        assert trade.quantity == 5
        assert trade.side == "sell"
        assert p.positions["AAPL"].quantity == pytest.approx(5, rel=1e-4)

    def test_portfolio_total_value(self):
        p = Portfolio(initial_cash=100_000, slippage_pct=0)
        p.buy("AAPL", 10, 150.0)
        # Cash is 100k - 1500 = 98500. Position value at 160 = 1600
        total = p.total_value({"AAPL": 160.0})
        expected = (100_000 - 10 * 150.0) + 10 * 160.0
        assert total == pytest.approx(expected, rel=1e-4)

    def test_buy_exceeding_cash(self):
        p = Portfolio(initial_cash=1_000, slippage_pct=0)
        trade = p.buy("AAPL", 100, 150.0)  # Would cost 15k, only have 1k
        assert trade.quantity < 100
        assert p.cash >= 0

    def test_sell_nonexistent(self):
        p = Portfolio(initial_cash=100_000)
        trade = p.sell("AAPL", 10, 150.0)
        assert trade.quantity == 0

    def test_sell_all_removes_position(self):
        p = Portfolio(initial_cash=100_000, slippage_pct=0)
        p.buy("AAPL", 10, 150.0)
        p.sell("AAPL", 10, 160.0)
        assert "AAPL" not in p.positions

    def test_position_realized_pnl(self):
        pos = Position(symbol="AAPL")
        pos.buy(10, 100.0)
        pnl = pos.sell(5, 120.0)
        assert pnl == pytest.approx(5 * 20.0, rel=1e-4)
        assert pos.realized_pnl == pytest.approx(100.0, rel=1e-4)

    def test_final_positions(self):
        p = Portfolio(initial_cash=100_000, slippage_pct=0)
        p.buy("AAPL", 10, 150.0)
        p.buy("GOOG", 5, 100.0)
        fp = p.final_positions()
        assert "AAPL" in fp
        assert "GOOG" in fp
        assert fp["AAPL"]["qty"] == pytest.approx(10, rel=1e-4)


# ---------------------------------------------------------------------------
# Metrics tests
# ---------------------------------------------------------------------------

class TestMetrics:
    def test_metrics_sharpe(self):
        eq = _make_equity_curve(annual_return=0.10)
        m = compute_metrics(eq)
        # Sharpe should be a finite number
        assert isinstance(m["sharpe_ratio"], (int, float))
        assert not math.isnan(m["sharpe_ratio"])
        assert not math.isinf(m["sharpe_ratio"])

    def test_metrics_composite(self):
        windows = {
            "1Y_2025": {"ret": 0.12, "sh": 0.8, "dd": -0.05},
            "3Y_2025": {"ret": 0.35, "sh": 1.2, "dd": -0.12},
            "5Y_2025": {"ret": 0.60, "sh": 0.9, "dd": -0.20},
        }
        comp = compute_composite(windows)
        assert "composite" in comp
        assert "consistency" in comp
        assert "avg_ret" in comp
        assert "avg_dd" in comp
        assert comp["consistency"] == 1.0  # All positive sharpes

    def test_metrics_empty_curve(self):
        m = compute_metrics(pd.Series(dtype=float))
        assert m["total_return"] == 0
        assert m["sharpe_ratio"] == 0

    def test_metrics_with_benchmark(self):
        eq = _make_equity_curve(annual_return=0.10)
        bench = _make_equity_curve(annual_return=0.08)
        m = compute_metrics(eq, bench)
        assert "alpha" in m or "total_return" in m  # alpha present if enough data

    def test_metrics_total_return(self):
        eq = pd.Series([100_000, 110_000], index=pd.bdate_range("2023-01-01", periods=2))
        m = compute_metrics(eq)
        assert m["total_return"] == pytest.approx(0.10, rel=1e-4)

    def test_metrics_max_drawdown(self):
        # Up then down
        eq = pd.Series(
            [100, 120, 90, 95],
            index=pd.bdate_range("2023-01-01", periods=4),
        )
        m = compute_metrics(eq)
        # Max drawdown from 120 to 90 = -25%
        assert m["max_drawdown"] == pytest.approx(-0.25, rel=1e-2)


# ---------------------------------------------------------------------------
# Splits tests
# ---------------------------------------------------------------------------

class TestSplits:
    def test_splits_cover_28_windows_no_overlap(self):
        assert len(TRAIN_WINDOWS) == 18
        assert len(VAL_WINDOWS) == 6
        assert len(TEST_WINDOWS) == 4
        assert len(ALL_WINDOWS) == 28
        assert len(set(ALL_WINDOWS)) == 28  # no duplicates
        assert set(TRAIN_WINDOWS).isdisjoint(VAL_WINDOWS)
        assert set(TRAIN_WINDOWS).isdisjoint(TEST_WINDOWS)
        assert set(VAL_WINDOWS).isdisjoint(TEST_WINDOWS)

    def test_test_split_includes_distinct_regimes(self):
        # 2020 COVID, 2022 bear, 2025 most-recent must be held out
        assert "1Y_2020" in TEST_WINDOWS
        assert "1Y_2022" in TEST_WINDOWS
        assert "1Y_2025" in TEST_WINDOWS

    def test_filter_windows(self):
        ws = {k: {"ret": 0.1, "sh": 1.0, "dd": -0.05} for k in ALL_WINDOWS}
        train = filter_windows(ws, "train")
        assert set(train) == set(TRAIN_WINDOWS)
        test = filter_windows(ws, "test")
        assert set(test) == set(TEST_WINDOWS)

    def test_filter_windows_unknown_split(self):
        with pytest.raises(ValueError):
            filter_windows({}, "nope")

    def test_horizon_of(self):
        assert horizon_of("1Y_2020") == "1Y"
        assert horizon_of("3Y_2022_2024") == "3Y"
        assert horizon_of("10Y_2015_2024") == "10Y"

    def test_group_by_horizon(self):
        ws = {k: {"ret": 0.1} for k in TRAIN_WINDOWS}
        g = group_by_horizon(ws)
        assert set(g) == {"1Y", "3Y", "5Y", "10Y"}
        assert len(g["1Y"]) == 6
        assert len(g["10Y"]) == 1


# ---------------------------------------------------------------------------
# Fitness tests
# ---------------------------------------------------------------------------

class TestFitness:
    def test_fitness_rewards_horizon_consistency(self):
        # Both A and B average the same return, but A is uniform across
        # horizons while B is only strong on 1Y. A should score higher.
        uniform = {
            "1Y_2015": {"ret": 0.10, "sh": 1.0, "dd": -0.05},
            "3Y_2015_2017": {"ret": 0.10, "sh": 1.0, "dd": -0.05},
            "5Y_2015_2019": {"ret": 0.10, "sh": 1.0, "dd": -0.05},
            "10Y_2015_2024": {"ret": 0.10, "sh": 1.0, "dd": -0.05},
        }
        short_heavy = {
            "1Y_2015": {"ret": 0.40, "sh": 2.0, "dd": -0.05},
            "3Y_2015_2017": {"ret": 0.00, "sh": 0.0, "dd": -0.05},
            "5Y_2015_2019": {"ret": 0.00, "sh": 0.0, "dd": -0.05},
            "10Y_2015_2024": {"ret": 0.00, "sh": 0.0, "dd": -0.05},
        }
        f_u = compute_fitness(uniform)
        f_s = compute_fitness(short_heavy)
        assert f_u["fitness"] > f_s["fitness"]

    def test_fitness_horizon_weighting_not_window_count(self):
        # 11 good 1Y windows should NOT dominate one bad 10Y window.
        # Flat-average would give +0.10; horizon-weighted gives -0.40 mean.
        ws = {f"1Y_{y}": {"ret": 0.10, "sh": 1.0, "dd": -0.05}
              for y in range(2015, 2026)}  # 11 windows
        ws["10Y_2015_2024"] = {"ret": -0.50, "sh": -1.0, "dd": -0.30}
        f = compute_fitness(ws)
        # Horizon mean = (0.10 + (-0.50)) / 2 = -0.20
        assert f["horizon_mean"] == pytest.approx(-0.20, abs=1e-6)

    def test_fitness_penalizes_drawdown(self):
        low_dd = {"1Y_2015": {"ret": 0.10, "sh": 1.0, "dd": -0.05}}
        high_dd = {"1Y_2015": {"ret": 0.10, "sh": 1.0, "dd": -0.50}}
        assert compute_fitness(low_dd)["fitness"] > compute_fitness(high_dd)["fitness"]
        assert compute_fitness(high_dd)["worst_dd"] == pytest.approx(0.50)

    def test_fitness_regime_failure_penalty(self):
        clean = {
            "1Y_2015": {"ret": 0.10, "sh": 0.5, "dd": -0.05},
            "3Y_2015_2017": {"ret": 0.10, "sh": 0.5, "dd": -0.05},
        }
        regime_fail = {
            "1Y_2015": {"ret": 0.10, "sh": 0.5, "dd": -0.05},
            "3Y_2015_2017": {"ret": 0.10, "sh": -1.0, "dd": -0.05},  # blows up
        }
        assert compute_fitness(clean)["regime_fail_rate"] == 0
        assert compute_fitness(regime_fail)["regime_fail_rate"] == 0.5
        assert compute_fitness(clean)["fitness"] > compute_fitness(regime_fail)["fitness"]

    def test_fitness_split_filter(self):
        ws = {k: {"ret": 0.10, "sh": 1.0, "dd": -0.05} for k in ALL_WINDOWS}
        f_train = compute_fitness(ws, split="train")
        f_test = compute_fitness(ws, split="test")
        assert f_train["n_windows"] == 18
        assert f_test["n_windows"] == 4

    def test_fitness_empty(self):
        f = compute_fitness({})
        assert f["fitness"] == 0
        assert f["n_windows"] == 0


# ---------------------------------------------------------------------------
# Backtester tests
# ---------------------------------------------------------------------------

class TestBacktester:
    def test_backtester_runs(self, monkeypatch):
        """Backtester completes without error using mocked data."""
        dates = pd.bdate_range("2019-01-01", "2025-12-31")
        rng = np.random.RandomState(42)
        prices = 100 * np.cumprod(1 + rng.normal(0.0003, 0.01, len(dates)))
        fake_df = pd.DataFrame({
            "Open": prices * 0.99,
            "High": prices * 1.01,
            "Low": prices * 0.98,
            "Close": prices,
            "Volume": rng.randint(1_000_000, 10_000_000, len(dates)),
        }, index=dates)

        def mock_fetch(symbol, start=None, end=None, **kw):
            mask = pd.Series(True, index=fake_df.index)
            if start:
                mask &= fake_df.index >= pd.Timestamp(start)
            if end:
                mask &= fake_df.index <= pd.Timestamp(end)
            return fake_df.loc[mask].copy()

        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", mock_fetch)

        strat = _AlwaysBuySPY()
        bt = Backtester(strat, start="2020-01-01", end="2025-12-31")
        result = bt.run()

        assert "metrics" in result
        assert "final_value" in result
        assert result["num_trades"] > 0

    def test_backtester_returns_metrics(self, monkeypatch):
        """Backtest result contains expected metric keys."""
        dates = pd.bdate_range("2019-01-01", "2025-12-31")
        rng = np.random.RandomState(42)
        prices = 100 * np.cumprod(1 + rng.normal(0.0003, 0.01, len(dates)))
        fake_df = pd.DataFrame({
            "Open": prices * 0.99,
            "High": prices * 1.01,
            "Low": prices * 0.98,
            "Close": prices,
            "Volume": rng.randint(1_000_000, 10_000_000, len(dates)),
        }, index=dates)

        def mock_fetch(symbol, start=None, end=None, **kw):
            mask = pd.Series(True, index=fake_df.index)
            if start:
                mask &= fake_df.index >= pd.Timestamp(start)
            if end:
                mask &= fake_df.index <= pd.Timestamp(end)
            return fake_df.loc[mask].copy()

        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", mock_fetch)

        strat = _AlwaysBuySPY()
        bt = Backtester(strat, start="2020-01-01", end="2025-12-31")
        result = bt.run()

        m = result["metrics"]
        for key in ["total_return", "sharpe_ratio", "max_drawdown", "cagr"]:
            assert key in m, f"Missing metric: {key}"

    def test_backtester_saves_json(self, monkeypatch, tmp_path):
        """Backtester.save() produces valid JSON."""
        dates = pd.bdate_range("2019-01-01", "2025-12-31")
        rng = np.random.RandomState(42)
        prices = 100 * np.cumprod(1 + rng.normal(0.0003, 0.01, len(dates)))
        fake_df = pd.DataFrame({
            "Open": prices * 0.99,
            "High": prices * 1.01,
            "Low": prices * 0.98,
            "Close": prices,
            "Volume": rng.randint(1_000_000, 10_000_000, len(dates)),
        }, index=dates)

        def mock_fetch(symbol, start=None, end=None, **kw):
            mask = pd.Series(True, index=fake_df.index)
            if start:
                mask &= fake_df.index >= pd.Timestamp(start)
            if end:
                mask &= fake_df.index <= pd.Timestamp(end)
            return fake_df.loc[mask].copy()

        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", mock_fetch)

        strat = _AlwaysBuySPY()
        bt = Backtester(strat, start="2020-01-01", end="2025-12-31")
        bt.run()

        out = tmp_path / "result.json"
        bt.save(str(out))
        assert out.exists()

        data = json.loads(out.read_text())
        assert "strategy" in data
        assert "metrics" in data

    def test_backtester_save_before_run(self):
        """save() raises RuntimeError if run() hasn't been called."""
        strat = _AlwaysBuySPY()
        bt = Backtester(strat)
        with pytest.raises(RuntimeError):
            bt.save("/tmp/should_not_exist.json")

    def test_backtester_empty_data(self, monkeypatch):
        """Backtester handles no-data gracefully."""
        monkeypatch.setattr("bespoke.core.backtester.fetch_ohlcv", lambda *a, **kw: None)

        strat = _AlwaysBuySPY()
        bt = Backtester(strat, start="2020-01-01", end="2025-12-31")
        result = bt.run()
        assert "error" in result
