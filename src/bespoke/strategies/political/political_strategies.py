"""Political and prediction-market trading strategies for bespoke.

Strategies based on congressional trading patterns, political ETFs,
and prediction market signals.

Strategies:
    1. NancyPelosi       — NANC-style Democratic congressional trading (74% since 2023)
    2. GOPTrading        — KRUZ/GOP-style Republican congressional trading
    3. BipartisanConsensus — Combined Dem+GOP overlap (both parties agree = strong signal)
    4. PolymarketSignal  — Political uncertainty → defensive; stability → risk-on
    5. DavidTepper       — Appaloosa macro: China + cyclicals + mean reversion
    6. KenGriffin        — Citadel: mega-cap tech concentration + quant signals
    7. DanLoeb           — Third Point: event-driven activist value
"""

from __future__ import annotations

from typing import Dict, List, Optional

from bespoke.strategies.base import BaseStrategy as BasePersona, StrategyConfig as PersonaConfig


# ---------------------------------------------------------------------------
# 1. Nancy Pelosi / NANC Style
# ---------------------------------------------------------------------------
class NancyPelosi(BasePersona):
    """NANC-style Democratic congressional trading strategy.

    Source: NANC ETF (Unusual Whales Subversive Democratic Trading)
    Performance: +74% since Feb 2023 launch, beat SPY by 6%+.
    Top holdings: NVDA 10.5%, MSFT 7.5%, heavy tech concentration.

    Strategy: Replicate Congressional Democrats' disclosed trades.
    Proxy: Buy momentum in tech-heavy quality names that politicians favor.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Nancy Pelosi (NANC Style)",
            description="Congressional Dem trading: tech-heavy quality momentum, +74% since 2023",
            risk_tolerance=0.6,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="monthly",
            # NANC top holdings + common congressional picks
            universe=universe or [
                "NVDA", "MSFT", "AAPL", "GOOGL", "AMZN", "META",
                "AVGO", "CRM", "NOW", "PANW",
                "V", "MA", "JPM", "GS",
                "DIS", "NFLX",
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
            vol = self._get_indicator(data, sym, "vol_20", date)
            if any(v is None for v in [sma50, sma200, rsi]):
                continue
            # Congressional style: quality momentum, buy dips
            score = 0.0
            if price > sma50 > sma200:
                score += 2.5
            elif price > sma50:
                score += 1.5
            if 30 < rsi < 65:
                score += 0.5
            if vol and vol < 0.02:
                score += 0.5  # Quality (low vol)
            if score >= 2.5:
                scored.append((sym, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 2. GOP / KRUZ Style
# ---------------------------------------------------------------------------
class GOPTrading(BasePersona):
    """GOP/KRUZ-style Republican congressional trading.

    Source: GOP ETF (formerly KRUZ). Tech 24%, Financials 16%, Industrials 14%.
    More diversified than NANC, less tech-concentrated.
    Outperformed SPY by 50%+ in first 2 years.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="GOP Congressional Trading",
            description="Republican congressional trades: diversified sectors, financials + industrials",
            risk_tolerance=0.5,
            max_position_size=0.10,
            max_positions=15,
            rebalance_frequency="monthly",
            # GOP/KRUZ sector weights: Tech, Financials, Industrials, Healthcare
            universe=universe or [
                "MSFT", "AAPL", "NVDA", "GOOGL",  # Tech (24%)
                "JPM", "BAC", "GS", "BRK-B", "V",  # Financials (16%)
                "CAT", "GE", "HON", "UNP", "LMT",  # Industrials (14%)
                "UNH", "JNJ", "ABBV",  # Healthcare
                "XOM", "CVX",  # Energy
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
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            if sma200 is None:
                continue
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            if discount > -0.10:
                score = max(discount + 0.10, 0.01) + 0.3
                if rsi and rsi < 50:
                    score += 0.2
                candidates.append((sym, score))
        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 3. Bipartisan Consensus
# ---------------------------------------------------------------------------
class BipartisanConsensus(BasePersona):
    """Stocks both Democrats AND Republicans are buying.

    Thesis: When both parties agree on a stock, it's likely based
    on genuine fundamentals rather than partisan policy bets.
    Overlap of NANC + GOP holdings = highest conviction.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Bipartisan Consensus",
            description="Stocks BOTH parties buy: strongest signal when Dems + GOP agree",
            risk_tolerance=0.4,
            max_position_size=0.10,
            max_positions=12,
            rebalance_frequency="monthly",
            # Overlap between NANC and GOP top holdings
            universe=universe or [
                "NVDA", "MSFT", "AAPL", "GOOGL", "AMZN",
                "JPM", "V", "MA",
                "UNH", "JNJ",
                "XOM", "CVX",
                "LMT", "GD",
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
            vol = self._get_indicator(data, sym, "vol_20", date)
            if any(v is None for v in [sma200, rsi]):
                continue
            if price < sma200 * 0.90:
                continue
            score = 0.0
            if sma50 and price > sma50 > sma200:
                score += 2.0
            elif price > sma200:
                score += 1.0
            if vol and vol < 0.02:
                score += 1.0
            if 30 < rsi < 60:
                score += 0.5
            if score >= 2.0:
                scored.append((sym, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 4. Polymarket Signal Strategy
# ---------------------------------------------------------------------------
class PolymarketSignal(BasePersona):
    """Political uncertainty → defensive; stability → risk-on.

    Thesis: When political uncertainty is HIGH (volatile markets,
    geopolitical events), go defensive. When stable, go risk-on.

    Proxy: We use market volatility as a proxy for political uncertainty
    (VIX-like signal from SPY vol). Polymarket odds would enhance this
    if we had API access.

    Polymarket accuracy: >94% one month before outcomes are known.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Polymarket Signal (Uncertainty Proxy)",
            description="Political uncertainty→defensive, stability→risk-on (Polymarket proxy)",
            risk_tolerance=0.4,
            max_position_size=0.30,
            max_positions=6,
            rebalance_frequency="weekly",
            universe=universe or [
                "SPY", "QQQ",  # Risk-on
                "XLV", "XLP", "XLU",  # Defensive sectors
                "TLT", "GLD", "SHY",  # Safe havens
                "LMT", "GD", "NOC",  # Defense (benefits from uncertainty)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        # Proxy for political uncertainty: SPY volatility
        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)
        spy_rsi = self._get_indicator(data, "SPY", "rsi_14", date)

        if spy_vol is None:
            return {"SPY": 0.30, "QQQ": 0.20, "TLT": 0.15, "GLD": 0.10}

        annualized_vol = spy_vol * (252 ** 0.5)

        if annualized_vol > 0.25 or (spy_rsi and spy_rsi < 35):
            # HIGH uncertainty → defensive
            return {
                "XLP": 0.20, "XLV": 0.15, "XLU": 0.10,  # Defensive sectors
                "TLT": 0.15, "GLD": 0.15,  # Safe havens
                "LMT": 0.10,  # Defense sector benefits
                "SPY": 0.0, "QQQ": 0.0,
            }
        elif annualized_vol < 0.12:
            # LOW uncertainty → full risk-on
            return {
                "SPY": 0.35, "QQQ": 0.35,
                "TLT": 0.05, "GLD": 0.05,
                "XLP": 0.0, "XLV": 0.0, "XLU": 0.0,
            }
        else:
            # MODERATE → balanced
            return {
                "SPY": 0.25, "QQQ": 0.20,
                "XLP": 0.10, "XLV": 0.10,
                "TLT": 0.10, "GLD": 0.10,
            }


# ---------------------------------------------------------------------------
# 5. David Tepper — Appaloosa
# ---------------------------------------------------------------------------
class DavidTepper(BasePersona):
    """David Tepper / Appaloosa macro + mean-reversion.

    Source: Appaloosa 13F. +24.2% in 2025, best since 2021.
    Q4 2025: Rotated into cyclicals + China, trimmed mega-cap tech.
    Whirlpool position increased 2000% (extreme mean-reversion bet).
    BABA remains largest position despite trimming.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="David Tepper (Appaloosa)",
            description="Macro mean-reversion: cyclicals + China, +24% in 2025",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "BABA", "PDD", "JD",  # China (actual top holdings)
                "WHR", "F", "GM",  # Cyclicals (actual trades)
                "AMZN", "GOOGL", "META",  # Tech (trimmed but held)
                "VST", "TSM",  # Winners (Vistra, TSMC)
                "XLF", "XLI",  # Sector ETFs
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
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            if any(v is None for v in [sma200, rsi]):
                continue
            # Tepper: mean-reversion on beaten-down + ride winners
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            if discount > 0.10 and rsi < 40:
                # Deep value mean-reversion (Tepper specialty)
                score = discount * 8 + (40 - rsi) / 40
                scored.append((sym, score))
            elif sma50 and price > sma50 > sma200 and rsi < 70:
                # Momentum winners (keep riding)
                score = 2.0
                scored.append((sym, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 6. Ken Griffin — Citadel
# ---------------------------------------------------------------------------
class KenGriffin(BasePersona):
    """Ken Griffin / Citadel mega-cap tech concentration.

    Source: Citadel 13F. $67B AUM. NVDA ~$4B, AMZN $3.2B positions.
    Doubled NVDA stake, added $2.5B AMZN.
    Strategy: Ultra-large positions in AI mega-caps with momentum.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Ken Griffin (Citadel)",
            description="Mega-cap AI concentration: $4B NVDA + $3.2B AMZN, $67B AUM",
            risk_tolerance=0.6,
            max_position_size=0.18,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "NVDA", "AMZN", "META", "GOOGL", "MSFT", "AAPL",
                "AVGO", "TSM", "CRM", "NOW",
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
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            macd = self._get_indicator(data, sym, "macd", date)
            macd_sig = self._get_indicator(data, sym, "macd_signal", date)
            if any(v is None for v in [sma50, sma200, rsi]):
                continue
            score = 0.0
            if price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            if 40 < rsi < 75:
                score += 0.5
            if score >= 3:
                scored.append((sym, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            total_score = sum(s for _, s in top)
            for sym, score in top:
                w = min((score / total_score) * 0.90, self.config.max_position_size)
                weights[sym] = w
        return weights


# ---------------------------------------------------------------------------
# 7. Dan Loeb — Third Point Event-Driven
# ---------------------------------------------------------------------------
class DanLoeb(BasePersona):
    """Dan Loeb / Third Point event-driven activist.

    Source: Third Point 13F. +24.2% in 2025.
    Top winners: Vistra, Amazon, Meta, TSM.
    Style: Activist value with catalyst-driven positions.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Dan Loeb (Third Point)",
            description="Event-driven activist: catalyst plays + quality momentum, +24% in 2025",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "VST", "AMZN", "META", "TSM",  # 2025 winners
                "GOOGL", "MSFT", "NVDA",  # Big tech
                "DIS", "PYPL", "UBER",  # Event-driven candidates
                "PG", "JNJ", "NEE",  # Defensive quality
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
            volume = self._get_indicator(data, sym, "Volume", date)
            vol_avg = self._get_indicator(data, sym, "volume_sma_20", date)
            if any(v is None for v in [sma50, rsi]):
                continue
            # Event-driven: momentum + volume confirmation
            score = 0.0
            if sma200 and price > sma50 > sma200:
                score += 2.0
            elif price > sma50:
                score += 1.0
            vol_ratio = volume / vol_avg if volume and vol_avg and vol_avg > 0 else 1
            if vol_ratio > 1.3:
                score += 1.0  # Volume = catalyst confirmation
            if 35 < rsi < 70:
                score += 0.5
            if score >= 2.5:
                scored.append((sym, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 8. Election Cycle Rotation
# ---------------------------------------------------------------------------
class ElectionCycleRotation(BasePersona):
    """Rotate sectors by presidential cycle year.

    Research: Since 1928, Year 3 (pre-election) positive 78% of time,
    avg +13.5%. Year 2 (midterm) weakest. Sector performance varies
    by cycle phase:
    - Year 1 (Early Cycle): Real Estate, Financials, Consumer Disc, IT
    - Year 2 (Midterm): Defensive sectors, lower exposure
    - Year 3 (Pre-Election): Growth sectors, max exposure
    - Year 4 (Election): Balanced, usually positive

    Strategy: Rotate sector ETFs based on presidential cycle year.
    Use momentum confirmation to filter within the sector universe
    for each phase. 2025=Y1, 2026=Y2, 2027=Y3, 2028=Y4.

    Source: CME Group, Fidelity, Stock Trader's Almanac.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Election Cycle Rotation",
            description="Sector rotation by presidential cycle year. Year 3 = max growth",
            risk_tolerance=0.5,
            max_position_size=0.20,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                # Growth / early cycle sectors
                "XLK", "XLY", "XLF", "XLRE", "XLI",
                # Defensive / late cycle sectors
                "XLP", "XLU", "XLV", "XLE", "XLB",
                # Broad + safe havens
                "SPY", "QQQ", "TLT", "GLD",
            ],
        )
        super().__init__(config)

    def _get_cycle_year(self, date):
        """Get presidential cycle year (1-4). 2025=Year 1."""
        year = date.year
        return ((year - 2025) % 4) + 1

    def generate_signals(self, date, prices, portfolio, data):
        cycle_year = self._get_cycle_year(date)

        # Define sector targets for each cycle year
        if cycle_year == 1:
            # Year 1 (Post-election honeymoon): early-cycle sectors
            target_sectors = ["XLF", "XLY", "XLK", "XLRE", "XLI"]
            target_weight = 0.80
            defensive_weight = 0.10
        elif cycle_year == 2:
            # Year 2 (Midterm): DEFENSIVE -- weakest year historically
            target_sectors = ["XLP", "XLU", "XLV", "XLE"]
            target_weight = 0.50
            defensive_weight = 0.35
        elif cycle_year == 3:
            # Year 3 (Pre-election): MAX GROWTH -- strongest year
            target_sectors = ["XLK", "XLY", "XLI", "XLB", "XLE"]
            target_weight = 0.85
            defensive_weight = 0.05
        else:
            # Year 4 (Election year): balanced, usually positive
            target_sectors = ["XLK", "XLF", "XLV", "XLI"]
            target_weight = 0.65
            defensive_weight = 0.20

        weights = {}
        scored = []

        # Score target sectors by momentum
        for sym in target_sectors:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]

            if sma50 is None or rsi is None:
                continue

            if rsi > 80:
                weights[sym] = 0.0
                continue

            score = 0.0
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5

            if 30 < rsi < 70:
                score += 1.0

            if score >= 1.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:5]

        if top:
            per_sector = min(target_weight / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_sector

        # Add defensive allocation
        if defensive_weight > 0:
            defensive_split = defensive_weight / 2
            if "TLT" in prices:
                weights["TLT"] = defensive_split
            if "GLD" in prices:
                weights["GLD"] = defensive_split

        # Zero out non-selected
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 9. Policy Catalyst
# ---------------------------------------------------------------------------
class PolicyCatalyst(BasePersona):
    """Trade on major policy announcement effects.

    Research: Infrastructure bills, tariffs, sanctions, and major
    policy changes create sector-specific catalysts. Event-driven
    strategies are popular among hedge funds for profiting from
    short-term price movements triggered by regulatory changes.

    Historical examples:
    - CHIPS Act (2022): semis surged (NVDA, AMD, INTC benefited)
    - Infrastructure Investment Act: construction/materials jumped
    - China tariffs: domestic manufacturers outperformed
    - Defense spending increases: LMT, RTX, NOC benefited
    - Clean energy policy: solar/wind stocks spiked

    Strategy: Monitor sectors that benefit from government policy
    catalysts. Use momentum + volume to detect policy-driven flows.
    When a policy-sensitive sector shows unusual momentum (SMA crossover
    + volume spike), it indicates a policy catalyst is being priced in.

    Source: LevelFields, CME Group, Fidelity.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Policy Catalyst",
            description="Event-driven: trade sectors benefiting from major policy announcements",
            risk_tolerance=0.6,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                # Semiconductors (CHIPS Act beneficiaries)
                "NVDA", "AMD", "INTC", "AVGO", "TSM",
                # Infrastructure / construction
                "CAT", "DE", "VMC", "MLM", "URI",
                # Defense (spending increases)
                "LMT", "RTX", "NOC", "GD",
                # Clean energy (climate policy)
                "ENPH", "FSLR", "NEE", "ICLN",
                # Domestic manufacturing (tariff beneficiaries)
                "X", "NUE", "CLF",
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

            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1

            # Exit: overbought post-catalyst
            if rsi > 80:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity > 0:
                    weights[sym] = 0.0
                continue

            # Exit: broken below SMA200 (policy failed to help)
            if sma200 is not None and price < sma200 * 0.85:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Policy catalyst proxy: strong momentum + volume
            # Policy effects show as persistent trend (not just one-day spikes)
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5

            # MACD bullish confirmation
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0

            # Volume elevation (institutional flows due to policy)
            if vol_ratio > 1.3:
                score += 1.0
            if vol_ratio > 2.0:
                score += 0.5  # Extra for very high volume

            # RSI in healthy momentum range
            if 40 < rsi < 70:
                score += 0.5
            elif 30 < rsi < 40:
                score += 0.3  # Slight discount for tepid momentum

            if score >= 3.0:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        # Zero out non-selected
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
POLITICAL_STRATEGIES = {
    "nancy_pelosi": NancyPelosi,
    "gop_trading": GOPTrading,
    "bipartisan_consensus": BipartisanConsensus,
    "polymarket_signal": PolymarketSignal,
    "david_tepper": DavidTepper,
    "ken_griffin": KenGriffin,
    "dan_loeb": DanLoeb,
    "election_cycle_rotation": ElectionCycleRotation,
    "policy_catalyst": PolicyCatalyst,
}


def get_political_strategy(name: str, **kwargs) -> BasePersona:
    cls = POLITICAL_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown: {name}. Available: {list(POLITICAL_STRATEGIES.keys())}")
    return cls(**kwargs)
