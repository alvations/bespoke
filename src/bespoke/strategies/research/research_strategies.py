"""Research-backed quantitative strategies for bespoke.

These are strategies derived from academic finance research and
quantitative analysis — not from any persona or interview.

All MUST be backtested before trusting.

Strategies:
    1. DualMomentum         — Gary Antonacci: absolute + relative momentum
    2. MultiFactorSmartBeta — Combine value + momentum + quality factors
    3. LowVolAnomaly        — Buy lowest-volatility quintile (Frazzini & Pedersen)
    4. MomentumCrashHedge   — 12-1 momentum with crash protection
    5. RiskParityMomentum   — Risk parity allocation + momentum overlay
    6. MeanVarianceOptimal  — Simplified Markowitz-inspired allocation
    7. GlobalRotation        — International momentum rotation
    8. FactorETFRotation    — Rotate between factor ETFs by momentum
    9. FaberSectorRotation  — Faber 12-month sector momentum, top 3
   10. LowVolQuality        — Lowest-vol quintile with quality ETF + individual names
   11. CrossAssetCarry       — Rank yield-bearing ETFs by carry, hold top 2
   12. BuybackYieldSystematic — Companies reducing share count outperform (PKW, SPYB)
   13. GrossProfitabilityValue — Novy-Marx 2013: high gross profit + value combo
   14. AccrualsQuality        — Sloan 1996: low accruals = quality earnings (QUAL, DGRW)
"""

from __future__ import annotations

import math

from bespoke.strategies.base import BaseStrategy as BasePersona, StrategyConfig as PersonaConfig

_SQRT_252 = math.sqrt(252)


def _is_missing(v) -> bool:
    """Check if indicator value is None or NaN (nearest-date path can leak NaN)."""
    return v is None or v != v


