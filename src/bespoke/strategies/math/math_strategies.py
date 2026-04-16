"""Mathematically-driven trading strategies for bespoke.

These strategies use specific mathematical techniques beyond simple
moving averages. Each is grounded in a specific mathematical concept.

Strategies:
    1. KellyOptimal        — Kelly criterion position sizing with momentum
    2. ZScoreReversion     — Statistical Z-score mean reversion
    3. HurstExponent       — Regime detection via Hurst exponent proxy
    4. VolatilityBreakout  — Donchian channel breakouts scaled by ATR
    5. EqualRiskContrib    — Equal risk contribution (ERC) portfolio
    6. EntropyRegime       — Shannon entropy-based regime detection
    7. CointegrationPairs  — Cointegration-based pairs trading (stat arb)
    8. OptimalStopping     — Optimal stopping theory for exit timing
"""

from __future__ import annotations




import pandas as pd

from bespoke.strategies.base import BaseStrategy as BasePersona, StrategyConfig as PersonaConfig


# ---------------------------------------------------------------------------
# 1. Kelly Criterion Optimal Sizing
# ---------------------------------------------------------------------------
class KellyOptimal(BasePersona):
    """Kelly criterion position sizing with momentum signal.

    Source: Kelly (1956) "A New Interpretation of Information Rate"

    f* = (p*b - q) / b
    where p = win probability, q = 1-p, b = win/loss ratio

    We estimate p and b from rolling 60-day returns, then use
    fractional Kelly (half-Kelly) for safety.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Kelly Criterion Optimal",
            description="Position sizing via Kelly criterion from rolling win rate and payoff ratio",
            risk_tolerance=0.5,
            max_position_size=0.20,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META",
                "JPM", "V", "UNH", "HD", "MCD", "PG",
                "SPY", "QQQ",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for sym in self.config.universe:
            if sym not in prices or sym not in data:
                continue

            df = data[sym]
            if "daily_return" not in df.columns or date not in df.index:
                continue

            # Get rolling 60-day returns window
            loc = df.index.get_loc(date)
            if loc < 60:
                continue
            window = df["daily_return"].iloc[loc-60:loc].dropna()
            if len(window) < 30:
                continue

            # Estimate Kelly parameters
            wins = window[window > 0]
            losses = window[window < 0]
            if len(wins) == 0 or len(losses) == 0:
                continue

            p = len(wins) / len(window)  # Win probability
            avg_win = wins.mean()
            avg_loss = abs(losses.mean())
            b = avg_win / avg_loss if avg_loss > 0 else 1  # Payoff ratio

            q = 1 - p
            kelly = (p * b - q) / b if b > 0 else 0

            # Half-Kelly for safety
            half_kelly = max(0, kelly * 0.5)

            # Only invest if Kelly > 0 and momentum is positive
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            price = prices[sym]
            if half_kelly > 0.01 and sma50 is not None and price > sma50:
                candidates.append((sym, half_kelly))

        # Normalize weights with redistribution from capped positions
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            top = candidates[:self.config.max_positions]
            total_kelly = sum(k for _, k in top)
            if total_kelly > 0.95:
                scale = 0.95 / total_kelly
            else:
                scale = 1.0
            cap = self.config.max_position_size
            for sym, k in top:
                weights[sym] = min(k * scale, cap)
            # Redistribute budget lost from capping to uncapped positions
            allocated = sum(weights.values())
            uncapped = [s for s, k in top if k * scale < cap]
            uncapped_total = sum(weights[s] for s in uncapped)
            if uncapped and uncapped_total > 0 and allocated < 0.95:
                boost = 1 + (0.95 - allocated) / uncapped_total
                for s in uncapped:
                    weights[s] = min(weights[s] * boost, cap)

        return weights


# ---------------------------------------------------------------------------
# 2. Z-Score Mean Reversion
# ---------------------------------------------------------------------------
class ZScoreReversion(BasePersona):
    """Statistical Z-score based mean reversion.

    Buy when a stock's price is >2 standard deviations below its
    60-day mean (Z < -2). Sell when it reverts to Z > 0.

    This is more rigorous than simple RSI — it uses actual
    statistical significance thresholds.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Z-Score Mean Reversion",
            description="Buy at Z < -2 (statistically oversold), sell at Z > 0",
            risk_tolerance=0.5,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="daily",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META",
                "JPM", "V", "UNH", "JNJ", "PG", "KO",
                "HD", "MCD", "WMT", "XOM", "CVX", "BAC",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for sym in self.config.universe:
            if sym not in prices or sym not in data:
                continue

            df = data[sym]
            if "Close" not in df.columns or date not in df.index:
                continue

            loc = df.index.get_loc(date)
            if loc < 60:
                continue

            window = df["Close"].iloc[loc-60:loc]
            if len(window) < 30:
                continue

            mean = window.mean()
            std = window.std()
            if not (std > 0):
                continue

            price = prices[sym]
            z_score = (price - mean) / std

            # Buy signal: Z < -2 (statistically significant oversold)
            if z_score < -2.0:
                # Score by how extreme the Z is
                score = abs(z_score) - 2.0
                sma200 = self._get_indicator(data, sym, "sma_200", date)
                # Only if not in structural downtrend
                if sma200 is not None and price > sma200 * 0.85:
                    candidates.append((sym, score))

            # Exit: Z > 0 (reverted to mean)
            elif z_score > 0.5:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity > 0:
                    weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 3. Hurst Exponent Regime Detection
