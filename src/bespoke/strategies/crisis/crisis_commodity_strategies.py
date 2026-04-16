"""Crisis, commodity, and event-catalyst trading strategies.

Based on research findings from agents:
- War/geopolitical → energy/defense spike
- Food crisis → fertilizer/agriculture
- Gaming/entertainment → content release catalysts
- Small cap value rotation
- Contrarian fallen angels

New additions:
- Rare earth / critical minerals
- Water scarcity plays
- Shipping / freight cycle

All backtested — never trust blindly.
"""

from __future__ import annotations

from bespoke.strategies.base import BaseStrategy as BasePersona, StrategyConfig as PersonaConfig


# ---------------------------------------------------------------------------
# 1. Geopolitical Crisis Alpha
# ---------------------------------------------------------------------------
class GeopoliticalCrisis(BasePersona):
    """Trade war/crisis → energy + defense beneficiaries.

    Research: Iran-Hormuz crisis (Feb 2026) doubled crude to $104+.
    XLE +40.8% YTD, ITA +54% trailing 12mo. Defense backlogs $1T+.

    Strategy: When market vol spikes (crisis proxy), rotate into
    energy + defense. When vol normalizes, reduce and take profits.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Geopolitical Crisis Alpha",
            description="War/crisis beneficiaries: energy + defense spike when vol rises",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "XLE", "XOP", "OXY", "DVN", "HAL", "SLB",  # Energy
                "LMT", "RTX", "NOC", "GD", "ITA",  # Defense
                "GLD", "SLV",  # Safe havens
                "SPY",  # Regime detection
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)
        ann_vol = spy_vol * (252 ** 0.5) if spy_vol is not None else 0.15

        weights = {}
        energy = ["XLE", "XOP", "OXY", "DVN", "HAL", "SLB"]
        defense = ["LMT", "RTX", "NOC", "GD", "ITA"]

        if ann_vol > 0.22:
            # Crisis mode: heavy energy + defense + safe havens
            crisis_picks = []
            for sym in energy + defense:
                if sym not in prices:
                    continue
                inds = self._get_indicators(data, sym, ["sma_50", "rsi_14"], date)
                sma50, rsi = inds["sma_50"], inds["rsi_14"]
                if rsi is not None and rsi > 80:
                    weights[sym] = 0.0
                    continue
                if sym in energy and (sma50 is None or prices[sym] <= sma50):
                    continue
                crisis_picks.append(sym)
            for sym in ["GLD", "SLV"]:
                if sym in self.config.universe and sym in prices and sym not in weights:
                    haven_rsi = self._get_indicator(data, sym, "rsi_14", date)
                    if haven_rsi is not None and haven_rsi > 80:
                        weights[sym] = 0.0
                    else:
                        crisis_picks.append(sym)
            if crisis_picks:
                per_stock = min(0.90 / len(crisis_picks), self.config.max_position_size)
                for sym in crisis_picks:
                    weights[sym] = per_stock
        else:
            # Normal: momentum-select best performers
            scored = []
            for sym in energy + defense:
                if sym not in prices:
                    continue
                inds = self._get_indicators(data, sym, ["sma_50", "sma_200"], date)
                sma50, sma200 = inds["sma_50"], inds["sma_200"]
                if sma50 is not None and sma200 is not None and sma200 > 0 and prices[sym] > sma50 > sma200:
                    scored.append((sym, (prices[sym] - sma200) / sma200))
            scored.sort(key=lambda x: x[1], reverse=True)
            top = scored[:self.config.max_positions]
            haven_budget = 0.0
            for sym in ["GLD", "SLV"]:
                if sym in self.config.universe and sym in prices:
                    haven_rsi = self._get_indicator(data, sym, "rsi_14", date)
                    if haven_rsi is not None and haven_rsi > 80:
                        weights[sym] = 0.0
                    else:
                        weights[sym] = 0.05
                        haven_budget += 0.05
            if top:
                per_stock = min((0.90 - haven_budget) / len(top), self.config.max_position_size)
                for sym, _ in top:
                    weights[sym] = per_stock

        # Close stale positions for symbols not in current weights
        for sym in self.config.universe:
            if sym in prices and sym != "SPY" and sym not in weights:
                weights[sym] = 0.0
        return {k: v for k, v in weights.items() if k in prices and k != "SPY"}


# ---------------------------------------------------------------------------
# 2. Agriculture & Food Security
# ---------------------------------------------------------------------------
class AgricultureFoodSecurity(BasePersona):
    """Food crisis / fertilizer shortage strategy.

    Research: Hormuz blockade cuts 33% of seaborne urea.
    NTR (largest potash), CF (low-cost gas), ADM, DE benefit.
    MOO ETF for broad agriculture equity exposure.

    Strategy: Momentum on agriculture + fertilizer names.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Agriculture & Food Security",
            description="Fertilizer + agriculture: food crisis beneficiaries",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "NTR", "CF", "MOS", "FMC",  # Fertilizer
                "ADM", "BG", "CTVA",  # Agribusiness
                "DE", "AGCO",  # Farm equipment
                "DBA", "MOO",  # Agriculture ETFs
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
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            if any(v is None for v in [sma50, rsi]):
                continue
            if rsi > 80:
                weights[sym] = 0.0
                continue
            if sma200 is not None and price < sma200 * 0.80:
                weights[sym] = 0.0
                continue
            score = 0.0
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5
            if 35 < rsi < 70:
                score += 0.5
            if score >= 2.0:
                scored.append((sym, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 3. Gaming Content Catalyst
# ---------------------------------------------------------------------------
class GamingContentCatalyst(BasePersona):
    """Buy-the-rumor-sell-the-news on game/content releases.

    Research findings:
    - NTDOY: buy 3-6mo before major launch, sell on release day
    - TTWO: buy delay dips (GTA VI delays = 7-10% drops, then +36% rallies)
    - DIS: box office barely moves stock, play earnings instead
    - NFLX: purely subscriber/earnings, content doesn't move stock
    - AMC: most correlated to individual movie weekends

    Strategy: Momentum in gaming publishers (strongest BRSN pattern).
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Gaming Content Catalyst",
            description="Buy-the-rumor on game publishers: NTDOY, TTWO, EA momentum",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "NTDOY", "TTWO", "EA",  # Game publishers (strongest signal)
                "RBLX", "U",  # Gaming platforms
                "DKNG", "FLUT",  # Gaming/betting (DraftKings + Flutter/FanDuel)
                "DIS", "NFLX",  # Entertainment (earnings plays)
                "CMCSA", "WBD",  # Media
                "SONY",  # PlayStation + entertainment conglomerate
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
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "Volume", "volume_sma_20"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            volume, vol_avg = inds["Volume"], inds["volume_sma_20"]
            if any(v is None for v in [sma50, rsi]):
                continue
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            # Buy momentum + volume confirmation (pre-launch buildup)
            score = 0.0
            if sma200 is not None and price > sma50 > sma200:
                score += 2.5
            elif price > sma50:
                score += 1.5
            if vol_ratio > 1.3:
                score += 1.0  # Volume = catalyst anticipation
            if 40 < rsi < 70:
                score += 0.5
            # Sell on extreme overbought (post-release selloff)
            if rsi > 80:
                weights[sym] = 0.0
                continue
            if score >= 2.5:
                scored.append((sym, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 4. Small Cap Value Rotation
# ---------------------------------------------------------------------------
class SmallCapValueRotation(BasePersona):
    """Small cap value rotation based on research.

    Research: Small caps at cheapest vs large caps in 50 YEARS.
    IWM +18% YTD 2026. AVUV 13.23% annualized since 2019.
    Multi-factor (value + quality + momentum) beats single-factor.

    Strategy: Rotate into small cap value ETFs + individual picks
    when small caps show momentum vs large caps.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Small Cap Value Rotation",
            description="Small caps at 50-year cheap: AVUV + momentum picks, 18% YTD 2026",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "AVUV", "DFSV", "VBR",  # Small cap value ETFs
                "IWM", "IWN",  # Small cap broad + value
                "GRC", "UCTT", "WTTR", "EVLV",  # Individual picks
                "SAIA", "DECK", "LULU", "CELH",  # Small cap winners
                "CAVA", "DUOL", "CWAN",  # Small cap growth picks
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
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            if any(v is None for v in [sma50, rsi]):
                continue
            if rsi > 80:
                weights[sym] = 0.0
                continue
            if sma200 is not None and price < sma200 * 0.80:
                weights[sym] = 0.0
                continue
            score = 0.0
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5
            if 35 < rsi < 70:
                score += 0.5
            # Small cap value premium: buy dips
            if sma200 is not None and price < sma200 * 1.05 and rsi < 40:
                score += 1.0  # Near SMA200 support
            if score >= 2.0:
                scored.append((sym, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 5. Contrarian Fallen Angels
# ---------------------------------------------------------------------------
class ContrarianFallenAngels(BasePersona):
    """Buy beaten-down quality stocks with activist/turnaround catalysts.

    Research: BA $682B backlog, INTC foundry milestones, PFE $60B+ revenue.
    NCLH (Elliott 10% stake, $56 target vs $21).
    CPI 2.4% + stabilizing rates = re-rating window.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Contrarian Fallen Angels",
            description="Buy beaten-down quality + activist catalysts: BA, INTC, PFE, NCLH",
            risk_tolerance=0.6,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "BA", "INTC", "PFE", "ENPH",  # Fallen angels
                "NCLH", "TRIP", "WEN",  # Activist targets
                "NKE", "PYPL", "DIS",  # Beaten-down quality
                "FMC", "CLX", "UPS",  # Deep value
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
            inds = self._get_indicators(data, sym, ["sma_200", "rsi_14", "Volume", "volume_sma_20"], date)
            sma200, rsi = inds["sma_200"], inds["rsi_14"]
            volume, vol_avg = inds["Volume"], inds["volume_sma_20"]
            if any(v is None for v in [sma200, rsi]):
                continue
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            # Exit structural freefall — >30% below SMA200 is falling knife
            if discount > 0.30:
                weights[sym] = 0.0
                continue
            # Buy deep discount + recovery signal
            if discount > 0.05 and rsi < 45:
                vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
                score = discount * 5 + max(0, 45 - rsi) / 45
                if vol_ratio > 1.5:
                    score *= 1.3  # Volume = institutional interest
                candidates.append((sym, score))
            # Take profits on recovery
            if rsi > 65 and discount < -0.10:
                weights[sym] = 0.0
        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 6. Rare Earth / Critical Minerals
# ---------------------------------------------------------------------------
class RareEarthCriticalMinerals(BasePersona):
    """Rare earth and critical minerals supply chain strategy.

    Hypothesis: China controls ~60% of rare earth mining and ~90% of
    processing. Any geopolitical tension, export restrictions, or
    supply disruption creates massive price spikes in rare earth
    miners and downstream users (EV, defense, semiconductors).
    The US CHIPS Act and EU Critical Raw Materials Act are creating
    secular demand for non-Chinese supply chains.

    Source: IEA (2021) "The Role of Critical Minerals in Clean Energy
    Transitions". US DoE Critical Materials Assessment (2023). MP
    Materials is the only US rare earth mine. Lynas (ASX:LYC, OTC:LYSCF)
    is the largest non-Chinese producer.

    Signal: Momentum in rare earth miners + materials ETFs. Buy on
    uptrend confirmation, exit on overbought or breakdown.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Rare Earth / Critical Minerals",
            description="Critical minerals supply chain: rare earth miners + battery metals",
            risk_tolerance=0.6,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                # Rare earth miners
                "MP",     # MP Materials (only US rare earth mine)
                # Lithium / battery metals
                "ALB",    # Albemarle (lithium)
                "SQM",    # Sociedad Quimica y Minera (lithium, Chile)
                "LAC",    # Lithium Americas
                "ALTM",   # Arcadium Lithium (ex-Livent/Allkem merger, acquired by RIO)
                # Uranium (nuclear renaissance)
                "CCJ",    # Cameco (uranium)
                "URA",    # Global X Uranium ETF
                # Copper (electrification metal)
                "FCX",    # Freeport-McMoRan (copper)
                "SCCO",   # Southern Copper
                # Broader materials
                "XME",    # SPDR S&P Metals & Mining ETF
                "PICK",   # iShares MSCI Global Metals & Mining
                "REMX",   # VanEck Rare Earth/Strategic Metals ETF
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

            # Exit: overbought commodity spike (take profits)
            if rsi > 80:
                weights[sym] = 0.0
                continue

            # Exit: broken below SMA200 (structural downturn)
            if sma200 is not None and price < sma200 * 0.85:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Momentum: uptrend in miners
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5

            # MACD bullish
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0

            # Volume confirmation (supply fears = volume surge)
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            if vol_ratio > 1.5:
                score += 0.5

            # RSI healthy range
            if 35 < rsi < 70:
                score += 0.5

            if score >= 2.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 7. Water Scarcity Plays
# ---------------------------------------------------------------------------
class WaterScarcity(BasePersona):
    """Water scarcity and water infrastructure investment strategy.

    Hypothesis: Global water stress is a secular mega-trend. 2 billion
    people lack safe drinking water (UN 2023). US water infrastructure
    needs $600B+ in investment (ASCE Infrastructure Report Card: D+).
    Water utilities have regulated returns + inflation pass-through,
    and water technology companies benefit from capex cycles.

    Source: Barclays "Blue Gold" (2019) -- water is the commodity of
    the 21st century. World Resources Institute: 17 countries (25% of
    world pop) face "extremely high" water stress. Xylem, Veolia, and
    American Water Works are the "Big 3" of water infrastructure.

    Signal: Momentum in water stocks + utilities. Low vol, defensive
    characteristics with secular growth tailwind.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Water Scarcity Plays",
            description="Water infrastructure and technology: secular scarcity mega-trend",
            risk_tolerance=0.4,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                # Water utilities
                "AWK",    # American Water Works (largest US water utility)
                "WTR",    # Essential Utilities (water + gas)
                "SJW",    # SJW Group (water utility, CA/TX)
                "YORW",   # York Water (oldest US utility, est. 1816)
                # Water technology / infrastructure
                "XYL",    # Xylem (water technology, pumps, analytics)
                "A",      # Agilent (water quality testing)
                "WTRG",   # Essential Utilities (Aqua America)
                "FBIN",   # Fortune Brands Innovations (water products)
                # Water ETFs
                "PHO",    # Invesco Water Resources ETF
                "FIW",    # First Trust Water ETF
                "CGW",    # Invesco S&P Global Water Index ETF
                # Broader infrastructure
                "ECL",    # Ecolab (water treatment / hygiene)
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
                ["sma_50", "sma_200", "rsi_14", "vol_20"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            vol20 = inds["vol_20"]

            if any(v is None for v in [sma50, rsi]):
                continue

            score = 0.0

            # Uptrend (quality filter for water utilities)
            if sma200 is not None and price > sma50 > sma200:
                score += 2.5
            elif price > sma50:
                score += 1.5
            else:
                continue  # Water stocks in downtrend = avoid

            # Low volatility bonus (water utilities are naturally low-vol)
            if vol20 is not None:
                if vol20 < 0.012:
                    score += 2.0
                elif vol20 < 0.018:
                    score += 1.0

            # RSI in healthy range
            if 30 < rsi < 65:
                score += 1.0
            elif rsi > 75:
                weights[sym] = 0.0
                continue

            if score >= 3.0:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 8. Shipping / Freight Cycle
# ---------------------------------------------------------------------------
class ShippingFreightCycle(BasePersona):
    """Shipping and freight cycle strategy.

    Hypothesis: Shipping is deeply cyclical with booms and busts driven
    by global trade volumes, fleet supply, and commodity demand. The
    Baltic Dry Index (BDI) is the best leading indicator of global
    growth. We proxy BDI via shipping stock performance.

    During upswings, container/bulk shippers see 3-5x earnings growth.
    During busts, they trade at deep discounts to NAV. The strategy
    buys shipping stocks in confirmed uptrends (momentum) and exits
    when momentum breaks.

    Source: Stopford (2009) "Maritime Economics" -- shipping cycles
    average 7-10 years. Greenwood & Hanson (2015) show investment in
    shipping perfectly inversely predicts returns. Alizadeh & Nomikos
    (2009) document mean reversion in freight rates.

    Signal: Momentum in shipping stocks. SMA50 > SMA200 = cycle upturn.
    Volume confirms institutional interest.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Shipping / Freight Cycle",
            description="Global shipping cycle: container/bulk shippers + freight ETFs",
            risk_tolerance=0.7,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                # Container shipping
                "ZIM",    # ZIM Integrated Shipping
                "MATX",   # Matson (Pacific container)
                # Dry bulk shipping
                "SBLK",   # Star Bulk Carriers
                "GOGL",   # Golden Ocean Group
                "GNK",    # Genco Shipping
                "EGLE",   # Eagle Bulk Shipping
                # Tankers
                "STNG",   # Scorpio Tankers
                "FRO",    # Frontline (VLCC tankers)
                "TNK",    # Teekay Tankers
                # LNG shipping
                "FLNG",   # Flex LNG
                # Shipping / logistics ETF
                "SEA",    # US Global Sea to Sky Cargo ETF
                # Freight / logistics
                "EXPD",   # Expeditors International
                "CHRW",   # CH Robinson (freight broker)
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
                 "Volume", "volume_sma_20", "atr_14"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]
            atr = inds["atr_14"]

            if any(v is None for v in [sma50, rsi]):
                continue

            # Exit: cycle bust signal (price crashed below SMA200)
            if sma200 is not None and price < sma200 * 0.80:
                weights[sym] = 0.0
                continue

            # Exit: overbought (take profits at cycle top)
            if rsi > 80:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Cycle upturn: SMA50 > SMA200 (golden cross = cycle starting)
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
                # Extra for strong momentum (typical in shipping booms)
                if sma200 > 0:
                    pct_above = (price - sma200) / sma200
                    score += min(pct_above * 3, 2.0)
            elif price > sma50:
                score += 1.5

            # MACD confirmation
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0

            # Volume rising (freight demand picking up)
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            if vol_ratio > 1.3:
                score += 0.5

            # RSI in momentum zone (not too hot, not too cold)
            if 40 < rsi < 70:
                score += 0.5

            if score >= 3.0:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 9. Product Tanker Shipping
# ---------------------------------------------------------------------------
class ProductTankerShipping(BasePersona):
    """Product tanker shipping cycle strategy.

    Thesis: Product tankers carry refined petroleum (gasoline, diesel,
    jet fuel) — distinct from crude tankers. The product tanker fleet
    is aging (average age 13+ years) with minimal newbuild orders due
    to uncertainty around future fuel standards. Ton-mile demand is
    growing as refinery capacity shifts to Middle East/Asia while
    consumption stays in West. TORM (TRMD) is the largest publicly
    traded product tanker company. Frontline (FRO) operates both
    crude and product tankers. Scorpio Tankers (STNG) has the youngest
    fleet. International Seaways (INSW) is a pure-play tanker with
    strong shareholder returns. These companies generate 30-50% FCF
    yields at peak rates.

    Source: Clarksons Research — product tanker earnings hit $50K/day
    in 2023-2024 vs $15K/day breakeven. Drewry: global product tanker
    fleet growth < 1% through 2027.

    Signal: Cycle timing via momentum. Buy when SMA50 > SMA200
    (freight rates rising). MACD and volume confirm institutional
    interest. Exit on overbought (rate normalization).
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Product Tanker Shipping",
            description="Product tanker cycle: aging fleet + ton-mile growth, 30-50% FCF yields at peak",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "TRMD",   # TORM plc (largest listed product tanker co)
                "FRO",    # Frontline Ltd (crude + product tankers)
                "STNG",   # Scorpio Tankers (youngest product tanker fleet)
                "INSW",   # International Seaways (pure-play tanker)
                "TNK",    # Teekay Tankers (product + crude tankers)
                "DHT",    # DHT Holdings (VLCC crude tankers)
                "HAFN",   # Hafnia Limited (product tanker pure-play)
                "ASC",    # Ardmore Shipping (MR product tankers)
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
                 "Volume", "volume_sma_20", "atr_14"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]

            if any(v is None for v in [sma50, rsi]):
                continue

            # Exit: cycle bust (price crashed below SMA200)
            if sma200 is not None and price < sma200 * 0.75:
                weights[sym] = 0.0
                continue

            # Exit: overbought (take profits at cycle top)
            if rsi > 80:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Cycle upturn: golden cross = freight rates rising
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
                # Extra for strong cycle momentum
                if sma200 > 0:
                    pct_above = (price - sma200) / sma200
                    score += min(pct_above * 3, 2.0)
            elif price > sma50:
                score += 1.5

            # MACD confirmation
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0

            # Volume rising (freight demand = cargo bookings)
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            if vol_ratio > 1.3:
                score += 0.5

            # RSI in momentum zone
            if 40 < rsi < 70:
                score += 0.5

            # Dip-buying in uptrend (pullback to SMA50 in bull cycle)
            if sma200 is not None and price > sma200 and rsi < 40:
                score += 1.5

            if score >= 3.0:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 10. Wartime Portfolio
# ---------------------------------------------------------------------------
class WartimePortfolio(BasePersona):
    """Historical wartime winners: defense, energy, commodities, gold.

    Research: During WWII, defense/energy sectors outperformed broad
    market. Gulf War 1990: oil surged 135%, defense stocks jumped.
    Post-9/11: gold sparked decade-long bull run. Ukraine 2022:
    Brent +75%, wheat +50%, defense stocks hit new highs.
    Defensive sectors outperform broader market by 8.5% during conflicts.
    LMT backlog $179B, NOC $92.8B (Q3 2025). Gold surges 15-40%
    during geopolitical crises.

    Strategy: Anti-fragile portfolio of historical wartime winners.
    Allocate across defense, energy, commodities, and gold. Use
    volatility regime to adjust weights -- higher vol = heavier
    wartime tilt. Momentum filter ensures we ride winners.

    Source: CFA Institute, Stock Trader's Almanac, Hero Bullion.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Wartime Portfolio",
            description="Anti-fragile: defense + energy + gold. Outperforms 8.5% during conflicts",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or [
                # Defense (record backlogs, conflict beneficiaries)
                "LMT", "RTX", "NOC", "GD", "LHX", "ITA",
                # Energy (oil supply disruption beneficiaries)
                "XLE", "XOM", "CVX", "OXY", "DVN",
                # Commodities / safe havens
                "GLD", "SLV", "DBA",
                # Broad market (regime detection)
                "SPY",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        # Detect volatility regime from SPY
        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)
        ann_vol = spy_vol * (252 ** 0.5) if spy_vol is not None else 0.15

        defense = ["LMT", "RTX", "NOC", "GD", "LHX", "ITA"]
        energy = ["XLE", "XOM", "CVX", "OXY", "DVN"]
        havens = ["GLD", "SLV", "DBA"]

        weights = {}
        scored = []

        # Higher vol = heavier wartime tilt
        if ann_vol > 0.25:
            target_defense = 0.40
            target_energy = 0.30
            target_haven = 0.20
        elif ann_vol > 0.18:
            target_defense = 0.30
            target_energy = 0.25
            target_haven = 0.15
        else:
            target_defense = 0.20
            target_energy = 0.20
            target_haven = 0.10

        # Score defense stocks
        def_picks = []
        for sym in defense:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            if rsi is not None and rsi > 80:
                weights[sym] = 0.0
                continue
            score = 0.0
            if sma50 is not None and prices[sym] > sma50:
                score += 2.0
            if sma200 is not None and prices[sym] > sma200:
                score += 1.0
            if rsi is not None and 35 < rsi < 70:
                score += 0.5
            if score >= 2.0:
                def_picks.append((sym, score))
        def_picks.sort(key=lambda x: x[1], reverse=True)

        # Score energy stocks
        ene_picks = []
        for sym in energy:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            if rsi is not None and rsi > 80:
                weights[sym] = 0.0
                continue
            score = 0.0
            if sma50 is not None and prices[sym] > sma50:
                score += 2.0
            if sma200 is not None and prices[sym] > sma200:
                score += 1.0
            if rsi is not None and 35 < rsi < 70:
                score += 0.5
            if score >= 2.0:
                ene_picks.append((sym, score))
        ene_picks.sort(key=lambda x: x[1], reverse=True)

        # Allocate defense budget
        if def_picks:
            per_stock = min(target_defense / len(def_picks), self.config.max_position_size)
            for sym, _ in def_picks:
                weights[sym] = per_stock

        # Allocate energy budget
        if ene_picks:
            per_stock = min(target_energy / len(ene_picks), self.config.max_position_size)
            for sym, _ in ene_picks:
                weights[sym] = per_stock

        # Safe havens (always hold some)
        haven_available = [s for s in havens if s in prices]
        if haven_available:
            per_haven = target_haven / len(haven_available)
            for sym in haven_available:
                rsi = self._get_indicator(data, sym, "rsi_14", date)
                if rsi is not None and rsi > 80:
                    weights[sym] = 0.0
                else:
                    weights[sym] = per_haven

        # Zero out symbols not selected
        for sym in self.config.universe:
            if sym in prices and sym != "SPY" and sym not in weights:
                weights[sym] = 0.0
        return {k: v for k, v in weights.items() if k in prices and k != "SPY"}


# ---------------------------------------------------------------------------
# 11. Crisis Rotation
# ---------------------------------------------------------------------------
class CrisisRotation(BasePersona):
    """Rotate between offense (growth) and defense (bonds/gold) by VIX regime.

    Research: Safe haven comparison shows gold effective across all
    major crises (1987, 1997, 2008). Short-term T-bills best during
    crises (no duration risk). During Gulf War, buying during
    uncertainty yielded 17.63% in 4 weeks. Contrarian buying during
    2008 crisis produced outsized returns.

    Strategy: Multi-regime rotation using volatility + momentum.
    Low vol: max growth. Medium vol: balanced. High vol: defensive.
    Extreme vol (VIX>35 proxy): contrarian buy -- historically,
    buying during extreme fear yields 81.5% win rate at 3 weeks
    (from VIXFearBuy research).

    More sophisticated than existing CrisisAlpha (which only switches
    between 2 states). This uses 4 regimes + contrarian signals.

    Source: ScienceDirect, Morningstar, Berkshire Edge.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Crisis Rotation",
            description="4-regime VIX rotation: growth/balanced/defensive/contrarian-buy",
            risk_tolerance=0.5,
            max_position_size=0.30,
            max_positions=8,
            rebalance_frequency="daily",
            universe=universe or [
                # Growth / offense
                "SPY", "QQQ", "IWM",
                # Defensive / safe havens
                "TLT", "GLD", "SHY",
                # Sector hedges
                "XLP", "XLV", "XLU",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)
        spy_rsi = self._get_indicator(data, "SPY", "rsi_14", date)
        spy_sma50 = self._get_indicator(data, "SPY", "sma_50", date)
        spy_sma200 = self._get_indicator(data, "SPY", "sma_200", date)
        spy_price = prices.get("SPY")

        if spy_vol is None or spy_price is None:
            return {"SPY": 0.30, "TLT": 0.20, "GLD": 0.15}

        ann_vol = spy_vol * (252 ** 0.5)

        # Check for 5-day cumulative loss (weekly crisis proxy)
        weekly_crisis = False
        if "SPY" in data and "Close" in data["SPY"].columns:
            try:
                loc = int(data["SPY"].index.get_loc(date))
                if loc >= 5:
                    close_5d = data["SPY"]["Close"].iloc[loc - 5]
                    if close_5d > 0:
                        ret_5d = data["SPY"]["Close"].iloc[loc] / close_5d - 1
                        if ret_5d < -0.05:
                            weekly_crisis = True
                        # Also check 10-day for deeper crisis
                        if loc >= 10:
                            close_10d = data["SPY"]["Close"].iloc[loc - 10]
                            if close_10d > 0:
                                ret_10d = data["SPY"]["Close"].iloc[loc] / close_10d - 1
                                if ret_10d < -0.10:
                                    weekly_crisis = True
            except (KeyError, TypeError, ValueError):
                pass

        # Regime 1: EXTREME FEAR (VIX > 35 proxy) -- contrarian buy
        if ann_vol > 0.35 or (spy_rsi is not None and spy_rsi < 20) or weekly_crisis:
            # Historical: buying extreme fear yields 81.5% win at 3 weeks
            return {
                "SPY": 0.35, "QQQ": 0.25, "IWM": 0.15,
                "GLD": 0.10, "TLT": 0.05,
                "XLP": 0.0, "XLV": 0.0, "XLU": 0.0, "SHY": 0.0,
            }

        # Regime 2: HIGH VOL (VIX 25-35) -- defensive
        if ann_vol > 0.25 or (spy_rsi is not None and spy_rsi < 30):
            return {
                "TLT": 0.25, "GLD": 0.20, "SHY": 0.15,
                "XLP": 0.15, "XLV": 0.10,
                "SPY": 0.05, "QQQ": 0.0, "IWM": 0.0,
                "XLU": 0.0,
            }

        # Regime 3: MODERATE VOL (VIX 15-25) -- balanced
        if ann_vol > 0.15:
            trend_up = spy_sma50 is not None and spy_price > spy_sma50
            if trend_up:
                return {
                    "SPY": 0.25, "QQQ": 0.20, "IWM": 0.10,
                    "TLT": 0.10, "GLD": 0.10,
                    "XLP": 0.05, "XLV": 0.05,
                    "SHY": 0.0, "XLU": 0.0,
                }
            else:
                return {
                    "SPY": 0.15, "QQQ": 0.10,
                    "TLT": 0.20, "GLD": 0.15,
                    "XLP": 0.10, "XLV": 0.10,
                    "IWM": 0.0, "SHY": 0.05, "XLU": 0.0,
                }

        # Regime 4: LOW VOL (VIX < 15) -- max growth
        return {
            "SPY": 0.35, "QQQ": 0.30, "IWM": 0.15,
            "TLT": 0.05, "GLD": 0.05,
            "XLP": 0.0, "XLV": 0.0, "XLU": 0.0, "SHY": 0.0,
        }


# ---------------------------------------------------------------------------
# 12. Commodity Supercycle
# ---------------------------------------------------------------------------
class CommoditySupercycle(BasePersona):
    """Ride commodity supercycles when commodities outperform stocks.

    Research: Commodity supercycles average 7-15 years. Key signals:
    broad price increases, structural demand shifts, supply bottlenecks,
    USD weakening, commodity stocks outperforming indices. Copper demand
    to grow 53% by 2040 (BloombergNEF). Oil surges 50-300% during
    major conflicts. Agriculture spikes on supply disruption (wheat
    +50%, corn +40% during Ukraine war).

    Strategy: Monitor commodity ETFs vs SPY. When commodities show
    3+ month outperformance (SMA50 > SMA200 in commodity ETFs while
    SPY is flat/down), increase commodity allocation. Use momentum
    across oil, copper, agriculture, and gold to ride the cycle.

    Source: Capital.com, Mining.com, World Bank.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Commodity Supercycle",
            description="Ride multi-commodity momentum when commodities outperform stocks",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                # Energy
                "XLE", "XOP", "USO",
                # Metals / mining
                "GLD", "SLV", "XME", "FCX", "SCCO",
                # Agriculture
                "DBA", "MOO", "NTR", "CF",
                # Copper / base metals
                "COPX",
                # Broad commodity
                "DJP", "GSG",
                # Reference for regime detection
                "SPY",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        # Detect supercycle regime: are commodities outperforming SPY?
        spy_sma50 = self._get_indicator(data, "SPY", "sma_50", date)
        spy_sma200 = self._get_indicator(data, "SPY", "sma_200", date)
        spy_price = prices.get("SPY")

        # Score each commodity group
        energy = ["XLE", "XOP", "USO"]
        metals = ["GLD", "SLV", "XME", "FCX", "SCCO"]
        agri = ["DBA", "MOO", "NTR", "CF"]
        base_metals = ["COPX"]
        broad = ["DJP", "GSG"]

        all_commodity = energy + metals + agri + base_metals + broad

        # Count how many commodity ETFs are in uptrend
        uptrend_count = 0
        total_checked = 0
        scored = []

        for sym in all_commodity:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]

            if sma50 is None:
                continue

            total_checked += 1

            # Check uptrend (supercycle signal)
            if sma200 is not None and price > sma50 > sma200:
                uptrend_count += 1

            # Skip overbought
            if rsi is not None and rsi > 80:
                continue

            score = 0.0
            # Momentum scoring
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5

            # MACD confirmation
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0

            # RSI healthy range
            if rsi is not None and 35 < rsi < 70:
                score += 0.5

            if score >= 2.0:
                scored.append((sym, score))

        # Determine supercycle regime
        uptrend_pct = uptrend_count / max(total_checked, 1)

        # Supercycle active: >50% of commodity ETFs in uptrend
        if uptrend_pct > 0.50:
            allocation_budget = 0.90  # Full commodity allocation
        elif uptrend_pct > 0.30:
            allocation_budget = 0.60  # Moderate allocation
        else:
            allocation_budget = 0.30  # Minimal allocation (some diversification)

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]

        weights = {}
        if top:
            per_stock = min(allocation_budget / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        # Zero out non-selected
        for sym in all_commodity:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return {k: v for k, v in weights.items() if k in prices and k != "SPY"}


CRISIS_COMMODITY_STRATEGIES = {
    "geopolitical_crisis": GeopoliticalCrisis,
    "agriculture_food": AgricultureFoodSecurity,
    "gaming_catalyst": GamingContentCatalyst,
    "small_cap_value_rotation": SmallCapValueRotation,
    "contrarian_fallen_angels": ContrarianFallenAngels,
    "rare_earth_minerals": RareEarthCriticalMinerals,
    "water_scarcity": WaterScarcity,
    "shipping_freight_cycle": ShippingFreightCycle,
    "product_tanker_shipping": ProductTankerShipping,
    "wartime_portfolio": WartimePortfolio,
    "crisis_rotation": CrisisRotation,
    "commodity_supercycle": CommoditySupercycle,
}


def get_crisis_commodity_strategy(name: str, **kwargs) -> BasePersona:
    cls = CRISIS_COMMODITY_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown: {name}. Available: {list(CRISIS_COMMODITY_STRATEGIES.keys())}")
    return cls(**kwargs)