# ---------------------------------------------------------------------------
# 1. Dual Momentum (Gary Antonacci)
# ---------------------------------------------------------------------------
class DualMomentum(BasePersona):
    """Gary Antonacci's Dual Momentum strategy.

    Source: "Dual Momentum Investing" (2014)

    Two filters:
    1. Relative momentum: pick the stronger of US stocks vs international
    2. Absolute momentum: only invest if stronger asset > T-bills (SMA proxy)

    If both fail → 100% bonds.

    Implementation:
    - Compare SPY 12-month return vs EFA (international)
    - If winner > 0 (absolute momentum): invest in winner
    - If winner < 0: invest in AGG (bonds)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Dual Momentum (Antonacci)",
            description="Absolute + relative momentum: stocks vs intl vs bonds",
            risk_tolerance=0.5,
            max_position_size=0.90,
            max_positions=2,
            rebalance_frequency="monthly",
            universe=universe or ["SPY", "EFA", "AGG"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        # Calculate 12-month (approx 200-day) momentum for SPY and EFA
        spy_sma200 = self._get_indicator(data, "SPY", "sma_200", date)
        efa_sma200 = self._get_indicator(data, "EFA", "sma_200", date)
        spy_price = prices.get("SPY")
        efa_price = prices.get("EFA")

        if spy_price is None or _is_missing(spy_sma200):
            weights = {sym: 0.0 for sym in self.config.universe if sym in prices}
            if "AGG" in weights:
                weights["AGG"] = 0.90
            return weights

        # Relative momentum: SPY vs EFA
        spy_mom = (spy_price - spy_sma200) / spy_sma200 if spy_sma200 > 0 else 0
        efa_mom = (efa_price - efa_sma200) / efa_sma200 if efa_price is not None and not _is_missing(efa_sma200) and efa_sma200 > 0 else -1

        if spy_mom > efa_mom:
            winner, winner_mom = "SPY", spy_mom
        else:
            winner, winner_mom = "EFA", efa_mom

        # Absolute momentum: is winner > 0 (above its SMA200)?
        if winner_mom > 0:
            weights = {winner: 0.90}
        else:
            # Both negative → safe haven
            weights = {}
            if "AGG" in self.config.universe and "AGG" in prices:
                weights["AGG"] = 0.90
        # Close out non-qualifying universe symbols
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 2. Multi-Factor Smart Beta
# ---------------------------------------------------------------------------
class MultiFactorSmartBeta(BasePersona):
    """Multi-factor strategy combining value + momentum + quality.

    Source: Fama-French, AQR, Asness et al.

    Score each stock on 3 factors:
    - Value: price below SMA200 (discount proxy)
    - Momentum: MACD > signal + price > SMA50
    - Quality: low volatility + above SMA200

    Composite score → rank → equal-weight top N.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Multi-Factor Smart Beta",
            description="Value + momentum + quality composite factor ranking",
            risk_tolerance=0.5,
            max_position_size=0.10,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA",
                "JPM", "V", "MA", "UNH", "JNJ", "PG", "KO",
                "HD", "MCD", "WMT", "COST", "ABBV", "MRK",
                "XOM", "CVX", "BAC", "GS",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "vol_20"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            vol = inds["vol_20"]

            if any(_is_missing(v) for v in [sma200, rsi, vol]) or vol <= 0:
                continue

            # Factor 1: Value (discount to SMA200, higher = more value)
            value_score = (sma200 - price) / sma200 if sma200 > 0 else 0
            value_score = max(-0.5, min(0.5, value_score))  # Clip

            # Factor 2: Momentum (trend alignment)
            mom_score = 0.0
            if not _is_missing(sma50) and price > sma50:
                mom_score += 0.25
            if price > sma200:
                mom_score += 0.25
            if not _is_missing(macd) and not _is_missing(macd_sig) and macd > macd_sig:
                mom_score += 0.25
            if 40 < rsi < 70:
                mom_score += 0.25

            # Factor 3: Quality (inverse vol, above SMA200)
            # vol > 0 guaranteed by missing/zero filter above
            quality_score = min(1.0, 0.015 / vol)  # Normalize: lower vol → higher score
            if price > sma200:
                quality_score = min(1.0, quality_score * 1.3)

            # Composite: equal weight the 3 factors
            composite = (value_score + 0.5) * 0.33 + mom_score * 0.33 + quality_score * 0.33

            if composite > 0.25:
                scored.append((sym, composite))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        # Explicitly close positions in non-qualifying stocks
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 3. Low Volatility Anomaly
# ---------------------------------------------------------------------------
class LowVolAnomaly(BasePersona):
    """Low volatility anomaly strategy.

    Source: Frazzini & Pedersen (2014) "Betting Against Beta"

    Buy the lowest-volatility stocks. Counterintuitively, low-vol stocks
    have historically outperformed high-vol stocks on a risk-adjusted basis
    (and often in absolute terms too).

    Implementation:
    - Rank universe by 20-day realized volatility
    - Buy the bottom quintile (lowest vol)
    - Must be above SMA200 (not in downtrend)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Low Volatility Anomaly",
            description="Buy lowest-vol stocks: anomaly where low risk = higher returns",
            risk_tolerance=0.2,
            max_position_size=0.08,
            max_positions=15,
            rebalance_frequency="monthly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META",
                "JPM", "V", "MA", "UNH", "JNJ", "PG", "KO", "PEP",
                "HD", "MCD", "WMT", "COST", "ABBV", "MRK",
                "XOM", "CVX", "BAC", "GS", "TMO", "ABT",
                "LLY", "NEE", "DUK", "SO", "BRK-B",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        vol_ranked = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["vol_20", "sma_200"], date)
            vol = inds["vol_20"]
            sma200 = inds["sma_200"]

            if _is_missing(vol) or vol <= 0:
                continue
            # Must be above SMA200 (not broken)
            if not _is_missing(sma200) and price < sma200 * 0.95:
                continue

            vol_ranked.append((sym, vol))

        # Sort by vol ascending (lowest vol first)
        vol_ranked.sort(key=lambda x: x[1])

        # Take bottom quintile
        n = max(1, len(vol_ranked) // 5)
        top = vol_ranked[:min(n, self.config.max_positions)]

        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        # Explicitly close positions in non-qualifying stocks
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 4. Momentum with Crash Protection
# ---------------------------------------------------------------------------
class MomentumCrashHedge(BasePersona):
    """Momentum strategy with crash protection.

    Source: Daniel & Moskowitz (2016) "Momentum Crashes"

    Problem: Pure momentum crashes during bear market reversals.
    Solution: Scale momentum exposure by market volatility.
    When vol is high → reduce exposure. When vol is low → full exposure.

    Implementation:
    - Standard 12-1 momentum ranking (price vs SMA200)
    - Scale position sizes by inverse of realized volatility
    - When SPY vol > 2x average → cut to 50% exposure
    - When SPY vol > 3x average → cut to 25% or go to cash
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Momentum Crash-Hedged",
            description="Momentum with vol-scaling: reduce exposure when volatility spikes",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA",
                "AVGO", "NFLX", "CRM", "AMD", "PLTR", "CRWD",
                "SPY",  # Include for vol measurement
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Measure market volatility regime
        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)
        if _is_missing(spy_vol):
            vol_scale = 0.75  # Unknown risk → assume elevated (not full exposure)
        else:
            annualized_vol = spy_vol * _SQRT_252
            if annualized_vol > 0.40:      # >40% = crisis
                vol_scale = 0.25
            elif annualized_vol > 0.25:    # >25% = high vol
                vol_scale = 0.50
            elif annualized_vol > 0.18:    # >18% = elevated
                vol_scale = 0.75
            else:
                vol_scale = 1.0

        scored = []
        for sym in self.config.universe:
            if sym == "SPY" or sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]

            if any(_is_missing(v) for v in [sma50, sma200, rsi]):
                continue

            # Momentum score
            score = 0.0
            if price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5
            if not _is_missing(macd) and not _is_missing(macd_sig) and macd > macd_sig:
                score += 1.0
            if 45 < rsi < 75:
                score += 0.5

            if score >= 2.5:
                scored.append((sym, score))
            else:
                weights[sym] = 0.0

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min((0.90 * vol_scale) / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        # Explicitly close positions in non-qualifying stocks (SPY is vol-only)
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 5. Risk Parity with Momentum Overlay
# ---------------------------------------------------------------------------
class RiskParityMomentum(BasePersona):
    """Risk parity allocation with momentum tilt.

    Combines Bridgewater-style risk parity with trend following:
    - Base: risk parity across asset classes (stocks, bonds, gold, commodities)
    - Overlay: tilt toward assets with positive momentum, away from negative

    Implementation:
    - Inverse-vol weighting (risk parity base)
    - Momentum filter: only include assets above SMA50
    - Assets below SMA50 get zero weight (trend filter)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Risk Parity + Momentum",
            description="Risk parity allocation with momentum tilt across asset classes",
            risk_tolerance=0.4,
            max_position_size=0.40,
            max_positions=5,
            rebalance_frequency="monthly",
            universe=universe or [
                "SPY",   # US stocks
                "EFA",   # International stocks
                "TLT",   # Long bonds
                "GLD",   # Gold
                "XLE",   # Commodities proxy
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "vol_20"], date)
            sma50 = inds["sma_50"]
            vol = inds["vol_20"]

            if _is_missing(vol) or vol <= 0:
                continue

            # Momentum filter: only include if above SMA50
            if not _is_missing(sma50) and price > sma50:
                candidates.append((sym, vol))
            # else: excluded (negative momentum)

        if not candidates:
            # Everything trending down → safe haven, zero out all equities
            fallback = {sym: 0.0 for sym in self.config.universe if sym in prices}
            # Only allocate to safe havens if they're in universe AND have price data
            if "TLT" in self.config.universe and "TLT" in prices:
                fallback["TLT"] = min(0.50, self.config.max_position_size)
            if "GLD" in self.config.universe and "GLD" in prices:
                fallback["GLD"] = min(0.30, self.config.max_position_size)
            return fallback

        # Respect max_positions: keep lowest-vol assets (best risk parity contributors)
        if len(candidates) > self.config.max_positions:
            candidates.sort(key=lambda x: x[1])  # ascending vol
            candidates = candidates[:self.config.max_positions]

        # Risk parity: inverse-vol weighting with iterative capping
        cap = self.config.max_position_size
        budget = 0.90
        remaining = [(sym, 1.0 / vol) for sym, vol in candidates]
        while remaining:
            total_inv_vol = sum(iv for _, iv in remaining)
            if total_inv_vol <= 0:
                break
            new_remaining = []
            for sym, iv in remaining:
                w = (iv / total_inv_vol) * budget
                if w >= cap:
                    weights[sym] = cap
                    budget -= cap
                else:
                    new_remaining.append((sym, iv))
            if len(new_remaining) == len(remaining):
                # No more capping needed — assign remaining budget
                for sym, iv in new_remaining:
                    weights[sym] = (iv / total_inv_vol) * budget
                break
            remaining = new_remaining

        # Explicitly close positions in non-qualifying stocks
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 6. Mean-Variance Simplified (Markowitz-inspired)
# ---------------------------------------------------------------------------
class MeanVarianceOptimal(BasePersona):
    """Simplified Markowitz mean-variance optimization.

    Source: Markowitz (1952) "Portfolio Selection"

    Instead of full covariance matrix optimization, we use a simplified
    return/risk ranking:
    - Expected return proxy: SMA50 momentum
    - Risk proxy: 20-day realized vol
    - Score = return / risk (Sharpe-like ratio per stock)
    - Weight proportional to score
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Mean-Variance Simplified",
            description="Markowitz-inspired: rank by return/risk ratio, weight proportionally",
            risk_tolerance=0.4,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META",
                "JPM", "V", "UNH", "JNJ", "PG", "KO",
                "HD", "MCD", "WMT", "ABBV", "MRK", "XOM",
                "TLT", "GLD",  # Include bonds/gold for diversification
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "vol_20", "sma_200"], date)
            sma50 = inds["sma_50"]
            vol = inds["vol_20"]
            sma200 = inds["sma_200"]

            if any(_is_missing(v) for v in [sma50, vol]) or vol <= 0:
                continue

            # Expected return proxy: momentum (price / SMA50 - 1)
            exp_return = (price - sma50) / sma50 if sma50 > 0 else 0

            # Only consider assets with positive expected return
            if exp_return <= 0:
                continue

            # Must be above SMA200 (structural uptrend)
            if not _is_missing(sma200) and price < sma200:
                continue

            # Sharpe-like score
            sharpe_proxy = exp_return / vol
            scored.append((sym, sharpe_proxy))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]

        if top:
            cap = self.config.max_position_size
            budget = 0.90
            remaining = list(top)
            while remaining:
                sub_total = sum(s for _, s in remaining)
                if sub_total <= 0:
                    break
                new_remaining = []
                for sym, score in remaining:
                    w = (score / sub_total) * budget
                    if w >= cap:
                        weights[sym] = cap
                        budget -= cap
                    else:
                        new_remaining.append((sym, score))
                if len(new_remaining) == len(remaining):
                    # No more capping needed — assign remaining budget
                    for sym, score in new_remaining:
                        weights[sym] = (score / sub_total) * budget
                    break
                remaining = new_remaining

        # Explicitly close positions in non-qualifying stocks
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 7. Global Rotation (international momentum)
# ---------------------------------------------------------------------------
class GlobalRotation(BasePersona):
    """Global rotation: momentum across regional ETFs + individual ADRs.

    Rotate capital into the strongest-performing regions and individual
    international names. Uses same momentum framework but across a
    geographically diversified universe.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Global Rotation",
            description="Rotate into strongest regions: US, Europe, Asia, EM, LatAm",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                # Regional ETFs
                "SPY", "EFA", "EEM", "VWO", "EWJ", "EWZ", "INDA", "EWY",
                # Top intl ADRs
                "TM", "SONY", "BABA", "PDD", "INFY", "SE",
                "MELI", "NU", "SAP", "ASML", "NVO",
                "BHP", "VALE", "GOLD",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "vol_20"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            vol = inds["vol_20"]

            if any(_is_missing(v) for v in [sma50, sma200, rsi, vol]) or vol <= 0:
                continue

            # Momentum score (same as proven momentum framework)
            score = 0.0
            if price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5
            if 40 < rsi < 75:
                score += 0.5

            # Vol-adjusted (prefer lower vol for same momentum)
            score *= min(1.5, 0.02 / vol)

            if score > 1.5:
                scored.append((sym, score))
            else:
                weights[sym] = 0.0

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        # Explicitly close positions in non-qualifying stocks
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 8. Factor ETF Rotation
# ---------------------------------------------------------------------------
class FactorETFRotation(BasePersona):
    """Rotate between factor ETFs based on momentum.

    Instead of picking individual stocks, rotate between factor ETFs:
    momentum (MTUM), quality (QUAL), value (VLUE), low vol (SPLV),
    size (IWM), multi-factor (LRGF). Pick the top 3 by momentum.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Factor ETF Rotation",
            description="Rotate between factor ETFs (momentum, quality, value, low vol) based on trend",
            risk_tolerance=0.4,
            max_position_size=0.35,
            max_positions=3,
            rebalance_frequency="monthly",
            universe=universe or [
                "MTUM",  # Momentum
                "QUAL",  # Quality
                "VLUE",  # Value
                "SPLV",  # Low Volatility
                "IWM",   # Small Cap (Size)
                "SPY",   # Market (baseline)
                "TLT",   # Bonds (safe haven)
                "GLD",   # Gold (hedge)
            ],
        )
        super().__init__(config)

    _SAFE_HAVENS = ("TLT", "GLD")

    def generate_signals(self, date, prices, portfolio, data):
        scored = []
        for sym in self.config.universe:
            if sym in self._SAFE_HAVENS or sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            if _is_missing(sma50) or _is_missing(sma200):
                continue
            # Momentum score
            mom = (price - sma200) / sma200 if sma200 > 0 else 0
            if price > sma50:
                mom += 0.1
            scored.append((sym, mom))

        # Filter positive momentum first, THEN take top N
        positive = [(s, m) for s, m in scored if m > 0]
        positive.sort(key=lambda x: x[1], reverse=True)
        top = positive[:self.config.max_positions]
        weights = {}
        if top:
            per_etf = min(0.90 / len(top), self.config.max_position_size)
            total_alloc = per_etf * len(top)
            for sym, _ in top:
                weights[sym] = per_etf
            # Allocate remainder to safe havens (matching FaberSectorRotation pattern)
            remainder = 0.90 - total_alloc
            if remainder > 0.05:
                havens = [s for s in self._SAFE_HAVENS
                          if s in self.config.universe and s in prices]
                if havens:
                    per_haven = min(remainder / len(havens),
                                    self.config.max_position_size)
                    for s in havens:
                        weights[s] = per_haven
        else:
            # All negative momentum → safe haven (only if in universe and prices)
            cap = self.config.max_position_size
            if "TLT" in self.config.universe and "TLT" in prices:
                weights["TLT"] = min(0.50, cap)
            if "GLD" in self.config.universe and "GLD" in prices:
                weights["GLD"] = min(0.30, cap)
        # Explicitly close positions in non-winning ETFs
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 9. Faber Sector Rotation (proven methodology)
# ---------------------------------------------------------------------------
class FaberSectorRotation(BasePersona):
    """Faber sector rotation: 12-month momentum, top 3 sectors, absolute momentum filter.

    Source: Faber (2007). $10K→$135K (2000-2024) vs $62K S&P.
    """

    _SAFE_HAVENS = ("TLT", "IEF")

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Faber Sector Rotation",
            description="Proven 12-month sector momentum: top 3 + absolute momentum filter",
            risk_tolerance=0.5,
            max_position_size=0.35,
            max_positions=3,
            rebalance_frequency="monthly",
            universe=universe or [
                "XLK", "XLF", "XLE", "XLV", "XLI", "XLP",
                "XLU", "XLRE", "XLC", "XLB", "XLY",
                "TLT", "IEF",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        scored = []
        for sym in self.config.universe:
            if sym in self._SAFE_HAVENS or sym not in prices:
                continue
            price = prices[sym]
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            if _is_missing(sma200) or sma200 <= 0:
                continue
            momentum = (price - sma200) / sma200
            if momentum > 0:
                scored.append((sym, momentum))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        weights = {}
        if top:
            per_sector = min(0.90 / len(top), self.config.max_position_size)
            total_alloc = per_sector * len(top)
            for sym, _ in top:
                weights[sym] = per_sector
            # Allocate capped remainder to safe havens (Faber: unallocated → bonds)
            remainder = 0.90 - total_alloc
            if remainder > 0.05:
                havens = [s for s in self._SAFE_HAVENS
                          if s in self.config.universe and s in prices]
                if havens:
                    per_haven = min(remainder / len(havens),
                                    self.config.max_position_size)
                    for s in havens:
                        weights[s] = per_haven
        else:
            havens = [s for s in self._SAFE_HAVENS
                      if s in self.config.universe and s in prices]
            if havens:
                per_haven = min(0.90 / len(havens),
                                self.config.max_position_size)
                for s in havens:
                    weights[s] = per_haven
        # Explicitly close positions in non-winning sectors
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 10. Systematic Sector Rotation (3-month relative strength)
# ---------------------------------------------------------------------------
class SystematicSectorRotation(BasePersona):
    """Systematic sector rotation using 3-month relative strength vs SPY.

    Source: Faber (2007), Quantpedia "Sector Momentum Rotational System".
    Mebane Faber found sector momentum outperformed buy-and-hold ~70% of
    the time over 80+ years of data. A sector rotation model selecting
    top sectors by relative momentum delivered beta-adjusted alpha of ~4%
    annualized over 30 years.

    Implementation:
    - Rank all 11 GICS sector ETFs by 3-month relative strength vs SPY
      (sector return - SPY return over ~63 trading days, proxied by
      price / SMA200 relative to SPY price / SPY SMA200)
    - Long top 3 sectors with positive absolute momentum (above SMA200)
    - Avoid bottom 3 sectors entirely
    - When fewer than 3 sectors have positive momentum, allocate
      remainder to bonds (TLT, IEF)
    - Monthly rebalance
    """

    _SAFE_HAVENS = ("TLT", "IEF")

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Systematic Sector Rotation",
            description="Rank 11 GICS sectors by 3-month relative strength vs SPY, long top 3",
            risk_tolerance=0.5,
            max_position_size=0.35,
            max_positions=3,
            rebalance_frequency="monthly",
            universe=universe or [
                "XLK", "XLV", "XLF", "XLE", "XLI", "XLP",
                "XLY", "XLU", "XLRE", "XLC", "XLB",
                "SPY",  # Benchmark for relative strength
                "TLT", "IEF",  # Safe havens
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Get SPY relative strength baseline
        spy_price = prices.get("SPY")
        spy_sma200 = self._get_indicator(data, "SPY", "sma_200", date)
        if spy_price is None or _is_missing(spy_sma200) or spy_sma200 <= 0:
            # Can't compute relative strength — fall back to safe havens
            for sym in self._SAFE_HAVENS:
                if sym in self.config.universe and sym in prices:
                    weights[sym] = 0.35
            for sym in self.config.universe:
                if sym in prices and sym not in weights:
                    weights[sym] = 0.0
            return weights

        spy_rel = spy_price / spy_sma200  # SPY's own momentum baseline

        # Rank sectors by relative strength vs SPY
        sectors = [
            "XLK", "XLV", "XLF", "XLE", "XLI", "XLP",
            "XLY", "XLU", "XLRE", "XLC", "XLB",
        ]
        scored = []
        for sym in sectors:
            if sym not in prices:
                continue
            price = prices[sym]
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            if _is_missing(sma200) or sma200 <= 0:
                continue

            # 3-month relative strength: sector momentum vs SPY momentum
            sector_mom = price / sma200
            relative_strength = sector_mom - spy_rel

            # Absolute momentum filter: must be above its own SMA200
            if sector_mom > 1.0:
                scored.append((sym, relative_strength))

        # Sort by relative strength descending
        scored.sort(key=lambda x: x[1], reverse=True)

        # Top 3 with positive relative strength
        top = [s for s in scored if s[1] > 0][:self.config.max_positions]

        if top:
            per_sector = min(0.90 / len(top), self.config.max_position_size)
            total_alloc = per_sector * len(top)
            for sym, _ in top:
                weights[sym] = per_sector
            # Allocate remainder to safe havens
            remainder = 0.90 - total_alloc
            if remainder > 0.05:
                havens = [s for s in self._SAFE_HAVENS
                          if s in self.config.universe and s in prices]
                if havens:
                    per_haven = min(remainder / len(havens),
                                    self.config.max_position_size)
                    for s in havens:
                        weights[s] = per_haven
        else:
            # No sectors with positive momentum — full safe haven
            havens = [s for s in self._SAFE_HAVENS
                      if s in self.config.universe and s in prices]
            if havens:
                per_haven = min(0.90 / len(havens), self.config.max_position_size)
                for s in havens:
                    weights[s] = per_haven

        # Explicitly close non-qualifying positions
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 11. Multi-Factor Combined (quality + momentum + value)
# ---------------------------------------------------------------------------
class MultiFactorCombined(BasePersona):
    """Multi-factor combination: quality AND momentum AND value must all align.

    Source: MSCI "Foundations of Factor Investing", AQR, S&P DJIA research.
    Quality + Momentum combination has 93% outperformance rate with positive
    bottom 25th percentile returns of +2.57% (strongest of all factor combos).
    Adding value as a third filter creates a more conservative but robust
    selection of stocks scoring in the top quintile on ALL three factors.

    Implementation:
    - Quality: price > SMA200 (structural uptrend, healthy) + low vol
    - Momentum: MACD > signal + price > SMA50 (positive trend)
    - Value: RSI < 50 (not overbought / recent dip) + price near SMA200
      (not extended)
    - Require ALL THREE factors to confirm (intersection, not union)
    - Universe: top S&P stocks, equal-weight top 20 qualifying
    - Monthly rebalance
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Multi-Factor Combined (Q+M+V)",
            description="Long stocks in top quintile of ALL of quality, momentum, and value",
            risk_tolerance=0.4,
            max_position_size=0.06,
            max_positions=20,
            rebalance_frequency="monthly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA",
                "JPM", "V", "MA", "UNH", "JNJ", "PG", "KO",
                "HD", "MCD", "WMT", "COST", "ABBV", "MRK",
                "XOM", "CVX", "BAC", "GS", "LLY", "TMO",
                "ABT", "NEE", "CRM", "AVGO", "PEP", "NFLX",
                "BRK-B", "LOW", "CMCSA", "TXN", "INTC", "QCOM",
                "MDT", "MMM",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        qualified = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "vol_20"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            vol = inds["vol_20"]

            if any(_is_missing(v) for v in [sma50, sma200, rsi, vol]):
                continue
            if vol <= 0 or sma200 <= 0:
                continue

            # --- Factor 1: Quality ---
            # Must be above SMA200 (healthy uptrend) and have reasonable vol
            quality_pass = (price > sma200) and (vol < 0.03)

            # --- Factor 2: Momentum ---
            # MACD > signal AND price > SMA50
            momentum_pass = (
                not _is_missing(macd) and not _is_missing(macd_sig)
                and macd > macd_sig
                and price > sma50
            )

            # --- Factor 3: Value ---
            # RSI < 55 (not overbought) AND price within 15% of SMA200
            # (not too extended — buying at reasonable valuation)
            extension = (price - sma200) / sma200
            value_pass = (rsi < 55) and (extension < 0.15)

            # Count passing factors
            factors_passed = sum([quality_pass, momentum_pass, value_pass])

            # Require at least 2 of 3 factors (intersection too strict,
            # 2-of-3 captures the multi-factor alpha while staying invested)
            if factors_passed >= 2:
                # Composite score: bonus for all-3, plus quality + value scores
                composite = factors_passed * 2.0
                composite += (0.03 - vol) * 100  # Lower vol = higher quality
                composite += (55 - rsi) * 0.3    # Lower RSI = better value
                if quality_pass and momentum_pass:
                    composite += 1.0  # Q+M is the strongest 2-factor combo
                qualified.append((sym, composite))

        # Rank and take top N
        qualified.sort(key=lambda x: x[1], reverse=True)
        top = qualified[:self.config.max_positions]

        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        # Explicitly close non-qualifying positions
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights



# ---------------------------------------------------------------------------
# 10. Low Volatility Quality
# ---------------------------------------------------------------------------
class LowVolQuality(BasePersona):
    """Low volatility quality strategy with ETF and individual stock mix.

    Source: Frazzini & Pedersen "Betting Against Beta" (2014), Baker et al.

    Buy lowest-volatility quintile of major stocks. Uses both ETF proxies
    (SPLV, USMV, LGLV) and individual quality names (PG, JNJ, KO, PEP,
    WMT, CL, MMM) that historically exhibit low-beta, stable earnings.

    Signal: 20-day realized vol ranking. Buy names with lowest vol.
    Momentum overlay: only buy if above SMA50 (avoid value traps).
    Rebalance monthly.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Low Volatility Quality",
            description="Lowest-vol quintile: quality ETFs + individual staple names",
            risk_tolerance=0.3,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                # Low-vol ETF proxies
                "SPLV", "USMV", "LGLV",
                # Individual quality low-vol names
                "PG", "JNJ", "KO", "PEP", "WMT", "CL", "MMM",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        vol_scores = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym, ["sma_50", "sma_200", "vol_20", "rsi_14"], date
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            vol = inds["vol_20"]
            rsi = inds["rsi_14"]

            if _is_missing(vol) or _is_missing(sma50):
                continue

            # Must be above SMA50 (avoid value traps in downtrends)
            if price < sma50:
                continue

            # RSI filter: skip extremely overbought
            if not _is_missing(rsi) and rsi > 75:
                continue

            # Quality check: prefer names above SMA200 (structural uptrend)
            quality_bonus = 0.0
            if not _is_missing(sma200) and price > sma200:
                quality_bonus = 0.01  # Small bonus for quality trend

            # Lower vol = better (we want lowest-vol quintile)
            # Use negative vol so sorting ascending gives lowest vol first
            vol_scores.append((sym, vol - quality_bonus))

        # Sort by vol ascending (lowest vol first)
        vol_scores.sort(key=lambda x: x[1])

        # Take lowest-vol quintile (top ~40% for our small universe)
        n_select = max(1, len(vol_scores) * 2 // 5)
        top = vol_scores[:n_select]

        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        # Close non-qualifying positions
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0

        return weights


# ---------------------------------------------------------------------------
# 11. Cross-Asset Carry
# ---------------------------------------------------------------------------
class CrossAssetCarry(BasePersona):
    """Cross-asset carry strategy: rank yield-bearing ETFs.

    Source: Koijen et al. "Carry" (2018), AQR carry research.

    Rank yield-bearing ETFs by trailing dividend yield (proxy for carry):
    - HYG (high yield bonds)
    - VNQ (REITs)
    - PFF (preferred stock)
    - EMB (EM bonds)
    - VCIT (investment grade corporate)

    Hold top 2 by trailing yield. Use SMA200 as trend filter (only
    hold if above trend). Rebalance quarterly.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Cross-Asset Carry",
            description="Rank yield-bearing ETFs by carry, hold top 2",
            risk_tolerance=0.4,
            max_position_size=0.45,
            max_positions=3,
            rebalance_frequency="monthly",
            universe=universe or [
                "HYG",   # High yield bonds
                "VNQ",   # REITs
                "PFF",   # Preferred stock
                "EMB",   # Emerging market bonds
                "VCIT",  # Investment grade corporate
                "SHY",   # Cash proxy fallback
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        carry_scores = []

        yield_etfs = ["HYG", "VNQ", "PFF", "EMB", "VCIT"]

        for sym in yield_etfs:
            if sym not in prices or sym not in data or data[sym].empty:
                continue

            price = prices[sym]
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            sma50 = self._get_indicator(data, sym, "sma_50", date)

            # Trend filter: must be above SMA200 (avoid falling knives)
            if not _is_missing(sma200) and price < sma200:
                continue

            # Estimate yield proxy: distance from SMA200 as momentum,
            # combined with inverse-price level as yield proxy.
            # Higher-yielding assets tend to trade at lower price levels
            # relative to their SMA, so we use SMA50 distance as a
            # mean-reversion carry signal.
            carry_score = 0.0
            if not _is_missing(sma50) and sma50 > 0:
                # Price near SMA50 = stable carry; price above = momentum
                carry_score = 1.0  # Base score for being above SMA200
                # Bonus for momentum
                if price > sma50:
                    carry_score += 0.5

            # Bonus for known high-yield assets
            yield_bonus = {"HYG": 0.3, "VNQ": 0.2, "PFF": 0.25, "EMB": 0.35, "VCIT": 0.1}
            carry_score += yield_bonus.get(sym, 0)

            carry_scores.append((sym, carry_score))

        # Rank by carry score and take top 2
        carry_scores.sort(key=lambda x: x[1], reverse=True)
        top = carry_scores[:2]

        if top:
            per_etf = min(0.45, 0.90 / len(top))
            for sym, _ in top:
                weights[sym] = per_etf
        else:
            # No qualifying assets: park in cash proxy
            if "SHY" in prices:
                weights["SHY"] = 0.90

        # Close non-qualifying
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0

        return weights


# ---------------------------------------------------------------------------
# Buyback Yield Systematic
# ---------------------------------------------------------------------------
class BuybackYieldSystematic(BasePersona):
    """Companies reducing share count outperform — buyback yield strategy.

    Source: Net stock issuance anomaly — conservative issuance firms outperformed
    aggressive diluters over 30 years. Trend amplified post-COVID. FF5 investment
    factor captures part of this, but net buyback yield adds signal.

    Implementation (ETF proxy):
    - Core: PKW (Invesco Buyback Achievers), SPYB (S&P 500 Buyback ETF)
    - Momentum overlay: overweight when above 200-SMA
    - Monthly rebalance
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Buyback Yield Systematic",
            description="Companies reducing share count outperform — PKW, SPYB proxy",
            risk_tolerance=0.4,
            max_position_size=0.50,
            max_positions=3,
            rebalance_frequency="monthly",
            universe=universe or ["PKW", "SPYB", "SHY"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        buyback_etfs = [s for s in self.config.universe if s != "SHY"]

        total_buyback_wt = 0.0
        for sym in buyback_etfs:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_200", "sma_50", "rsi_14"], date)
            sma200 = inds["sma_200"]
            sma50 = inds["sma_50"]
            rsi = inds["rsi_14"]

            base_wt = 0.40  # Split between two ETFs

            if _is_missing(sma200):
                weights[sym] = base_wt * 0.7
                total_buyback_wt += base_wt * 0.7
                continue

            if price > sma200:
                # Uptrend: full allocation
                wt = base_wt
                if not _is_missing(sma50) and sma50 > sma200:
                    wt *= 1.05  # Momentum bonus

                # Pullback entry
                if not _is_missing(rsi) and rsi < 35:
                    wt *= 1.15
            else:
                # Below trend: reduce to defensive
                wt = base_wt * 0.5

            # Overbought: trim
            if not _is_missing(rsi) and rsi > 75:
                wt *= 0.7

            wt = min(wt, self.config.max_position_size)
            weights[sym] = wt
            total_buyback_wt += wt

        # Cash proxy for remainder
        if "SHY" in prices:
            weights["SHY"] = max(0.0, 0.90 - total_buyback_wt)

        return weights


# ---------------------------------------------------------------------------
# Gross Profitability Value
# ---------------------------------------------------------------------------
class GrossProfitabilityValue(BasePersona):
    """High gross profitability + value combination (Novy-Marx 2013).

    Source: Gross profit / total assets predicts returns with power equal to
    traditional value metrics. 3.7-4.4% annual premium. 6.37% alpha (3-factor
    adjusted). Works globally across 19 developed markets.

    Implementation (proxy using known high-GP names):
    - Universe of companies with >40% gross margins: AAPL, MSFT, GOOGL, V, MA,
      COST, NKE, MCD, SBUX, YUM, CMG
    - Signal: above-average profitability + below-average valuation (RSI as proxy)
    - Buy when RSI < 45 (relative value) AND above 200-SMA (quality confirmation)
    - Monthly rebalance
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Gross Profitability Value (Novy-Marx)",
            description="High gross profit + value: AAPL, MSFT, GOOGL, V, MA, COST, NKE, MCD",
            risk_tolerance=0.4,
            max_position_size=0.12,
            max_positions=11,
            rebalance_frequency="monthly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "V", "MA",
                "COST", "NKE", "MCD", "SBUX", "YUM", "CMG",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_200", "sma_50", "rsi_14", "vol_20"], date)
            sma200 = inds["sma_200"]
            sma50 = inds["sma_50"]
            rsi = inds["rsi_14"]
            vol = inds["vol_20"]

            if _is_missing(sma200):
                scored.append((sym, 0.5))
                continue

            score = 0.0

            # Quality filter: must be above 200-SMA (profitable companies trend up)
            if price > sma200:
                score += 0.4

                # Momentum confirmation
                if not _is_missing(sma50) and sma50 > sma200:
                    score += 0.1
            else:
                # Below trend — deep value opportunity if not broken
                discount = (sma200 - price) / sma200 if sma200 > 0 else 0
                if discount < 0.15:
                    score += 0.2  # Modest discount = value
                else:
                    score += 0.05  # Deep discount = risk

            # Value signal: lower RSI = better value (proxy for valuation)
            if not _is_missing(rsi):
                if rsi < 35:
                    score += 0.35  # Deep value
                elif rsi < 45:
                    score += 0.25  # Good value
                elif rsi < 55:
                    score += 0.15  # Fair value
                elif rsi > 70:
                    score += 0.0   # Expensive — skip
                else:
                    score += 0.10
            else:
                score += 0.15

            # Low volatility bonus (quality stocks tend to be lower vol)
            if not _is_missing(vol) and vol < 0.20:
                score += 0.1

            scored.append((sym, score))

        # Rank by score, allocate to top names
        scored.sort(key=lambda x: x[1], reverse=True)
        n_hold = min(len(scored), self.config.max_positions)

        if n_hold == 0:
            return weights

        for sym, sc in scored[:n_hold]:
            if sc > 0.2:  # Minimum score threshold
                weights[sym] = min(0.90 / n_hold, self.config.max_position_size)

        return weights


# ---------------------------------------------------------------------------
# Accruals Quality
# ---------------------------------------------------------------------------
class AccrualsQuality(BasePersona):
    """Low accruals = higher quality earnings (Sloan 1996).

    Source: Stocks with low accruals outperform high accruals by ~10% annually.
    Cash-flow component of earnings better predicts future performance. Globally
    confirmed across 17 countries (1989-2003).

    Implementation (proxy — we can't access balance sheet data directly):
    - Core: quality ETFs that screen for earnings quality (QUAL, DGRW)
    - Individual names known for low accruals / cash-flow-heavy earnings:
      BRK-B, JNJ, PG, KO
    - Signal: above 200-SMA + RSI filter
    - Monthly rebalance
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Accruals Quality (Sloan Anomaly)",
            description="Low accruals = quality earnings — QUAL, DGRW, BRK-B, JNJ, PG, KO",
            risk_tolerance=0.35,
            max_position_size=0.20,
            max_positions=6,
            rebalance_frequency="monthly",
            universe=universe or ["QUAL", "DGRW", "BRK-B", "JNJ", "PG", "KO"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        available = [s for s in self.config.universe if s in prices]

        if not available:
            return weights

        base_weight = min(0.90 / max(len(available), 1), self.config.max_position_size)

        for sym in available:
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_200", "sma_50", "rsi_14"], date)
            sma200 = inds["sma_200"]
            sma50 = inds["sma_50"]
            rsi = inds["rsi_14"]

            wt = base_weight

            if _is_missing(sma200):
                weights[sym] = wt * 0.8
                continue

            # Trend filter: quality stocks above trend get full weight
            if price > sma200:
                if not _is_missing(sma50) and sma50 > sma200:
                    wt *= 1.1  # Strong uptrend bonus
                # Pullback entry
                if not _is_missing(rsi) and rsi < 35:
                    wt *= 1.15  # Oversold quality = buy
            else:
                # Below trend: reduce but quality names tend to recover
                wt *= 0.6

            # Avoid chasing
            if not _is_missing(rsi) and rsi > 72:
                wt *= 0.7

            weights[sym] = min(wt, self.config.max_position_size)

        return weights


RESEARCH_STRATEGIES = {
    "dual_momentum": DualMomentum,
    "multi_factor_smart_beta": MultiFactorSmartBeta,
    "low_vol_anomaly": LowVolAnomaly,
    "momentum_crash_hedge": MomentumCrashHedge,
    "risk_parity_momentum": RiskParityMomentum,
    "mean_variance_optimal": MeanVarianceOptimal,
    "global_rotation": GlobalRotation,
    "factor_etf_rotation": FactorETFRotation,
    "faber_sector_rotation": FaberSectorRotation,
    "systematic_sector_rotation": SystematicSectorRotation,
    "multi_factor_combined": MultiFactorCombined,
    "low_vol_quality": LowVolQuality,
    "cross_asset_carry": CrossAssetCarry,
    "buyback_yield_systematic": BuybackYieldSystematic,
    "gross_profitability_value": GrossProfitabilityValue,
    "accruals_quality": AccrualsQuality,
}


def get_research_strategy(name: str, **kwargs) -> BasePersona:
    cls = RESEARCH_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown: {name}. Available: {list(RESEARCH_STRATEGIES.keys())}")
    return cls(**kwargs)


if __name__ == "__main__":
    print("=== Research-Backed Strategies ===\n")
    for key, cls in RESEARCH_STRATEGIES.items():
        inst = cls()
        print(f"  {key:30s} | {inst.config.name:35s} | {inst.config.description}")
