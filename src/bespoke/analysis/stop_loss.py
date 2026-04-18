"""Smart stop loss -- market-aware stop loss that distinguishes crashes from thesis failure.

Usage:
    from bespoke.analysis import check_stop_loss

    result = check_stop_loss(
        symbol="AAPL", entry_price=150.0, current_price=125.0,
        stop_pct=0.15, benchmark="SPY",
    )
"""

from __future__ import annotations

from typing import Any, Dict, Optional


def check_stop_loss(
    symbol: str,
    entry_price: float,
    current_price: float,
    stop_pct: float = 0.15,
    benchmark: str = "SPY",
    benchmark_entry: Optional[float] = None,
    benchmark_current: Optional[float] = None,
    crash_threshold: float = 0.50,
) -> Dict[str, Any]:
    """Smart stop loss that distinguishes stock-specific drops from market crashes.

    Logic:
        - If the stock is down more than stop_pct AND the benchmark is roughly flat/up,
          the stock is underperforming independently -> EXIT.
        - If both the stock AND benchmark have dropped significantly,
          it's a market-wide crash -> HOLD for recovery.
        - crash_threshold: if benchmark drop accounts for >50% of stock drop, it's a crash.

    Args:
        symbol: Stock ticker
        entry_price: Price at which the position was entered
        current_price: Current stock price
        stop_pct: Stop loss percentage (default 15%)
        benchmark: Benchmark ticker (default "SPY")
        benchmark_entry: Benchmark price at entry (fetched if None)
        benchmark_current: Benchmark current price (fetched if None)
        crash_threshold: Fraction of stock loss explained by market to call it a crash

    Returns:
        {
            "action": "EXIT" | "HOLD" | "OK",
            "reason": str,
            "stock_change_pct": float,
            "benchmark_change_pct": float,
            "is_market_crash": bool,
        }
    """
    if entry_price <= 0:
        return {"action": "OK", "reason": "Invalid entry price", "error": True}

    stock_change = (current_price - entry_price) / entry_price
    stock_pct = round(stock_change * 100, 2)

    # Not at stop loss level yet
    if stock_change >= -stop_pct:
        return {
            "action": "OK",
            "reason": f"{symbol} is {stock_pct:+.1f}%, within stop loss threshold of -{stop_pct:.0%}",
            "stock_change_pct": stock_pct,
            "benchmark_change_pct": None,
            "is_market_crash": False,
        }

    # Stock has hit stop loss -- check if it's a market crash
    if benchmark_entry is None or benchmark_current is None:
        bench_prices = _fetch_benchmark_prices(benchmark)
        if benchmark_entry is None:
            benchmark_entry = bench_prices.get("entry", entry_price)
        if benchmark_current is None:
            benchmark_current = bench_prices.get("current", entry_price)

    if benchmark_entry <= 0:
        benchmark_entry = 1.0  # Avoid division by zero

    bench_change = (benchmark_current - benchmark_entry) / benchmark_entry
    bench_pct = round(bench_change * 100, 2)

    # Determine if this is a market crash or stock-specific failure
    is_crash = False
    if bench_change < 0 and stock_change < 0:
        # Both down -- check how much of the stock's drop is explained by market
        explanation_ratio = abs(bench_change) / abs(stock_change) if stock_change != 0 else 0
        is_crash = explanation_ratio >= crash_threshold

    if is_crash:
        action = "HOLD"
        reason = (
            f"Market also down {bench_pct:+.1f}% -- broad crash, not thesis failure. "
            f"Hold for recovery."
        )
    else:
        action = "EXIT"
        if bench_change >= 0:
            reason = (
                f"{symbol} down {stock_pct:+.1f}% while {benchmark} is {bench_pct:+.1f}% -- "
                f"stock-specific decline, thesis broken."
            )
        else:
            reason = (
                f"{symbol} down {stock_pct:+.1f}% vs {benchmark} down {bench_pct:+.1f}% -- "
                f"stock underperforming market significantly."
            )

    return {
        "action": action,
        "reason": reason,
        "stock_change_pct": stock_pct,
        "benchmark_change_pct": bench_pct,
        "is_market_crash": is_crash,
    }


def _fetch_benchmark_prices(benchmark: str) -> Dict[str, float]:
    """Fetch recent benchmark prices."""
    try:
        import yfinance as yf
        import pandas as pd

        df = yf.download(benchmark, period="6mo", progress=False, auto_adjust=False)
        if df.empty:
            return {}

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        return {
            "entry": float(df["Close"].iloc[0]),
            "current": float(df["Close"].iloc[-1]),
        }
    except Exception:
        return {}
