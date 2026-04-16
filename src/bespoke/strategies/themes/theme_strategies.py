"""Theme-based trading strategies for bespoke.

These personas trade based on macro themes and megatrends rather than
individual investor philosophies. Each theme targets a specific sector
thesis with its own universe and timing signals.

Themes:
    1. AIRevolution              — AI/ML infrastructure and applications
    2. CleanEnergy               — Renewables, EVs, batteries, grid
    3. DefenseAerospace          — Defense contractors, space, cybersecurity
    4. BiotechBreakout           — Biotech/pharma innovation and FDA catalysts
    5. ChinaTechRebound          — China tech ADRs recovery play
    6. LatAmGrowth               — Latin American growth (fintech, commodities)
    7. InfrastructureBoom        — Infrastructure spending (bridges, 5G, data centers)
    8. SmallCapValue             — Small cap deep value (IWM universe)
    9. CryptoEcosystem           — Crypto-adjacent public companies
    10. AgingPopulation          — Healthcare, senior living, pharma for aging demographics
    11. GLP1Obesity              — GLP-1 / weight loss drug megatrend
    12. RoboticsAutonomous       — Humanoid robots + autonomous vehicles
    + SemiconductorValue         — Semi picks-and-shovels at value
    + SubscriptionMonopoly       — Sticky subscription moats
    + ContrastivePairs           — Long value side of hype sectors
    + GlobalFinancialInfra       — Financial infrastructure monopolies
    + ReshoringIndustrial        — US reshoring beneficiaries
    + WaterMonopoly              — Water utility monopolies
    + RegulatedData              — Regulated data monopolies
    + ChinaADRDeepValue          — China ADR deep value
    + CloudCyberValue            — Cloud & cybersecurity value entries
    + GlobalAirlinesTravel       — Airlines & travel recovery / momentum
    + UtilityInfraIncome         — Utility & infrastructure income
    + JapanIndustrialFinance     — Japan industrial & finance reform
    + DefensePrimeContractors    — Defense prime contractors (NATO spend)
    + GlobalConsumerStaples      — Global consumer staples income
    + EmergingMarketETFValue     — Emerging market ETF value
    + GlobalPharmaPipeline       — Global pharma pipeline value
    + SingaporeAlpha             — Singapore heritage consumer + REITs
    + UKEuropeanBanking          — UK & European bank deep value
    + TelecomEquipment5G         — 5G equipment & infrastructure
    + GigEconomySaaSDisruptors   — Gig economy + SaaS growth disruptors
    + KoreanChaebols             — Korean chaebol conglomerates + fintech
    + RideshareMobility          — Rideshare & mobility platforms
    + NvidiaSupplyChain          — NVIDIA peripheral supply chain (non-megacap)
    + Mag7HiddenSuppliers        — Hidden supply chain monopolies ALL Mag7 depend on
    + Mag7DominoHedge            — Supply chain stress early-warning hedge
    + AIInfrastructureLayer      — Railroad builders of AI (data centers, power, cooling)
    + AIApplicationSurvivors     — The Amazons: real-revenue AI apps that survive the bust
    + AIAdoptersNotBuilders      — Walmart principle: established companies adopting AI
    + LateCycleBubbleHedge       — 1999 detector: rotate to value when AI gets frothy
    + PicksAndShovelsAI          — Levi Strauss principle: sell tools to AI miners
    + InfrastructureReshoring    — US infrastructure spending: PAVE, heavy equipment, materials
    + AnthropicEcosystem         — Anthropic supply chain + investors pre-IPO (Q4 2026)
    + OpenAIEcosystem            — OpenAI/Microsoft-centric AI ecosystem
    + AIInfraPicksShovels        — Arms dealer: wins regardless of which AI company dominates
    + AIMegaEcosystem            — All 41 AI tickers, conviction-weighted mega-strategy
    + GenomicsRevolution         — Gene editing, synthetic bio, diagnostics (ARK ARKG)
    + HumanoidRoboticsSupplyChain — Brain + body + integrator robotics (KraneShares KOID)
"""

from __future__ import annotations


def _is_missing(v):
    """Check if value is None or NaN."""
    return v is None or v != v

from bespoke.strategies.base import BaseStrategy as BasePersona, StrategyConfig as PersonaConfig


