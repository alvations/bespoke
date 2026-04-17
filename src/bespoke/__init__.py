"""Bespoke — trading strategy library."""

__version__ = "0.1.4"

from bespoke.core.backtester import Backtester
from bespoke.strategies.base import BaseStrategy, StrategyConfig
from bespoke.strategies.registry import get_strategy, list_strategies
