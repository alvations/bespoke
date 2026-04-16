"""Performance metrics calculations."""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd


def compute_metrics(
    equity_curve: pd.Series,
    benchmark_curve: Optional[pd.Series] = None,
    risk_free_rate: float = 0.05,
) -> Dict[str, Any]:
    """Compute strategy performance metrics from an equity curve.

    Args:
        equity_curve: Daily portfolio values indexed by date
        benchmark_curve: Optional benchmark values for alpha/beta
        risk_free_rate: Annual risk-free rate (default 5%)

    Returns:
        Dict with total_return, cagr, sharpe_ratio, max_drawdown, etc.
    """
    if equity_curve.empty or len(equity_curve) < 2:
        return _empty_metrics()

    returns = equity_curve.pct_change().dropna()
    if returns.empty:
        return _empty_metrics()

    # Basic returns
    total_return = (equity_curve.iloc[-1] / equity_curve.iloc[0]) - 1
    n_days = (equity_curve.index[-1] - equity_curve.index[0]).days
    years = max(n_days / 365.25, 0.01)
    cagr = (1 + total_return) ** (1 / years) - 1

    # Risk
    annual_vol = returns.std() * np.sqrt(252)
    daily_rf = (1 + risk_free_rate) ** (1 / 252) - 1
    excess = returns - daily_rf
    sharpe = (excess.mean() / excess.std() * np.sqrt(252)) if excess.std() > 0 else 0

    # Sortino (downside deviation)
    downside = returns[returns < 0]
    downside_std = downside.std() * np.sqrt(252) if len(downside) > 0 else 0.0001
    sortino = (returns.mean() * 252 - risk_free_rate) / downside_std if downside_std > 0 else 0

    # Drawdown
    cummax = equity_curve.cummax()
    drawdown = (equity_curve - cummax) / cummax
    max_drawdown = drawdown.min()
    max_dd_date = drawdown.idxmin() if not drawdown.empty else None

    # Calmar
    calmar = cagr / abs(max_drawdown) if max_drawdown != 0 else 0

    # Win rate
    win_rate = (returns > 0).sum() / len(returns) if len(returns) > 0 else 0

    # Profit factor
    gains = returns[returns > 0].sum()
    losses = abs(returns[returns < 0].sum())
    profit_factor = gains / losses if losses > 0 else float("inf")

    metrics = {
        "total_return": _safe(total_return),
        "cagr": _safe(cagr),
        "annual_volatility": _safe(annual_vol),
        "sharpe_ratio": _safe(sharpe),
        "sortino_ratio": _safe(sortino),
        "calmar_ratio": _safe(calmar),
        "max_drawdown": _safe(max_drawdown),
        "max_drawdown_date": str(max_dd_date) if max_dd_date else None,
        "win_rate": _safe(win_rate),
        "profit_factor": _safe(profit_factor),
        "num_trading_days": len(returns),
    }

    # Alpha/beta if benchmark provided
    if benchmark_curve is not None and len(benchmark_curve) > 1:
        bench_returns = benchmark_curve.pct_change().dropna()
        aligned = pd.concat([returns, bench_returns], axis=1).dropna()
        if len(aligned) > 10:
            aligned.columns = ["strategy", "benchmark"]
            cov = np.cov(aligned["strategy"], aligned["benchmark"])
            beta = cov[0, 1] / cov[1, 1] if cov[1, 1] != 0 else 0
            alpha = (returns.mean() - beta * bench_returns.mean()) * 252
            metrics["alpha"] = _safe(alpha)
            metrics["beta"] = _safe(beta)

    return metrics


def compute_composite(
    windows: Dict[str, Dict[str, float]],
    window_keys: Optional[List[str]] = None,
) -> Dict[str, float]:
    """Compute composite score from rolling window results.

    Args:
        windows: {window_name: {ret, sh, dd}}
        window_keys: Optional subset of windows to use (default: all)

    Returns:
        {composite, consistency, avg_ret, avg_dd}
    """
    if window_keys:
        w = {k: v for k, v in windows.items() if k in window_keys}
    else:
        w = windows

    if not w:
        return {"composite": 0, "consistency": 0, "avg_ret": 0, "avg_dd": 0}

    sharpes = [v.get("sh", 0) for v in w.values()]
    rets = [v.get("ret", 0) for v in w.values()]
    dds = [abs(v.get("dd", 0)) for v in w.values()]

    consistency = sum(1 for s in sharpes if s > 0) / len(sharpes)
    avg_ret = sum(rets) / len(rets)
    avg_dd = sum(dds) / len(dds)
    composite = avg_ret * consistency * (1 - avg_dd)

    return {
        "composite": round(composite, 4),
        "consistency": round(consistency, 2),
        "avg_ret": round(avg_ret, 4),
        "avg_dd": round(avg_dd, 4),
    }


def _safe(v):
    """Return 0 if value is NaN or inf."""
    if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
        return 0
    return round(v, 6)


def _empty_metrics() -> Dict[str, Any]:
    return {
        "total_return": 0, "cagr": 0, "annual_volatility": 0,
        "sharpe_ratio": 0, "sortino_ratio": 0, "calmar_ratio": 0,
        "max_drawdown": 0, "max_drawdown_date": None,
        "win_rate": 0, "profit_factor": 0, "num_trading_days": 0,
    }