# ---------------------------------------------------------------------------
# 1. AI Revolution
# ---------------------------------------------------------------------------
class AIRevolution(BasePersona):
    """AI/ML megatrend strategy.

    Thesis: AI is a generational shift. Companies building AI infrastructure
    (GPUs, cloud, data centers) and AI applications will outperform.

    Signals: Buy on trend alignment (SMA50 > SMA200), momentum.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="AI Revolution",
            description="AI megatrend: GPUs, cloud, data centers, AI applications",
            risk_tolerance=0.8,
            max_position_size=0.20,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "NVDA", "AMD", "AVGO", "MRVL", "ARM",  # AI chips
                "TSM", "ASML",  # AI chip manufacturing (picks & shovels)
                "MSFT", "GOOGL", "AMZN", "META",  # AI cloud/apps
                "PLTR", "AI", "PATH", "SNOW",  # AI software
                "SMH", "SOXX",  # Semiconductor ETFs
                "SMCI", "DELL", "HPE",  # AI servers
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
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]

            if any(v is None for v in [sma50, sma200, rsi]):
                continue

            # Thesis broken
            if price < sma200 * 0.90:
                weights[sym] = 0.0
                continue
            if rsi > 80:
                weights[sym] = 0.0
                continue

            score = 0.0
            if price > sma50 > sma200:
                score += 3.0  # Full trend alignment
            elif price > sma50:
                score += 1.5
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            if 40 < rsi < 75:
                score += 0.5

            if score > 2:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 2. Clean Energy
# ---------------------------------------------------------------------------
class CleanEnergy(BasePersona):
    """Clean energy / green transition strategy.

    Thesis: Global energy transition to renewables creates multi-decade growth.
    Buy solar, wind, EV, battery, and grid companies.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Clean Energy Transition",
            description="Renewables, EVs, batteries: buy the green transition",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "ENPH", "SEDG", "FSLR", "RUN",  # Solar
                "TSLA", "RIVN", "LCID", "NIO", "LI", "XPEV",  # EVs
                "ALB", "SQM",  # Lithium/batteries (LTHM merged into Arcadium/RIO)
                "NEE", "AES", "BEP",  # Utilities/renewables
                "ICLN", "TAN", "QCLN",  # Clean energy ETFs
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

            # Broken trend: >15% below SMA200 (clean energy is volatile)
            if sma200 is not None and price < sma200 * 0.85:
                weights[sym] = 0.0
                continue

            # Buy dips in uptrend or recovery from oversold
            if sma200 is not None and price > sma200 and rsi < 55:
                score = 2.0
                if sma50 > 0 and abs(price - sma50) / sma50 < 0.05:
                    score += 1.0  # Near SMA50 support
                scored.append((sym, score))
            elif rsi < 30:
                scored.append((sym, 1.5))  # Oversold bounce
            elif rsi > 80:
                weights[sym] = 0.0

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 3. Defense & Aerospace
# ---------------------------------------------------------------------------
class DefenseAerospace(BasePersona):
    """Defense, aerospace, and cybersecurity strategy.

    Thesis: Geopolitical tensions drive sustained defense spending.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Defense & Aerospace",
            description="Defense spending boom: contractors, space, cybersecurity",
            risk_tolerance=0.4,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "LMT", "RTX", "NOC", "GD", "BA", "LHX",  # Defense
                "PLTR", "CRWD", "PANW", "ZS", "FTNT",  # Cybersecurity
                "RKLB", "ASTS", "LUNR",  # Space
                "ITA", "XAR",  # Defense ETFs
                "HII", "TDG", "HWM",  # Niche defense
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
            inds = self._get_indicators(data, sym, ["sma_200", "rsi_14"], date)
            sma200, rsi = inds["sma_200"], inds["rsi_14"]
            if sma200 is None:
                continue

            # Defense stocks tend to be stable — buy near SMA200
            # Broken trend: >20% below SMA200
            if price < sma200 * 0.80:
                weights[sym] = 0.0
                continue
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            if discount > -0.10 and (rsi is None or rsi < 65):
                score = max(discount + 0.10, 0.01) + 0.3
                candidates.append((sym, score))
            elif rsi is not None and rsi > 80:
                weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 4. Biotech Breakout
# ---------------------------------------------------------------------------
class BiotechBreakout(BasePersona):
    """Biotech innovation and catalyst strategy.

    Thesis: Biotech has binary outcomes — buy diversified basket,
    overweight momentum leaders, cut losers fast.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Biotech Breakout",
            description="Biotech innovation: diversified basket, momentum leaders, cut losers",
            risk_tolerance=0.8,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or [
                "MRNA", "REGN", "VRTX", "GILD", "BIIB",  # Large biotech
                "ALNY", "IONS", "BMRN", "ARGX",  # Mid biotech (SGEN acquired by PFE)
                "XBI", "IBB", "BBH",  # Biotech ETFs
                "ISRG", "DXCM", "HIMS",  # MedTech
                "LLY", "ABBV", "MRK", "AMGN",  # Big pharma with biotech pipelines
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
            sma50, sma200 = inds["sma_50"], inds["sma_200"]
            rsi, vol = inds["rsi_14"], inds["vol_20"]
            if any(v is None for v in [sma50, rsi]):
                continue

            # Cut losers fast (biotech-specific)
            if sma200 is not None and price < sma200 * 0.85:
                weights[sym] = 0.0
                continue

            score = 0.0
            if price > sma50:
                score += 1.5
            if sma200 is not None and sma50 > sma200:
                score += 1.0
            if 35 < rsi < 70:
                score += 0.5
            # Prefer lower-vol names (less binary risk)
            if vol is not None and vol < 0.03:
                score += 0.5

            if score > 1.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 5. China Tech Rebound
# ---------------------------------------------------------------------------
class ChinaTechRebound(BasePersona):
    """China tech ADR recovery strategy.

    Thesis: China tech crackdown created deep value. Recovery plays in
    BABA, JD, PDD etc when regulation stabilizes.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="China Tech Rebound",
            description="China tech ADR recovery: deep value after regulatory crackdown",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "BABA", "JD", "PDD", "BIDU", "NIO", "XPEV", "LI",
                "TME", "BILI", "NTES", "IQ", "WB",
                "TCOM", "ZTO", "FUTU",  # Travel, logistics, fintech
                "KWEB", "MCHI", "FXI",  # China ETFs
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

            # Recovery signal: price crossing above SMA50
            if price > sma50 and rsi < 60:
                score = 2.0
                if sma200 is not None and price > sma200:
                    score += 1.5  # Full recovery
                scored.append((sym, score))
            elif rsi < 25:
                scored.append((sym, 1.5))  # Deep oversold bounce
            elif rsi > 75:
                weights[sym] = 0.0  # Take profits

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 6. LatAm Growth
# ---------------------------------------------------------------------------
class LatAmGrowth(BasePersona):
    """Latin American growth strategy.

    Thesis: LatAm fintech, e-commerce, and commodity exporters benefit
    from structural digitization and commodity supercycle.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="LatAm Growth",
            description="Latin American fintech, e-commerce, commodities growth",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "MELI", "NU", "STNE", "PAGS",  # Fintech/e-commerce
                "VALE", "PBR", "ITUB", "BSBR",  # Brazilian blue chips
                "SQM", "GGAL", "CRESY",  # Chile/Argentina
                "AMX", "FMX", "BSMX",  # Mexican blue chips
                "EWZ", "EWW", "ILF",  # LatAm ETFs
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

            # Broken trend: >15% below SMA200 (LatAm stocks can freefall)
            if sma200 is not None and price < sma200 * 0.85:
                weights[sym] = 0.0
                continue

            if price > sma50 and rsi < 65:
                score = 1.5
                if sma200 is not None and price > sma200:
                    score += 1.0
                scored.append((sym, score))
            elif rsi < 30:
                scored.append((sym, 1.0))
            elif rsi > 75:
                weights[sym] = 0.0

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 7. Infrastructure Boom
# ---------------------------------------------------------------------------
class InfrastructureBoom(BasePersona):
    """Infrastructure spending megatrend.

    Thesis: IIJA + CHIPS Act + global infra spending creates multi-year
    tailwind for construction, 5G, data centers.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Infrastructure Boom",
            description="Infrastructure spending: construction, 5G, data centers, utilities",
            risk_tolerance=0.4,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "CAT", "DE", "VMC", "MLM",  # Construction/materials
                "AMT", "CCI", "EQIX", "DLR",  # Towers/data centers
                "T", "VZ", "TMUS",  # Telecom/5G
                "NEE", "DUK", "SO",  # Utilities
                "PAVE", "IFRA",  # Infrastructure ETFs
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
            inds = self._get_indicators(data, sym, ["sma_200", "rsi_14"], date)
            sma200, rsi = inds["sma_200"], inds["rsi_14"]
            if sma200 is None:
                continue

            # Broken trend: >20% below SMA200
            if price < sma200 * 0.80:
                weights[sym] = 0.0
                continue
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            if rsi is not None and rsi > 70:
                weights[sym] = 0.0
            elif discount > -0.10:
                score = max(discount + 0.10, 0.01) + 0.3
                if rsi is not None and rsi < 40:
                    score += 0.2
                candidates.append((sym, score))

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 8. Small Cap Deep Value
# ---------------------------------------------------------------------------
class SmallCapValue(BasePersona):
    """Small cap deep value strategy.

    Thesis: Small caps are inefficiently priced. Buy deeply oversold
    small caps with volume confirmation for mean-reversion.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Small Cap Deep Value",
            description="Small cap inefficiency: buy deeply oversold with volume spikes",
            risk_tolerance=0.7,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or [
                "SMCI", "CELH", "CAVA", "DUOL", "RELY", "CWAN",
                "HUBS", "SAIA", "RCL", "BURL", "DECK", "LULU",
                "EXAS", "FTNT", "MTDR", "CEIX",
                "IWM", "IWO", "SCHA",  # Small cap ETFs
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
            inds = self._get_indicators(data, sym, ["bb_lower", "rsi_14", "Volume", "volume_sma_20"], date)
            bb_lower, rsi = inds["bb_lower"], inds["rsi_14"]
            volume, vol_avg = inds["Volume"], inds["volume_sma_20"]
            if rsi is None:
                continue

            # Deep value: oversold + volume spike
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            if rsi < 30 and vol_ratio > 1.5:
                score = (30 - rsi) / 30 * 3 + min(vol_ratio, 3.0)
                scored.append((sym, score))
            elif bb_lower is not None and price < bb_lower and rsi < 35 and vol_ratio > 0.5:
                score = 2.0
                scored.append((sym, score))
            elif rsi > 80:
                weights[sym] = 0.0

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 9. Crypto Ecosystem
# ---------------------------------------------------------------------------
class CryptoEcosystem(BasePersona):
    """Crypto-adjacent public companies strategy.

    Thesis: Crypto adoption creates value for miners, exchanges,
    and companies with BTC on balance sheet.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Crypto Ecosystem",
            description="Crypto-adjacent: miners, exchanges, BTC treasury companies",
            risk_tolerance=0.9,
            max_position_size=0.20,
            max_positions=6,
            rebalance_frequency="daily",
            universe=universe or [
                "COIN", "MARA", "RIOT", "CLSK",  # Mining/exchange
                "MSTR", "HUT",  # BTC treasury
                "SQ", "PYPL",  # Payment + crypto
                "BITO", "IBIT",  # Bitcoin ETFs
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
            inds = self._get_indicators(data, sym, ["sma_20", "sma_50", "rsi_14", "Volume", "volume_sma_20"], date)
            sma20, sma50, rsi = inds["sma_20"], inds["sma_50"], inds["rsi_14"]
            volume, vol_avg = inds["Volume"], inds["volume_sma_20"]
            if any(v is None for v in [sma20, rsi]):
                continue

            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1

            # Crypto is momentum-driven — ride breakouts
            if price > sma20 and rsi < 75 and vol_ratio > 1.2:
                score = 2.0 + min(vol_ratio, 5.0)
                if sma50 is not None and price > sma50:
                    score += 1.0
                scored.append((sym, score))
            elif rsi > 85:
                weights[sym] = 0.0
            elif rsi < 20 and vol_ratio > 2:
                scored.append((sym, 3.0))  # Capitulation buy

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            total_score = sum(s for _, s in top)
            cap = self.config.max_position_size
            for sym, score in top:
                weights[sym] = min((score / total_score) * 0.90, cap)
            # Iteratively redistribute clipped excess until fully allocated
            for _ in range(10):
                total_w = sum(weights[sym] for sym, _ in top)
                if total_w >= 0.899 or total_w <= 0:
                    break
                uncapped = [(sym, s) for sym, s in top if weights[sym] < cap - 1e-9]
                if not uncapped:
                    break
                uncapped_w = sum(weights[sym] for sym, _ in uncapped)
                if uncapped_w <= 0:
                    break
                surplus = 0.90 - total_w
                for sym, _ in uncapped:
                    weights[sym] = min(weights[sym] + surplus * weights[sym] / uncapped_w, cap)
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 10. Aging Population
# ---------------------------------------------------------------------------
class AgingPopulation(BasePersona):
    """Aging population demographic megatrend.

    Thesis: Global aging drives demand for healthcare, senior living,
    pharmaceuticals, and medical devices.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Aging Population",
            description="Demographic megatrend: healthcare, pharma, senior care",
            risk_tolerance=0.3,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                "UNH", "HUM", "CI", "ELV",  # Health insurance
                "JNJ", "PFE", "MRK", "LLY", "ABBV",  # Big pharma
                "ISRG", "SYK", "MDT", "ABT",  # Medical devices
                "XLV", "VHT",  # Healthcare ETFs
                "WELL", "VTR",  # Senior housing REITs
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
            inds = self._get_indicators(data, sym, ["sma_200", "rsi_14"], date)
            sma200, rsi = inds["sma_200"], inds["rsi_14"]
            if sma200 is None:
                continue

            # Broken trend: >20% below SMA200
            if price < sma200 * 0.80:
                weights[sym] = 0.0
                continue
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            # Defensive: buy near or below SMA200
            if rsi is not None and rsi > 70:
                weights[sym] = 0.0
            elif discount > -0.10:
                score = max(discount + 0.10, 0.01) + 0.3
                if rsi is not None and rsi < 40:
                    score += 0.1
                candidates.append((sym, score))

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 11. GLP-1 / Obesity Revolution
# ---------------------------------------------------------------------------
class GLP1Obesity(BasePersona):
    """GLP-1 / weight loss drug megatrend.

    2026: $73-87B market, LLY past $1T. Oral pills coming.
    30M Americans on GLP-1 by 2030.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="GLP-1 / Obesity Revolution",
            description="Weight loss drug megatrend: $73-87B market, LLY/NVO leaders",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "LLY", "NVO", "AMGN", "VKTX",  # GLP-1 leaders
                "ZEAL",  # Zealand Pharma (GLP-1 pipeline)
                "PFE", "ABBV", "MRK",  # Big pharma with obesity programs
                "HIMS", "PLNT",  # Weight loss ecosystem
                "ISRG",  # Bariatric surgery (competitive angle)
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
            if sma200 is not None and price < sma200 * 0.90:
                weights[sym] = 0.0
                continue
            if rsi > 80:
                weights[sym] = 0.0
                continue

            score = 0.0
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5
            if 35 < rsi < 75:
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
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 12. Robotics & Autonomous Vehicles
# ---------------------------------------------------------------------------
class RoboticsAutonomous(BasePersona):
    """Robotics and autonomous vehicles megatrend.

    CES 2026: humanoid robots commercially viable, Level 4 autonomy.
    Global robotics market > $200B by decade end.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Robotics & Autonomous",
            description="Humanoid robots + autonomous vehicles: $200B market by 2030",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "ISRG", "NVDA", "INTC", "TER", "CGNX",
                "GOOGL", "TSLA", "GM",
                "ROK", "ABB", "HON",  # Industrial automation / robotics
                "BOTZ", "ROBO",  # Robotics & AI ETFs
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
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]
            if any(v is None for v in [sma50, rsi]):
                continue
            if sma200 is not None and price < sma200 * 0.85:
                weights[sym] = 0.0
                continue
            if rsi > 80:
                weights[sym] = 0.0
                continue

            score = 0.0
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            if 40 < rsi < 75:
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
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 13. Semiconductor Value (not AI hype — supply chain deep value)
# ---------------------------------------------------------------------------
class SemiconductorValue(BasePersona):
    """Buy the semiconductor PICKS AND SHOVELS at value prices, not AI hype.

    Everyone chases NVDA. Smart money buys the companies NVDA depends on:
    TSMC (makes the chips), ASML (makes the machines that make the chips),
    memory companies at cyclical lows (WDC, MU), and equipment companies (LRCX, KLAC).

    Edge: Semi cycles are predictable — buy at low RSI when inventory clears.
    Memory is a commodity cycle: oversupply → crash → consolidation → undersupply → boom.
    Equipment companies have 80%+ recurring service revenue nobody prices in.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Semiconductor Value (Picks & Shovels)",
            description="Semi supply chain at value prices: TSMC, ASML, memory at cyclical lows, equipment recurring revenue",
            risk_tolerance=0.6,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "TSM",    # TSMC — makes 90% of advanced chips
                "ASML",   # ASML — monopoly on EUV lithography
                "AVGO",   # Broadcom — custom AI chips + VMware
                "SSNLF",  # Samsung (OTC) — memory + foundry
                "WDC",    # Western Digital — NAND flash, cyclical low
                "MU",     # Micron — DRAM/NAND, HBM for AI
                "LRCX",   # Lam Research — etch equipment
                "KLAC",   # KLA Corp — inspection equipment
                "AMAT",   # Applied Materials — deposition equipment
                "CRSR",   # Corsair Gaming — peripherals, undervalued
                "ON",     # ON Semi — auto/industrial chips
                "MRVL",   # Marvell — data center networking
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # VALUE: buy below SMA200 (cyclical low)
            if price < sma200 * 0.90:
                score += 3.0  # Deep cyclical discount
            elif price < sma200:
                score += 1.5
            # Also ride uptrends (secular growth)
            elif price > sma200 and sma50 is not None and sma50 > sma200:
                score += 1.5
            # RSI value zone
            if rsi < 35:
                score += 2.5  # Max fear in semis = best entry
            elif rsi < 50:
                score += 1.0
            # MACD reversal
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            if score >= 2.5:
                scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 14. Subscription Monopoly (Recurring Revenue Moats)
# ---------------------------------------------------------------------------
class SubscriptionMonopoly(BasePersona):
    """Companies with sticky subscriptions that customers never cancel.

    CRM (Salesforce): once your sales team is on it, switching cost is enormous.
    ADP: every company's payroll — 40M employees processed, never switches.
    NFLX: 260M subscribers, content moat deepening.
    SPOT: 600M users, podcasts + music + audiobooks ecosystem.
    ADBE: every designer/marketer on Creative Cloud.

    Edge: Subscription = predictable revenue + negative churn (upselling).
    These trade at high multiples but actually DESERVE it because cash flow
    visibility is 95%+. Buy dips — they always recover.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Subscription Monopoly (Recurring Revenue)",
            description="Sticky subscriptions nobody cancels: CRM, ADP, NFLX, SPOT — predictable cash flow machines",
            risk_tolerance=0.5,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "CRM",    # Salesforce — enterprise CRM monopoly
                "ADP",    # Automatic Data Processing — payroll monopoly
                "NFLX",   # Netflix — content + scale moat
                "SPOT",   # Spotify — audio ecosystem
                "ADBE",   # Adobe — Creative Cloud lock-in
                "INTU",   # Intuit — TurboTax + QuickBooks (tax monopoly)
                "HRB",    # H&R Block — tax prep for masses
                "VEEV",   # Veeva Systems — pharma CRM monopoly
                "HUBS",   # HubSpot — SMB marketing automation
                "ZM",     # Zoom — enterprise video (sticky post-COVID)
                "PANW",   # Palo Alto — cybersecurity subscription pivot
                "FTNT",   # Fortinet — network security subscriptions
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "vol_20"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Uptrend = growing subscribers
            if price > sma200:
                score += 2.0
            if sma50 is not None and price > sma50:
                score += 1.0
            # Buy pullbacks (subscriptions = reliable recovery)
            if 30 < rsi < 45 and price > sma200:
                score += 2.5
            elif 45 <= rsi < 60:
                score += 1.0
            # Low vol preferred (stable subscription base)
            vol = inds["vol_20"]
            if vol is not None and not _is_missing(vol) and vol < 0.020:
                score += 0.5
            if score >= 3:
                scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 15. Contrastive Pairs (Long Value vs Short Hype within same sector)
# ---------------------------------------------------------------------------
class ContrastivePairs(BasePersona):
    """Long the cheap, short the expensive within the same theme.

    Within every hot sector, there's a value stock and a hype stock.
    This strategy goes long the undervalued one and avoids/shorts the overvalued one.
    Since we can't short in our backtester, we just concentrate in the VALUE side
    of each pair and avoid the hype side entirely.

    Pairs: WDC (value) vs NVDA (hype), HRB (value) vs SNOW (hype),
    ADP (value) vs WDAY (hype), NFLX (value) vs ROKU (hype).

    Edge: Mean reversion within sectors. The value side catches up.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Contrastive Pairs (Value Side of Hype Sectors)",
            description="Long the cheap stock in every hot sector: WDC not NVDA, HRB not SNOW, ADP not WDAY",
            risk_tolerance=0.5,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                # Semi value (not NVDA)
                "WDC", "MU", "ON",
                # Tax/payroll value (not cloud hype)
                "HRB", "ADP", "PAYX",
                # Streaming value (not money-burners)
                "NFLX", "WBD",
                # Enterprise value (not overpriced SaaS)
                "ORCL", "IBM",
                # Fintech value (not speculative)
                "FISV", "FIS",
                # Hardware value (not meme)
                "HPQ", "DELL",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # VALUE signal: below SMA200 or recently recovered
            if price < sma200:
                score += 2.0  # In value zone
                if rsi < 40:
                    score += 2.0  # Deep value
            # Momentum recovery signal
            if price > sma200:
                score += 1.0
            if sma50 is not None and price > sma50 > sma200:
                score += 1.5  # Breaking out of value zone
            # MACD reversal from below
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            if 40 < rsi < 65:
                score += 0.5
            if score >= 2.5:
                scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 16. Global Financial Infrastructure
# ---------------------------------------------------------------------------
class GlobalFinancialInfra(BasePersona):
    """Payment rails + global banks + trading houses = backbone of world finance.

    Combines US payment monopolies (V, MA, AXP), US mega-banks (JPM, GS, BK),
    Japanese trading houses (Marubeni/MRBEY, Mitsubishi/MITSY),
    and Singapore banks (D05.SI, U11.SI, O39.SI).

    Edge: Cross-geography diversification with correlated upside (global growth)
    but uncorrelated downside (different regulatory/economic cycles).
    Singapore banks yield 5%+ with pristine asset quality. Japanese sogo shoshas
    trade at book value with 15%+ ROE. US payments grow with global digitization.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Global Financial Infrastructure",
            description="Payment rails + mega-banks + Japanese trading houses + Singapore banks — backbone of world finance",
            risk_tolerance=0.5,
            max_position_size=0.10,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or [
                # US payment monopolies
                "V", "MA", "AXP",
                # US mega-banks
                "JPM", "GS", "BK",
                # Capital One (consumer credit cycle play)
                "COF",
                # Japanese sogo shoshas (Buffett-approved)
                "MRBEY",  # Marubeni
                "MITSY",  # Mitsubishi Corp
                "ITOCY",  # Itochu
                # Singapore banks (5%+ dividend, AAA country)
                "D05.SI",  # DBS
                "U11.SI",  # UOB
                "O39.SI",  # OCBC
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Uptrend
            if price > sma200:
                score += 2.0
            if sma50 is not None and price > sma50:
                score += 1.0
            # Buy dips in financials (they recover with rate cycles)
            if 30 < rsi < 50 and price > sma200:
                score += 2.0
            elif 50 <= rsi < 65:
                score += 0.5
            # MACD momentum
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            if score >= 3:
                scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 17. Reshoring Industrial Renaissance — 2% implemented, 98% orders pending
# ---------------------------------------------------------------------------
class ReshoringIndustrial(BasePersona):
    """US reshoring + CHIPS Act + IRA = multi-decade industrial capex.

    Only 2% of manufacturers have FULLY reshored — 98% of orders pending.
    ETN picks-and-shovels for electrification, NUE domestic steel at premium,
    CAT 19% earnings growth, URI rents equipment to build every factory.
    """
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Reshoring Industrial Renaissance",
            description="CHIPS Act + IRA + reshoring: 2% implemented, 98% of orders still coming. ETN, CAT, NUE, URI.",
            risk_tolerance=0.5, max_position_size=0.10, max_positions=12, rebalance_frequency="weekly",
            universe=universe or ["ETN", "EMR", "ROK", "AME", "GE", "CAT", "NUE", "STLD", "RS", "TT", "GNRC", "VMC", "MLM", "URI"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi): continue
            price = prices[sym]
            score = 0.0
            if price > sma200: score += 2.0
            if sma50 is not None and sma50 > sma200: score += 1.5
            if 40 < rsi < 55: score += 1.5
            macd, ms = inds["macd"], inds["macd_signal"]
            if macd is not None and ms is not None and macd > ms: score += 1.0
            if score >= 3: scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        if scored:
            total = sum(s for _, s in scored[:self.config.max_positions])
            for sym, sc in scored[:self.config.max_positions]:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 18. Water Infrastructure Monopoly — $45B mandated EPA spending
# ---------------------------------------------------------------------------
class WaterMonopoly(BasePersona):
    """Regulated water monopolies with zero competition. You can't choose your water provider.

    EPA lead pipe mandate = $45B MUST be spent, utilities MUST be made whole via rate hikes.
    AWK 10% below fair value. WTRG unanimous Strong Buy +25% upside.
    """
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Water Infrastructure Monopoly",
            description="Regulated water monopolies: $45B EPA mandate, AWK below fair value, 8-9% rate base growth guaranteed",
            risk_tolerance=0.3, max_position_size=0.15, max_positions=8, rebalance_frequency="monthly",
            universe=universe or ["AWK", "WTRG", "WTR", "SJW", "XYL", "WTS", "FELE", "PNR", "ECL"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma200, rsi = inds["sma_200"], inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi): continue
            price = prices[sym]
            score = 1.0  # Always some allocation (utility income)
            if price > sma200: score += 2.0
            sma50 = inds["sma_50"]
            if sma50 is not None and price > sma50: score += 0.5
            if 30 < rsi < 45: score += 2.0
            elif rsi < 30: score += 2.5  # Rare panic = gift
            elif 45 <= rsi < 60: score += 0.5
            if score >= 3: scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        if scored:
            total = sum(s for _, s in scored[:self.config.max_positions])
            for sym, sc in scored[:self.config.max_positions]:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 19. Regulated Data Infrastructure — SPGI 31.9% DCF upside
# ---------------------------------------------------------------------------
class RegulatedData(BasePersona):
    """Data monopolies REQUIRED by regulation. 85-95% subscription, 100%+ NRR.

    VRSK: sole insurance actuarial data provider. SPGI/MCO: required by Basel III.
    MSCI indexes determine $15T+ in fund allocations. Arms dealers of finance.
    """
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Regulated Data Infrastructure",
            description="VRSK/SPGI/MSCI: regulatory-required data monopolies, 85-95% subscription, 100%+ NRR",
            risk_tolerance=0.4, max_position_size=0.12, max_positions=10, rebalance_frequency="monthly",
            universe=universe or ["VRSK", "FDS", "MSCI", "SPGI", "MCO", "TRI", "NDAQ", "MORN", "DNB", "ENV"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "vol_20"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi): continue
            price = prices[sym]
            score = 0.0
            if price > sma200: score += 2.0
            if sma50 is not None and sma50 > sma200: score += 1.5
            if 35 < rsi < 50 and price > sma200: score += 2.0
            elif 50 <= rsi < 65: score += 1.0
            vol = inds["vol_20"]
            if vol is not None and not _is_missing(vol) and vol < 0.015: score += 1.0
            if score >= 4: scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        if scored:
            total = sum(s for _, s in scored[:self.config.max_positions])
            for sym, sc in scored[:self.config.max_positions]:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 20. China ADR Deep Value — JD/PDD 9x P/E
# ---------------------------------------------------------------------------
class ChinaADRDeepValue(BasePersona):
    """Chinese ADRs at lowest valuations in history. Delisting fear resolved.

    JD 9x P/E, PDD 9.4x forward. BABA dominant e-commerce + cloud below intrinsic.
    Government pivoted to stimulus. Geopolitical fear = persistent mispricing.
    MAX POSITION SIZE SMALL due to tail risk.
    """
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="China ADR Deep Value",
            description="JD/PDD 9x P/E, BABA below intrinsic — delisting resolved, stimulus pivot, geopolitical discount",
            risk_tolerance=0.6, max_position_size=0.08, max_positions=10, rebalance_frequency="weekly",
            universe=universe or ["BABA", "JD", "PDD", "BIDU", "NIO", "XPEV", "LI", "VIPS", "BILI", "TME", "ZTO", "YUMC", "TCOM", "MNSO"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "volume_sma_20"], date)
            sma200, rsi = inds["sma_200"], inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi): continue
            price = prices[sym]
            score = 0.0
            if price < sma200 * 0.85: score += 3.0
            elif price < sma200: score += 1.5
            if rsi < 35: score += 2.0
            elif rsi < 45: score += 1.0
            macd, ms = inds["macd"], inds["macd_signal"]
            if macd is not None and ms is not None and macd > ms: score += 1.5
            vol_sma = inds["volume_sma_20"]
            if vol_sma is not None and not _is_missing(vol_sma) and sym in data:
                try:
                    cv = data[sym].loc[:date, "Volume"].iloc[-1]
                    if cv > vol_sma * 2.0: score += 1.5
                except Exception: pass
            if score >= 4: scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        if scored:
            total = sum(s for _, s in scored[:self.config.max_positions])
            for sym, sc in scored[:self.config.max_positions]:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# Cloud & Cybersecurity Value
