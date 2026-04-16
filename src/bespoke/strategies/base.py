"""Base strategy class — all strategies inherit from this."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import pandas as pd


@dataclass
class StrategyConfig:
    """Configuration for a strategy."""

    name: str
    description: str = ""
    universe: List[str] = field(default_factory=list)
    benchmark: str = "SPY"
    rebalance_frequency: str = "monthly"  # daily, weekly, monthly
    max_positions: int = 20
    max_position_size: float = 0.20
    risk_tolerance: float = 0.5
    category: str = "generic"


class BaseStrategy:
    """Base class for all trading strategies.

    Subclasses must implement generate_signals().
    """

    def __init__(self, config: Optional[StrategyConfig] = None, **kwargs):
        if config is not None:
            self.config = config
        else:
            self.config = StrategyConfig(
                name=kwargs.get("name", self.__class__.__name__),
                description=kwargs.get("description", ""),
                universe=kwargs.get("universe", []),
                benchmark=kwargs.get("benchmark", "SPY"),
                rebalance_frequency=kwargs.get("rebalance_frequency", "monthly"),
                max_positions=kwargs.get("max_positions", 20),
                max_position_size=kwargs.get("max_position_size", 0.20),
                category=kwargs.get("category", "generic"),
            )

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def universe(self) -> List[str]:
        return self.config.universe

    def generate_signals(
        self,
        date: pd.Timestamp,
        prices: Dict[str, float],
        portfolio: Dict,
        data: Dict[str, pd.DataFrame],
    ) -> Dict[str, float]:
        """Generate trading signals.

        Args:
            date: Current date
            prices: {symbol: current_price}
            portfolio: Current portfolio state
            data: {symbol: DataFrame with OHLCV + indicators}

        Returns:
            {symbol: weight} where weight > 0 means long
        """
        raise NotImplementedError("Subclasses must implement generate_signals()")

    def __call__(self, date, prices, portfolio, data):
        return self.generate_signals(date, prices, portfolio, data)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, universe={len(self.universe)} tickers)"
