"""Bespoke analysis tools -- entry scoring, regime detection, validation, and more."""

from bespoke.analysis.entry_scorer import score_entry
from bespoke.analysis.regime import detect_regime, regime_allocations
from bespoke.analysis.validation import walk_forward_test
from bespoke.analysis.correlation import strategy_correlation
from bespoke.analysis.stop_loss import check_stop_loss
from bespoke.analysis.benchmarks import compare_benchmarks

__all__ = [
    "score_entry",
    "detect_regime",
    "regime_allocations",
    "walk_forward_test",
    "strategy_correlation",
    "check_stop_loss",
    "compare_benchmarks",
]