# ---------------------------------------------------------------------------
class CloudCyberValue(BasePersona):
    """Cloud and cybersecurity value strategy.

    Thesis: Cloud infrastructure and cybersecurity are non-discretionary spend.
    Companies like Cloudflare, Datadog, CrowdStrike have durable moats via
    network effects and switching costs. Buy on pullbacks to SMA200 with
    MACD reversal for value entries in secular growth names.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Cloud & Cybersecurity Value",
            description="Cloud/cyber non-discretionary spend: buy dips in Cloudflare, Datadog, CrowdStrike, Palo Alto",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "NET", "DDOG", "SNOW", "CRWD",  # Cloud/observability
                "PANW", "FTNT", "ZS", "S",  # Cybersecurity
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
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]

            if any(_is_missing(v) for v in [sma200, rsi]):
                continue

            # Broken trend: >15% below SMA200 (growth names can gap down)
            if price < sma200 * 0.85:
                weights[sym] = 0.0
                continue
            if rsi > 80:
                weights[sym] = 0.0
                continue

            score = 0.0
            # Value entry: below SMA200 with low RSI
            if price < sma200 and rsi < 45:
                score += 2.5  # Below long-term avg = value zone
            # Uptrend confirmation
            if sma50 is not None and price > sma50 > sma200:
                score += 2.0
            elif sma50 is not None and price > sma50:
                score += 1.0
            # MACD reversal (key signal for value entry timing)
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5
            # Not overbought
            if 30 < rsi < 65:
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
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Global Airlines & Travel
# ---------------------------------------------------------------------------
class GlobalAirlinesTravel(BasePersona):
    """Global airlines and travel recovery / momentum strategy.

    Thesis: Post-pandemic travel demand is structural. Airlines are cyclical
    but international travel (BKNG, TCOM) has durable pricing power.
    Buy on pullbacks using SMA200 support with golden cross confirmation.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Global Airlines & Travel",
            description="Airlines and OTAs: DAL, UAL, BKNG, ABNB — post-pandemic travel demand",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "DAL", "LUV", "UAL", "JBLU", "AAL",  # US airlines
                "BKNG", "ABNB", "EXPE",  # OTAs / travel platforms
                "TCOM",  # Trip.com (China/Asia travel)
                "MAR", "HLT",  # Hotels (travel ecosystem)
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
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "bb_lower"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]
            bb_lower = inds["bb_lower"]

            if any(_is_missing(v) for v in [sma50, rsi]):
                continue

            # Airlines are cyclical — cut at >20% below SMA200
            if sma200 is not None and price < sma200 * 0.80:
                weights[sym] = 0.0
                continue
            if rsi > 78:
                weights[sym] = 0.0
                continue

            score = 0.0
            # Golden cross: strong momentum signal for cyclicals
            if sma200 is not None and sma50 > sma200 and price > sma50:
                score += 3.0
            elif price > sma50:
                score += 1.5
            # Pullback entry near Bollinger lower band
            if bb_lower is not None and not _is_missing(bb_lower) and price < bb_lower * 1.03:
                score += 1.5
            # MACD confirmation
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            # RSI sweet spot
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
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Utility & Infrastructure Income
# ---------------------------------------------------------------------------
class UtilityInfraIncome(BasePersona):
    """Utility and infrastructure income strategy.

    Thesis: Regulated utilities, data center REITs, and defensive consumer
    names provide steady income with inflation-linked pricing.
    Always maintain some allocation; buy more on dips below SMA200.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Utility & Infrastructure Income",
            description="Utilities, data centers, telecom: steady income, buy dips for yield",
            risk_tolerance=0.2,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "SO", "D", "DUK", "PPL", "NEE",  # Regulated utilities
                "EQIX", "DLR",  # Data center REITs
                "TMUS", "VZ",  # Telecom (income)
                "COST",  # Costco (defensive consumer)
                "SCHW",  # Schwab (financial infrastructure)
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
            inds = self._get_indicators(data, sym, ["sma_200", "rsi_14", "sma_50"], date)
            sma200, rsi, sma50 = inds["sma_200"], inds["rsi_14"], inds["sma_50"]
            if _is_missing(sma200):
                continue

            # Income: always some allocation (base weight)
            base_weight = 0.08
            # Buy more on dips below SMA200
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            if discount > 0.05:
                # 5%+ below SMA200 = accumulate aggressively
                score = 2.0 + discount * 5
                if rsi is not None and rsi < 35:
                    score += 1.0
                candidates.append((sym, score, 0.12))
            elif discount > -0.05:
                # Near SMA200 = normal income allocation
                score = 1.5
                if rsi is not None and rsi < 45:
                    score += 0.5
                candidates.append((sym, score, base_weight))
            elif discount > -0.15:
                # Up to 15% above SMA200 = reduced but still hold for income
                candidates.append((sym, 1.0, 0.06))
            # More than 15% above SMA200 and RSI overbought = trim
            elif rsi is not None and rsi > 75:
                weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        for sym, _, wt in top:
            weights[sym] = min(wt, self.config.max_position_size)
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Japan Industrial & Finance
# ---------------------------------------------------------------------------
class JapanIndustrialFinance(BasePersona):
    """Japan industrial and financial sector strategy.

    Thesis: Japan's corporate governance reform (TSE push for ROE > 8%)
    is unlocking value in keiretsu conglomerates and megabanks.
    Buy ADRs of quality Japanese industrials and financials on dips.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Japan Industrial & Finance",
            description="Japan governance reform: Toyota, Sony, Nomura, MUFG, trading houses",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "MKTAY", "NMR", "SMFG", "MUFG",  # Finance / industrial
                "ITOCY", "MITSY", "MRBEY",  # Trading houses (Buffett favorites)
                "TM", "SONY", "HMC",  # Consumer / auto
                "EWJ",  # Japan broad ETF
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
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]

            if any(_is_missing(v) for v in [sma200, rsi]):
                continue

            # Japan ADRs can be volatile — cut at >20% below SMA200
            if price < sma200 * 0.80:
                weights[sym] = 0.0
                continue

            score = 0.0
            # Value entry: below SMA200 with low RSI (governance reform unlocks value)
            if price < sma200 and rsi < 45:
                score += 2.5
            # Uptrend = reform thesis working
            if sma50 is not None and price > sma50 > sma200:
                score += 2.0
            elif sma50 is not None and price > sma50:
                score += 1.0
            # MACD reversal
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            # Not overbought
            if 30 < rsi < 65:
                score += 0.5
            # Deep oversold = contrarian buy
            if rsi < 30:
                score += 1.5

            if score >= 2.0:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Defense Prime Contractors
# ---------------------------------------------------------------------------
class DefensePrimeContractors(BasePersona):
    """Defense prime contractors focused strategy.

    Thesis: NATO 2%+ GDP spending targets, geopolitical tensions, and
    long-duration defense contracts create predictable revenue streams.
    Primes have cost-plus contracts = guaranteed margins.
    Buy on value dips, hold for steady compounding.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Defense Prime Contractors",
            description="NATO spending boom: LMT, NOC, RTX, BAE, GD — cost-plus contracts = guaranteed margins",
            risk_tolerance=0.3,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "LMT", "NOC", "RTX", "BAESY",  # Top primes
                "GD", "HII", "LHX", "LDOS",  # Second tier primes
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
            inds = self._get_indicators(data, sym, ["sma_200", "rsi_14", "sma_50", "vol_20"], date)
            sma200, rsi = inds["sma_200"], inds["rsi_14"]
            sma50, vol = inds["sma_50"], inds["vol_20"]
            if _is_missing(sma200):
                continue

            # Defense primes are stable — cut only at >15% below SMA200
            if price < sma200 * 0.85:
                weights[sym] = 0.0
                continue

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            score = 0.0

            # Value: buy near or below SMA200
            if discount > 0:
                score += 2.0 + discount * 5  # More discount = higher score
            elif discount > -0.10:
                score += 1.0

            # Low RSI = oversold (defense rarely stays oversold)
            if rsi is not None and rsi < 40:
                score += 1.5
            elif rsi is not None and rsi < 55:
                score += 0.5
            elif rsi is not None and rsi > 75:
                weights[sym] = 0.0
                continue

            # Low vol bonus (stable defense contractor = good)
            if vol is not None and not _is_missing(vol) and vol < 0.015:
                score += 0.5

            if score >= 1.5:
                candidates.append((sym, score))

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Global Consumer Staples
# ---------------------------------------------------------------------------
class GlobalConsumerStaples(BasePersona):
    """Global consumer staples strategy.

    Thesis: Global staples (Unilever, Nestle, P&G, KO) have pricing power
    across economic cycles. Buy for income and stability — always maintain
    some allocation, accumulate on dips.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Global Consumer Staples",
            description="Global pricing power: Unilever, Nestle, P&G, KO, Deere — income + stability",
            risk_tolerance=0.2,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "UL", "MKC", "DE", "NVO",  # International staples/health
                "PG", "KO", "NSRGY", "COST",  # US/global staples
                "PEP", "CL", "KHC",  # Additional consumer staples
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
            inds = self._get_indicators(data, sym, ["sma_200", "rsi_14", "sma_50"], date)
            sma200, rsi, sma50 = inds["sma_200"], inds["rsi_14"], inds["sma_50"]
            if _is_missing(sma200):
                continue

            # Income strategy: always hold some, buy more on dips
            base_weight = 0.08
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            if discount > 0.05:
                # >5% below SMA200: accumulate (staples always recover)
                wt = 0.13
                score = 2.5
                if rsi is not None and rsi < 35:
                    score += 1.0
                    wt = 0.15
                candidates.append((sym, score, wt))
            elif discount > -0.05:
                # Near SMA200: normal income allocation
                score = 1.5
                if rsi is not None and rsi < 45:
                    score += 0.5
                candidates.append((sym, score, base_weight))
            elif discount > -0.12:
                # Moderate uptrend: smaller allocation
                candidates.append((sym, 1.0, 0.06))
            else:
                # Extended above SMA200 + overbought: trim
                if rsi is not None and rsi > 75:
                    weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        for sym, _, wt in top:
            weights[sym] = min(wt, self.config.max_position_size)
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Emerging Market ETF Value
# ---------------------------------------------------------------------------
class EmergingMarketETFValue(BasePersona):
    """Emerging market ETF value strategy.

    Thesis: EM equities are structurally undervalued vs DM. Country ETFs
    (Vietnam, Korea, Singapore, India, Taiwan) provide diversified EM
    exposure. Buy when RSI is low and price is below SMA200 for value entries.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Emerging Market ETF Value",
            description="EM country ETFs at value prices: Vietnam, Korea, India, Taiwan, Singapore",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "NU", "VNM", "EWY", "EWS",  # LatAm fintech, Vietnam, Korea, Singapore
                "EPI", "INDA", "EEM", "EWT",  # India, broad EM, Taiwan
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
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]

            if any(_is_missing(v) for v in [sma200, rsi]):
                continue

            # EM can freefall — cut at >20% below SMA200
            if price < sma200 * 0.80:
                weights[sym] = 0.0
                continue
            if rsi > 78:
                weights[sym] = 0.0
                continue

            score = 0.0
            # Value: below SMA200 with low RSI
            if price < sma200 and rsi < 40:
                score += 3.0  # Deep EM value
            elif price < sma200 and rsi < 55:
                score += 2.0
            # Momentum recovery: above SMA200 with golden cross
            if sma50 is not None and price > sma50 > sma200:
                score += 2.0
            elif sma50 is not None and price > sma50:
                score += 1.0
            # MACD reversal = turning point
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            # Deep oversold bounce
            if rsi < 25:
                score += 1.5

            if score >= 2.0:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Global Pharma Pipeline
# ---------------------------------------------------------------------------
class GlobalPharmaPipeline(BasePersona):
    """Global pharma pipeline strategy.

    Thesis: Big pharma companies with deep pipelines (Roche, AstraZeneca,
    Merck, GSK, Takeda) trade at value multiples despite having
    blockbuster drugs in late-stage trials. Buy on patent cliff fears.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Global Pharma Pipeline",
            description="Global pharma at value: Roche, AZN, MRK, GSK, TAK — deep pipelines, patent cliff fears",
            risk_tolerance=0.4,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "RHHBY", "MRK", "BAYRY", "NVS",  # Global pharma
                "AZN", "GSK", "TAK", "SNY",  # EU/Japan pharma
                "LLY", "ABBV",  # US pharma with deep pipelines
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
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "bb_lower"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]
            bb_lower = inds["bb_lower"]

            if any(_is_missing(v) for v in [sma200, rsi]):
                continue

            # Pharma can gap on FDA news — cut at >20% below SMA200
            if price < sma200 * 0.80:
                weights[sym] = 0.0
                continue

            score = 0.0
            # Value: below SMA200 (patent cliff fears = opportunity)
            if price < sma200 * 0.90:
                score += 3.0
            elif price < sma200:
                score += 2.0
            # RSI oversold (pharma recovers when pipeline delivers)
            if rsi < 35:
                score += 2.0
            elif rsi < 45:
                score += 1.0
            # MACD reversal = pipeline catalyst turning sentiment
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5
            # Bollinger lower = statistical extreme
            if bb_lower is not None and not _is_missing(bb_lower) and price < bb_lower * 1.02:
                score += 1.0
            # Also buy uptrending pharma (pipeline thesis confirmed)
            if sma50 is not None and price > sma50 > sma200:
                score += 1.5
            elif rsi > 75:
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
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Singapore Alpha (Heritage Consumer + REITs combined)
# ---------------------------------------------------------------------------
class SingaporeAlpha(BasePersona):
    """Singapore equities: heritage consumer brands + REITs.

    Thesis: Singapore is a AAA-rated financial hub with world-class
    governance. Heritage consumer brands (Haw Par/Tiger Balm, Wilmar
    International, Thai Beverage) are cash-generative with regional
    distribution. Singapore REITs (S-REITs) offer 4-6% yields backed
    by prime commercial real estate in Asia's most transparent market.
    Combined, they offer income + growth from Singapore's structural
    advantages: rule of law, low tax, regional HQ status.

    Signal: Income-oriented — buy on dips below SMA200 for yield,
    hold in uptrend for total return.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Singapore Alpha",
            description="Singapore heritage consumer + banks + REITs: AAA-rated income + growth",
            risk_tolerance=0.3,
            max_position_size=0.12,
            max_positions=11,
            rebalance_frequency="monthly",
            universe=universe or [
                # Heritage consumer brands
                "H02.SI",   # Haw Par Corporation (Tiger Balm, healthcare)
                "F34.SI",   # Wilmar International (world's largest palm oil)
                "Y92.SI",   # Thai Beverage (Chang Beer, spirits, regional)
                # Singapore banks (AAA-rated, 5%+ yield)
                "D05.SI",   # DBS Group Holdings (Singapore's largest bank)
                "U11.SI",   # UOB (United Overseas Bank)
                "O39.SI",   # OCBC (Oversea-Chinese Banking Corp)
                # Singapore REITs (S-REITs)
                "A17U.SI",  # CapitaLand Ascendas REIT (industrial, data centers)
                "N2IU.SI",  # Mapletree Pan Asia Commercial Trust
                "C38U.SI",  # CapitaLand Integrated Commercial Trust
                "ME8U.SI",  # Mapletree Industrial Trust
                "AJBU.SI",  # Keppel DC REIT (data center REIT)
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
            inds = self._get_indicators(data, sym, ["sma_200", "sma_50", "rsi_14"], date)
            sma200, sma50, rsi = inds["sma_200"], inds["sma_50"], inds["rsi_14"]
            if _is_missing(sma200):
                continue

            # Income strategy: always maintain allocation, buy dips
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            if discount > 0.05:
                # 5%+ below SMA200 = accumulate (yield pickup)
                score = 2.5 + discount * 5
                if rsi is not None and rsi < 35:
                    score += 1.0
                candidates.append((sym, score, 0.13))
            elif discount > -0.05:
                # Near SMA200 = normal income allocation
                score = 1.5
                if rsi is not None and rsi < 45:
                    score += 0.5
                candidates.append((sym, score, 0.10))
            elif discount > -0.15:
                # Moderately above SMA200 = hold for income
                candidates.append((sym, 1.0, 0.08))
            else:
                # >15% above SMA200 and RSI overbought = trim
                if rsi is not None and rsi > 75:
                    weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        for sym, _, wt in top:
            weights[sym] = min(wt, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# UK & European Banking Value
# ---------------------------------------------------------------------------
class UKEuropeanBanking(BasePersona):
    """UK and European banking value strategy.

    Thesis: European banks trade at 0.5-0.8x book value vs US banks
    at 1.2-1.5x despite improving ROE from higher rates. NatWest,
    Barclays, HSBC benefit from UK rate normalization. UBS (post-CS
    integration) is the world's largest wealth manager. BNP Paribas
    and Deutsche Bank are restructuring successfully. Dividend yields
    of 4-7% provide downside cushion.

    Signal: Deep value + MACD reversal. Buy when below book (SMA200
    proxy) with momentum confirmation. Sell on overbought.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="UK & European Banking Value",
            description="European bank deep value: 0.5-0.8x book, 4-7% yield, rate normalization",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "NWG",    # NatWest Group (UK retail/commercial bank)
                "BARC",   # Barclays (UK investment + retail bank)
                "HSBC",   # HSBC Holdings (global, Asia-focused)
                "UBS",    # UBS Group (wealth management leader post-CS)
                "BNPQF",  # BNP Paribas (France, largest eurozone bank)
                "DB",     # Deutsche Bank (German restructuring play)
                "LYG",    # Lloyds Banking Group (UK mortgage leader)
                "ING",    # ING Group (Netherlands digital banking)
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
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "bb_lower"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            bb_low = inds["bb_lower"]

            if _is_missing(sma200) or _is_missing(rsi):
                continue

            score = 0.0

            # Value: banks below SMA200 = below "book value" proxy
            if price < sma200 * 0.92:
                score += 3.0
            elif price < sma200:
                score += 1.5

            # RSI oversold = peak pessimism on European banks
            if rsi < 35:
                score += 2.0
            elif rsi < 45:
                score += 1.0

            # MACD bullish crossover = turnaround signal
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5

            # Bollinger lower band = statistical extreme
            if bb_low is not None and not _is_missing(bb_low) and price < bb_low * 1.02:
                score += 1.0

            # Momentum confirmation for established uptrend
            if sma50 is not None and price > sma50 > sma200:
                score += 2.0
            elif sma50 is not None and price > sma50:
                score += 1.0

            # Overbought: take profits (banks are cyclical)
            if rsi > 75:
                weights[sym] = 0.0
                continue

            if score >= 2.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# Telecom Equipment & 5G
