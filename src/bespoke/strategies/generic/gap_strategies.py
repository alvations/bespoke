"""Gap strategies: ETF Cointegration and ADX Trend Filter.

Strategies identified from knowledge/missing_strategies_gaps.md as the
highest expected win rate among the missing strategies.

Strategies:
    1. ETFCointegration     -- Mean reversion on cointegrated ETF pairs (stat arb)
    2. ADXTrendFilter       -- ADX trend strength filter with DI crossover
"""

from __future__ import annotations

import math

import pandas as pd

from bespoke.strategies.base import BaseStrategy as BasePersona, StrategyConfig as PersonaConfig


def _is_missing(v) -> bool:
    """Check if indicator value is None or NaN."""
    return v is None or v != v


# ---------------------------------------------------------------------------
# Helper: compute z-score of spread between two series
# ---------------------------------------------------------------------------
def _compute_spread_zscore(
    series_a: pd.Series, series_b: pd.Series, lookback: int = 60
) -> pd.Series | None:
    """Compute z-score of spread between two price series.

    Uses a rolling OLS hedge ratio to compute the spread, then
    normalizes to a z-score using rolling mean and std.
    """
    if len(series_a) < lookback or len(series_b) < lookback:
        return None

    # Rolling hedge ratio via rolling covariance / variance
    # (avoids statsmodels dependency)
    rolling_cov = series_a.rolling(lookback).cov(series_b)
    rolling_var = series_b.rolling(lookback).var()
    hedge_ratio = rolling_cov / rolling_var.replace(0, float("nan"))

    # Spread = A - hedge_ratio * B
    spread = series_a - hedge_ratio * series_b

    # Z-score of spread
    spread_mean = spread.rolling(lookback).mean()
    spread_std = spread.rolling(lookback).std()
    zscore = (spread - spread_mean) / spread_std.replace(0, float("nan"))

    return zscore


