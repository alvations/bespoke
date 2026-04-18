"""Regime detection -- detect market regime from VIX + SPY trend.

Usage:
    from bespoke.analysis import detect_regime, regime_allocations

    regime = detect_regime()  # "bull", "cautious", "fear", or "panic"
    alloc = regime_allocations()  # allocation dict per regime
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import pandas as pd


# Regime thresholds
_REGIMES = {
    "panic": {"vix_min": 35, "vix_max": float("inf")},
    "fear": {"vix_min": 25, "vix_max": 35},
    "cautious": {"vix_min": 20, "vix_max": 25},
    "bull": {"vix_min": 0, "vix_max": 20},
}

# Suggested allocations per regime (equities / bonds / cash)
_ALLOCATIONS = {
    "bull": {"equities": 0.80, "bonds": 0.15, "cash": 0.05},
    "cautious": {"equities": 0.60, "bonds": 0.25, "cash": 0.15},
    "fear": {"equities": 0.35, "bonds": 0.30, "cash": 0.35},
    "panic": {"equities": 0.15, "bonds": 0.25, "cash": 0.60},
}


def detect_regime(
    vix_data: Optional[pd.DataFrame] = None,
    spy_data: Optional[pd.DataFrame] = None,
) -> Dict[str, Any]:
    """Detect current market regime from VIX level and SPY trend.

    Regimes:
        - "bull":     VIX < 20 and SPY > SMA200
        - "cautious": VIX 20-25
        - "fear":     VIX 25-35
        - "panic":    VIX > 35

    Args:
        vix_data: Optional pre-loaded VIX DataFrame. If None, fetches via yfinance.
        spy_data: Optional pre-loaded SPY DataFrame. If None, fetches via yfinance.

    Returns:
        {
            "regime": str,
            "vix": float,
            "spy_above_sma200": bool,
            "spy_price": float,
            "spy_sma200": float,
            "description": str,
        }
    """
    if vix_data is None or spy_data is None:
        fetched = _fetch_regime_data()
        if vix_data is None:
            vix_data = fetched.get("vix")
        if spy_data is None:
            spy_data = fetched.get("spy")

    # Get current VIX
    vix_level = _get_latest_close(vix_data)
    if vix_level is None:
        return {"regime": "cautious", "error": "VIX data unavailable", "vix": None}

    # Get SPY trend
    spy_price = _get_latest_close(spy_data)
    spy_sma200 = _get_sma200(spy_data)
    spy_above_sma200 = (spy_price is not None and spy_sma200 is not None and spy_price > spy_sma200)

    # Determine regime by VIX level
    if vix_level > 35:
        regime = "panic"
    elif vix_level > 25:
        regime = "fear"
    elif vix_level > 20:
        regime = "cautious"
    else:
        # VIX < 20, but check SPY trend
        if spy_above_sma200:
            regime = "bull"
        else:
            regime = "cautious"  # Low VIX but weak trend

    descriptions = {
        "bull": "Low volatility, strong uptrend. Favor equities.",
        "cautious": "Moderate volatility or weakening trend. Reduce risk.",
        "fear": "Elevated volatility. Defensive positioning.",
        "panic": "Extreme volatility. Preserve capital.",
    }

    return {
        "regime": regime,
        "vix": round(vix_level, 2),
        "spy_above_sma200": spy_above_sma200,
        "spy_price": round(spy_price, 2) if spy_price else None,
        "spy_sma200": round(spy_sma200, 2) if spy_sma200 else None,
        "description": descriptions[regime],
    }


def regime_allocations(regime: Optional[str] = None) -> Dict[str, Any]:
    """Get suggested allocations for a regime.

    Args:
        regime: One of "bull", "cautious", "fear", "panic".
                If None, detects current regime first.

    Returns:
        {"regime": str, "allocations": {"equities": float, "bonds": float, "cash": float}}
    """
    if regime is None:
        detected = detect_regime()
        regime = detected["regime"]

    if regime not in _ALLOCATIONS:
        regime = "cautious"

    return {
        "regime": regime,
        "allocations": dict(_ALLOCATIONS[regime]),
    }


def _get_latest_close(df: Optional[pd.DataFrame]) -> Optional[float]:
    """Get the most recent Close price from a DataFrame."""
    if df is None or df.empty:
        return None
    try:
        val = df["Close"].iloc[-1]
        if pd.isna(val):
            return None
        return float(val)
    except (KeyError, IndexError):
        return None


def _get_sma200(df: Optional[pd.DataFrame]) -> Optional[float]:
    """Get the current SMA200 from a DataFrame."""
    if df is None or df.empty or len(df) < 200:
        return None
    try:
        sma = df["Close"].rolling(200).mean().iloc[-1]
        if pd.isna(sma):
            return None
        return float(sma)
    except (KeyError, IndexError):
        return None


def _fetch_regime_data() -> Dict[str, Optional[pd.DataFrame]]:
    """Fetch VIX and SPY data via yfinance."""
    result: Dict[str, Optional[pd.DataFrame]] = {"vix": None, "spy": None}
    try:
        import yfinance as yf

        for key, symbol in [("vix", "^VIX"), ("spy", "SPY")]:
            try:
                df = yf.download(symbol, period="1y", progress=False, auto_adjust=False)
                if not df.empty:
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = df.columns.get_level_values(0)
                    result[key] = df
            except Exception:
                pass
    except ImportError:
        pass

    return result