# ---------------------------------------------------------------------------
class HurstExponent(BasePersona):
    """Regime detection using Hurst exponent proxy.

    H > 0.5: trending (use momentum)
    H < 0.5: mean-reverting (use mean reversion)
    H = 0.5: random walk (stay out)

    We estimate H from the autocorrelation of returns as a fast proxy.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Hurst Regime Detector",
            description="Adaptive: momentum when trending, mean-reversion when reverting",
            risk_tolerance=0.5,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META",
                "JPM", "V", "UNH", "JNJ", "PG", "KO",
                "HD", "MCD", "WMT", "SPY", "QQQ",
            ],
        )
        super().__init__(config)

    def _estimate_hurst(self, returns: pd.Series) -> float:
        """Estimate Hurst exponent from autocorrelation proxy."""
        if len(returns) < 20:
            return 0.5  # Unknown → random walk
        # Use lag-1 autocorrelation as quick Hurst proxy
        # H ≈ 0.5 + autocorr/2
        autocorr = returns.autocorr(lag=1)
        if pd.isna(autocorr):
            return 0.5
        return 0.5 + autocorr / 2

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        mom_candidates = []
        mr_candidates = []

        for sym in self.config.universe:
            if sym not in prices or sym not in data:
                continue

            df = data[sym]
            if "daily_return" not in df.columns or date not in df.index:
                continue

            loc = df.index.get_loc(date)
            if loc < 60:
                continue

            returns = df["daily_return"].iloc[loc-60:loc].dropna()
            hurst = self._estimate_hurst(returns)

            price = prices[sym]
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            bb_lower = self._get_indicator(data, sym, "bb_lower", date)

            if any(v is None for v in [sma50, rsi]):
                continue

            if hurst > 0.55:
                # Trending regime → use momentum
                if price > sma50 and rsi < 75:
                    score = hurst * 2
                    if sma200 is not None and sma50 > sma200:
                        score += 1
                    mom_candidates.append((sym, score))
            elif hurst < 0.45:
                # Mean-reverting regime → buy oversold
                if rsi < 30 and bb_lower is not None and price < bb_lower:
                    score = (0.5 - hurst) * 5
                    mr_candidates.append((sym, score))
            # 0.45-0.55 → random walk, stay out

        # Combine both signal types
        all_candidates = mom_candidates + mr_candidates
        all_candidates.sort(key=lambda x: x[1], reverse=True)
        top = all_candidates[:self.config.max_positions]

        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 4. Volatility Breakout (Donchian + ATR)
# ---------------------------------------------------------------------------
class VolatilityBreakout(BasePersona):
    """Volatility breakout: Donchian channel breakout scaled by ATR.

    Source: Turtle Trading system (Richard Dennis, 1983)

    Buy when price breaks above the 20-day high (Donchian upper).
    Position size = risk budget / ATR (risk-normalize position).
    Exit when price breaks below 10-day low.

    We approximate Donchian with BB upper and use ATR for sizing.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Volatility Breakout (Turtle)",
            description="Donchian breakout with ATR position sizing (Turtle Trading)",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="daily",
            universe=universe or [
                "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA",
                "GLD", "TLT", "XLE", "SPY", "QQQ",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices or sym not in data:
                continue

            price = prices[sym]
            bb_upper = self._get_indicator(data, sym, "bb_upper", date)
            bb_lower = self._get_indicator(data, sym, "bb_lower", date)
            atr = self._get_indicator(data, sym, "atr_14", date)
            sma20 = self._get_indicator(data, sym, "sma_20", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)

            if any(v is None for v in [bb_upper, atr, sma20]):
                continue

            # Breakout: price above BB upper (Donchian proxy)
            if price > bb_upper and rsi is not None and rsi < 80:
                # ATR-scaled scoring (lower ATR = stronger breakout signal)
                if atr > 0:
                    atr_pct = atr / price
                    score = 3.0 / max(atr_pct * 100, 0.5)  # Inverse of ATR %
                    scored.append((sym, score, atr))

            # Exit: price below SMA20 (simplified Donchian lower)
            elif price < sma20:
                weights[sym] = 0.0

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]

        if top:
            risk_per_position = 0.002  # 0.2% portfolio risk per ATR per position
            for sym, score, atr in top:
                if atr > 0:
                    # Turtle sizing: w = risk / (ATR/price)
                    w = min(risk_per_position * prices[sym] / atr,
                            self.config.max_position_size)
                    weights[sym] = w

        return weights


