"""Baseline strategies — benchmarks for comparing all other strategies.

Three baselines that any strategy must beat to justify its complexity:

1. SPYBuyAndHold — 100% SPY, never trade. The simplest possible strategy.
2. BalancedSixtyForty — 60% SPY + 40% AGG, rebalance monthly. Classic allocation.
3. ThreeFundPassive — 50% SPY + 30% QQQ + 20% GLD. Simple diversification.

If your strategy can't beat at least one of these on a risk-adjusted basis,
it's not worth the complexity.
"""

from __future__ import annotations

from bespoke.strategies.base import BaseStrategy, StrategyConfig


class SPYBuyAndHold(BaseStrategy):
    """100% S&P 500. The bar every strategy must clear."""

    def __init__(self):
        super().__init__(StrategyConfig(
            name="spy_buy_and_hold",
            description="100% SPY buy and hold — the simplest baseline",
            universe=["SPY"],
            benchmark="SPY",
            rebalance_frequency="monthly",
            max_positions=1,
            max_position_size=1.0,
            category="generic",
        ))

    def generate_signals(self, date, prices, portfolio, data):
        if "SPY" in prices:
            return {"SPY": 1.0}
        return {}


class BalancedSixtyForty(BaseStrategy):
    """Classic 60/40 stocks/bonds. The traditional benchmark."""

    def __init__(self):
        super().__init__(StrategyConfig(
            name="balanced_sixty_forty",
            description="60% SPY + 40% AGG — traditional balanced portfolio",
            universe=["SPY", "AGG"],
            benchmark="SPY",
            rebalance_frequency="monthly",
            max_positions=2,
            max_position_size=0.65,
            category="generic",
        ))

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        if "SPY" in prices:
            weights["SPY"] = 0.60
        if "AGG" in prices:
            weights["AGG"] = 0.40
        return weights


class ThreeFundPassive(BaseStrategy):
    """50% US equity + 30% tech + 20% gold. Simple diversification."""

    def __init__(self):
        super().__init__(StrategyConfig(
            name="three_fund_passive",
            description="50% SPY + 30% QQQ + 20% GLD — simple diversified baseline",
            universe=["SPY", "QQQ", "GLD"],
            benchmark="SPY",
            rebalance_frequency="monthly",
            max_positions=3,
            max_position_size=0.55,
            category="generic",
        ))

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        if "SPY" in prices:
            weights["SPY"] = 0.50
        if "QQQ" in prices:
            weights["QQQ"] = 0.30
        if "GLD" in prices:
            weights["GLD"] = 0.20
        return weights
