"""Strategy correlation matrix -- analyze return correlations across strategies.

Usage:
    from bespoke.analysis import strategy_correlation

    matrix = strategy_correlation(
        strategies=["spy_buy_and_hold", "balanced_sixty_forty", "three_fund_passive"],
        start="2020-01-01",
    )
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import pandas as pd


def strategy_correlation(
    strategies: List[str],
    start: str = "2020-01-01",
    end: Optional[str] = None,
    initial_cash: float = 100_000,
    benchmark: str = "SPY",
    high_corr_threshold: float = 0.80,
) -> Dict[str, Any]:
    """Compute correlation matrix of strategy returns.

    Args:
        strategies: List of strategy names from registry
        start: Start date
        end: End date (default: today)
        initial_cash: Starting capital for each backtest
        benchmark: Benchmark symbol
        high_corr_threshold: Threshold for flagging high correlation pairs

    Returns:
        {
            "correlation_matrix": pd.DataFrame,
            "high_pairs": list of (strat_a, strat_b, corr) tuples,
            "low_pairs": list of low-correlation pairs (good diversifiers),
        }
    """
    from bespoke.core.backtester import Backtester
    from bespoke.strategies.registry import get_strategy

    # Run backtest for each strategy and collect equity curves
    equity_curves: Dict[str, pd.Series] = {}

    for name in strategies:
        strat = get_strategy(name)
        bt = Backtester(
            strat,
            start=start,
            end=end,
            initial_cash=initial_cash,
            benchmark=benchmark,
        )
        result = bt.run()
        if "equity_curve" in result and isinstance(result["equity_curve"], pd.Series):
            equity_curves[name] = result["equity_curve"]

    if len(equity_curves) < 2:
        return {
            "correlation_matrix": pd.DataFrame(),
            "high_pairs": [],
            "low_pairs": [],
            "error": f"Need at least 2 strategies with data, got {len(equity_curves)}",
        }

    # Convert to daily returns
    returns_df = pd.DataFrame({
        name: curve.pct_change().dropna()
        for name, curve in equity_curves.items()
    }).dropna()

    if returns_df.empty or len(returns_df) < 5:
        return {
            "correlation_matrix": pd.DataFrame(),
            "high_pairs": [],
            "low_pairs": [],
            "error": "Insufficient overlapping data for correlation",
        }

    # Compute correlation matrix
    corr_matrix = returns_df.corr()

    # Find high and low correlation pairs
    high_pairs: List[Tuple[str, str, float]] = []
    low_pairs: List[Tuple[str, str, float]] = []

    names = list(corr_matrix.columns)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            corr = corr_matrix.loc[names[i], names[j]]
            if abs(corr) >= high_corr_threshold:
                high_pairs.append((names[i], names[j], round(corr, 4)))
            elif abs(corr) < 0.30:
                low_pairs.append((names[i], names[j], round(corr, 4)))

    # Sort by correlation magnitude
    high_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    low_pairs.sort(key=lambda x: abs(x[2]))

    return {
        "correlation_matrix": corr_matrix,
        "high_pairs": high_pairs,
        "low_pairs": low_pairs,
        "num_strategies": len(equity_curves),
        "num_trading_days": len(returns_df),
    }