# ---------------------------------------------------------------------------
# 5. Equal Risk Contribution (ERC)
# ---------------------------------------------------------------------------
class EqualRiskContrib(BasePersona):
    """Equal Risk Contribution portfolio.

    Source: Maillard, Roncalli, Teiletche (2010)

    Each asset contributes equally to portfolio risk.
    Weight_i proportional to 1 / (sigma_i * sum(1/sigma_j))

    Combined with a momentum filter to avoid investing in downtrending assets.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Equal Risk Contribution (ERC)",
            description="Each asset contributes equal risk, with momentum filter",
            risk_tolerance=0.4,
            max_position_size=0.25,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "SPY", "QQQ", "IWM",  # US equities
                "EFA", "EEM",          # International
                "TLT", "IEF",         # Bonds
                "GLD",                  # Gold
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        eligible = []

        for sym in self.config.universe:
            if sym not in prices or sym not in data:
                continue

            vol = self._get_indicator(data, sym, "vol_20", date)
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            price = prices[sym]

            if vol is None or not (vol > 0):
                continue

            # Momentum filter: only include assets above SMA50
            if sma50 is not None and price > sma50:
                eligible.append((sym, vol))

        if not eligible:
            # Everything bearish → defensive allocation from available universe
            fallback = {"TLT": 0.50, "IEF": 0.30, "GLD": 0.10}
            universe_set = set(self.config.universe)
            available = {s: w for s, w in fallback.items()
                         if s in prices and s in universe_set}
            if available:
                return available
            return {}

        # Cap at max_positions, preferring strongest momentum
        eligible.sort(key=lambda x: prices[x[0]] / (self._get_indicator(data, x[0], "sma_50", date) or prices[x[0]]), reverse=True)
        eligible = eligible[:self.config.max_positions]

        # ERC: weight inversely proportional to vol
        total_inv_vol = sum(1 / v for _, v in eligible)
        for sym, vol in eligible:
            w = (1 / vol) / total_inv_vol * 0.90
            weights[sym] = min(w, self.config.max_position_size)

        return weights


# ---------------------------------------------------------------------------
# 6. Entropy-Based Regime Detection
# ---------------------------------------------------------------------------
class EntropyRegime(BasePersona):
    """Shannon entropy-based market regime detection.

    Hypothesis: Market entropy (disorder of return distribution)
    indicates regime type. Low entropy = orderly trends (momentum
    works). High entropy = chaotic/random (mean reversion works or
    stay out). By measuring the entropy of the return distribution,
    we adapt strategy selection to the current regime.

    We discretize returns into bins and compute Shannon entropy:
    H = -sum(p_i * log2(p_i))
    Max entropy = log2(n_bins) for uniform distribution (random walk).
    Low entropy = concentrated returns (trending).

    Source: Bandt & Pompe (2002) "Permutation Entropy" for complexity.
    Pincus (1991) "Approximate Entropy" for time series regularity.
    Granger & Lin (1994) show entropy measures predict volatility
    regimes. Real quant funds use entropy in their regime models
    (AQR, Two Sigma).
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Entropy Regime Detector",
            description="Shannon entropy of returns: momentum in low-entropy, defensive in high",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META",
                "JPM", "V", "UNH", "HD",
                "SPY", "QQQ",
                "TLT", "GLD",  # Defensive assets
            ],
        )
        super().__init__(config)
        self._n_bins = 10  # Discretization bins for entropy

    def _compute_entropy(self, returns: pd.Series) -> float:
        """Compute Shannon entropy of return distribution."""
        import math
        if len(returns) < 20:
            return float('inf')  # Unknown
        # Discretize returns into bins and compute probabilities
        binned = pd.cut(returns, bins=self._n_bins, labels=False, duplicates='drop')
        counts = binned.value_counts()
        total = counts.sum()
        if total == 0:
            return float('inf')
        probs = counts / total
        entropy = 0.0
        for p in probs:
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy

    def generate_signals(self, date, prices, portfolio, data):
        import math
        weights = {}
        max_entropy = math.log2(self._n_bins)  # Max possible entropy

        # Compute market-wide entropy from SPY
        market_entropy_ratio = 0.5  # Default: unknown
        if "SPY" in data:
            df = data["SPY"]
            if "daily_return" in df.columns and date in df.index:
                loc = df.index.get_loc(date)
                if loc >= 60:
                    returns = df["daily_return"].iloc[loc - 60:loc].dropna()
                    if len(returns) >= 30:
                        ent = self._compute_entropy(returns)
                        market_entropy_ratio = ent / max_entropy if max_entropy > 0 else 0.5

        mom_candidates = []
        defensive_candidates = []

        for sym in self.config.universe:
            if sym not in prices or sym not in data:
                continue
            price = prices[sym]
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            vol20 = self._get_indicator(data, sym, "vol_20", date)

            if sma50 is None or rsi is None:
                continue

            if market_entropy_ratio < 0.65:
                # LOW ENTROPY: orderly trends -- use momentum
                if price > sma50 and rsi < 75:
                    score = 2.0
                    if sma200 is not None and sma50 > sma200:
                        score += 1.5
                    if 40 < rsi < 70:
                        score += 0.5
                    mom_candidates.append((sym, score))
            elif market_entropy_ratio > 0.85:
                # HIGH ENTROPY: chaotic -- go defensive
                if sym in ("TLT", "GLD"):
                    defensive_candidates.append((sym, 3.0))
                elif vol20 is not None and vol20 < 0.015 and price > sma50:
                    # Only very low-vol stocks in chaos regime
                    defensive_candidates.append((sym, 1.0))
            else:
                # MEDIUM ENTROPY: mixed signals -- reduced exposure
                if price > sma50 and rsi < 65:
                    score = 1.0
                    if sma200 is not None and sma50 > sma200:
                        score += 1.0
                    mom_candidates.append((sym, score * 0.6))

        # Select based on regime
        if market_entropy_ratio < 0.65:
            candidates = mom_candidates
        elif market_entropy_ratio > 0.85:
            candidates = defensive_candidates
        else:
            candidates = mom_candidates + defensive_candidates

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 7. Cointegration Pairs Trading
# ---------------------------------------------------------------------------
class CointegrationPairs(BasePersona):
    """Cointegration-based pairs trading (statistical arbitrage).

    Hypothesis: Certain stock pairs have a long-run equilibrium
    relationship (cointegration). When the spread deviates, it
    reverts. This is more rigorous than correlation -- cointegrated
    pairs have a stationary spread even if individual prices are
    non-stationary (I(1)).

    We approximate cointegration testing via the spread Z-score of
    known economic pairs (same sector, similar business model).
    When the spread Z-score exceeds +/-2, we go long the laggard
    and short the leader (or just long the laggard since we're
    long-only).

    Source: Engle & Granger (1987) "Co-Integration and Error
    Correction". Gatev et al. (2006) show pairs trading returns
    ~11% annualized. Vidyamurthy (2004) "Pairs Trading" textbook.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Cointegration Pairs Trading",
            description="Long laggard in cointegrated pairs when spread Z > 2",
            risk_tolerance=0.5,
            max_position_size=0.12,
            max_positions=8,
            rebalance_frequency="daily",
            universe=universe or [
                # Classic cointegrated pairs (same-sector economic substitutes)
                "KO", "PEP",      # Coke vs Pepsi
                "V", "MA",        # Visa vs Mastercard
                "HD", "LOW",      # Home Depot vs Lowe's
                "XOM", "CVX",     # Exxon vs Chevron
                "JPM", "BAC",     # JP Morgan vs Bank of America
                "GOOGL", "META",  # Google vs Meta (ad revenue)
                "UPS", "FDX",     # UPS vs FedEx
                "PG", "CL",      # Procter & Gamble vs Colgate
            ],
        )
        super().__init__(config)
        # Define pairs (each pair is a tuple)
        self._pairs = [
            ("KO", "PEP"),
            ("V", "MA"),
            ("HD", "LOW"),
            ("XOM", "CVX"),
            ("JPM", "BAC"),
            ("GOOGL", "META"),
            ("UPS", "FDX"),
            ("PG", "CL"),
        ]

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for sym_a, sym_b in self._pairs:
            if (sym_a not in data or sym_b not in data or
                    sym_a not in prices or sym_b not in prices):
                continue

            df_a, df_b = data[sym_a], data[sym_b]
            if ("Close" not in df_a.columns or "Close" not in df_b.columns or
                    date not in df_a.index or date not in df_b.index):
                continue

            loc_a = df_a.index.get_loc(date)
            loc_b = df_b.index.get_loc(date)
            if loc_a < 60 or loc_b < 60:
                continue

            # Compute log price ratio (spread) over 60 days
            window_a = df_a["Close"].iloc[loc_a - 60:loc_a + 1]
            window_b = df_b["Close"].iloc[loc_b - 60:loc_b + 1]

            # Align by position (both should be same trading days)
            min_len = min(len(window_a), len(window_b))
            if min_len < 30:
                continue
            window_a = window_a.iloc[-min_len:]
            window_b = window_b.iloc[-min_len:]

            import numpy as np
            ratio = np.log(window_a.values / window_b.values)
            mean_ratio = ratio[:-1].mean()
            std_ratio = ratio[:-1].std()
            if not (std_ratio > 0):
                continue

            current_z = (ratio[-1] - mean_ratio) / std_ratio

            # Long the laggard when spread is extreme
            if current_z > 2.0:
                # A is expensive, B is cheap -> buy B
                sma200_b = self._get_indicator(data, sym_b, "sma_200", date)
                if sma200_b is not None and prices[sym_b] > sma200_b * 0.85:
                    candidates.append((sym_b, abs(current_z) - 2.0))
                # Exit A if held
                pos_a = portfolio.get_position(sym_a)
                if pos_a and pos_a.quantity > 0:
                    weights[sym_a] = 0.0

            elif current_z < -2.0:
                # B is expensive, A is cheap -> buy A
                sma200_a = self._get_indicator(data, sym_a, "sma_200", date)
                if sma200_a is not None and prices[sym_a] > sma200_a * 0.85:
                    candidates.append((sym_a, abs(current_z) - 2.0))
                # Exit B if held
                pos_b = portfolio.get_position(sym_b)
                if pos_b and pos_b.quantity > 0:
                    weights[sym_b] = 0.0

            else:
                # Spread near mean: exit positions (take profit on convergence)
                if abs(current_z) < 0.5:
                    for sym in (sym_a, sym_b):
                        pos = portfolio.get_position(sym)
                        if pos and pos.quantity > 0:
                            weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 8. Optimal Stopping (Exit Timing)
# ---------------------------------------------------------------------------
class OptimalStopping(BasePersona):
    """Optimal stopping theory applied to exit timing.

    Hypothesis: The "secretary problem" / optimal stopping rule says
    to observe for 1/e (~37%) of the period, then pick the first
    option that exceeds the best seen so far. Applied to trading:
    observe the stock for a lookback window, track the running max,
    and sell when the price starts declining from a level that
    exceeded the 37th percentile of recent highs.

    Combined with momentum entry (buy in uptrends), the optimal
    stopping rule improves exit timing by avoiding the common trap
    of selling too early or too late.

    Source: Ferguson (1989) "Who Solved the Secretary Problem?"
    Shiryaev et al. (2008) "Optimal Stopping and Free-Boundary
    Problems" applied to financial mathematics. The 1/e rule is
    provably optimal for maximizing the probability of selecting
    the best option.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Optimal Stopping (Exit Timer)",
            description="Secretary problem applied to exits: sell after peak exceeds 37th pctile",
            risk_tolerance=0.5,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="daily",
            universe=universe or [
                "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA",
                "JPM", "V", "UNH", "HD", "MCD",
                "SPY", "QQQ",
            ],
        )
        super().__init__(config)
        self._lookback = 60  # Observation window
        self._observe_fraction = 0.37  # 1/e rule

    def generate_signals(self, date, prices, portfolio, data):
        import math
        weights = {}
        buy_candidates = []
        observe_days = int(self._lookback * self._observe_fraction)  # ~22 days

        for sym in self.config.universe:
            if sym not in prices or sym not in data:
                continue

            df = data[sym]
            if "Close" not in df.columns or date not in df.index:
                continue

            price = prices[sym]
            loc = df.index.get_loc(date)
            if loc < self._lookback:
                continue

            window = df["Close"].iloc[loc - self._lookback:loc + 1]
            if len(window) < self._lookback:
                continue

            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)

            if sma50 is None or rsi is None:
                continue

            # Observation phase: track the max in first 37% of window
            observe_window = window.iloc[:observe_days]
            observe_max = observe_window.max()

            # Decision phase: the remaining window
            decision_window = window.iloc[observe_days:]
            current_price = window.iloc[-1]

            # Check if we hold this position
            pos = portfolio.get_position(sym)
            holding = pos is not None and pos.quantity > 0

            if holding:
                # EXIT LOGIC (optimal stopping for selling)
                # Has price exceeded the observation max? (the "best seen so far")
                exceeded_threshold = any(decision_window > observe_max)

                if exceeded_threshold:
                    # We're in the "stop if declining" zone
                    # Recent peak in decision window
                    recent_peak = decision_window.max()
                    drawdown_from_peak = (recent_peak - current_price) / recent_peak if recent_peak > 0 else 0

                    # Sell if we've drawn down >5% from the post-threshold peak
                    if drawdown_from_peak > 0.05:
                        weights[sym] = 0.0
                        continue

                    # Also sell if RSI overbought (momentum exhaustion)
                    if rsi > 78:
                        weights[sym] = 0.0
                        continue

                # If we haven't exceeded threshold yet, keep holding
                # (we're still in observation equivalent)

            else:
                # ENTRY LOGIC: standard momentum entry
                if price > sma50 and rsi < 72:
                    score = 0.0
                    if sma200 is not None and sma50 > sma200:
                        score += 2.0
                    else:
                        score += 1.0

                    # Prefer stocks near the start of a move (not extended)
                    if sma200 is not None and sma200 > 0:
                        extension = (price - sma200) / sma200
                        if extension < 0.10:
                            score += 1.5  # Early in move
                        elif extension < 0.20:
                            score += 0.5

                    if rsi < 60:
                        score += 0.5

                    if score >= 2.0:
                        buy_candidates.append((sym, score))

        buy_candidates.sort(key=lambda x: x[1], reverse=True)
        top = buy_candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 9. Volatility Premium Harvest (low-vol anomaly with quantitative sizing)
