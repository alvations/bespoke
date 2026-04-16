"""Tests for bespoke.strategies — registry, base class, baselines."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from bespoke.strategies.base import BaseStrategy, StrategyConfig
from bespoke.strategies.registry import get_strategy, list_strategies, strategy_names
from bespoke.core.backtester import Backtester


class TestRegistry:
    def test_list_strategies(self):
        """At least 3 baseline strategies are registered."""
        names = strategy_names()
        assert len(names) >= 3
        assert "spy_buy_and_hold" in names
        assert "balanced_sixty_forty" in names
        assert "three_fund_passive" in names

    def test_get_strategy(self):
        """get_strategy returns a BaseStrategy instance."""
        strat = get_strategy("spy_buy_and_hold")
        assert isinstance(strat, BaseStrategy)
        assert strat.name == "spy_buy_and_hold"

    def test_get_strategy_missing(self):
        """get_strategy raises KeyError for unknown names."""
        with pytest.raises(KeyError):
            get_strategy("nonexistent_strategy_xyz_12345")

    def test_strategy_has_generate_signals(self):
        """Every registered strategy has a callable generate_signals."""
        for strat in list_strategies():
            assert hasattr(strat, "generate_signals")
            assert callable(strat.generate_signals)

    def test_strategy_is_callable(self):
        """Strategies can be called directly (via __call__)."""
        strat = get_strategy("spy_buy_and_hold")
        date = pd.Timestamp("2023-06-15")
        prices = {"SPY": 450.0}
        signals = strat(date, prices, {}, {})
        assert isinstance(signals, dict)

    def test_strategy_config_fields(self):
        """Each strategy has required config fields."""
        for strat in list_strategies():
            assert strat.config.name
            assert strat.config.rebalance_frequency in ("daily", "weekly", "monthly")
            assert isinstance(strat.config.max_positions, int)
            assert 0 < strat.config.max_position_size <= 1.0


class TestBaselines:
    def test_spy_buy_and_hold_signals(self):
        strat = get_strategy("spy_buy_and_hold")
        signals = strat.generate_signals(
            pd.Timestamp("2023-01-01"), {"SPY": 400.0}, {}, {},
        )
        assert signals == {"SPY": 1.0}

    def test_balanced_sixty_forty_signals(self):
        strat = get_strategy("balanced_sixty_forty")
        signals = strat.generate_signals(
            pd.Timestamp("2023-01-01"),
            {"SPY": 400.0, "AGG": 100.0},
            {}, {},
        )
        assert signals["SPY"] == pytest.approx(0.60)
        assert signals["AGG"] == pytest.approx(0.40)

    def test_three_fund_passive_signals(self):
        strat = get_strategy("three_fund_passive")
        signals = strat.generate_signals(
            pd.Timestamp("2023-01-01"),
            {"SPY": 400.0, "QQQ": 350.0, "GLD": 180.0},
            {}, {},
        )
        assert signals["SPY"] == pytest.approx(0.50)
        assert signals["QQQ"] == pytest.approx(0.30)
        assert signals["GLD"] == pytest.approx(0.20)

    def test_baseline_backtest_returns_positive(self, monkeypatch):
        """Baselines should produce positive returns on synthetic upward data."""
        dates = pd.bdate_range("2019-01-01", "2025-12-31")
        rng = np.random.RandomState(42)
        # Upward trending market
        prices = 100 * np.cumprod(1 + rng.normal(0.0004, 0.008, len(dates)))
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

        strat = get_strategy("spy_buy_and_hold")
        bt = Backtester(strat, start="2020-01-01", end="2025-12-31")
        result = bt.run()
        assert result["metrics"]["total_return"] > 0


class TestBaseStrategy:
    def test_subclass_must_implement_generate_signals(self):
        """BaseStrategy raises NotImplementedError if not overridden."""

        class Incomplete(BaseStrategy):
            pass

        strat = Incomplete(name="incomplete", universe=["SPY"])
        with pytest.raises(NotImplementedError):
            strat.generate_signals(pd.Timestamp("2023-01-01"), {}, {}, {})

    def test_custom_strategy(self):
        """A custom subclass works correctly."""

        class MyStrat(BaseStrategy):
            def __init__(self):
                super().__init__(StrategyConfig(
                    name="my_custom",
                    universe=["AAPL"],
                    max_position_size=1.0,
                ))

            def generate_signals(self, date, prices, portfolio, data):
                return {"AAPL": 1.0} if "AAPL" in prices else {}

        strat = MyStrat()
        assert strat.name == "my_custom"
        assert strat.universe == ["AAPL"]
        signals = strat(pd.Timestamp("2023-01-01"), {"AAPL": 150.0}, {}, {})
        assert signals == {"AAPL": 1.0}

    def test_repr(self):
        strat = get_strategy("spy_buy_and_hold")
        r = repr(strat)
        assert "spy_buy_and_hold" in r
