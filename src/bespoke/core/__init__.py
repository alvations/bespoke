"""Core engine — backtester, portfolio, metrics."""

from bespoke.core.backtester import Backtester
from bespoke.core.portfolio import Portfolio, Position, Trade, Side
from bespoke.core.metrics import compute_metrics, compute_composite