# ---------------------------------------------------------------------------
class TelecomEquipment5G(BasePersona):
    """Telecom equipment and 5G infrastructure strategy.

    Thesis: 5G capex cycle is multi-year ($1.7T global spend by 2030).
    Equipment vendors (Ericsson, Nokia) have oligopoly with Huawei
    restricted from Western markets. Qualcomm dominates 5G modems.
    Marvell provides custom silicon for 5G base stations. Keysight
    is the picks-and-shovels play (test equipment for every 5G rollout).
    Secular tailwind from AI requiring low-latency 5G edge networks.

    Signal: Momentum in equipment names. Buy uptrend + MACD bullish.
    Sell on overbought or trend breakdown.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Telecom Equipment & 5G",
            description="5G infrastructure: equipment oligopoly + semiconductor + test & measurement",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "ERIC",   # Ericsson (5G RAN leader, Huawei displacement)
                "NOK",    # Nokia (5G equipment + submarine cables)
                "QCOM",   # Qualcomm (5G modem monopoly + licensing)
                "MRVL",   # Marvell Technology (5G custom silicon)
                "KEYS",   # Keysight Technologies (5G test equipment)
                "ANET",   # Arista Networks (data center + 5G backhaul)
                "LITE",   # Lumentum (optical components for 5G)
                "VIAV",   # Viavi Solutions (network test + assurance)
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
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal",
                 "Volume", "volume_sma_20"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]

            if _is_missing(sma50) or _is_missing(rsi):
                continue

            # Exit: overbought (take profits)
            if rsi > 80:
                weights[sym] = 0.0
                continue

            # Exit: broken trend
            if sma200 is not None and price < sma200 * 0.85:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Uptrend: golden cross
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5

            # MACD bullish = capex cycle accelerating
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0

            # Volume confirmation (carrier orders = institutional buying)
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            if vol_ratio > 1.3:
                score += 0.5

            # RSI healthy range
            if 35 < rsi < 70:
                score += 0.5

            if score >= 2.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
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
# Gig Economy & SaaS Disruptors
# ---------------------------------------------------------------------------
class GigEconomySaaSDisruptors(BasePersona):
    """Gig economy platforms and SaaS disruptors strategy.

    Thesis: The gig economy is restructuring labor markets globally.
    Upwork and Fiverr connect 100M+ freelancers with enterprises.
    Toast is replacing legacy restaurant POS with cloud-native SaaS.
    Rocket Lab is disrupting SpaceX with small-launch dominance.
    These names trade at growth discounts after 2022 selloff but are
    approaching profitability / already profitable. Revenue growth
    25-50% with expanding margins = re-rating potential.

    Signal: Growth momentum. Buy on uptrend + volume. Sell overbought.
    Higher risk tolerance for these high-beta names.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Gig Economy & SaaS Disruptors",
            description="Gig platforms + SaaS disruptors: growth at reasonable price, high beta",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "UPWK",   # Upwork (freelance marketplace leader)
                "FVRR",   # Fiverr (gig economy marketplace)
                "TOST",   # Toast (restaurant SaaS / fintech)
                "RKLB",   # Rocket Lab (small-launch space disruptor)
                "DDOG",   # Datadog (observability SaaS)
                "NET",    # Cloudflare (edge computing / CDN)
                "CFLT",   # Confluent (data streaming SaaS)
                "HUBS",   # HubSpot (marketing SaaS)
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
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal",
                 "Volume", "volume_sma_20"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]

            if _is_missing(sma50) or _is_missing(rsi):
                continue

            # Exit: overbought growth names (take profits aggressively)
            if rsi > 78:
                weights[sym] = 0.0
                continue

            # Exit: structural breakdown
            if sma200 is not None and price < sma200 * 0.75:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Growth momentum: strong uptrend
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
                # Extra for breakout momentum
                if sma200 > 0:
                    pct_above = (price - sma200) / sma200
                    score += min(pct_above * 2, 1.5)
            elif price > sma50:
                score += 1.5

            # MACD bullish = earnings acceleration
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0

            # Volume surge (institutional accumulation)
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            if vol_ratio > 1.5:
                score += 1.0
            elif vol_ratio > 1.2:
                score += 0.5

            # RSI in healthy momentum zone
            if 40 < rsi < 70:
                score += 0.5

            if score >= 2.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
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
# Korean Chaebols & Fintech
# ---------------------------------------------------------------------------
class KoreanChaebols(BasePersona):
    """Korean chaebol conglomerates and fintech strategy.

    Thesis: Korean chaebols are global leaders trading at "Korea discount"
    (30-50% vs global peers) due to governance concerns. Reforms underway:
    Korea Value-Up Program (2024) follows Japan's TSE model. Coupang is
    Korea's Amazon (dominant e-commerce + logistics). Samsung (SSNLF) is
    the world's largest semiconductor manufacturer. KB Financial and
    Shinhan are top banks with 5%+ dividend yields. POSCO is the world's
    most efficient steelmaker + battery materials play.

    Signal: Value + momentum. Buy Korea discount names in uptrend.
    MACD reversal for turnaround signals.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Korean Chaebols & Fintech",
            description="Korea discount value: chaebols + fintech, governance reform catalyst",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "CPNG",   # Coupang (Korea's Amazon, dominant e-commerce)
                "SKM",    # SK Telecom (5G leader + AI investments)
                "SSNLF",  # Samsung Electronics (memory + foundry)
                "KB",     # KB Financial Group (Korea's largest bank)
                "SHG",    # Shinhan Financial (premium Korean bank)
                "PKX",    # POSCO Holdings (steel + battery materials)
                "LPL",    # LG Display (OLED technology leader)
                "HMC",    # Hyundai Motor (global auto + EV + robotics)
                "EWY",    # iShares MSCI South Korea ETF (broad exposure)
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
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "bb_lower"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            bb_low = inds["bb_lower"]

            if _is_missing(sma200) or _is_missing(rsi):
                continue

            score = 0.0

            # Korea discount: buy below SMA200 (value entry)
            if price < sma200 * 0.92:
                score += 2.5
            elif price < sma200:
                score += 1.5

            # Also buy momentum (governance reform re-rating)
            if sma50 is not None and price > sma50 > sma200:
                score += 2.5
            elif sma50 is not None and price > sma50:
                score += 1.0

            # RSI oversold = Korea sentiment trough
            if rsi < 35:
                score += 2.0
            elif rsi < 45:
                score += 1.0

            # MACD bullish crossover = reform momentum building
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0

            # Bollinger lower band extreme
            if bb_low is not None and not _is_missing(bb_low) and price < bb_low * 1.02:
                score += 0.5

            # Overbought: take profits (Korea rallies are sharp but short)
            if rsi > 75:
                weights[sym] = 0.0
                continue

            if score >= 2.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
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
# Rideshare & Mobility
# ---------------------------------------------------------------------------
class RideshareMobility(BasePersona):
    """Rideshare and mobility platform strategy.

    Thesis: Rideshare is a winner-take-most market. Uber is the global
    leader (150M+ monthly active users, 37 countries). Lyft is the #2
    US player approaching sustained profitability. Grab is the SE Asia
    super-app (rideshare + food + payments). DoorDash dominates US food
    delivery with 65%+ market share. All four have crossed the
    profitability inflection point with expanding margins. Network
    effects + autonomous driving optionality = long runway.

    Signal: Growth momentum. Buy on uptrend + volume confirmation.
    Sell on overbought or breakdown.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Rideshare & Mobility",
            description="Mobility platforms: rideshare + delivery, profitability inflection",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "UBER",   # Uber Technologies (global rideshare + delivery leader)
                "LYFT",   # Lyft (US #2 rideshare, margin expansion)
                "GRAB",   # Grab Holdings (SE Asia super-app)
                "DASH",   # DoorDash (US food delivery dominant)
                "ABNB",   # Airbnb (mobility-adjacent: travel platform)
                "TCOM",   # Trip.com (China travel + mobility)
                "BKNG",   # Booking Holdings (global travel platform)
                "CPRT",   # Copart (vehicle remarketing — mobility value chain)
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
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal",
                 "Volume", "volume_sma_20"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]

            if _is_missing(sma50) or _is_missing(rsi):
                continue

            # Exit: overbought
            if rsi > 78:
                weights[sym] = 0.0
                continue

            # Exit: broken below SMA200
            if sma200 is not None and price < sma200 * 0.80:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Growth momentum: strong uptrend
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5

            # MACD bullish = earnings momentum
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0

            # Volume confirmation
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            if vol_ratio > 1.3:
                score += 0.5

            # RSI healthy range
            if 35 < rsi < 70:
                score += 0.5

            # Dip-buy: oversold mobility names
            if rsi < 35 and sma200 is not None and price > sma200 * 0.90:
                score += 1.5

            if score >= 2.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
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
# 35. NVIDIA Supply Chain (Non-Megacap Peripheral Suppliers)
# ---------------------------------------------------------------------------
class NvidiaSupplyChain(BasePersona):
    """NVIDIA peripheral supply chain: the non-megacap companies NVIDIA
    depends on for packaging, testing, materials, cooling, and power delivery.

    Thesis: Everyone buys NVDA directly. But NVIDIA's GPUs require an entire
    ecosystem of smaller, less-followed companies: ABF substrate makers
    (Ajinomoto, Ibiden), advanced packaging OSATs (Amkor, ASE), semiconductor
    test equipment (Cohu, FormFactor, Onto Innovation), chip chemicals and
    filtration (Entegris), power delivery ICs (Monolithic Power), PCB/substrate
    fabricators (TTM Technologies), data center cooling (Modine, nVent), and
    rare earth magnets (MP Materials). These companies have high NVIDIA revenue
    exposure but trade at fraction of NVDA's multiple.

    Signal: NVDA-led momentum. When NVDA is in a strong uptrend (above its
    SMA50 and SMA200), supply chain companies accelerate with a lag. Buy
    supply chain names that are in uptrends with healthy RSI when NVDA is
    strong. Sell when NVDA breaks down or individual names get overbought.

    Edge: Supply chain multiplier effect -- a 20% increase in NVDA GPU shipments
    can mean 30-50% revenue growth for a substrate or packaging company that
    has 40%+ exposure. Market prices NVDA efficiently but under-covers these
    smaller names.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="NVIDIA Supply Chain (Peripheral)",
            description="Non-megacap companies NVIDIA depends on: packaging, testing, materials, cooling, power",
            risk_tolerance=0.7,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                # Chip Packaging & OSAT (Outsourced Assembly & Test)
                "AMKR",   # Amkor Technology — #2 OSAT, advanced packaging for NVDA GPUs (~$12B mkt cap)
                "ASX",    # ASE Technology — #1 OSAT globally, CoWoS packaging partner (~$20B mkt cap)
                "KLIC",   # Kulicke & Soffa — wire/wedge bonding equipment for packaging (~$3.4B mkt cap)
                # Semiconductor Test Equipment
                "COHU",   # Cohu — ATE for chip testing, automotive + AI exposure (~$1.7B mkt cap)
                "FORM",   # FormFactor — probe cards for wafer testing, HBM test (~$7.2B mkt cap)
                "ONTO",   # Onto Innovation — process control & lithography for advanced nodes (~$10.7B mkt cap)
                # Semiconductor Chemicals & Materials
                "ENTG",   # Entegris — filters, chemicals, CMP slurries for fabs (~$17.7B mkt cap)
                # Power Delivery for AI GPUs
                "MPWR",   # Monolithic Power Systems — DC-DC power for AI GPU server racks (~$30B mkt cap)
                # PCB & Substrate Fabrication
                "TTMI",   # TTM Technologies — high-layer-count PCBs for AI servers (~$5B mkt cap)
                # Data Center Cooling (AI GPU thermal management)
                "MOD",    # Modine Manufacturing — liquid cooling, 119% DC sales growth (~$12B mkt cap)
                "NVT",    # nVent Electric — power distribution + cooling for NVDA racks (~$18B mkt cap)
                # Rare Earth & Strategic Materials
                "MP",     # MP Materials — rare earth magnets for motors/electronics (~$9B mkt cap)
                # ABF Substrate (Japan ADRs — lower liquidity but critical supply chain)
                "AJINY",  # Ajinomoto — invented ABF substrate film, monopoly supplier (~$28B mkt cap)
                "IBIDY",  # Ibiden — #2 ABF substrate maker, NVDA GPU packaging (~$14B mkt cap)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        # ---- NVDA leader signal ----
        # Check if NVDA (the demand driver) is in an uptrend
        nvda_strong = False
        nvda_bullish_score = 0.0
        if "NVDA" in prices:
            nvda_inds = self._get_indicators(
                data, "NVDA",
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"],
                date,
            )
            nvda_price = prices["NVDA"]
            nvda_sma50 = nvda_inds["sma_50"]
            nvda_sma200 = nvda_inds["sma_200"]
            nvda_rsi = nvda_inds["rsi_14"]
            nvda_macd = nvda_inds["macd"]
            nvda_macd_sig = nvda_inds["macd_signal"]

            if not _is_missing(nvda_sma50) and not _is_missing(nvda_sma200):
                if nvda_price > nvda_sma50 > nvda_sma200:
                    nvda_bullish_score = 3.0  # Full uptrend
                    nvda_strong = True
                elif nvda_price > nvda_sma50:
                    nvda_bullish_score = 1.5  # Partial uptrend
                    nvda_strong = True
                elif nvda_price > nvda_sma200:
                    nvda_bullish_score = 0.5  # Above long-term trend

            if not _is_missing(nvda_macd) and not _is_missing(nvda_macd_sig):
                if nvda_macd > nvda_macd_sig:
                    nvda_bullish_score += 0.5

        # ---- Score each supply chain name ----
        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal",
                 "Volume", "volume_sma_20"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]

            if _is_missing(sma50) or _is_missing(rsi):
                continue

            # Hard exit: overbought
            if rsi > 80:
                weights[sym] = 0.0
                continue

            # Hard exit: collapsed below SMA200 (supply chain broken)
            if not _is_missing(sma200) and price < sma200 * 0.80:
                weights[sym] = 0.0
                continue

            score = 0.0

            # NVDA-linked momentum boost: supply chain follows the leader
            if nvda_strong:
                score += min(nvda_bullish_score * 0.5, 1.5)

            # Own-stock trend alignment
            if not _is_missing(sma200) and price > sma50 > sma200:
                score += 2.5  # Full uptrend
            elif price > sma50:
                score += 1.0

            # MACD bullish crossover
            if not _is_missing(macd) and not _is_missing(macd_sig) and macd > macd_sig:
                score += 1.0

            # Volume surge confirmation
            if not _is_missing(volume) and not _is_missing(vol_avg) and vol_avg > 0:
                vol_ratio = volume / vol_avg
                if vol_ratio > 1.5:
                    score += 0.5

            # RSI sweet spot (not overbought, not oversold)
            if 30 < rsi < 65:
                score += 0.5

            # Oversold dip-buy when NVDA is strong (supply chain lagging = opportunity)
            if nvda_strong and rsi < 35 and not _is_missing(sma200) and price > sma200 * 0.85:
                score += 2.0  # High conviction: oversold supply chain + strong NVDA

            # Minimum threshold
            if score >= 2.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.90, self.config.max_position_size)
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# Mag7 Hidden Suppliers
# ---------------------------------------------------------------------------
class Mag7HiddenSuppliers(BasePersona):
    """Long the hidden supply chain monopolies that ALL Magnificent 7 depend on.

    Thesis: The Mag7 collectively spend $320B+ annually on AI infrastructure.
    Every dollar flows through a handful of under-followed monopoly/oligopoly
    suppliers: Ajinomoto (95% ABF substrate monopoly), ASML (100% EUV monopoly),
    Lasertec (100% EUV mask inspection), Shin-Etsu/SUMCO (90% silicon wafers),
    Murata (40% MLCC capacitors), Entegris (ultra-pure chemicals), Disco Corp
    (70% wafer dicing), Corning (glass + fiber optic), and SK Hynix (62% HBM).
    These are picks-and-shovels for the entire tech ecosystem -- they capture
    guaranteed revenue regardless of which Mag7 company wins the AI race.

    Signal: Buy when Mag7 aggregate capex trend is strong (QQQ above SMA200)
    and individual supply chain names show trend alignment + healthy RSI.
    Overweight names with strongest monopoly positions. Reduce exposure only
    when the entire tech capex cycle breaks (QQQ below SMA200).

    Edge: Market obsesses over Mag7 directly. These suppliers are under-covered,
    trade at lower multiples, and have guaranteed revenue from ALL Mag7 capex.
    An activist investor called Ajinomoto "the world's most under-monetised
    monopoly in AI infrastructure." Lasertec has 100% market share in sub-5nm
    EUV mask inspection. These are the companies nobody talks about until they
    break.
    """

    # Monopoly strength tiers for weighting: tier1 = true monopoly, tier2 = dominant oligopoly
    _TIER1_MONOPOLY = {"ASML", "AJINY", "LSRCY", "ENTG"}  # 90%+ share or sole supplier
    _TIER2_DOMINANT = {"SHECY", "DSCOY", "TOELY", "MRAAY", "GLW", "HXSCF", "SUOPY", "IBIDY"}

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Mag7 Hidden Suppliers",
            description="Hidden supply chain monopolies ALL Magnificent 7 depend on: ABF, EUV, wafers, capacitors",
            risk_tolerance=0.65,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or [
                # Tier 1: True monopolies / near-monopolies (90%+ share)
                "ASML",    # ASML — 100% EUV lithography monopoly (~350B EUR mkt cap)
                "AJINY",   # Ajinomoto Fine-Techno — 95%+ ABF substrate film monopoly (~$28B mkt cap)
                "LSRCY",   # Lasertec — 100% EUV mask inspection for sub-5nm (~$8B mkt cap)
                "ENTG",    # Entegris — ultra-pure chemicals, filters for ALL advanced fabs (~$17B mkt cap)

                # Tier 2: Dominant oligopoly positions (40-70% share)
                "SHECY",   # Shin-Etsu Chemical — #1 silicon wafer maker, 30% share (~$65B mkt cap)
                "SUOPY",   # SUMCO — #2 silicon wafer maker, 30% share (duopoly with Shin-Etsu) (~$4B mkt cap)
                "DSCOY",   # Disco Corp — 70%+ wafer dicing/grinding monopoly (~$15B mkt cap)
                "TOELY",   # Tokyo Electron — #1 Asia etch/deposition equipment (~$65B mkt cap)
                "MRAAY",   # Murata Manufacturing — #1 MLCC capacitors, 40% global share (~$40B mkt cap)
                "GLW",     # Corning — Gorilla Glass + fiber optic for ALL data centers (~$45B mkt cap)
                "HXSCF",   # SK Hynix — 62% HBM memory market, NVIDIA primary supplier (~$90B mkt cap)
                "IBIDY",   # Ibiden — sole AI server IC substrate supplier to NVIDIA (~$14B mkt cap)

                # Tier 3: Critical but more competitive
                "AMKR",    # Amkor Technology — #2 OSAT, advanced packaging for GPUs (~$12B mkt cap)
                "MPWR",    # Monolithic Power Systems — DC-DC power for AI GPU racks (~$30B mkt cap)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        # ---- Tech capex cycle signal (QQQ as proxy) ----
        capex_strong = False
        capex_score = 0.0
        if "QQQ" in prices:
            qqq_inds = self._get_indicators(
                data, "QQQ",
                ["sma_50", "sma_200", "rsi_14"],
                date,
            )
            qqq_price = prices["QQQ"]
            qqq_sma50 = qqq_inds["sma_50"]
            qqq_sma200 = qqq_inds["sma_200"]

            if not _is_missing(qqq_sma50) and not _is_missing(qqq_sma200):
                if qqq_price > qqq_sma50 > qqq_sma200:
                    capex_strong = True
                    capex_score = 3.0
                elif qqq_price > qqq_sma200:
                    capex_strong = True
                    capex_score = 1.5
                elif qqq_price > qqq_sma200 * 0.95:
                    capex_score = 0.5  # Marginal — near support

        # ---- Score each supply chain name ----
        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]

            if _is_missing(sma50) or _is_missing(rsi):
                continue

            # Hard exits
            if rsi > 82:
                weights[sym] = 0.0
                continue
            if not _is_missing(sma200) and price < sma200 * 0.75:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Monopoly tier bonus: true monopolies get structural premium
            if sym in self._TIER1_MONOPOLY:
                score += 1.5
            elif sym in self._TIER2_DOMINANT:
                score += 0.75

            # Tech capex cycle boost
            if capex_strong:
                score += min(capex_score * 0.4, 1.2)

            # Own-stock trend alignment
            if not _is_missing(sma200) and price > sma50 > sma200:
                score += 2.5
            elif price > sma50:
                score += 1.0
            elif not _is_missing(sma200) and price > sma200:
                score += 0.3

            # MACD bullish
            if not _is_missing(macd) and not _is_missing(macd_sig) and macd > macd_sig:
                score += 0.8

            # RSI sweet spot
            if 30 < rsi < 65:
                score += 0.5
            # Oversold dip-buy for monopolies (they always recover)
            elif rsi < 30 and sym in self._TIER1_MONOPOLY:
                if not _is_missing(sma200) and price > sma200 * 0.80:
                    score += 2.5

            if score >= 2.0:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.92, self.config.max_position_size)
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# Mag7 Domino Hedge
# ---------------------------------------------------------------------------
class Mag7DominoHedge(BasePersona):
    """Supply chain stress early-warning system that hedges Mag7 exposure.

    Thesis: Supply chain companies break BEFORE the Mag7 themselves. When
    critical suppliers (TSMC, ASML, Ajinomoto, SK Hynix, Entegris) show
    technical stress (price below SMA200 + volume spike), it's an early
    warning of Mag7 correction 2-6 weeks before it hits the megacaps.

    The strategy monitors a basket of "canary" supply chain names. In
    normal conditions, it holds equal-weight Mag7 + QQQ for growth exposure.
    When supply chain stress signals fire, it systematically rotates into
    defensive positions (staples, utilities, gold, treasuries).

    Stress detection:
    - Level 0 (green): 0-1 canaries stressed -> full Mag7 allocation
    - Level 1 (yellow): 2-3 canaries stressed -> reduce to 60% Mag7, add 30% defensive
    - Level 2 (orange): 4-5 canaries stressed -> 30% Mag7, 60% defensive
    - Level 3 (red): 6+ canaries stressed -> 0% Mag7, full defensive rotation

    A "stressed" canary = price below SMA200 AND (volume > 1.5x avg OR RSI < 35).

    Edge: Institutional investors monitor Mag7 directly but ignore their supply
    chain. A TSMC volume spike or Ajinomoto breakdown is visible weeks before
    it shows up in NVDA or AAPL earnings. This strategy front-runs the domino.
    """

    # Supply chain canaries — the early warning signals
    _CANARIES = [
        "TSM",     # TSMC — if the foundry breaks, everything breaks
        "ASML",    # ASML — EUV monopoly, bellwether for chip capex
        "AJINY",   # Ajinomoto — ABF substrate, hidden linchpin
        "HXSCF",   # SK Hynix — HBM memory, NVIDIA supply chain
        "ENTG",    # Entegris — fab chemicals, canary for fab utilization
        "LSRCY",   # Lasertec — EUV inspection, canary for leading-edge demand
        "SHECY",   # Shin-Etsu — silicon wafers, canary for broad chip demand
        "MRAAY",   # Murata — MLCC capacitors, canary for electronics demand
        "DSCOY",   # Disco Corp — wafer dicing, canary for chip output volume
        "GLW",     # Corning — glass + fiber, canary for both consumer + DC
    ]

    # Mag7 tickers for growth allocation
    _MAG7 = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA"]

    # Defensive rotation targets
    _DEFENSIVE = [
        "XLP",   # Consumer Staples ETF
        "XLU",   # Utilities ETF
        "GLD",   # Gold ETF
        "TLT",   # Long-term Treasury ETF
        "XLV",   # Healthcare ETF
        "PG",    # Procter & Gamble
        "JNJ",   # Johnson & Johnson
        "KO",    # Coca-Cola
    ]

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Mag7 Domino Hedge",
            description="Supply chain stress early-warning: rotates Mag7 to defensive when canaries break",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or (
                self._CANARIES + self._MAG7 + self._DEFENSIVE + ["QQQ", "SPY"]
            ),
        )
        super().__init__(config)

    def _count_stressed_canaries(self, date, prices, data):
        """Count how many supply chain canaries show stress signals.

        A canary is 'stressed' when:
        1. Price is below SMA200 (broken long-term trend), AND
        2. At least one of: volume > 1.5x average (panic selling) or RSI < 35 (oversold)
        """
        stressed = 0
        canary_details = []

        for sym in self._CANARIES:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym,
                ["sma_200", "rsi_14", "Volume", "volume_sma_20"],
                date,
            )
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]

            if _is_missing(sma200):
                continue

            below_sma200 = price < sma200
            vol_spike = (
                not _is_missing(volume) and not _is_missing(vol_avg)
                and vol_avg > 0 and volume > vol_avg * 1.5
            )
            oversold = not _is_missing(rsi) and rsi < 35

            if below_sma200 and (vol_spike or oversold):
                stressed += 1
                canary_details.append(sym)

        return stressed, canary_details

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # ---- Detect supply chain stress level ----
        stressed_count, _ = self._count_stressed_canaries(date, prices, data)

        # Determine allocation regime
        if stressed_count <= 1:
            # Level 0 (green): full growth
            mag7_pct = 0.85
            defensive_pct = 0.10
        elif stressed_count <= 3:
            # Level 1 (yellow): reduce growth, add defense
            mag7_pct = 0.55
            defensive_pct = 0.35
        elif stressed_count <= 5:
            # Level 2 (orange): heavy defensive
            mag7_pct = 0.25
            defensive_pct = 0.65
        else:
            # Level 3 (red): full defensive rotation
            mag7_pct = 0.0
            defensive_pct = 0.90

        # ---- Allocate Mag7 portion ----
        if mag7_pct > 0:
            mag7_scored = []
            for sym in self._MAG7:
                if sym not in prices:
                    continue
                inds = self._get_indicators(
                    data, sym,
                    ["sma_50", "sma_200", "rsi_14"],
                    date,
                )
                sma50 = inds["sma_50"]
                sma200 = inds["sma_200"]
                rsi = inds["rsi_14"]
                price = prices[sym]

                score = 1.0  # Base score for being in Mag7
                if not _is_missing(sma50) and not _is_missing(sma200):
                    if price > sma50 > sma200:
                        score += 2.0
                    elif price > sma50:
                        score += 1.0
                if not _is_missing(rsi) and 35 < rsi < 75:
                    score += 0.5
                # Skip overbought names even in growth mode
                if not _is_missing(rsi) and rsi > 80:
                    score = 0.0

                if score > 0:
                    mag7_scored.append((sym, score))

            mag7_scored.sort(key=lambda x: -x[1])
            # Take top names, allocate proportionally
            top_mag7 = mag7_scored[:7]
            if top_mag7:
                total = sum(s for _, s in top_mag7)
                for sym, sc in top_mag7:
                    w = (sc / total) * mag7_pct
                    weights[sym] = min(w, self.config.max_position_size)

            # Add QQQ as broad tech exposure
            if "QQQ" in prices:
                weights["QQQ"] = min(mag7_pct * 0.10, 0.08)

        # ---- Allocate defensive portion ----
        if defensive_pct > 0:
            def_available = [s for s in self._DEFENSIVE if s in prices]
            if def_available:
                per_def = min(defensive_pct / len(def_available), self.config.max_position_size)
                for sym in def_available:
                    weights[sym] = per_def

        # ---- Zero out anything not allocated ----
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0

        return weights


# ---------------------------------------------------------------------------
# Tech Boom Cycle Strategies (Historical Pattern)
# Research: knowledge/tech_boom_cycles_research.md
# ---------------------------------------------------------------------------


def _days_below_sma200(data, symbol, date, max_lookback=30):
    """Count consecutive trading days the symbol's Close was below its SMA200.

    Looks backward from *date* in data[symbol]. Returns 0 if currently above
    SMA200 or if data is unavailable.
    """
    if symbol not in data:
        return 0
    df = data[symbol]
    if "Close" not in df.columns or "sma_200" not in df.columns:
        return 0
    mask = df.index <= date
    subset = df.loc[mask].tail(max_lookback)
    if subset.empty:
        return 0
    count = 0
    for idx in reversed(subset.index):
        row = subset.loc[idx]
        close_val = row["Close"]
        sma_val = row["sma_200"]
        if hasattr(close_val, "iloc"):
            close_val = close_val.iloc[-1]
        if hasattr(sma_val, "iloc"):
            sma_val = sma_val.iloc[-1]
        try:
            if close_val != close_val or sma_val != sma_val:  # NaN check
                break
        except (TypeError, ValueError):
            break
        if close_val < sma_val:
            count += 1
        else:
            break
    return count


# ---------------------------------------------------------------------------
# AI Infrastructure Layer — the "railroad builders" of AI
# ---------------------------------------------------------------------------
class AIInfrastructureLayer(BasePersona):
    """AI physical infrastructure strategy.

    Historical parallel: Railroad builders in the 1840s, fiber optic companies
    in the 1990s. Companies building the physical layer always benefit during
    tech booms — data centers, power, cooling, networking.

    Signal: momentum following NVDA as lead indicator. Buy uptrends, cut below
    SMA200. NVDA acts as the canary — when it trends up, infrastructure demand
    is confirmed.

    Exit logic (in generate_signals):
    - Take profit: NVDA RSI > 80 AND 3+ infra stocks RSI > 75 → trim ALL by 30%.
    - Stop loss: NVDA below SMA200 (10+ days or any day) → EXIT ALL.
    - Per-stock: RSI > 80 → zero weight. Below SMA200 → zero weight.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="AI Infrastructure Layer",
            description="Railroad builders of AI: data centers, power, cooling, networking",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "EQIX", "DLR",          # Data center REITs
                "VST", "CEG", "NRG",    # Power for AI
                "VRT", "MOD",           # Cooling infrastructure
                "ANET", "MRVL",         # Networking
                "AMT", "CCI",           # Fiber / connectivity
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # ---- NVDA bellwether check ----
        nvda_below_sma200 = False
        nvda_rsi = None
        if "NVDA" in data:
            nvda_inds = self._get_indicators(
                data, "NVDA", ["sma_200", "rsi_14", "sma_50"], date
            )
            nvda_sma200 = nvda_inds["sma_200"]
            nvda_rsi = nvda_inds["rsi_14"]
            nvda_sma50 = nvda_inds["sma_50"]
            if "NVDA" in prices and not _is_missing(nvda_sma200):
                if prices["NVDA"] < nvda_sma200:
                    nvda_below_sma200 = True

        # STOP LOSS: NVDA below SMA200 AND stays below 10+ trading days
        # → AI capex cycle slowing → EXIT ALL
        if nvda_below_sma200:
            days_below = _days_below_sma200(data, "NVDA", date, max_lookback=30)
            if days_below >= 10:
                for sym in self.config.universe:
                    weights[sym] = 0.0
                return weights

        # Even single-day below SMA200 for NVDA → exit all (capex signal)
        if nvda_below_sma200:
            for sym in self.config.universe:
                weights[sym] = 0.0
            return weights

        # ---- Count infra stocks with RSI > 75 (overheating detection) ----
        high_rsi_count = 0
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["rsi_14"], date)
            rsi = inds["rsi_14"]
            if not _is_missing(rsi) and rsi > 75:
                high_rsi_count += 1

        # TAKE PROFIT: NVDA RSI > 80 AND 3+ infra stocks RSI > 75
        # → infrastructure overheated → trim ALL positions by 30%
        trim_factor = 1.0
        if (not _is_missing(nvda_rsi) and nvda_rsi > 80
                and high_rsi_count >= 3):
            trim_factor = 0.70

        # ---- Score each stock ----
        scored = []
        nvda_up = False
        if "NVDA" in prices and not _is_missing(nvda_sma200):
            nvda_sma50_val = nvda_inds["sma_50"] if "NVDA" in data else None
            if (not _is_missing(nvda_sma50_val) and not _is_missing(nvda_sma200)
                    and prices["NVDA"] > nvda_sma50_val > nvda_sma200):
                nvda_up = True

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"],
                date,
            )
            sma50, sma200 = inds["sma_50"], inds["sma_200"]
            rsi = inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]

            if _is_missing(sma200):
                continue

            # Per-stock: RSI > 80 → zero weight (overheated)
            if not _is_missing(rsi) and rsi > 80:
                weights[sym] = 0.0
                continue

            # Below SMA200 → broken trend
            if price < sma200:
                weights[sym] = 0.0
                continue

            score = 0.0
            if not _is_missing(sma50) and price > sma50 > sma200:
                score += 3.0
            elif not _is_missing(sma50) and price > sma50:
                score += 1.5

            if not _is_missing(macd) and not _is_missing(macd_sig) and macd > macd_sig:
                score += 1.0

            if nvda_up:
                score += 1.0

            if not _is_missing(rsi) and 35 < rsi < 70:
                score += 0.5

            if score > 2:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock * trim_factor
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# AI Application Survivors — the "Amazons" that will survive the bust
# ---------------------------------------------------------------------------
class AIApplicationSurvivors(BasePersona):
    """AI application survivor strategy.

    Historical parallel: Amazon survived the dotcom crash because it had REAL
    revenue and adapted its business model. Pets.com died because it had neither.
    Pick application companies with real revenue, not just AI hype.

    Signal: price > SMA200 AND positive MACD. Avoid stocks below SMA50 for
    extended periods (proxy for revenue weakness).

    Exit logic (in generate_signals):
    - Take profit: price > 3x SMA200 → halve weight (speculative territory).
    - Stop loss: below SMA200 for 20+ days → zero weight (not a survivor).
      Below SMA200 at all → zero weight.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="AI Application Survivors",
            description="The Amazons of AI: real-revenue application companies that survive the bust",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "CRM",    # Enterprise (Salesforce)
                "NOW",    # IT automation (ServiceNow)
                "ADBE",   # Creative tools (Adobe)
                "INTU",   # Tax/accounting (Intuit)
                "VEEV",   # Pharma data (Veeva)
                "HUBS",   # Marketing (HubSpot)
                "PANW",   # Cybersecurity (Palo Alto)
                "WDAY",   # HR/finance (Workday)
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
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"],
                date,
            )
            sma50, sma200 = inds["sma_50"], inds["sma_200"]
            rsi = inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]

            if _is_missing(sma200):
                continue

            # STOP LOSS: Below SMA200 for 20+ days → dead, not a survivor
            if price < sma200:
                days_below = _days_below_sma200(data, sym, date, max_lookback=30)
                if days_below >= 20:
                    weights[sym] = 0.0
                    continue
                # Even if < 20 days, below SMA200 = zero weight
                weights[sym] = 0.0
                continue

            # TAKE PROFIT: price/SMA200 > 3.0 → speculative territory → halve weight
            price_sma_ratio = price / sma200 if sma200 > 0 else 1.0
            halve_factor = 0.5 if price_sma_ratio > 3.0 else 1.0

            # Revenue-weakness proxy: below SMA50 = avoid
            if not _is_missing(sma50) and price < sma50:
                weights[sym] = 0.0
                continue

            # MACD must be positive — momentum confirmation
            macd_positive = (
                not _is_missing(macd)
                and not _is_missing(macd_sig)
                and macd > macd_sig
            )
            if not macd_positive:
                weights[sym] = 0.0
                continue

            # Overbought caution
            if not _is_missing(rsi) and rsi > 78:
                weights[sym] = 0.0
                continue

            score = 2.0  # Base: passed all filters
            # Above both MAs: strong
            if not _is_missing(sma50) and price > sma50 > sma200:
                score += 2.0
            # RSI sweet spot
            if not _is_missing(rsi) and 40 < rsi < 65:
                score += 1.0  # Not overheated = sustainable
            elif not _is_missing(rsi) and rsi < 40:
                score += 0.5  # Dip opportunity

            scored.append((sym, score, halve_factor))

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _, halve in top:
                weights[sym] = per_stock * halve
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# AI Adopters Not Builders — Walmart survived, e-commerce startups died
# ---------------------------------------------------------------------------
class AIAdoptersNotBuilders(BasePersona):
    """Traditional companies aggressively adopting AI.

    Historical parallel: Walmart adopted the internet for supply chain and
    e-commerce — survived and thrived. Most pure e-commerce startups died.
    Banks that adopted mobile banking outperformed fintech startups.

    Buy established companies in uptrends that are investing in AI. These are
    NOT valued as tech stocks, so they avoid the bubble premium.

    Exit logic (in generate_signals):
    - Take profit: RSI > 70 → trim (halve weight). RSI > 75 → zero weight.
      Adopters should not get speculative.
    - Stop loss: below SMA200 = adoption thesis failed → zero weight.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="AI Adopters Not Builders",
            description="Walmart principle: established companies adopting AI outperform tech builders",
            risk_tolerance=0.4,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "JPM",   # AI trading, fraud detection
                "UNH",   # AI healthcare / claims processing
                "WMT",   # AI supply chain / inventory
                "CAT",   # Autonomous equipment
                "DE",    # Precision agriculture
                "JNJ",   # AI drug discovery
                "UPS",   # AI logistics optimization
                "GE",    # AI industrial / jet engines
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
            inds = self._get_indicators(
                data, sym, ["sma_50", "sma_200", "rsi_14"], date,
            )
            sma50, sma200 = inds["sma_50"], inds["sma_200"]
            rsi = inds["rsi_14"]

            if _is_missing(sma200):
                continue

            # STOP LOSS: Below SMA200 = adoption thesis failed → exit
            if price < sma200:
                weights[sym] = 0.0
                continue

            # TAKE PROFIT: RSI > 75 → overextended for an adopter → no allocation
            if not _is_missing(rsi) and rsi > 75:
                weights[sym] = 0.0
                continue

            # Reject speculative overshoot (>50% above SMA200)
            if price > sma200 * 1.50:
                weights[sym] = 0.0
                continue

            # TAKE PROFIT: Trim at RSI > 70 — adopters should not get speculative
            trim_factor = 1.0
            if not _is_missing(rsi) and rsi > 70:
                trim_factor = 0.5  # Reduce allocation at RSI 70-75

            score = 1.0  # Base: in uptrend
            # Steady growth: close to SMA200 (within 20%) = healthy
            pct_above = (price - sma200) / sma200
            if pct_above < 0.20:
                score += 2.0  # Near SMA200 = steady, not speculative
            elif pct_above < 0.35:
                score += 1.0

            # SMA50 trend confirmation
            if not _is_missing(sma50) and sma50 > sma200:
                score += 1.0

            # RSI middle ground = sustainable
            if not _is_missing(rsi) and 35 < rsi < 60:
                score += 1.0
            elif not _is_missing(rsi) and rsi < 35:
                score += 0.5  # Dip buy

            if score > 2:
                scored.append((sym, score, trim_factor))

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _, trim in top:
                weights[sym] = per_stock * trim
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Late-Cycle Bubble Hedge — the "1999 detector"
# ---------------------------------------------------------------------------
class LateCycleBubbleHedge(BasePersona):
    """Late-cycle bubble detector and rotation strategy.

    THIS IS THE EXIT STRATEGY ITSELF. When AI froth is detected, rotate to
    value. When froth subsides, ride growth.

    Froth detection: Count how many of [NVDA, SMCI, ARM, PLTR, AI, MSTR]
    have RSI > 75.
    - froth >= 3 → 100% value allocation
    - froth 1-2 → 50% value, 50% growth
    - froth 0 → 100% growth
    """

    _FROTH_CANARIES = ["NVDA", "SMCI", "ARM", "PLTR", "AI", "MSTR"]
    _VALUE_ROTATION = ["BRK-B", "JNJ", "PG", "KO", "PEP", "MRK", "WMT", "XOM"]
    _GROWTH_STOCKS = ["MSFT", "AAPL", "GOOGL", "AMZN", "NVDA", "AVGO", "AMD", "QQQ"]

    def __init__(self, universe: list[str] | None = None):
        full_universe = list(set(
            LateCycleBubbleHedge._FROTH_CANARIES
            + LateCycleBubbleHedge._VALUE_ROTATION
            + LateCycleBubbleHedge._GROWTH_STOCKS
        ))
        config = PersonaConfig(
            name="Late-Cycle Bubble Hedge",
            description="Dynamic value/growth rotation based on AI froth detection",
            risk_tolerance=0.3,
            max_position_size=0.15,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or full_universe,
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # ---- Count froth canaries with RSI > 75 ----
        froth_count = 0
        for sym in self._FROTH_CANARIES:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["rsi_14"], date)
            rsi = inds["rsi_14"]
            if not _is_missing(rsi) and rsi > 75:
                froth_count += 1

        # ---- Determine allocation regime ----
        if froth_count >= 3:
            # Full defensive: 100% value
            value_pct = 1.0
            growth_pct = 0.0
        elif froth_count >= 1:
            # Half defensive: 50% value, 50% growth
            value_pct = 0.5
            growth_pct = 0.5
        else:
            # No froth: 100% growth
            value_pct = 0.0
            growth_pct = 1.0

        # ---- Allocate value portion ----
        if value_pct > 0:
            value_available = [s for s in self._VALUE_ROTATION if s in prices]
            if value_available:
                value_scored = []
                for sym in value_available:
                    inds = self._get_indicators(data, sym, ["sma_200", "rsi_14"], date)
                    sma200, rsi = inds["sma_200"], inds["rsi_14"]
                    price = prices[sym]
                    score = 1.0
                    if not _is_missing(sma200) and price > sma200:
                        score += 1.0
                    if not _is_missing(rsi) and rsi < 60:
                        score += 0.5
                    value_scored.append((sym, score))
                value_scored.sort(key=lambda x: -x[1])
                top_val = value_scored[:self.config.max_positions]
                if top_val:
                    per_stock = min(
                        value_pct * 0.90 / len(top_val),
                        self.config.max_position_size,
                    )
                    for sym, _ in top_val:
                        weights[sym] = per_stock

        # ---- Allocate growth portion ----
        if growth_pct > 0:
            growth_scored = []
            for sym in self._GROWTH_STOCKS:
                if sym not in prices:
                    continue
                price = prices[sym]
                inds = self._get_indicators(
                    data, sym, ["sma_50", "sma_200", "rsi_14"], date,
                )
                sma50, sma200 = inds["sma_50"], inds["sma_200"]
                rsi = inds["rsi_14"]
                if _is_missing(sma200):
                    continue
                if price < sma200:
                    weights[sym] = 0.0
                    continue
                score = 1.0
                if not _is_missing(sma50) and price > sma50 > sma200:
                    score += 2.0
                if not _is_missing(rsi) and 35 < rsi < 70:
                    score += 0.5
                growth_scored.append((sym, score))

            growth_scored.sort(key=lambda x: -x[1])
            top_growth = growth_scored[:8]
            if top_growth:
                total = sum(s for _, s in top_growth)
                for sym, sc in top_growth:
                    w = (sc / total) * growth_pct * 0.90
                    weights[sym] = min(w, self.config.max_position_size)

        # ---- Zero out unallocated ----
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Picks and Shovels AI — the Levi Strauss principle
# ---------------------------------------------------------------------------
class PicksAndShovelsAI(BasePersona):
    """Sell tools to the AI miners, don't mine.

    Historical parallel: Levi Strauss sold work clothes to gold miners and
    died worth ~$1B (today's money). Never mined an ounce of gold. During
    the internet boom, companies selling routers and servers (Cisco) profited
    while individual dotcoms failed.

    Universe: companies selling tools/services to AI chip and infrastructure
    companies. Not the AI companies themselves.

    Exit logic (in generate_signals):
    - Take profit: RSI > 80 → zero weight (shovel makers overpriced = gold
      rush ending).
    - Stop loss: NVDA AND ASML both below SMA200 → EXIT ALL (semiconductor
      cycle turning). Individual stock below SMA200 → zero weight.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Picks and Shovels AI",
            description="Levi Strauss principle: sell tools to AI miners, don't mine",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "ENTG",   # Chip chemicals (Entegris)
                "KLAC",   # Chip inspection (KLA Corp)
                "CDNS",   # Chip design software (Cadence)
                "SNPS",   # Chip design (Synopsys)
                "ANSS",   # Simulation software (Ansys)
                "KEYS",   # Test equipment (Keysight)
                "FLEX",   # Contract manufacturing (Flex)
                "LRCX",   # Wafer fabrication (Lam Research)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # ---- Cycle check: NVDA + ASML both below SMA200 = semi cycle turning ----
        nvda_below = False
        asml_below = False
        for leader in ["NVDA", "ASML"]:
            if leader in data:
                inds = self._get_indicators(data, leader, ["sma_200"], date)
                sma200 = inds["sma_200"]
                if leader in prices and not _is_missing(sma200):
                    if prices[leader] < sma200:
                        if leader == "NVDA":
                            nvda_below = True
                        else:
                            asml_below = True

        # STOP LOSS: Both NVDA AND ASML below SMA200 = entire semiconductor
        # cycle is turning → EXIT ALL
        if nvda_below and asml_below:
            for sym in self.config.universe:
                weights[sym] = 0.0
            return weights

        # ---- NVDA demand multiplier (softer signal when only one is weak) ----
        demand_mult = 1.0
        if "NVDA" in prices and "NVDA" in data:
            nvda_inds = self._get_indicators(
                data, "NVDA", ["sma_50", "sma_200"], date
            )
            nvda_sma50 = nvda_inds["sma_50"]
            nvda_sma200 = nvda_inds["sma_200"]
            if not _is_missing(nvda_sma50) and not _is_missing(nvda_sma200):
                nvda_price = prices["NVDA"]
                if nvda_price > nvda_sma50 > nvda_sma200:
                    demand_mult = 1.3
                elif nvda_price > nvda_sma200:
                    demand_mult = 1.0
                else:
                    demand_mult = 0.5

        # ---- Score each picks-and-shovels stock ----
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"],
                date,
            )
            sma50, sma200 = inds["sma_50"], inds["sma_200"]
            rsi = inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]

            if _is_missing(sma200):
                continue

            # TAKE PROFIT: RSI > 80 → shovel makers overpriced → zero
            if not _is_missing(rsi) and rsi > 80:
                weights[sym] = 0.0
                continue

            # Below SMA200 → individual trend broken
            if price < sma200:
                weights[sym] = 0.0
                continue

            score = 0.0
            if not _is_missing(sma50) and price > sma50 > sma200:
                score += 3.0
            elif not _is_missing(sma50) and price > sma50:
                score += 1.5

            if not _is_missing(macd) and not _is_missing(macd_sig) and macd > macd_sig:
                score += 1.0

            if not _is_missing(rsi) and 35 < rsi < 70:
                score += 0.5

            score *= demand_mult

            if score > 2:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# ESG Momentum
# ---------------------------------------------------------------------------
class ESGMomentum(BasePersona):
    """ESG momentum: ride institutional flows favoring ESG leaders.

    Source: ESGU returned ~19% over past year edging out SPY's 18%.
    Five-year: ESGU +76% vs SPY +74%. ESGV 3-year return 20.64%.
    A $100 investment in sustainable funds in Dec 2018 grew to $136
    vs $131 for traditional funds. However ESG saw $84B net outflows
    in 2025, so this is a momentum play on when flows return.

    Thesis: When institutional flows favor ESG (ESGU/ESGV trending up),
    ESG leaders outperform. When ESG is out of favor, rotate to
    high-quality ESG-rated individual names that outperform regardless.

    Implementation:
    - Track ESGU and ESGV momentum as ESG flow proxy
    - When ESG ETFs trend up (above SMA50): overweight ESG ETFs + leaders
    - When ESG ETFs trend down: focus on quality individual ESG names
      with strong momentum (these outperform regardless of ESG flows)
    - Weekly rebalance
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="ESG Momentum",
            description="ESG leaders when institutional flows favor sustainability, quality names always",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                # ESG ETFs (flow proxy)
                "ESGU",   # iShares ESG Aware MSCI USA
                "ESGV",   # Vanguard ESG U.S. Stock
                "SUSL",   # iShares ESG MSCI USA Leaders
                # Top ESG-rated individual stocks
                "MSFT", "CRM", "ADBE", "NVDA", "GOOGL", "PG", "JNJ",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Determine ESG flow regime from ETF momentum
        esg_etfs = ["ESGU", "ESGV", "SUSL"]
        esg_strong = 0
        esg_total = 0

        for etf in esg_etfs:
            if etf not in prices:
                continue
            esg_total += 1
            sma50 = self._get_indicator(data, etf, "sma_50", date)
            if not _is_missing(sma50) and prices[etf] > sma50:
                esg_strong += 1

        esg_flow_positive = esg_total > 0 and esg_strong >= (esg_total / 2)

        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]

            if _is_missing(sma50):
                continue

            score = 0.0

            if esg_flow_positive and sym in esg_etfs:
                # ESG flows strong — overweight ETFs
                if price > sma50:
                    score += 3.0
                    if not _is_missing(sma200) and sma50 > sma200:
                        score += 1.0
            else:
                # Focus on individual quality names
                if price > sma50:
                    score += 2.0
                    if not _is_missing(sma200) and price > sma200:
                        score += 1.0

            if not _is_missing(rsi) and 35 < rsi < 70:
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
# Africa & Frontier Markets
# ---------------------------------------------------------------------------
class AfricaFrontier(BasePersona):
    """Africa and frontier markets: diversification + growth.

    Source: AFK (VanEck Africa Index ETF) returned 57.5% YTD in 2025,
    outperforming both IEMG (29.4%) and EMXC (24.7%). MSCI Frontier
    Markets Africa Index returned 40.81% (gross) in 2025 and 9.84%
    in 2024. However, since inception AFK has posted -2.3% annualized,
    showing the importance of momentum timing.

    Thesis: Frontier markets are largely uncorrelated with US equities,
    providing genuine diversification. When momentum aligns (above SMA),
    Africa/frontier exposure can add alpha. When momentum is negative,
    stay out entirely.

    Implementation:
    - Universe: Africa and frontier ETFs + gold miners (African exposure)
    - Strict momentum filter: only buy when above SMA50 AND SMA200
    - Include GOLD, HMY, SBSW for gold/Africa mining exposure
    - Weekly rebalance with trend following
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Africa & Frontier Markets",
            description="Frontier markets for diversification: Africa, Nigeria, S. Africa + gold miners",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "AFK",   # VanEck Africa Index ETF
                "FM",    # iShares MSCI Frontier and Select EM ETF
                "NGE",   # Global X MSCI Nigeria ETF
                "EZA",   # iShares MSCI South Africa ETF
                "GOLD",  # Barrick Gold (Africa mining ops)
                "HMY",   # Harmony Gold Mining (South Africa)
                "SBSW",  # Sibanye Stillwater (S. Africa)
                "VALE",  # Vale (Brazil/Africa mining)
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
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "vol_20"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            vol = inds["vol_20"]

            if _is_missing(sma50) or _is_missing(sma200):
                continue

            # Strict momentum: must be above BOTH SMAs
            if price <= sma50 or price <= sma200:
                continue

            score = 0.0

            # Trend alignment
            if sma50 > sma200:
                score += 3.0  # Golden cross
            else:
                score += 1.5  # Above both but not yet crossed

            # RSI sweet spot
            if not _is_missing(rsi):
                if 40 < rsi < 70:
                    score += 1.0
                elif rsi >= 75:
                    continue  # Overbought frontier = dangerous

            # Prefer lower vol (frontier can be very volatile)
            if not _is_missing(vol) and vol > 0:
                score *= min(1.5, 0.025 / vol)

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
# Southeast Asia Growth
# ---------------------------------------------------------------------------
class SoutheastAsiaGrowth(BasePersona):
    """Southeast Asia / ASEAN growth play.

    Source: ASEAN GDP growth forecast 4.6-4.8% for 2024-2025 (vs US ~2%).
    ASEA ETF returned 28.13% in the past year. Young demographics,
    rising middle class, and manufacturing shift from China create a
    structural growth tailwind.

    Thesis: ASEAN economies are growing 5%+, with young demographics
    and rising middle class driving consumption. Vietnam, Indonesia,
    and Philippines are the fastest growers. Singapore is the financial
    hub. When momentum aligns, ASEAN ETFs offer growth + diversification.

    Implementation:
    - Country ETFs for targeted ASEAN exposure
    - Momentum filter: above SMA50 for entry
    - Rank by relative strength, take top positions
    - Monthly rebalance (ASEAN markets less liquid)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Southeast Asia Growth",
            description="ASEAN growth play: 5%+ GDP, young demographics, rising middle class",
            risk_tolerance=0.6,
            max_position_size=0.20,
            max_positions=6,
            rebalance_frequency="monthly",
            universe=universe or [
                "EWS",   # iShares MSCI Singapore
                "EWM",   # iShares MSCI Malaysia
                "THD",   # iShares MSCI Thailand
                "VNM",   # VanEck Vietnam ETF
                "EIDO",  # iShares MSCI Indonesia
                "EPHE",  # iShares MSCI Philippines
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
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "vol_20"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            vol = inds["vol_20"]

            if _is_missing(sma50):
                continue

            # Momentum filter: above SMA50
            if price <= sma50:
                continue

            score = 0.0

            # Trend strength
            if not _is_missing(sma200) and price > sma200:
                score += 2.0
                if sma50 > sma200:
                    score += 1.5  # Strong uptrend
            else:
                score += 1.0  # Above SMA50 but not SMA200 yet

            # RSI filter
            if not _is_missing(rsi):
                if 40 < rsi < 65:
                    score += 1.0  # Sweet spot
                elif 65 <= rsi < 75:
                    score += 0.5
                elif rsi >= 75:
                    continue  # Overbought EM = risk

            # Vol adjustment (prefer lower vol EM)
            if not _is_missing(vol) and vol > 0:
                score *= min(1.3, 0.02 / vol)

            if score >= 1.5:
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
# Infrastructure Reshoring
# ---------------------------------------------------------------------------
class InfrastructureReshoring(BasePersona):
    """Infrastructure reshoring theme strategy.

    Source: IIJA ($1.2T), CHIPS Act ($280B), IRA ($369B) — secular US
    infrastructure spending spanning bridges, roads, data centers,
    domestic manufacturing.

    Universe:
    - PAVE (Global X US Infrastructure ETF)
    - CAT (Caterpillar — heavy equipment)
    - DE (Deere — construction/ag equipment)
    - VMC (Vulcan Materials — aggregates/cement)
    - MLM (Martin Marietta — aggregates)
    - URI (United Rentals — equipment rental)

    Equal weight with momentum tilt: overweight names above SMA50
    (active spending phase), underweight names below (project delays).
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Infrastructure Reshoring",
            description="US infrastructure spending: PAVE, heavy equipment, materials",
            risk_tolerance=0.6,
            max_position_size=0.20,
            max_positions=6,
            rebalance_frequency="monthly",
            universe=universe or [
                "PAVE",  # US Infrastructure ETF
                "CAT",   # Caterpillar
                "DE",    # Deere
                "VMC",   # Vulcan Materials
                "MLM",   # Martin Marietta
                "URI",   # United Rentals
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        above_sma = []
        below_sma = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym, ["sma_50", "sma_200", "rsi_14"], date
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]

            # Skip if severely broken trend (>20% below SMA200)
            if not _is_missing(sma200) and sma200 > 0:
                if price < sma200 * 0.80:
                    weights[sym] = 0.0
                    continue

            # RSI filter: skip extremely overbought
            if not _is_missing(rsi) and rsi > 80:
                weights[sym] = 0.0
                continue

            # Momentum tilt: classify above/below SMA50
            if not _is_missing(sma50) and price > sma50:
                above_sma.append(sym)
            else:
                below_sma.append(sym)

        # Equal weight with momentum tilt
        # Above SMA50 names get 1.5x the weight of below-SMA50 names
        total_units = len(above_sma) * 1.5 + len(below_sma) * 1.0
        if total_units > 0:
            base_weight = min(0.90 / total_units, self.config.max_position_size)
            for sym in above_sma:
                weights[sym] = base_weight * 1.5
            for sym in below_sma:
                weights[sym] = base_weight * 1.0

        # Close non-qualifying
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0

        return weights


# ---------------------------------------------------------------------------
# Anthropic Ecosystem (Pre-IPO Play)
# ---------------------------------------------------------------------------
class AnthropicEcosystem(BasePersona):
    """Invest in the Anthropic supply chain, investors, and customers before
    its expected Q4 2026 IPO.

    Source: knowledge/anthropic_ecosystem_research.md
    Anthropic is the fastest-growing enterprise AI company ($30B+ ARR as of
    April 2026, ~1400% YoY). IPO expected Q4 2026 at $380B+ valuation.
    80% enterprise revenue mix, multi-cloud strategy (AWS, Google Cloud, Azure).

    Universe (tiered):
    - Tier 1-2 (Direct/Investor, 2x weight): AMZN ($8B invested, 7.8% stake),
      GOOGL ($3B+, 14% stake), MSFT (up to $5B), NVDA (up to $10B), CRM (investor)
    - Tier 3 (Supply chain, 1.5x weight): AVGO (TPU design, $21-42B est revenue),
      ANET (DC networking), VRT (power+cooling), EQIX (data center REIT),
      MU (HBM memory), CLS (AI server mfg)
    - Tier 4 (Customers, 1x weight): SNOW ($200M partnership), ACN (30K trained),
      GTLB (marketplace partner)
    - Tier 5 (Power, 1x weight): CEG (largest US nuclear), VST (2nd largest)

    Signal logic:
    - Core holdings (AMZN, GOOGL, AVGO, NVDA) get 2x base weight
    - Momentum tilt: above SMA50 = full weight, below = half weight
    - Risk-off filter: if SPY RSI > 75, reduce all to 50%
    - Equal-weight base across tiers with tier multipliers

    ## Passive Investor Section
    For buy-and-hold investors who want Anthropic pre-IPO exposure without
    active management: equal-weight AMZN, GOOGL, MSFT, NVDA, AVGO. These 5
    names give direct investor exposure + supply chain. Rebalance quarterly.
    Expected to outperform SPY as Anthropic IPO catalysts emerge in H2 2026.
    """

    # Tier assignments for weight multipliers
    TIER_12 = {"AMZN", "GOOGL", "MSFT", "NVDA", "CRM"}  # 2x
    TIER_3 = {"AVGO", "ANET", "VRT", "EQIX", "MU", "CLS"}  # 1.5x
    TIER_45 = {"SNOW", "ACN", "GTLB", "CEG", "VST"}  # 1x
    CORE = {"AMZN", "GOOGL", "AVGO", "NVDA"}  # extra 2x conviction

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Anthropic Ecosystem",
            description="Anthropic supply chain + investors pre-IPO (Q4 2026 expected)",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                # Tier 1-2: Direct investors
                "AMZN", "GOOGL", "MSFT", "NVDA", "CRM",
                # Tier 3: Supply chain
                "AVGO", "ANET", "VRT", "EQIX", "MU", "CLS",
                # Tier 4: Customers
                "SNOW", "ACN", "GTLB",
                # Tier 5: Power
                "CEG", "VST",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # --- Risk-off filter: check SPY RSI ---
        risk_off_mult = 1.0
        if "SPY" in data:
            spy_rsi = self._get_indicator(data, "SPY", "rsi_14", date)
            if not _is_missing(spy_rsi) and spy_rsi > 75:
                risk_off_mult = 0.5  # Overbought market -> reduce exposure

        # --- Score and weight each ticker ---
        qualified = []  # (sym, tier_mult, momentum_mult)

        for sym in self.config.universe:
            if sym not in data or sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym, ["sma_50", "sma_200", "rsi_14"], date
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]

            if _is_missing(sma50):
                continue

            # Skip extremely overbought individual names
            if not _is_missing(rsi) and rsi > 80:
                weights[sym] = 0.0
                continue

            # Skip broken trends (>25% below SMA200)
            if not _is_missing(sma200) and sma200 > 0 and price < sma200 * 0.75:
                weights[sym] = 0.0
                continue

            # Tier multiplier
            if sym in self.TIER_12:
                tier_mult = 2.0
            elif sym in self.TIER_3:
                tier_mult = 1.5
            else:
                tier_mult = 1.0

            # Core conviction bonus
            if sym in self.CORE:
                tier_mult *= 2.0

            # Momentum tilt: above SMA50 = full, below = half
            if price > sma50:
                momentum_mult = 1.0
            else:
                momentum_mult = 0.5

            qualified.append((sym, tier_mult * momentum_mult))

        # --- Distribute weights proportionally ---
        total_units = sum(mult for _, mult in qualified)
        if total_units > 0:
            base = 0.90 / total_units
            for sym, mult in qualified:
                w = base * mult * risk_off_mult
                weights[sym] = min(w, self.config.max_position_size)

        # Zero out anything not qualified
        for sym in self.config.universe:
            if sym not in weights and sym in prices:
                weights[sym] = 0.0

        return weights


# ---------------------------------------------------------------------------
# OpenAI Ecosystem (Microsoft-centric)
# ---------------------------------------------------------------------------
class OpenAIEcosystem(BasePersona):
    """Invest in OpenAI's ecosystem -- Microsoft-centric since MSFT is the
    primary partner (49% stake, $13B+ invested).

    Source: knowledge/ai_competitors_research.md
    OpenAI at $852B valuation, $24B ARR. Microsoft is the dominant public
    proxy: Azure AI at $13B run-rate, GitHub Copilot at 26M+ users,
    Copilot in M365 with only 3.3% conversion (massive upside).

    Universe:
    - Direct/Investor: MSFT (49% stake, 3x weight), ORCL (Stargate project, 2x),
      NVDA (GPU supplier)
    - Supply chain: AVGO, AMD, TSM, ASML, ANET, VRT, MU
    - Infrastructure: EQIX, DLR, CEG, VST
    - Customers/Partners: CRM (Einstein GPT), NOW (ServiceNow), ADBE

    Signal logic:
    - MSFT gets 3x base weight (dominant OpenAI exposure)
    - ORCL gets 2x (Stargate project)
    - Momentum tilt: above SMA50 = full weight, below = half
    - Risk-off filter: SPY RSI > 75 -> reduce all to 50%

    ## Passive Investor Section
    For buy-and-hold: MSFT (40%), ORCL (15%), NVDA (15%), AVGO (10%),
    CRM (10%), NOW (10%). MSFT is the single best public proxy for OpenAI.
    Rebalance quarterly. If MSFT Copilot conversion goes from 3.3% to 10%,
    that alone is $20B+ incremental revenue.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="OpenAI Ecosystem",
            description="OpenAI ecosystem play: Microsoft-centric, Stargate infrastructure",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                # Direct/Investor
                "MSFT", "ORCL", "NVDA",
                # Supply chain
                "AVGO", "AMD", "TSM", "ASML", "ANET", "VRT", "MU",
                # Infrastructure
                "EQIX", "DLR", "CEG", "VST",
                # Customers/Partners
                "CRM", "NOW", "ADBE",
            ],
        )
        super().__init__(config)

    # Weight overrides
    _WEIGHT_OVERRIDE = {"MSFT": 3.0, "ORCL": 2.0}

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # --- Risk-off filter: check SPY RSI ---
        risk_off_mult = 1.0
        if "SPY" in data:
            spy_rsi = self._get_indicator(data, "SPY", "rsi_14", date)
            if not _is_missing(spy_rsi) and spy_rsi > 75:
                risk_off_mult = 0.5

        # --- Score each ticker ---
        qualified = []  # (sym, weight_mult)

        for sym in self.config.universe:
            if sym not in data or sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym, ["sma_50", "sma_200", "rsi_14"], date
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]

            if _is_missing(sma50):
                continue

            # Skip overbought
            if not _is_missing(rsi) and rsi > 80:
                weights[sym] = 0.0
                continue

            # Skip broken trend (>25% below SMA200)
            if not _is_missing(sma200) and sma200 > 0 and price < sma200 * 0.75:
                weights[sym] = 0.0
                continue

            # Base multiplier from override or 1.0
            base_mult = self._WEIGHT_OVERRIDE.get(sym, 1.0)

            # Momentum tilt: above SMA50 = full, below = half
            if price > sma50:
                momentum_mult = 1.0
            else:
                momentum_mult = 0.5

            qualified.append((sym, base_mult * momentum_mult))

        # --- Distribute weights proportionally ---
        total_units = sum(mult for _, mult in qualified)
        if total_units > 0:
            base = 0.90 / total_units
            for sym, mult in qualified:
                w = base * mult * risk_off_mult
                weights[sym] = min(w, self.config.max_position_size)

        # Zero out anything not qualified
        for sym in self.config.universe:
            if sym not in weights and sym in prices:
                weights[sym] = 0.0

        return weights


