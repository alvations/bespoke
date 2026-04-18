"""Entry scoring — rate a stock entry opportunity 0-100 across 7 factors.

Usage:
    from bespoke.analysis import score_entry
    result = score_entry("AAPL")
    # Returns: {"score": 65, "signal": "BUY", "breakdown": {...}}
"""

from __future__ import annotations

from typing import Any, Dict, Optional


def score_entry(
    symbol: str,
    data: Optional[Any] = None,
) -> Dict[str, Any]:
    """Score an entry opportunity for a symbol on a scale of 0-100.

    Factors (max 100):
        +20: Price above SMA50 (trend confirmed)
        +20: RSI 30-45 (pullback zone)
        +15: Within 5% of SMA50 (near support)
        +15: Volume > 1.5x 20-day average
        +10: MACD crossing above signal
        +10: Above SMA200 (long-term uptrend)
        +10: Recent pullback 3-10% from 20-day high

    Args:
        symbol: Ticker symbol (e.g. "AAPL")
        data: Optional pre-loaded DataFrame with OHLCV + indicators.
              If None, fetches via yfinance internally.

    Returns:
        {"score": int, "signal": str, "breakdown": dict}
    """
    import pandas as pd

    if data is None:
        data = _fetch_data(symbol)

    if data is None or data.empty or len(data) < 50:
        return {"score": 0, "signal": "WAIT", "breakdown": {}, "error": "Insufficient data"}

    # Add indicators if missing
    if "SMA_50" not in data.columns:
        from bespoke.data.fetcher import add_indicators
        data = add_indicators(data)

    latest = data.iloc[-1]
    close = float(latest["Close"])

    breakdown = {}
    score = 0

    # Factor 1: Price above SMA50 (+20)
    sma50 = _safe_float(latest, "SMA_50")
    if sma50 is not None and close > sma50:
        score += 20
        breakdown["above_sma50"] = {"points": 20, "detail": f"Close {close:.2f} > SMA50 {sma50:.2f}"}
    else:
        breakdown["above_sma50"] = {"points": 0, "detail": f"Close {close:.2f} <= SMA50 {sma50:.2f}" if sma50 else "SMA50 unavailable"}

    # Factor 2: RSI in pullback zone 30-45 (+20)
    rsi = _safe_float(latest, "RSI_14")
    if rsi is not None and 30 <= rsi <= 45:
        score += 20
        breakdown["rsi_pullback"] = {"points": 20, "detail": f"RSI {rsi:.1f} in pullback zone [30-45]"}
    else:
        breakdown["rsi_pullback"] = {"points": 0, "detail": f"RSI {rsi:.1f} outside pullback zone" if rsi else "RSI unavailable"}

    # Factor 3: Within 5% of SMA50 (+15)
    if sma50 is not None and sma50 > 0:
        pct_from_sma50 = abs(close - sma50) / sma50
        if pct_from_sma50 <= 0.05:
            score += 15
            breakdown["near_sma50"] = {"points": 15, "detail": f"{pct_from_sma50:.1%} from SMA50 (within 5%)"}
        else:
            breakdown["near_sma50"] = {"points": 0, "detail": f"{pct_from_sma50:.1%} from SMA50 (>5%)"}
    else:
        breakdown["near_sma50"] = {"points": 0, "detail": "SMA50 unavailable"}

    # Factor 4: Volume > 1.5x 20-day average (+15)
    if "Volume" in data.columns and len(data) >= 20:
        vol = float(latest["Volume"])
        avg_vol = float(data["Volume"].iloc[-20:].mean())
        if avg_vol > 0 and vol > 1.5 * avg_vol:
            score += 15
            ratio = vol / avg_vol
            breakdown["high_volume"] = {"points": 15, "detail": f"Volume {ratio:.1f}x above 20-day avg"}
        else:
            ratio = vol / avg_vol if avg_vol > 0 else 0
            breakdown["high_volume"] = {"points": 0, "detail": f"Volume {ratio:.1f}x (need >1.5x)"}
    else:
        breakdown["high_volume"] = {"points": 0, "detail": "Volume data unavailable"}

    # Factor 5: MACD crossing above signal (+10)
    macd = _safe_float(latest, "MACD")
    macd_signal = _safe_float(latest, "MACD_signal")
    if macd is not None and macd_signal is not None:
        # Check current and previous for crossover
        if len(data) >= 2:
            prev = data.iloc[-2]
            prev_macd = _safe_float(prev, "MACD")
            prev_signal = _safe_float(prev, "MACD_signal")
            if prev_macd is not None and prev_signal is not None:
                if macd > macd_signal and prev_macd <= prev_signal:
                    score += 10
                    breakdown["macd_cross"] = {"points": 10, "detail": "MACD just crossed above signal"}
                elif macd > macd_signal:
                    # Already above but not fresh cross — give partial recognition
                    score += 5
                    breakdown["macd_cross"] = {"points": 5, "detail": "MACD above signal (no fresh cross)"}
                else:
                    breakdown["macd_cross"] = {"points": 0, "detail": "MACD below signal"}
            else:
                breakdown["macd_cross"] = {"points": 0, "detail": "Previous MACD data unavailable"}
        else:
            breakdown["macd_cross"] = {"points": 0, "detail": "Need 2+ days for crossover check"}
    else:
        breakdown["macd_cross"] = {"points": 0, "detail": "MACD unavailable"}

    # Factor 6: Above SMA200 (+10)
    sma200 = _safe_float(latest, "SMA_200")
    if sma200 is not None and close > sma200:
        score += 10
        breakdown["above_sma200"] = {"points": 10, "detail": f"Close {close:.2f} > SMA200 {sma200:.2f}"}
    else:
        breakdown["above_sma200"] = {"points": 0, "detail": f"Close {close:.2f} <= SMA200 {sma200:.2f}" if sma200 else "SMA200 unavailable"}

    # Factor 7: Recent pullback 3-10% from 20-day high (+10)
    if len(data) >= 20:
        high_20 = float(data["Close"].iloc[-20:].max())
        if high_20 > 0:
            pullback_pct = (high_20 - close) / high_20
            if 0.03 <= pullback_pct <= 0.10:
                score += 10
                breakdown["recent_pullback"] = {"points": 10, "detail": f"{pullback_pct:.1%} pullback from 20-day high"}
            else:
                breakdown["recent_pullback"] = {"points": 0, "detail": f"{pullback_pct:.1%} pullback (need 3-10%)"}
        else:
            breakdown["recent_pullback"] = {"points": 0, "detail": "20-day high is zero"}
    else:
        breakdown["recent_pullback"] = {"points": 0, "detail": "Need 20+ days for pullback check"}

    # Determine signal
    if score >= 75:
        signal = "STRONG BUY"
    elif score >= 50:
        signal = "BUY"
    elif score >= 30:
        signal = "WEAK BUY"
    else:
        signal = "WAIT"

    return {
        "score": score,
        "signal": signal,
        "breakdown": breakdown,
        "symbol": symbol,
    }


def _safe_float(row, col: str) -> Optional[float]:
    """Safely extract a float from a row, handling NaN and missing columns."""
    import pandas as pd

    try:
        val = row[col]
        if isinstance(val, pd.Series):
            val = val.iloc[-1]
        if pd.isna(val):
            return None
        return float(val)
    except (KeyError, IndexError, TypeError):
        return None


def _fetch_data(symbol: str, period: str = "6mo"):
    """Fetch data for scoring via yfinance."""
    try:
        import yfinance as yf
        import pandas as pd

        df = yf.download(symbol, period=period, progress=False, auto_adjust=False)
        if df.empty:
            return None

        # Flatten multi-index columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        from bespoke.data.fetcher import add_indicators
        df = add_indicators(df)
        return df
    except Exception:
        return None
