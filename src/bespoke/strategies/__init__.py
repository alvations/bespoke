"""Strategy module — auto-discovers and registers all strategies."""

from bespoke.strategies.base import BaseStrategy, StrategyConfig
from bespoke.strategies.registry import get_strategy, list_strategies, register_strategy, strategy_names