# ---------------------------------------------------------------------------
# AI Infrastructure Picks & Shovels (Arms Dealer)
# ---------------------------------------------------------------------------
class AIInfraPicksShovels(BasePersona):
    """The 'arms dealer' strategy -- companies that win regardless of which
    AI company dominates. Pure picks-and-shovels infrastructure play.

    Source: knowledge/anthropic_ecosystem_research.md + ai_competitors_research.md
    Every AI company needs the same infrastructure: chips, data centers,
    networking, power, memory. This strategy owns the shared layer.

    Universe:
    - Chips: NVDA, AVGO, AMD, TSM, ASML, AMAT, LRCX, MRVL, ARM
    - Data centers: EQIX, DLR, VRT, ETN, CLS, ANET
    - Power: CEG, VST
    - Memory: MU

    Signal logic:
    - Equal-weight across all tickers
    - Semiconductor over-weight when SOX proxy (NVDA+AMD+AVGO avg) momentum
      is positive (above SMA50)
    - Power stocks get bonus weight when VIX > 20 (defensive quality)
    - Momentum tilt: above SMA200 = full weight, below = half weight
      (longer-term trend for infrastructure)

    ## Passive Investor Section
    For buy-and-hold: equal-weight NVDA, AVGO, TSM, ASML, EQIX, ANET, CEG.
    These 7 names span the full AI infrastructure stack: chips, foundry,
    lithography, data centers, networking, power. Rebalance quarterly.
    This portfolio wins whether Anthropic, OpenAI, Google, or Meta leads AI.
    """

    CHIP_NAMES = {"NVDA", "AVGO", "AMD", "TSM", "ASML", "AMAT", "LRCX", "MRVL", "ARM"}
    POWER_NAMES = {"CEG", "VST"}
    SOX_PROXY = ["NVDA", "AMD", "AVGO"]  # Average momentum as semi cycle proxy

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="AI Infrastructure Picks & Shovels",
            description="Arms dealer strategy: wins regardless of which AI company dominates",
            risk_tolerance=0.6,
            max_position_size=0.12,
            max_positions=15,
            rebalance_frequency="monthly",
            universe=universe or [
                # Chips
                "NVDA", "AVGO", "AMD", "TSM", "ASML", "AMAT", "LRCX", "MRVL", "ARM",
                # Data centers
                "EQIX", "DLR", "VRT", "ETN", "CLS", "ANET",
                # Power
                "CEG", "VST",
                # Memory
                "MU",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # --- SOX proxy: average of NVDA+AMD+AVGO above their SMA50 ---
        sox_above = 0
        sox_total = 0
        for leader in self.SOX_PROXY:
            if leader in data and leader in prices:
                sox_total += 1
                sma50 = self._get_indicator(data, leader, "sma_50", date)
                if not _is_missing(sma50) and prices[leader] > sma50:
                    sox_above += 1
        semi_momentum_positive = sox_total > 0 and sox_above > sox_total / 2

        # --- VIX proxy: use SPY volatility via RSI (no direct VIX data) ---
        # High volatility regime when SPY RSI < 40 (fear) as proxy for VIX > 20
        high_vol_regime = False
        if "SPY" in data:
            spy_rsi = self._get_indicator(data, "SPY", "rsi_14", date)
            if not _is_missing(spy_rsi) and spy_rsi < 40:
                high_vol_regime = True

        # --- Score each ticker ---
        qualified = []  # (sym, weight_mult)

        for sym in self.config.universe:
            if sym not in data or sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym, ["sma_50", "sma_200", "rsi_14"], date
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]

            if _is_missing(sma200):
                # ARM and other newer tickers may not have SMA200 history
                # Fall back to SMA50 for these
                if _is_missing(sma50):
                    continue
                # Use SMA50 as trend proxy for short-history tickers
                if price > sma50:
                    momentum_mult = 1.0
                else:
                    momentum_mult = 0.5
            else:
                # Skip severely broken trend (>30% below SMA200)
                if sma200 > 0 and price < sma200 * 0.70:
                    weights[sym] = 0.0
                    continue

                # Momentum tilt: above SMA200 = full, below = half
                if price > sma200:
                    momentum_mult = 1.0
                else:
                    momentum_mult = 0.5

            # Skip extremely overbought
            if not _is_missing(rsi) and rsi > 80:
                weights[sym] = 0.0
                continue

            # Base weight = 1.0 (equal weight)
            weight_mult = 1.0

            # Semiconductor over-weight when semi momentum is positive
            if sym in self.CHIP_NAMES and semi_momentum_positive:
                weight_mult *= 1.5

            # Power stocks bonus when volatility is high (defensive quality)
            if sym in self.POWER_NAMES and high_vol_regime:
                weight_mult *= 1.5

            qualified.append((sym, weight_mult * momentum_mult))

        # --- Distribute weights proportionally ---
        total_units = sum(mult for _, mult in qualified)
        if total_units > 0:
            base = 0.90 / total_units
            for sym, mult in qualified:
                w = base * mult
                weights[sym] = min(w, self.config.max_position_size)

        # Zero out anything not qualified
        for sym in self.config.universe:
            if sym not in weights and sym in prices:
                weights[sym] = 0.0

        return weights


