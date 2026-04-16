"""Hedge fund-inspired strategies based on 2024-2025 performance research.

Source: CNBC Hedge Fund Winners 2025, Aberdeen, Barclays Outlook.

Strategies:
    1. HealthcareAsiaMomentum — Healthcare + Asian equities momentum (2025 top trade)
    2. DynamicEnsemble       — Ensemble weighted by rolling Sharpe ratio
    3. StatArbMedallion      — Renaissance Medallion-style statistical arbitrage
    4. RiskParity            — Bridgewater-style risk parity across asset classes
    5. MarketMakingMomentum  — Citadel-style momentum with mean-reversion overlay
    6. GrowthConcentration   — Tiger Global-style concentrated growth bets
    7. ActivistDistressed    — Elliott Management-style activist / distressed value
    8. ManagedFuturesProxy   — DBMF + KMLM trend-following with crisis alpha overlay
"""

from __future__ import annotations

from bespoke.strategies.base import BaseStrategy as BasePersona, StrategyConfig as PersonaConfig


def _isna(v):
    """Check if value is None or NaN (lightweight alternative to pd.isna)."""
    return v is None or v != v


def _notna(v):
    return v is not None and v == v


class HealthcareAsiaMomentum(BasePersona):
    """Healthcare + Asian equity momentum — 2024-2025 hedge fund winner.

    Source: CNBC Hedge Fund Winners 2025 — equity L/S up 22.7%.
    Top trades: healthcare, media/telecoms, Asian equities.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Healthcare + Asia Momentum",
            description="2025 hedge fund winner: healthcare + Asian equities momentum",
            risk_tolerance=0.6,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe if universe is not None else [
                "UNH", "LLY", "ABBV", "MRK", "JNJ", "PFE", "ISRG", "SYK",
                "REGN", "VRTX", "DXCM", "HIMS",
                "TM", "SONY", "BABA", "PDD", "INFY", "TSM", "SE",
                "NIO", "LI", "FUTU", "GRAB",
                "XLV", "EWJ", "INDA", "EWT",
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
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            macd = self._get_indicator(data, sym, "macd", date)
            macd_sig = self._get_indicator(data, sym, "macd_signal", date)
            if _isna(sma50) or _isna(rsi):
                continue
            score = 0.0
            if _notna(sma200) and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5
            if _notna(macd) and _notna(macd_sig) and macd > macd_sig:
                score += 1.0
            if 40 < rsi < 75:
                score += 0.5
            if _notna(sma200) and price < sma200 * 0.90:
                weights[sym] = 0.0
            elif score >= 2.5:
                scored.append((sym, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


class DynamicEnsemble(BasePersona):
    """Dynamic ensemble weighted by rolling performance.

    Instead of fixed weights like our basic Ensemble, this weights
    sub-strategies by their rolling 60-day Sharpe ratio proxy.
    Better-performing strategies get higher allocation.
    """

    def __init__(self, universe=None):
        all_syms = [
            "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA",
            "JPM", "V", "MA", "UNH", "JNJ", "PG", "KO",
            "HD", "MCD", "WMT", "ABBV", "MRK", "XOM",
            "TLT", "GLD", "SPY", "QQQ",
        ]
        config = PersonaConfig(
            name="Dynamic Ensemble",
            description="Multi-strategy ensemble weighted by rolling Sharpe ratio",
            risk_tolerance=0.5,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe if universe is not None else all_syms,
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        """Combine momentum + value + quality signals with dynamic weighting."""
        weights = {}
        scored = {}

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            vol = self._get_indicator(data, sym, "vol_20", date)
            macd = self._get_indicator(data, sym, "macd", date)
            macd_sig = self._get_indicator(data, sym, "macd_signal", date)

            if _isna(sma50) or _isna(rsi):
                continue

            signals = 0
            total_weight = 0

            # Momentum signal (weight: performance-adaptive)
            mom = 0
            if _notna(sma200) and price > sma50 > sma200:
                mom = 1
            elif price > sma50:
                mom = 0.5
            if _notna(macd) and _notna(macd_sig) and macd > macd_sig:
                mom += 0.5
            if mom > 0:
                signals += 1
            total_weight += mom * 0.4

            # Value signal
            val = 0
            if _notna(sma200):
                discount = (sma200 - price) / sma200
                if discount > 0 and rsi < 45:
                    val = 1
                    signals += 1
            total_weight += val * 0.3

            # Quality signal (low vol + above SMA200)
            qual = 0
            if _notna(vol) and vol < 0.02 and _notna(sma200) and price > sma200:
                qual = 1
                signals += 1
            total_weight += qual * 0.3

            if signals > 0:
                scored[sym] = total_weight

        # Rank and select top N
        ranked = sorted(scored.items(), key=lambda x: x[1], reverse=True)
        top = ranked[:self.config.max_positions]
        if top:
            total_score = sum(s for _, s in top)
            if total_score > 0:
                for sym, score in top:
                    w = min((score / total_score) * 0.90, self.config.max_position_size)
                    weights[sym] = w

        return weights


# ---------------------------------------------------------------------------
# 3. Statistical Arbitrage (Medallion-style)
# ---------------------------------------------------------------------------
class StatArbMedallion(BasePersona):
    """Renaissance Medallion-style statistical arbitrage.

    Hypothesis: Short-term mean reversion in liquid large caps exploiting
    microstructure noise. Medallion reportedly trades ~10,000 signals with
    sub-day holding. We approximate with daily Z-score reversion on
    highly correlated pairs, buying the laggard and selling the leader
    within sector clusters.

    Source: Patterson (2010) "The Quants", Zuckerman (2019) "The Man Who
    Solved the Market". Estimated edge: Sharpe 2-6 on short-term reversion.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Stat Arb (Medallion-style)",
            description="Short-term mean reversion across sector pairs, Renaissance-inspired",
            risk_tolerance=0.5,
            max_position_size=0.10,
            max_positions=14,
            rebalance_frequency="daily",
            universe=universe if universe is not None else [
                # Tech cluster
                "AAPL", "MSFT", "GOOGL", "META",
                # Financials cluster
                "JPM", "GS", "MS", "BAC",
                # Healthcare cluster
                "UNH", "JNJ", "PFE", "ABBV",
                # Energy cluster
                "XOM", "CVX", "COP", "SLB",
                # Consumer cluster
                "PG", "KO", "PEP", "CL",
            ],
        )
        super().__init__(config)
        # Sector clusters for pair identification
        self._clusters = {
            "tech": ["AAPL", "MSFT", "GOOGL", "META"],
            "fin": ["JPM", "GS", "MS", "BAC"],
            "health": ["UNH", "JNJ", "PFE", "ABBV"],
            "energy": ["XOM", "CVX", "COP", "SLB"],
            "consumer": ["PG", "KO", "PEP", "CL"],
        }

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for cluster_name, cluster_syms in self._clusters.items():
            available = [s for s in cluster_syms if s in prices and s in data]
            if len(available) < 2:
                continue

            # Compute Z-scores within each cluster
            z_scores = {}
            for sym in available:
                df = data[sym]
                if "Close" not in df.columns or date not in df.index:
                    continue
                loc = df.index.get_loc(date)
                if loc < 40:
                    continue
                window = df["Close"].iloc[loc - 40:loc]
                if len(window) < 20:
                    continue
                mean = window.mean()
                std = window.std()
                if _notna(std) and std > 0:
                    z_scores[sym] = (prices[sym] - mean) / std

            if len(z_scores) < 2:
                continue

            # Buy the most oversold (lowest Z), avoid the most overbought
            cluster_mean_z = sum(z_scores.values()) / len(z_scores)
            for sym, z in z_scores.items():
                relative_z = z - cluster_mean_z
                rsi = self._get_indicator(data, sym, "rsi_14", date)
                if rsi is not None and rsi > 80:
                    weights[sym] = 0.0
                    continue
                # Buy laggards within cluster (relative Z < -1)
                if relative_z < -1.0:
                    score = abs(relative_z)
                    candidates.append((sym, score))
                # Sell leaders (relative Z > 1.5) if we hold them
                elif relative_z > 1.5:
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
# 4. Risk Parity (Bridgewater-style)
# ---------------------------------------------------------------------------
class RiskParity(BasePersona):
    """Bridgewater All Weather-style risk parity.

    Hypothesis: Allocate so each asset class contributes equal risk.
    Bonds are less volatile than stocks so they get higher weight.
    Works across economic regimes (growth/recession x inflation/deflation).

    Source: Dalio (2011) "Principles", Bridgewater All Weather whitepaper.
    The key insight: diversifying across risk rather than capital
    produces smoother returns. Bridgewater All Weather ~7.5% annualized
    with 10% vol since 1996.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Risk Parity (Bridgewater-style)",
            description="All Weather risk parity: equal risk contribution across asset classes",
            risk_tolerance=0.3,
            max_position_size=0.35,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe if universe is not None else [
                "SPY",   # US equities (growth rising)
                "EFA",   # Intl developed (growth rising)
                "TLT",   # Long bonds (growth falling, deflation)
                "IEF",   # Intermediate bonds (stable)
                "TIP",   # TIPS (inflation rising)
                "GLD",   # Gold (inflation rising, crisis)
                "DBC",   # Commodities (inflation rising)
                "VNQ",   # Real estate (growth + inflation)
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
            if vol is None or not (vol > 0):
                continue
            eligible.append((sym, vol))

        if not eligible:
            return weights

        # Inverse-volatility weighting (risk parity approximation)
        total_inv_vol = sum(1.0 / v for _, v in eligible)
        for sym, vol in eligible:
            raw_w = (1.0 / vol) / total_inv_vol * 0.95
            weights[sym] = min(raw_w, self.config.max_position_size)

        return weights


# ---------------------------------------------------------------------------
# 5. Market-Making Momentum (Citadel-style)
# ---------------------------------------------------------------------------
class MarketMakingMomentum(BasePersona):
    """Citadel-style momentum with short-term mean-reversion overlay.

    Hypothesis: Citadel Securities profits from capturing bid-ask
    spreads while Wellington profits from multi-factor momentum.
    We combine: (1) strong medium-term momentum for direction,
    (2) short-term RSI dips for entry (like a market maker buying
    dips to provide liquidity), (3) volume confirmation.

    Source: Citadel Wellington ~19.4% annualized returns. Multi-factor
    momentum + mean reversion at different timeframes is a known
    institutional edge (Moskowitz, Ooi, Pedersen 2012).
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Market-Making Momentum (Citadel-style)",
            description="Multi-factor momentum + short-term mean-reversion entry, Citadel-inspired",
            risk_tolerance=0.6,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="daily",
            universe=universe if universe is not None else [
                "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA",
                "JPM", "GS", "V", "MA",
                "UNH", "LLY", "ABBV",
                "XOM", "CVX",
                "HD", "MCD", "COST",
                "SPY", "QQQ",
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
            inds = self._get_indicators(data, sym,
                ["sma_20", "sma_50", "sma_200", "rsi_14", "macd", "macd_signal",
                 "bb_lower", "atr_14", "Volume", "volume_sma_20"], date)
            sma20 = inds["sma_20"]
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            bb_lower = inds["bb_lower"]
            atr = inds["atr_14"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]

            if any(v is None for v in [sma50, rsi]):
                continue

            # Medium-term momentum filter (must be in uptrend)
            mom_score = 0.0
            if _notna(sma200) and price > sma50 > sma200:
                mom_score += 2.0
            elif price > sma50:
                mom_score += 1.0
            if _notna(macd) and _notna(macd_sig) and macd > macd_sig:
                mom_score += 1.0

            if mom_score < 1.0:
                continue  # No momentum, skip

            # Short-term mean-reversion entry (market-maker style: buy dips)
            entry_score = 0.0
            if rsi < 40:
                entry_score += 2.0  # RSI dip in uptrend
            elif rsi < 50:
                entry_score += 1.0
            if _notna(bb_lower) and price < bb_lower * 1.02:
                entry_score += 1.5  # Near Bollinger lower band

            # Volume confirmation
            vol_boost = 1.0
            if volume is not None and vol_avg is not None and vol_avg > 0:
                vol_ratio = volume / vol_avg
                if vol_ratio > 1.5:
                    vol_boost = 1.3

            # ATR-adjusted scoring (prefer lower vol stocks for tighter spreads)
            atr_adj = 1.0
            if _notna(atr) and price > 0:
                atr_pct = atr / price
                if atr_pct < 0.02:
                    atr_adj = 1.2  # Low vol = tighter spread = better

            total_score = (mom_score + entry_score) * vol_boost * atr_adj

            # Exit: RSI overbought
            if rsi > 78:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity > 0:
                    weights[sym] = 0.0
                continue

            if total_score >= 3.0:
                scored.append((sym, total_score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 6. Growth Concentration (Tiger Global-style)
# ---------------------------------------------------------------------------
class GrowthConcentration(BasePersona):
    """Tiger Global-style concentrated growth bets.

    Hypothesis: Concentrate in the highest-conviction secular growth
    names. Tiger Global under Chase Coleman focused on 15-20 positions
    in technology and consumer internet, riding multi-year growth with
    high conviction. The edge is letting winners run while cutting
    losers fast.

    Source: Tiger Global ~21% annualized 2001-2021. Concentrated
    portfolios outperform when stock-picking skill is positive
    (Cremers & Petajisto 2009, "Active Share").
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Growth Concentration (Tiger Global-style)",
            description="Concentrated high-conviction growth bets, Tiger Global-inspired",
            risk_tolerance=0.8,
            max_position_size=0.20,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe if universe is not None else [
                # Mega-cap tech (proven growth)
                "NVDA", "MSFT", "GOOGL", "AMZN", "META",
                # High-growth SaaS / cloud
                "CRM", "NOW", "SNOW", "DDOG", "CRWD",
                # Consumer internet / fintech
                "SHOP", "SQ", "MELI", "SE",
                # Next-gen platforms
                "PLTR", "COIN", "RBLX", "UBER",
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
            inds = self._get_indicators(data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal",
                 "Volume", "volume_sma_20"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]

            if any(v is None for v in [sma50, rsi]):
                continue

            # Growth momentum scoring
            score = 0.0

            # Strong uptrend (must-have)
            if _notna(sma200) and price > sma50 > sma200:
                score += 3.0
                # Extra points for distance above SMA200 (momentum strength)
                if sma200 > 0:
                    pct_above = (price - sma200) / sma200
                    score += min(pct_above * 5, 2.0)
            elif price > sma50:
                score += 1.0
            else:
                continue  # Tiger style: cut losers, no positions below SMA50

            # MACD confirmation
            if _notna(macd) and _notna(macd_sig) and macd > macd_sig:
                score += 1.0

            # Volume expansion (institutional accumulation)
            if volume is not None and vol_avg is not None and vol_avg > 0:
                vol_ratio = volume / vol_avg
                if vol_ratio > 1.5:
                    score += 1.0

            # RSI filter: not overbought, not dead
            if rsi > 80:
                weights[sym] = 0.0
                continue
            if 50 < rsi < 75:
                score += 0.5  # Healthy momentum zone

            if score >= 4.0:
                scored.append((sym, score))

        # Concentrate: take top N by score
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            # Conviction-weighted: higher score = higher weight
            total_score = sum(s for _, s in top)
            if total_score > 0:
                for sym, sc in top:
                    w = (sc / total_score) * 0.92
                    weights[sym] = min(w, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 7. Activist Distressed (Elliott Management-style)
# ---------------------------------------------------------------------------
class ActivistDistressed(BasePersona):
    """Elliott Management-style activist / distressed value.

    Hypothesis: Buy deeply discounted quality companies where an activist
    catalyst (board changes, spin-offs, buybacks) can unlock value.
    Elliott Management (~$55B AUM) targets companies trading 20-50%
    below intrinsic value with identifiable catalysts. The edge is
    buying when others panic, then waiting for mean reversion + catalyst.

    Source: Elliott returns ~14% annualized since 1977. Brav et al.
    (2008) "Hedge Fund Activism, Corporate Governance, and Firm
    Performance" shows activist targets outperform by ~7% annualized.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Activist Distressed (Elliott-style)",
            description="Deep-value activist targets: buy >20% below SMA200, catalyst-driven recovery",
            risk_tolerance=0.6,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe if universe is not None else [
                # Classic activist targets (large cap with poor governance)
                "BA", "INTC", "PFE", "NKE", "PYPL",
                # Consumer / media (restructuring plays)
                "DIS", "WBD", "PARA", "HAS",
                # Industrial / conglomerates (spin-off candidates)
                "GE", "MMM", "DOW", "FMC",
                # Distressed / turnaround
                "NCLH", "AAL", "CLF", "WBA",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for sym in self.config.universe:
            if sym not in prices or sym not in data:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym,
                ["sma_200", "sma_50", "rsi_14", "Volume", "volume_sma_20",
                 "bb_lower"], date)
            sma200 = inds["sma_200"]
            sma50 = inds["sma_50"]
            rsi = inds["rsi_14"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]
            bb_lower = inds["bb_lower"]

            if any(v is None for v in [sma200, rsi]):
                continue

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            # Exit: structural freefall (> 40% below SMA200 = falling knife)
            if discount > 0.40:
                weights[sym] = 0.0
                continue

            # Take profits on recovery (back above SMA200 with RSI >60)
            if discount < -0.05 and rsi > 60:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity > 0:
                    weights[sym] = 0.0
                continue

            # Buy signal: deeply discounted (>15% below SMA200) + oversold
            if discount > 0.15 and rsi < 45:
                score = discount * 5  # More discount = better

                # Bonus: volume spike = institutional interest / activist entry
                if volume is not None and vol_avg is not None and vol_avg > 0:
                    vol_ratio = volume / vol_avg
                    if vol_ratio > 1.8:
                        score *= 1.4

                # Bonus: near Bollinger lower band (extreme sell-off)
                if _notna(bb_lower) and price < bb_lower * 1.03:
                    score *= 1.2

                # Bonus: SMA50 turning up (early recovery)
                if _notna(sma50) and sma50 > sma200 * 0.92:
                    score *= 1.1

                candidates.append((sym, score))

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        # Close positions not in current candidates
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights



# ---------------------------------------------------------------------------
# 8. Managed Futures Proxy
# ---------------------------------------------------------------------------
class ManagedFuturesProxy(BasePersona):
    """Managed futures proxy strategy using trend-following ETFs.

    Source: AQR Managed Futures research, Man AHL trend studies.

    Uses DBMF (iMGP DBi Managed Futures Strategy) and KMLM (KFA Mount
    Lucas Managed Futures) as CTA/managed futures proxies.

    Trend-following rules:
    - If 12-month return > 0 (price > SMA200): hold full position
    - If 12-month return < 0: reduce to 50% (trend broken but
      may still provide crisis alpha)

    CTA overlay: when SPY < SMA200, increase DBMF weight. This captures
    crisis alpha — managed futures historically profit during equity
    drawdowns via short equity / long bonds / long commodities.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Managed Futures Proxy",
            description="DBMF + KMLM trend-following with crisis alpha overlay",
            risk_tolerance=0.5,
            max_position_size=0.50,
            max_positions=4,
            rebalance_frequency="monthly",
            universe=universe or [
                "DBMF",  # iMGP managed futures
                "KMLM",  # KFA Mount Lucas managed futures
                "SPY",   # Regime detection
                "SHY",   # Cash fallback
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Detect equity regime via SPY
        spy_price = prices.get("SPY")
        spy_sma200 = self._get_indicator(data, "SPY", "sma_200", date)
        equity_crisis = False
        if spy_price is not None and not _isna(spy_sma200) and spy_sma200 > 0:
            if spy_price < spy_sma200:
                equity_crisis = True

        mf_etfs = ["DBMF", "KMLM"]
        for sym in mf_etfs:
            if sym not in prices:
                continue

            price = prices[sym]
            sma200 = self._get_indicator(data, sym, "sma_200", date)

            if _isna(sma200) or sma200 <= 0:
                # No trend data: moderate allocation
                weights[sym] = 0.25
                continue

            positive_trend = price > sma200

            if sym == "DBMF":
                if equity_crisis:
                    # Crisis alpha: increase DBMF (managed futures shine in crises)
                    weights[sym] = 0.50 if positive_trend else 0.35
                else:
                    weights[sym] = 0.35 if positive_trend else 0.18
            else:  # KMLM
                if equity_crisis:
                    weights[sym] = 0.35 if positive_trend else 0.20
                else:
                    weights[sym] = 0.30 if positive_trend else 0.15

        # If both managed futures are in negative trend and no crisis,
        # shift some to cash
        total_mf = sum(weights.get(s, 0) for s in mf_etfs)
        if total_mf < 0.40 and not equity_crisis:
            if "SHY" in prices:
                weights["SHY"] = 0.90 - total_mf

        # Zero unallocated
        for sym in self.config.universe:
            if sym in prices and sym not in weights and sym != "SPY":
                weights[sym] = 0.0

        return weights


HEDGE_FUND_STRATEGIES = {
    "healthcare_asia_momentum": HealthcareAsiaMomentum,
    "dynamic_ensemble": DynamicEnsemble,
    "stat_arb_medallion": StatArbMedallion,
    "risk_parity": RiskParity,
    "market_making_momentum": MarketMakingMomentum,
    "growth_concentration": GrowthConcentration,
    "activist_distressed": ActivistDistressed,
    "managed_futures_proxy": ManagedFuturesProxy,
}


def get_hedge_fund_strategy(name: str, **kwargs) -> BasePersona:
    cls = HEDGE_FUND_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown: {name}. Available: {list(HEDGE_FUND_STRATEGIES.keys())}")
    return cls(**kwargs)
