"""Walk-forward validation -- test for overfitting by comparing train vs test performance.

Usage:
    from bespoke.analysis import walk_forward_test

    result = walk_forward_test(
        strategies={"spy_buy_and_hold": 0.60, "balanced_sixty_forty": 0.40},
        train_end="2022-12-31",
        test_start="2023-01-01",
    )
"""

from __future__ import annotations

from typing import Any, Dict, Optional


def walk_forward_test(
    strategies: Dict[str, float],
    train_end: str = "2022-12-31",
    test_start: str = "2023-01-01",
    train_start: str = "2015-01-01",
    test_end: Optional[str] = None,
    initial_cash: float = 100_000,
    benchmark: str = "SPY",
    overfit_threshold: float = 0.50,
) -> Dict[str, Any]:
    """Run walk-forward validation: train on one period, test on another.

    Flags OVERFIT if test Sharpe < overfit_threshold * train Sharpe.

    Args:
        strategies: {strategy_name: allocation_weight}
        train_end: End of training period
        test_start: Start of test period
        train_start: Start of training period (default: 2015-01-01)
        test_end: End of test period (default: today)
        initial_cash: Starting capital
        benchmark: Benchmark symbol
        overfit_threshold: Flag as overfit if test_sharpe / train_sharpe < this

    Returns:
        {
            "train_metrics": dict,
            "test_metrics": dict,
            "overfit_assessment": str,
            "sharpe_ratio_decay": float,
        }
    """
    from bespoke.core.combiner import backtest_combination

    # Run training period backtest
    train_result = backtest_combination(
        strategies=strategies,
        start=train_start,
        end=train_end,
        initial_cash=initial_cash,
        benchmark=benchmark,
    )

    # Run test period backtest
    test_result = backtest_combination(
        strategies=strategies,
        start=test_start,
        end=test_end,
        initial_cash=initial_cash,
        benchmark=benchmark,
    )

    train_metrics = train_result.get("metrics", {})
    test_metrics = test_result.get("metrics", {})

    train_sharpe = train_metrics.get("sharpe_ratio", 0)
    test_sharpe = test_metrics.get("sharpe_ratio", 0)

    # Compute Sharpe decay
    if train_sharpe > 0:
        sharpe_ratio = test_sharpe / train_sharpe
    elif train_sharpe == 0:
        sharpe_ratio = 1.0 if test_sharpe >= 0 else 0.0
    else:
        # Negative train Sharpe -- if test is also negative, not necessarily overfit
        sharpe_ratio = 1.0

    # Assessment
    if train_sharpe <= 0:
        assessment = "INCONCLUSIVE: Train Sharpe non-positive, cannot assess overfitting"
    elif sharpe_ratio >= 0.80:
        assessment = "ROBUST: Test performance closely matches training"
    elif sharpe_ratio >= overfit_threshold:
        assessment = "ACCEPTABLE: Some performance decay but within tolerance"
    else:
        assessment = f"OVERFIT: Test Sharpe ({test_sharpe:.2f}) < {overfit_threshold:.0%} of train Sharpe ({train_sharpe:.2f})"

    return {
        "strategies": dict(strategies),
        "train_period": f"{train_start} to {train_end}",
        "test_period": f"{test_start} to {test_end or 'present'}",
        "train_metrics": train_metrics,
        "test_metrics": test_metrics,
        "train_sharpe": train_sharpe,
        "test_sharpe": test_sharpe,
        "sharpe_ratio_decay": round(sharpe_ratio, 4),
        "overfit_assessment": assessment,
    }
