"""Bespoke — trading strategy library."""

__version__ = "0.2.0"

from bespoke.core.backtester import Backtester
from bespoke.core.combiner import backtest_combination
from bespoke.strategies.base import BaseStrategy, StrategyConfig
from bespoke.strategies.registry import get_strategy, list_strategies
from bespoke.analysis.entry_scorer import score_entry
from bespoke.analysis.regime import detect_regime, regime_allocations
from bespoke.analysis.validation import walk_forward_test
from bespoke.analysis.correlation import strategy_correlation
from bespoke.analysis.stop_loss import check_stop_loss
from bespoke.analysis.benchmarks import compare_benchmarks