# ---------------------------------------------------------------------------
# Open-Source AI Ecosystem (HuggingFace + Mistral proxy + fine-tuning infra)
# ---------------------------------------------------------------------------
class OpenSourceAIEcosystem(BasePersona):
    """Invest in the open-source / emerging AI ecosystem -- HuggingFace investors,
    Mistral proxy (ASML), fine-tuning infrastructure, and companies building on
    open-source models.

    Source: knowledge/emerging_ai_ecosystem_research.md
    Open-source models capture 30% of global AI usage in 2026 (up from 1.2%
    in late 2024). HuggingFace ($4.5B val, $130M rev, 5M+ users) is the
    distribution layer; Mistral AI ($14B val, ASML owns 11%) is the leading
    European open-source model provider; Unsloth/Reka/Thinking Machines are
    driving fine-tuning and inference demand.

    Universe (tiered by exposure):
    - ASML: 2x weight (11% Mistral ownership -- only public proxy for open-source
      model layer; also enables ALL chip manufacturing)
    - NVDA: 2x weight (invested in HuggingFace, Reka, Thinking Machines, Mistral;
      acquired Groq; 92% GPU market share)
    - META: 1.5x weight (Llama is THE dominant open-source model family)
    - HuggingFace investors (1x): GOOGL, AMZN, CRM, INTC, AMD, QCOM, IBM
    - Infrastructure (1x): TSM, AVGO, MU, ANET, VRT, EQIX
    - Enterprise adopters (1x): SNOW (Reka co-lead, open model user),
      NOW (ServiceNow, Thinking Machines investor)

    Signal logic:
    - Momentum tilt: above SMA50 = full weight, below = half weight
    - Risk-off filter: SPY RSI > 75 -> reduce all to 50%
    - Skip overbought (RSI > 80) and broken trends (>25% below SMA200)
    - Monthly rebalance

    ## Passive Investor Section
    For buy-and-hold investors who want open-source AI exposure without active
    management: equal-weight NVDA, ASML, META, GOOGL, AMZN, TSM. These 6 names
    span GPU monopoly, Mistral proxy, Llama ecosystem, HuggingFace investors,
    and chip fabrication. Rebalance quarterly. Expected to outperform SPY as
    open-source AI usage grows from 30% toward 50%+ of global AI workloads.
    """

    # Weight multipliers by tier
    _WEIGHT_OVERRIDE = {
        "ASML": 2.0,   # 11% Mistral ownership = best open-source model proxy
        "NVDA": 2.0,   # HuggingFace + Reka + Thinking Machines + Mistral investor
        "META": 1.5,   # Llama = dominant open-source model
    }

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Open-Source AI Ecosystem",
            description="HuggingFace investors, Mistral proxy (ASML), open-source AI infrastructure",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=15,
            rebalance_frequency="monthly",
            universe=universe or [
                # Tier 1: Conviction overweights
                "ASML", "NVDA", "META",
                # Tier 2: HuggingFace Series D investors
                "GOOGL", "AMZN", "CRM", "INTC", "AMD", "QCOM", "IBM",
                # Tier 3: Infrastructure (chip fab, memory, networking, power, DC)
                "TSM", "AVGO", "MU", "ANET", "VRT", "EQIX",
                # Tier 4: Enterprise adopters of open-source models
                "SNOW", "NOW",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # --- Risk-off filter: check SPY RSI ---
        risk_off_mult = 1.0
        if "SPY" in data:
            spy_rsi = self._get_indicator(data, "SPY", "rsi_14", date)
            if not _is_missing(spy_rsi) and spy_rsi > 75:
                risk_off_mult = 0.5  # Overbought market -> reduce exposure

        # --- Score each ticker ---
        qualified = []  # (sym, weight_mult)

        for sym in self.config.universe:
            if sym not in data or sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym, ["sma_50", "sma_200", "rsi_14"], date
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]

            if _is_missing(sma50):
                continue

            # Skip extremely overbought individual names
            if not _is_missing(rsi) and rsi > 80:
                weights[sym] = 0.0
                continue

            # Skip broken trends (>25% below SMA200)
            if not _is_missing(sma200) and sma200 > 0 and price < sma200 * 0.75:
                weights[sym] = 0.0
                continue

            # Base multiplier from override or 1.0
            base_mult = self._WEIGHT_OVERRIDE.get(sym, 1.0)

            # Momentum tilt: above SMA50 = full weight, below = half
            if price > sma50:
                momentum_mult = 1.0
            else:
                momentum_mult = 0.5

            qualified.append((sym, base_mult * momentum_mult))

        # --- Distribute weights proportionally ---
        total_units = sum(mult for _, mult in qualified)
        if total_units > 0:
            base = 0.90 / total_units
            for sym, mult in qualified:
                w = base * mult * risk_off_mult
                weights[sym] = min(w, self.config.max_position_size)

        # Zero out anything not qualified
        for sym in self.config.universe:
            if sym not in weights and sym in prices:
                weights[sym] = 0.0

        return weights