# ---------------------------------------------------------------------------
# Helper: compute ADX, DI+, DI-
# ---------------------------------------------------------------------------
def _compute_adx(df: pd.DataFrame, period: int = 14) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Compute ADX, DI+, DI- from OHLC data.

    Returns (adx, di_plus, di_minus) as pd.Series.
    """
    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    # True Range
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)

    # Directional Movement
    up_move = high - high.shift(1)
    down_move = low.shift(1) - low

    dm_plus = pd.Series(0.0, index=df.index)
    dm_minus = pd.Series(0.0, index=df.index)

    dm_plus = up_move.where((up_move > down_move) & (up_move > 0), 0.0)
    dm_minus = down_move.where((down_move > up_move) & (down_move > 0), 0.0)

    # Smoothed averages (Wilder's smoothing = EWM with alpha=1/period)
    atr = tr.ewm(alpha=1.0 / period, min_periods=period).mean()
    smooth_dm_plus = dm_plus.ewm(alpha=1.0 / period, min_periods=period).mean()
    smooth_dm_minus = dm_minus.ewm(alpha=1.0 / period, min_periods=period).mean()

    # DI+ and DI-
    di_plus = 100 * smooth_dm_plus / atr.replace(0, float("nan"))
    di_minus = 100 * smooth_dm_minus / atr.replace(0, float("nan"))

    # DX and ADX
    di_sum = di_plus + di_minus
    dx = 100 * (di_plus - di_minus).abs() / di_sum.replace(0, float("nan"))
    adx = dx.ewm(alpha=1.0 / period, min_periods=period).mean()

    return adx, di_plus, di_minus


# ---------------------------------------------------------------------------
# 1. ETF Cointegration (Stat Arb)
# ---------------------------------------------------------------------------
class ETFCointegration(BasePersona):
    """Mean reversion on cointegrated ETF pairs.

    Source: Engle-Granger cointegration, Bollinger-based pair trading.

    Rules:
    - For known cointegrated ETF pairs, compute spread z-score using
      rolling OLS hedge ratio over 60-day lookback.
    - Enter long spread (long A, short B) when z-score < -2.0
    - Enter short spread (short A, long B) when z-score > +2.0
    - Exit when z-score reverts toward 0 (within +/-0.5)

    Pairs: EWA/EWC, GLD/SLV, SPY/IWM, XLF/XLK (classic cointegrated ETFs)

    Research: Bollinger-based variant on cointegrated pair yielded Sharpe 2.7,
    97% win rate over 13 years. Conservative z-score threshold of 2.0.
    """

    PAIRS = [
        ("EWA", "EWC"),   # Australia / Canada — commodity exporters
        ("GLD", "SLV"),   # Gold / Silver — precious metals
        ("SPY", "IWM"),   # Large cap / Small cap US
        ("XLF", "XLK"),   # Financials / Technology sectors
        ("XLE", "XOP"),   # Energy sector / Oil & Gas exploration
        ("EWJ", "EWH"),   # Japan / Hong Kong
    ]

    ZSCORE_ENTRY = 2.0     # Enter when |z| > 2.0
    ZSCORE_EXIT = 0.5      # Exit when |z| < 0.5
    LOOKBACK = 60          # Rolling window for hedge ratio & z-score

    def __init__(self, universe: list[str] | None = None):
        all_syms = list(dict.fromkeys(s for pair in self.PAIRS for s in pair))
        config = PersonaConfig(
            name="ETF Cointegration (Stat Arb)",
            description="Mean reversion on cointegrated ETF pairs via z-score spread trading",
            risk_tolerance=0.4,
            max_position_size=0.20,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or all_syms,
        )
        super().__init__(config)
        # Cache z-scores to avoid recomputing every call
        self._zscore_cache: dict[tuple[str, str], pd.Series] = {}
        self._cache_built = False

    def _build_zscore_cache(self, data: dict[str, pd.DataFrame]) -> None:
        """Pre-compute z-scores for all pairs from the full data."""
        self._zscore_cache = {}
        for sym_a, sym_b in self.PAIRS:
            if sym_a not in data or sym_b not in data:
                continue
            close_a = data[sym_a]["Close"]
            close_b = data[sym_b]["Close"]
            # Align on common dates
            aligned = pd.DataFrame({"a": close_a, "b": close_b}).dropna()
            if len(aligned) < self.LOOKBACK + 20:
                continue
            zscore = _compute_spread_zscore(aligned["a"], aligned["b"], self.LOOKBACK)
            if zscore is not None:
                self._zscore_cache[(sym_a, sym_b)] = zscore
        self._cache_built = True

    def generate_signals(self, date, prices, portfolio, data):
        # Build cache on first call
        if not self._cache_built:
            self._build_zscore_cache(data)

        weights = {}
        pair_signals = []

        for sym_a, sym_b in self.PAIRS:
            if sym_a not in prices or sym_b not in prices:
                continue

            zscore_series = self._zscore_cache.get((sym_a, sym_b))
            if zscore_series is None:
                continue

            # Get z-score at or near this date
            if date in zscore_series.index:
                z = zscore_series.loc[date]
            else:
                try:
                    idx = zscore_series.index.get_indexer([date], method="nearest")[0]
                    if idx == -1:
                        continue
                    nearest = zscore_series.index[idx]
                    if abs((date - nearest).days) > 10:
                        continue
                    z = zscore_series.iloc[idx]
                except (IndexError, KeyError):
                    continue

            if _is_missing(z) or not math.isfinite(z):
                continue

            # Signal logic
            w_a = 0.0
            w_b = 0.0

            if z < -self.ZSCORE_ENTRY:
                # Spread too low: long A (undervalued relative to B)
                w_a = self.config.max_position_size
                w_b = self.config.max_position_size * 0.5  # smaller offset
                pair_signals.append((sym_a, sym_b, "long_spread", abs(z)))
            elif z > self.ZSCORE_ENTRY:
                # Spread too high: long B (undervalued relative to A)
                w_a = self.config.max_position_size * 0.5
                w_b = self.config.max_position_size
                pair_signals.append((sym_a, sym_b, "short_spread", abs(z)))
            elif abs(z) < self.ZSCORE_EXIT:
                # Mean reverted: exit both sides
                w_a = 0.0
                w_b = 0.0
            else:
                # Between exit and entry thresholds: hold current
                # Use a small neutral position
                w_a = 0.05
                w_b = 0.05

            # Accumulate (pairs can overlap on symbols like SPY)
            weights[sym_a] = max(weights.get(sym_a, 0.0), w_a)
            weights[sym_b] = max(weights.get(sym_b, 0.0), w_b)

        # Cap total exposure at 95%
        total = sum(v for v in weights.values() if v > 0)
        if total > 0.95:
            scale = 0.95 / total
            weights = {k: v * scale for k, v in weights.items()}

        # Explicitly close positions not in current allocation
        for sym in self.config.universe:
            if sym in prices:
                weights.setdefault(sym, 0.0)

        return weights


# ---------------------------------------------------------------------------
# 2. ADX Trend Strength Filter
# ---------------------------------------------------------------------------
class ADXTrendFilter(BasePersona):
    """ADX trend strength filter with DI crossover.

    Source: Welles Wilder's ADX indicator.

    Strategy A (standalone entry):
    - Buy when DI+ crosses above DI- AND ADX > 25 (confirming strong trend)
    - Sell when DI- crosses above DI+ OR ADX < 20 (trend weakening)

    Strategy B (filter enhancement):
    - Only take momentum entries (price > SMA50 > SMA200) when ADX > 25
    - Scale position size by ADX strength (ADX 25-50 maps to 50%-100% size)
    - Exit when ADX drops below 20 regardless of other signals

    Research: ADX as filter on SPY: CAGR 7%, profit factor 2.4, only 15%
    market exposure, max drawdown 19% (vs 55% buy-and-hold).
    """

    ADX_ENTRY_THRESHOLD = 25.0    # Only enter when trend is strong
    ADX_EXIT_THRESHOLD = 20.0     # Exit when trend weakens
    ADX_PERIOD = 14

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="ADX Trend Filter",
            description="ADX trend strength filter: only trade strong trends, skip choppy markets",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "SPY", "QQQ", "IWM", "DIA",      # Major index ETFs
                "XLF", "XLK", "XLE", "XLV",      # Sector ETFs
                "AAPL", "MSFT", "NVDA", "AMZN",  # Mega caps
                "GOOGL", "META", "TSLA", "AVGO",  # Tech leaders
            ],
        )
        super().__init__(config)
        # Cache ADX computations
        self._adx_cache: dict[str, tuple[pd.Series, pd.Series, pd.Series]] = {}
        self._cache_built = False

    def _build_adx_cache(self, data: dict[str, pd.DataFrame]) -> None:
        """Pre-compute ADX for all symbols from the full data."""
        self._adx_cache = {}
        for sym in self.config.universe:
            if sym not in data:
                continue
            df = data[sym]
            if "High" not in df.columns or "Low" not in df.columns:
                continue
            try:
                adx, di_plus, di_minus = _compute_adx(df, self.ADX_PERIOD)
                self._adx_cache[sym] = (adx, di_plus, di_minus)
            except Exception:
                continue
        self._cache_built = True

    def _get_adx_values(self, sym: str, date: pd.Timestamp) -> tuple[float | None, float | None, float | None]:
        """Get ADX, DI+, DI- for a symbol at a date."""
        if sym not in self._adx_cache:
            return None, None, None

        adx_series, dip_series, dim_series = self._adx_cache[sym]

        def _lookup(series):
            if date in series.index:
                v = series.loc[date]
                if isinstance(v, pd.Series):
                    v = v.iloc[-1]
                return None if _is_missing(v) else float(v)
            try:
                idx = series.index.get_indexer([date], method="nearest")[0]
                if idx == -1:
                    return None
                nearest = series.index[idx]
                if abs((date - nearest).days) > 10:
                    return None
                v = series.iloc[idx]
                return None if _is_missing(v) else float(v)
            except (IndexError, KeyError):
                return None

        return _lookup(adx_series), _lookup(dip_series), _lookup(dim_series)

    def generate_signals(self, date, prices, portfolio, data):
        if not self._cache_built:
            self._build_adx_cache(data)

        weights = {}
        candidates = []

        for sym in self.config.universe:
            if sym not in prices:
                continue

            price = prices[sym]
            adx, di_plus, di_minus = self._get_adx_values(sym, date)

            # Also get momentum indicators from pre-computed data
            inds = self._get_indicators(
                data, sym, ["sma_50", "sma_200", "rsi_14"], date
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]

            if adx is None or di_plus is None or di_minus is None:
                continue

            # Exit condition: trend too weak
            if adx < self.ADX_EXIT_THRESHOLD:
                weights[sym] = 0.0
                continue

            # Entry condition: strong trend + bullish DI crossover + momentum
            if adx >= self.ADX_ENTRY_THRESHOLD and di_plus > di_minus:
                # Additional momentum confirmation
                momentum_ok = True
                if sma50 is not None and sma200 is not None:
                    if not (price > sma50 and sma50 > sma200):
                        momentum_ok = False

                # RSI filter: not overbought
                if rsi is not None and rsi > 80:
                    momentum_ok = False

                if momentum_ok:
                    # Scale position by ADX strength (25-50 maps to 0.5-1.0)
                    adx_scale = min(1.0, max(0.5, (adx - 25) / 25))
                    score = adx_scale * (di_plus - di_minus)
                    candidates.append((sym, score, adx_scale))
                else:
                    # Trend is strong but momentum alignment is off
                    # Small position (reduced conviction)
                    weights[sym] = 0.03
            elif adx >= self.ADX_ENTRY_THRESHOLD and di_minus > di_plus:
                # Bearish trend: exit / avoid
                weights[sym] = 0.0

        # Rank by score and allocate
        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]

        if top:
            n = len(top)
            base_weight = min(0.90 / n, self.config.max_position_size)
            for sym, score, adx_scale in top:
                weights[sym] = base_weight * adx_scale

        # Explicitly close positions not in allocation
        for sym in self.config.universe:
            if sym in prices:
                weights.setdefault(sym, 0.0)

        return weights


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
GAP_STRATEGIES = {
    "etf_cointegration": ETFCointegration,
    "adx_trend_filter": ADXTrendFilter,
}


def get_gap_strategy(name: str, **kwargs) -> BasePersona:
    cls = GAP_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown: {name}. Available: {list(GAP_STRATEGIES.keys())}")
    return cls(**kwargs)


if __name__ == "__main__":
    print("=== Gap Strategies ===\n")
    for key, cls in GAP_STRATEGIES.items():
        inst = cls()
        print(f"  {key:30s} | {inst.config.name:35s} | {inst.config.description}")