# ---------------------------------------------------------------------------
class VolatilityPremium(BasePersona):
    """Harvest the volatility premium: long low-vol, avoid high-vol.

    Source: Frazzini & Pedersen (2014) "Betting Against Beta". Fischer Black
    (1972) first documented the low-beta anomaly. SPLV (low vol ETF) delivers
    similar returns to SPY but with 13.3% vol vs 16.3% — virtually identical
    Sharpe. With mathematical risk-normalization, the low-vol portfolio
    outperforms on a risk-adjusted basis.

    Academic evidence: Low-volatility stocks outperform high-volatility stocks
    on a risk-adjusted basis consistently across all major equity markets and
    over 50+ years of data. The anomaly persists because of leverage constraints,
    lottery preferences, and benchmarking to market-cap-weighted indices.

    Implementation:
    - Compute 20-day realized vol for each stock
    - Rank by vol, split into low-vol quintile and high-vol quintile
    - Long low-vol stocks (buy SPLV and lowest-vol individual names)
    - Avoid high-vol stocks (never buy SPHB or highest-vol names)
    - Weight inversely proportional to vol (risk parity within low-vol)
    - Apply leverage-like effect: allocate more total capital to low-vol
      (up to 90% vs typical 50-60%) since vol is lower
    - Monthly rebalance
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Volatility Premium Harvest",
            description="Long low-vol stocks, avoid high-vol: harvesting the low-volatility anomaly",
            risk_tolerance=0.3,
            max_position_size=0.15,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                "SPLV",   # Low Volatility ETF (core holding)
                # 10 historically low-beta S&P names
                "JNJ", "PG", "KO", "PEP", "WMT",
                "MCD", "CL", "MMM", "SO", "DUK",
                # High-beta ETF (benchmark, never buy)
                "SPHB",
                # Additional low-vol candidates
                "NEE", "WEC", "AEP", "ED", "BRK-B",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        vol_data = []

        # Never buy the high-beta ETF
        high_vol_avoid = {"SPHB"}

        for sym in self.config.universe:
            if sym in high_vol_avoid:
                if sym in prices:
                    weights[sym] = 0.0
                continue
            if sym not in prices:
                continue

            price = prices[sym]
            inds = self._get_indicators(data, sym, ["vol_20", "sma_200", "sma_50"], date)
            vol = inds["vol_20"]
            sma200 = inds["sma_200"]
            sma50 = inds["sma_50"]

            if vol is None or not (vol == vol) or vol <= 0:
                continue

            # Must be above SMA200 (not in structural downtrend)
            if sma200 is not None and sma200 == sma200 and price < sma200 * 0.95:
                continue

            # Bonus for being above SMA50 (positive momentum)
            momentum_bonus = 1.0
            if sma50 is not None and sma50 == sma50 and price > sma50:
                momentum_bonus = 1.2

            vol_data.append((sym, vol, momentum_bonus))

        if not vol_data:
            # Fallback to SPLV if available
            if "SPLV" in prices:
                weights["SPLV"] = 0.90
            return weights

        # Sort by vol ascending (lowest vol first)
        vol_data.sort(key=lambda x: x[1])

        # Take low-vol quintile (bottom 20%) or at least top 3
        n_low = max(3, len(vol_data) // 5)
        low_vol = vol_data[:min(n_low, self.config.max_positions)]

        # Inverse-vol weighting within low-vol group
        total_inv_vol = sum(m / v for _, v, m in low_vol)
        if total_inv_vol <= 0:
            return weights

        cap = self.config.max_position_size
        budget = 0.90

        for sym, vol, mom in low_vol:
            raw_w = (mom / vol) / total_inv_vol * budget
            weights[sym] = min(raw_w, cap)

        # Explicitly close non-qualifying positions
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0

        return weights


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
MATH_STRATEGIES = {
    "kelly_optimal": KellyOptimal,
    "zscore_reversion": ZScoreReversion,
    "hurst_regime": HurstExponent,
    "volatility_breakout": VolatilityBreakout,
    "equal_risk_contrib": EqualRiskContrib,
    "entropy_regime": EntropyRegime,
    "cointegration_pairs": CointegrationPairs,
    "optimal_stopping": OptimalStopping,
    "volatility_premium": VolatilityPremium,
}


def get_math_strategy(name: str, **kwargs) -> BasePersona:
    cls = MATH_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown: {name}. Available: {list(MATH_STRATEGIES.keys())}")
    return cls(**kwargs)


if __name__ == "__main__":
    print("=== Math-Driven Strategies ===\n")
    for key, cls in MATH_STRATEGIES.items():
        inst = cls()
        print(f"  {key:25s} | {inst.config.name:35s} | {inst.config.description}")