# ---------------------------------------------------------------------------
# AI Mega Ecosystem (union of all 6 AI strategies, conviction-weighted)
# ---------------------------------------------------------------------------
class AIMegaEcosystem(BasePersona):
    """Diversified mega-strategy combining ALL tickers from the 6 individual AI
    ecosystem strategies into one conviction-weighted portfolio.

    The 6 component strategies:
    1. ai_revolution — Broad AI theme (GPUs, cloud, AI apps)
    2. ai_token_economy — NVDA compute demand proxy
    3. anthropic_ecosystem — Anthropic supply chain + investors
    4. openai_ecosystem — Microsoft/Stargate-centric
    5. ai_infra_picks_shovels — Arms dealers, win regardless
    6. open_source_ai_ecosystem — HuggingFace/Mistral/Llama

    Conviction weighting: Tickers appearing in more sub-strategies get higher
    base weight (6/6 = 3x, 5/6 = 2.5x, 4/6 = 2x, 3/6 = 1.5x, 1-2/6 = 1x).

    Signal logic:
    - Apply conviction weights as base
    - Momentum tilt: above SMA50 = full weight, below SMA50 = half weight
    - Risk-off: if SPY RSI > 75, reduce all to 60%
    - Monthly rebalance

    ## Passive Investor Section
    For buy-and-hold investors who want maximum AI diversification without active
    management: equal-weight the top-conviction names NVDA, AVGO, ANET, EQIX,
    VRT, AMD, TSM, ASML. These 8 names span GPU monopoly, networking, data
    centers, cooling, and fabrication -- the entire AI infrastructure stack.
    Rebalance quarterly. This is the "own the whole AI economy" passive play.
    """

    # Conviction multipliers based on how many of the 6 strategies each ticker appears in
    CONVICTION = {
        # 6/6 highest conviction
        "NVDA": 3.0, "AVGO": 3.0,
        # 5/6
        "ANET": 2.5, "EQIX": 2.5, "VRT": 2.5, "AMD": 2.5,
        # 4/6
        "CEG": 2.0, "VST": 2.0, "ASML": 2.0, "TSM": 2.0, "MU": 2.0,
        # 3/6
        "DLR": 1.5, "MRVL": 1.5, "CRM": 1.5, "MSFT": 1.5,
        "AMZN": 1.5, "SNOW": 1.5, "GOOGL": 1.5,
        # 1-2/6 (all others default to 1.0)
    }

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="AI Mega Ecosystem",
            description="All 41 AI tickers conviction-weighted: 6 strategies combined into one diversified mega-portfolio",
            risk_tolerance=0.7,
            max_position_size=0.08,
            max_positions=41,
            rebalance_frequency="monthly",
            universe=universe or [
                # 6/6 conviction (highest)
                "NVDA", "AVGO",
                # 5/6 conviction
                "ANET", "EQIX", "VRT", "AMD",
                # 4/6 conviction
                "CEG", "VST", "ASML", "TSM", "MU",
                # 3/6 conviction
                "DLR", "MRVL", "CRM", "MSFT", "AMZN", "SNOW", "GOOGL",
                # 1-2/6 conviction
                "ACN", "ADBE", "AI", "AMAT", "ARM", "CLS", "DELL",
                "ETN", "GTLB", "HPE", "IBM", "INTC", "LRCX", "META",
                "NOW", "NRG", "ORCL", "PATH", "PLTR", "QCOM", "SMCI",
                "SMH", "SOXX",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # --- Risk-off filter: SPY RSI > 75 -> reduce to 60% ---
        risk_off_mult = 1.0
        if "SPY" in data:
            spy_rsi = self._get_indicator(data, "SPY", "rsi_14", date)
            if not _is_missing(spy_rsi) and spy_rsi > 75:
                risk_off_mult = 0.6

        # --- Score each ticker ---
        qualified = []  # (sym, weight_mult)

        for sym in self.config.universe:
            if sym not in data or sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym, ["sma_50", "sma_200", "rsi_14"], date
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]

            if _is_missing(sma50):
                continue

            # Skip extremely overbought individual names
            if not _is_missing(rsi) and rsi > 80:
                weights[sym] = 0.0
                continue

            # Skip broken trends (>25% below SMA200)
            if not _is_missing(sma200) and sma200 > 0 and price < sma200 * 0.75:
                weights[sym] = 0.0
                continue

            # Conviction weight from sub-strategy overlap count
            conviction_mult = self.CONVICTION.get(sym, 1.0)

            # Momentum tilt: above SMA50 = full weight, below = half
            if price > sma50:
                momentum_mult = 1.0
            else:
                momentum_mult = 0.5

            qualified.append((sym, conviction_mult * momentum_mult))

        # --- Distribute weights proportionally ---
        total_units = sum(mult for _, mult in qualified)
        if total_units > 0:
            base = 0.90 / total_units
            for sym, mult in qualified:
                w = base * mult * risk_off_mult
                weights[sym] = min(w, self.config.max_position_size)

        # Zero out anything not qualified
        for sym in self.config.universe:
            if sym not in weights and sym in prices:
                weights[sym] = 0.0

        return weights


