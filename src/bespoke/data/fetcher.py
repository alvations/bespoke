"""Data fetcher — OHLCV data with caching and technical indicators."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


CACHE_DIR = Path.home() / ".bespoke" / "cache"


def fetch_ohlcv(
    symbol: str,
    start: str = "2015-01-01",
    end: Optional[str] = None,
    interval: str = "1d",
    cache: bool = True,
) -> Optional[pd.DataFrame]:
    """Fetch OHLCV data for a symbol.

    Uses yfinance with parquet caching.
    """
    cache_path = CACHE_DIR / f"ohlcv_{symbol.replace('^', '_')}_{interval}.parquet"

    # Try cache first
    if cache and cache_path.exists():
        try:
            df = pd.read_parquet(cache_path)
            cached_max = df.index.max()
            req_end = pd.Timestamp(end) if end else pd.Timestamp.now()

            # If cache covers the range, use it
            if cached_max >= req_end - pd.Timedelta(days=2):
                mask = df.index >= pd.Timestamp(start)
                if end:
                    mask &= df.index <= pd.Timestamp(end)
                return df.loc[mask].copy()
        except Exception:
            pass

    # Fetch from yfinance
    try:
        import yfinance as yf

        df = yf.download(
            symbol, start=start, end=end, interval=interval,
            progress=False, auto_adjust=False,
        )
        if df.empty:
            return None

        # Flatten multi-index columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Cache
        if cache:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            # Merge with existing cache
            if cache_path.exists():
                try:
                    old = pd.read_parquet(cache_path)
                    df = pd.concat([old, df]).sort_index()
                    df = df[~df.index.duplicated(keep="last")]
                except Exception:
                    pass
            df.to_parquet(cache_path)

        mask = df.index >= pd.Timestamp(start)
        if end:
            mask &= df.index <= pd.Timestamp(end)
        return df.loc[mask].copy()

    except Exception:
        return None


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add technical indicators to a DataFrame."""
    if df.empty or "Close" not in df.columns:
        return df

    df = df.copy()
    close = df["Close"]

    # Moving averages
    df["SMA_20"] = close.rolling(20).mean()
    df["SMA_50"] = close.rolling(50).mean()
    df["SMA_200"] = close.rolling(200).mean()

    # RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss.replace(0, 1e-10)
    df["RSI_14"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_signal"] = df["MACD"].ewm(span=9).mean()

    # Bollinger Bands
    sma20 = df["SMA_20"]
    std20 = close.rolling(20).std()
    df["BB_upper"] = sma20 + 2 * std20
    df["BB_lower"] = sma20 - 2 * std20

    # ATR
    if "High" in df.columns and "Low" in df.columns:
        tr = pd.concat([
            df["High"] - df["Low"],
            (df["High"] - close.shift()).abs(),
            (df["Low"] - close.shift()).abs(),
        ], axis=1).max(axis=1)
        df["ATR_14"] = tr.rolling(14).mean()

    return df
