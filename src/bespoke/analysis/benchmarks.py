"""Benchmark comparison -- compare portfolio return against market benchmarks.

Usage:
    from bespoke.analysis import compare_benchmarks

    result = compare_benchmarks(
        portfolio_return=0.25,
        benchmarks=["SPY", "VT"],
        period_start="2024-01-01",
    )
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def compare_benchmarks(
    portfolio_return: float,
    benchmarks: Optional[List[str]] = None,
    period_start: str = "2024-01-01",
    period_end: Optional[str] = None,
    benchmark_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Compare a portfolio's return against one or more benchmark indices.

    Args:
        portfolio_return: Portfolio total return over the period (e.g. 0.25 for 25%)
        benchmarks: List of benchmark tickers (default: ["SPY", "VT"])
        period_start: Start of comparison period
        period_end: End of comparison period (default: today)
        benchmark_data: Optional pre-loaded benchmark returns.
                        Dict of {ticker: {"start_price": float, "end_price": float}}

    Returns:
        {
            "portfolio_return": float,
            "benchmarks": {
                "SPY": {"return": 0.20, "beating": True, "alpha": 0.05},
                ...
            },
            "beating_all": bool,
            "best_alpha": float,
        }
    """
    if benchmarks is None:
        benchmarks = ["SPY", "VT"]

    results: Dict[str, Dict[str, Any]] = {}

    for ticker in benchmarks:
        bench_return = _get_benchmark_return(ticker, period_start, period_end, benchmark_data)

        if bench_return is not None:
            alpha = portfolio_return - bench_return
            results[ticker] = {
                "return": round(bench_return, 6),
                "beating": portfolio_return > bench_return,
                "alpha": round(alpha, 6),
            }
        else:
            results[ticker] = {
                "return": None,
                "beating": None,
                "alpha": None,
                "error": f"Could not fetch data for {ticker}",
            }

    # Summary
    valid_results = {k: v for k, v in results.items() if v.get("return") is not None}
    beating_all = all(v["beating"] for v in valid_results.values()) if valid_results else False
    alphas = [v["alpha"] for v in valid_results.values() if v["alpha"] is not None]
    best_alpha = max(alphas) if alphas else 0

    return {
        "portfolio_return": portfolio_return,
        "period": f"{period_start} to {period_end or 'present'}",
        "benchmarks": results,
        "beating_all": beating_all,
        "best_alpha": round(best_alpha, 6),
    }


def _get_benchmark_return(
    ticker: str,
    start: str,
    end: Optional[str],
    pre_loaded: Optional[Dict[str, Any]] = None,
) -> Optional[float]:
    """Get total return for a benchmark over a period."""
    # Use pre-loaded data if available
    if pre_loaded and ticker in pre_loaded:
        data = pre_loaded[ticker]
        if "start_price" in data and "end_price" in data:
            if data["start_price"] > 0:
                return (data["end_price"] - data["start_price"]) / data["start_price"]
        if "return" in data:
            return data["return"]

    # Fetch via yfinance
    try:
        from bespoke.data.fetcher import fetch_ohlcv

        df = fetch_ohlcv(ticker, start=start, end=end)
        if df is None or df.empty or len(df) < 2:
            return None

        start_price = float(df["Close"].iloc[0])
        end_price = float(df["Close"].iloc[-1])

        if start_price <= 0:
            return None

        return (end_price - start_price) / start_price
    except Exception:
        return None