# ---------------------------------------------------------------------------
# Genomics Revolution (ARK ARKG thesis)
# ---------------------------------------------------------------------------
class GenomicsRevolution(BasePersona):
    """Gene editing, synthetic biology, and molecular diagnostics megatrend.

    Source: ARK Invest ARKG thesis -- genomics is a convergence of DNA
    sequencing cost decline, CRISPR gene editing, and AI-driven drug
    discovery.  This is the biggest gap in the portfolio (zero genomics
    coverage until now).

    Universe:
    - Core gene editing: CRSP, BEAM, NTLA, EDIT
    - Synthetic biology / multi-omics: TWST, TXG, TEM
    - Diagnostics & tools: ILMN, A, TMO
    - ETF proxy: ARKG

    Signal logic:
    - Equal weight across genomics names
    - Momentum tilt: above SMA50 = full weight, below = half
    - Core names (CRSP, BEAM, ILMN) get 1.5x weight (highest conviction)
    - Monthly rebalance

    ## Passive Investor Section
    For buy-and-hold investors: equal-weight CRSP, BEAM, ILMN, TMO, TWST.
    These five span gene editing leaders, sequencing monopoly, and tools.
    Or simply buy ARKG for managed genomics exposure. Rebalance quarterly.
    """

    CORE_NAMES = {"CRSP", "BEAM", "ILMN"}

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Genomics Revolution",
            description="Gene editing, synthetic biology, molecular diagnostics (ARK ARKG thesis)",
            risk_tolerance=0.8,
            max_position_size=0.15,
            max_positions=11,
            rebalance_frequency="monthly",
            universe=universe or [
                "CRSP", "BEAM", "NTLA", "EDIT",      # Gene editing
                "TWST", "TXG", "TEM",                 # Synthetic bio / multi-omics
                "ILMN", "A", "TMO",                   # Diagnostics & tools
                "ARKG",                                # ETF proxy
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        qualified = []  # (sym, weight_multiplier)

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym, ["sma_50", "sma_200", "rsi_14"], date
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]

            # Skip if no SMA data at all (ticker too new)
            if _is_missing(sma50):
                # Still include with reduced weight for new tickers
                qualified.append((sym, 0.5))
                continue

            # Overbought filter
            if not _is_missing(rsi) and rsi > 80:
                weights[sym] = 0.0
                continue

            # Broken trend filter (>30% below SMA200 -- biotech is volatile)
            if not _is_missing(sma200) and sma200 > 0 and price < sma200 * 0.70:
                weights[sym] = 0.0
                continue

            # Conviction weight: core names get 1.5x
            conviction = 1.5 if sym in self.CORE_NAMES else 1.0

            # Momentum tilt: above SMA50 = full, below = half
            if price > sma50:
                momentum = 1.0
            else:
                momentum = 0.5

            qualified.append((sym, conviction * momentum))

        # Distribute weights proportionally
        total_units = sum(mult for _, mult in qualified)
        if total_units > 0:
            base = 0.90 / total_units
            for sym, mult in qualified:
                w = base * mult
                weights[sym] = min(w, self.config.max_position_size)

        # Zero out unqualified
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)

        return weights


# ---------------------------------------------------------------------------
# Humanoid Robotics Supply Chain (KraneShares KOID thesis)
# ---------------------------------------------------------------------------
class HumanoidRoboticsSupplyChain(BasePersona):
    """Humanoid robotics value chain: brain + body + integrator stack.

    Source: KraneShares KOID ETF thesis -- humanoid robots require three
    layers: Brain (AI compute, sensors), Body (actuators, connectors,
    motors), and Integrators (companies assembling complete systems).

    Universe:
    - Brain (AI/sensors): NVDA, MBLY, ADI, TER
    - Body (actuators/connectors): APH, TEL, JBL, RRX
    - Integrators: ISRG, ROK, ABB
    - ETF proxies: BOTZ

    Signal logic:
    - Brain tier: 1.5x weight (AI compute is the bottleneck)
    - Body tier: 1.0x weight
    - Integrators: 1.25x weight
    - Momentum tilt: above SMA50 = full, below = half
    - Monthly rebalance

    ## Passive Investor Section
    For buy-and-hold investors: equal-weight NVDA, ISRG, APH, ROK, ADI.
    These five span the compute brain, surgical precision integrator,
    connectivity backbone, industrial automation, and analog sensing.
    Or buy BOTZ for managed robotics exposure. Rebalance quarterly.
    """

    TIER_WEIGHTS = {
        # Brain tier: 1.5x (AI compute is the bottleneck)
        "NVDA": 1.5, "MBLY": 1.5, "ADI": 1.5, "TER": 1.5,
        # Integrators: 1.25x
        "ISRG": 1.25, "ROK": 1.25, "ABB": 1.25,
        # Body tier: 1.0x
        "APH": 1.0, "TEL": 1.0, "JBL": 1.0, "RRX": 1.0,
        # ETF proxies: 1.0x
        "BOTZ": 1.0,
    }

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Humanoid Robotics Supply Chain",
            description="Brain + body + integrator robotics stack (KraneShares KOID thesis)",
            risk_tolerance=0.7,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                "NVDA", "MBLY", "ADI", "TER",      # Brain (AI/sensors)
                "APH", "TEL", "JBL", "RRX",         # Body (actuators/connectors)
                "ISRG", "ROK", "ABB",                # Integrators
                "BOTZ",                               # ETF proxy
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        qualified = []  # (sym, weight_multiplier)

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym, ["sma_50", "sma_200", "rsi_14"], date
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]

            # Fallback for tickers with short history
            if _is_missing(sma50):
                tier_wt = self.TIER_WEIGHTS.get(sym, 1.0)
                qualified.append((sym, tier_wt * 0.5))
                continue

            # Overbought filter
            if not _is_missing(rsi) and rsi > 80:
                weights[sym] = 0.0
                continue

            # Broken trend: >25% below SMA200
            if not _is_missing(sma200) and sma200 > 0 and price < sma200 * 0.75:
                weights[sym] = 0.0
                continue

            # Tier-based conviction weight
            tier_wt = self.TIER_WEIGHTS.get(sym, 1.0)

            # Momentum tilt: above SMA50 = full, below = half
            if price > sma50:
                momentum = 1.0
            else:
                momentum = 0.5

            qualified.append((sym, tier_wt * momentum))

        # Distribute weights proportionally
        total_units = sum(mult for _, mult in qualified)
        if total_units > 0:
            base = 0.90 / total_units
            for sym, mult in qualified:
                w = base * mult
                weights[sym] = min(w, self.config.max_position_size)

        # Zero out unqualified
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)

        return weights


THEME_STRATEGIES = {
    "ai_revolution": AIRevolution,
    "clean_energy": CleanEnergy,
    "defense_aerospace": DefenseAerospace,
    "biotech_breakout": BiotechBreakout,
    "china_tech_rebound": ChinaTechRebound,
    "latam_growth": LatAmGrowth,
    "infrastructure_boom": InfrastructureBoom,
    "small_cap_value": SmallCapValue,
    "crypto_ecosystem": CryptoEcosystem,
    "aging_population": AgingPopulation,
    "glp1_obesity": GLP1Obesity,
    "robotics_autonomous": RoboticsAutonomous,
    "semiconductor_value": SemiconductorValue,
    "subscription_monopoly": SubscriptionMonopoly,
    "contrastive_pairs": ContrastivePairs,
    "global_financial_infra": GlobalFinancialInfra,
    "reshoring_industrial": ReshoringIndustrial,
    "water_monopoly": WaterMonopoly,
    "regulated_data": RegulatedData,
    "china_adr_deep_value": ChinaADRDeepValue,
    "cloud_cyber_value": CloudCyberValue,
    "global_airlines_travel": GlobalAirlinesTravel,
    "utility_infra_income": UtilityInfraIncome,
    "japan_industrial_finance": JapanIndustrialFinance,
    "defense_prime_contractors": DefensePrimeContractors,
    "global_consumer_staples": GlobalConsumerStaples,
    "emerging_market_etf_value": EmergingMarketETFValue,
    "global_pharma_pipeline": GlobalPharmaPipeline,
    "singapore_alpha": SingaporeAlpha,
    "uk_european_banking": UKEuropeanBanking,
    "telecom_equipment_5g": TelecomEquipment5G,
    "gig_economy_saas": GigEconomySaaSDisruptors,
    "korean_chaebols": KoreanChaebols,
    "rideshare_mobility": RideshareMobility,
    "nvidia_supply_chain": NvidiaSupplyChain,
    "mag7_hidden_suppliers": Mag7HiddenSuppliers,
    "mag7_domino_hedge": Mag7DominoHedge,
    # Tech boom cycle strategies (historical pattern)
    "ai_infrastructure_layer": AIInfrastructureLayer,
    "ai_application_survivors": AIApplicationSurvivors,
    "ai_adopters_not_builders": AIAdoptersNotBuilders,
    "late_cycle_bubble_hedge": LateCycleBubbleHedge,
    "picks_and_shovels_ai": PicksAndShovelsAI,
    # Regional & thematic growth
    "esg_momentum": ESGMomentum,
    "africa_frontier": AfricaFrontier,
    "southeast_asia_growth": SoutheastAsiaGrowth,
    # Infrastructure spending
    "infrastructure_reshoring": InfrastructureReshoring,
    # AI ecosystem plays (research-backed)
    "anthropic_ecosystem": AnthropicEcosystem,
    "openai_ecosystem": OpenAIEcosystem,
    "ai_infra_picks_shovels": AIInfraPicksShovels,
    "open_source_ai_ecosystem": OpenSourceAIEcosystem,
    "ai_mega_ecosystem": AIMegaEcosystem,
    # CICC / KraneShares / ARK research-backed (2026-04-13)
    "genomics_revolution": GenomicsRevolution,
    "humanoid_robotics_supply_chain": HumanoidRoboticsSupplyChain,
}


def get_theme_strategy(name: str, **kwargs) -> BasePersona:
    cls = THEME_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown theme: {name}. Available: {list(THEME_STRATEGIES.keys())}")
    return cls(**kwargs)


def list_theme_strategies():
    result = []
    for key, cls in THEME_STRATEGIES.items():
        instance = cls()
        result.append({
            "key": key,
            "name": instance.config.name,
            "description": instance.config.description,
        })
    return result


if __name__ == "__main__":
    print("=== Theme-Based Strategies ===\n")
    for p in list_theme_strategies():
        print(f"  {p['key']:25s} | {p['name']:30s} | {p['description']}")
