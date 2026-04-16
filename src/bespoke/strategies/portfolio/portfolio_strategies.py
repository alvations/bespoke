"""Combined portfolio strategies with hedging for agents-assemble.

These are PORTFOLIO-LEVEL strategies that combine multiple asset classes
(equities, bonds, commodities, defensive sectors) with explicit hedging.

Strategies:
    1. StaplesHedgedGrowth          — Growth core + staples/dividend hedge
    2. BarbellPortfolio             — Short-duration bonds + long-duration bonds + equities
    3. AllWeatherModern             — Updated Dalio All-Weather with 2026 adjustments
    4. AdaptiveEnsemble             — Regime-aware ensemble that shifts between strategies
    5. CoreSatellite                — 60% passive core + 40% active satellite
    6. IncomeShield                 — High-dividend stocks + bond income for downside protection
    7. BondFixedIncome              — Diversified bond and fixed income portfolio
    8. HighYieldREITBDCIncome       — High-yield REIT, BDC & Real Estate Income
    9. DividendAristocratBlueChips  — Dividend aristocrat blue chip income
   10. BuffettHODL                  — Buffett buy-and-hold forever (wide moat, never sell)
   11. BogleThreeFund               — Bogleheads Three-Fund passive baseline
   12. PermanentPortfolio           — Harry Browne 25/25/25/25 all-weather
   13. DividendGrowthCompounding    — Dividend growth + DRIP compounding
   14. MagicFormula                 — Greenblatt magic formula (earnings yield + ROIC)
   15. EqualWeightSP500             — Equal weight S&P 500 top holdings
   16. AllWeatherPassive            — Ray Dalio All Weather (simplified passive)
   17. QualityDividendAristocrats   — Quality factor + Dividend Aristocrats
   18. BondDurationTrade            — Yield curve steepening/flattening trade
   19. CreditSpreadTrade            — High yield vs investment grade rotation
   20. CoveredCallIncome            — Covered call ETF income with VIX overlay
   21. DualMomentumGlobal           — Antonacci dual momentum: SPY vs EFA vs AGG
   22. PreferredEquityIncome        — Preferred stock ETFs with rate sensitivity
   23. TaxHarvestRotation           — Tax-loss harvesting via correlated ETF swaps
   24. SelfStorageREIT              — Counter-cyclical self-storage REITs (PSA, EXR, CUBE)
   25. ClosedEndFundDiscount        — CEF discount arbitrage (PDI, PTY, UTF, UTG, GOF)
   26. CanadianAristocratIncome     — Canadian dividend aristocrats (ENB, TRP, FTS, BNS)
   27. PreIPOInnovationFunds        — Private company exposure via AGIX, BSTZ, DXYZ, ARKK, ARKW
"""

from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np

from bespoke.strategies.base import BaseStrategy as BasePersona, StrategyConfig as PersonaConfig


def _is_missing(v) -> bool:
    """Check if indicator value is None or NaN (nearest-date path can leak NaN)."""
    return v is None or v != v


# ---------------------------------------------------------------------------
# 1. Staples-Hedged Growth
# ---------------------------------------------------------------------------
class StaplesHedgedGrowth(BasePersona):
    """Growth stocks hedged with consumer staples and dividends.

    Core: 60% in momentum/growth (top tech)
    Hedge: 25% in staples (XLP, PG, KO, WMT) — low beta, steady income
    Buffer: 15% in gold/bonds — crisis protection

    When growth is strong (SMA50>SMA200 on SPY): full growth allocation.
    When growth weakens: shift to 40% staples, 30% bonds/gold.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Staples-Hedged Growth",
            description="Growth core + consumer staples/dividend hedge + gold/bond buffer",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or [
                # Growth core
                "NVDA", "MSFT", "AAPL", "GOOGL", "AMZN", "META",
                # Staples hedge
                "XLP", "PG", "KO", "WMT", "COST", "PEP",
                # Bond/gold buffer
                "TLT", "GLD", "SHY",
                # SPY for regime detection
                "SPY",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        # Detect growth regime via SPY
        spy_sma50 = self._get_indicator(data, "SPY", "sma_50", date)
        spy_sma200 = self._get_indicator(data, "SPY", "sma_200", date)
        spy_price = prices.get("SPY")

        growth_mode = True
        if spy_sma50 and spy_sma200 and spy_price:
            if spy_price < spy_sma200 or spy_sma50 < spy_sma200:
                growth_mode = False

        weights = {}
        growth = ["NVDA", "MSFT", "AAPL", "GOOGL", "AMZN", "META"]
        staples = ["XLP", "PG", "KO", "WMT", "COST", "PEP"]
        safe = ["TLT", "GLD", "SHY"]

        if growth_mode:
            # Risk-on: 60% growth, 25% staples, 15% buffer
            for sym in growth:
                if sym in prices:
                    rsi = self._get_indicator(data, sym, "rsi_14", date)
                    sma50 = self._get_indicator(data, sym, "sma_50", date)
                    if sma50 and prices[sym] > sma50 and (rsi is None or rsi < 75):
                        weights[sym] = 0.10
            for sym in staples:
                if sym in prices:
                    weights[sym] = 0.04
            weights["GLD"] = 0.05
            weights["SHY"] = 0.05
        else:
            # Risk-off: 20% growth, 40% staples, 30% safe, 10% cash
            for sym in growth[:3]:
                if sym in prices:
                    weights[sym] = 0.07
            for sym in staples:
                if sym in prices:
                    weights[sym] = 0.07
            weights["TLT"] = 0.12
            weights["GLD"] = 0.10
            weights["SHY"] = 0.08

        return {k: v for k, v in weights.items() if k in prices and k != "SPY"}


# ---------------------------------------------------------------------------
# 2. Barbell Portfolio
# ---------------------------------------------------------------------------
class BarbellPortfolio(BasePersona):
    """Barbell strategy: short-duration + long-duration + equities.

    Source: BlackRock barbell positioning for volatility.

    Barbell: concentrate in extremes, avoid the middle.
    - Short-duration bonds (SHY): stability, low vol
    - Long-duration bonds (TLT): convexity, crisis protection
    - High-growth equities: maximum upside

    Skip intermediate bonds — they have worst risk/reward.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Barbell Portfolio",
            description="Short bonds + long bonds + growth equities — skip the middle",
            risk_tolerance=0.5,
            max_position_size=0.25,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "SHY", "TLT",  # Bond barbell
                "NVDA", "MSFT", "GOOGL", "AMZN",  # Growth equities
                "GLD",  # Gold alternative
                "SPY",  # Regime detection
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)
        ann_vol = spy_vol * (252 ** 0.5) if spy_vol else 0.15

        if ann_vol > 0.25:
            # High vol: heavy bonds + gold
            return {"SHY": 0.30, "TLT": 0.25, "GLD": 0.20,
                    "NVDA": 0.05, "MSFT": 0.05}
        elif ann_vol < 0.12:
            # Low vol: heavy equities
            return {"NVDA": 0.20, "MSFT": 0.15, "GOOGL": 0.15, "AMZN": 0.15,
                    "SHY": 0.10, "TLT": 0.10, "GLD": 0.05}
        else:
            # Normal: balanced barbell
            return {"SHY": 0.20, "TLT": 0.15, "GLD": 0.10,
                    "NVDA": 0.15, "MSFT": 0.10, "GOOGL": 0.10, "AMZN": 0.10}


# ---------------------------------------------------------------------------
# 3. All-Weather Modern (2026 update)
# ---------------------------------------------------------------------------
class AllWeatherModern(BasePersona):
    """Updated All-Weather portfolio for 2026 environment.

    Classic Dalio: 30% stocks, 40% long bonds, 15% intermediate, 7.5% gold, 7.5% commodities.

    2026 adjustments:
    - Reduce long bonds (TLT) — rate uncertainty
    - Add TIPS for inflation protection
    - Add crypto-adjacent for diversification
    - Use momentum tilt within each sleeve
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="All-Weather Modern (2026)",
            description="Updated Dalio All-Weather: reduced bonds, added TIPS + crypto exposure",
            risk_tolerance=0.3,
            max_position_size=0.25,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "VTI", "VEA",  # Stocks (US + intl)
                "TLT", "IEF", "TIP", "SHY",  # Bonds (duration ladder + TIPS)
                "GLD",  # Gold
                "XLE",  # Commodities proxy
                "COIN",  # Crypto proxy (small allocation)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        # Risk parity: weight by inverse vol
        vols = {}
        for sym in self.config.universe:
            if sym not in prices:
                continue
            vol = self._get_indicator(data, sym, "vol_20", date)
            if vol and vol > 0:
                vols[sym] = vol

        if not vols:
            return {"VTI": 0.25, "TLT": 0.20, "IEF": 0.15, "GLD": 0.10, "TIP": 0.10, "SHY": 0.10}

        # Detect rate-hike regime: TLT trending down (10Y yield rising)
        tlt_sma50 = self._get_indicator(data, "TLT", "sma_50", date)
        tlt_sma200 = self._get_indicator(data, "TLT", "sma_200", date)
        tlt_price = prices.get("TLT")
        rate_hike_regime = (
            tlt_price is not None and tlt_sma50 is not None and tlt_sma200 is not None
            and tlt_price < tlt_sma50 < tlt_sma200
        )

        # Momentum filter: only include assets above SMA50
        filtered = {}
        for sym, vol in vols.items():
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            price = prices[sym]
            if sma50 and price > sma50:
                filtered[sym] = vol
            elif sym in ("SHY", "TIP"):
                filtered[sym] = vol  # Always include short bonds + TIPS
            elif sym == "GLD" and rate_hike_regime:
                filtered[sym] = vol  # Gold as bond substitute in rate hikes

        if not filtered:
            filtered = vols

        # In rate-hike regime, boost gold/SHY/TIP and reduce TLT
        if rate_hike_regime:
            # Override: reduce long bond exposure, boost alternatives
            if "TLT" in filtered:
                filtered["TLT"] = filtered["TLT"] * 3  # Higher vol = lower weight
            if "GLD" in vols and "GLD" not in filtered:
                filtered["GLD"] = vols["GLD"]

        total_inv = sum(1/v for v in filtered.values())
        if total_inv <= 0:
            return {"VTI": 0.25, "GLD": 0.15, "SHY": 0.20, "TIP": 0.15, "IEF": 0.10}
        for sym, vol in filtered.items():
            w = (1/vol) / total_inv * 0.90
            weights[sym] = min(w, self.config.max_position_size)

        return weights


# ---------------------------------------------------------------------------
# 4. Adaptive Ensemble
# ---------------------------------------------------------------------------
class AdaptiveEnsemble(BasePersona):
    """Regime-aware ensemble that shifts between strategy types.

    Bull (SPY > SMA200, vol low): 70% momentum, 20% growth, 10% bonds
    Bear (SPY < SMA200, vol high): 20% defensive, 40% bonds, 30% gold, 10% staples
    Transition: 40% quality, 30% dividend, 20% bonds, 10% gold

    This is a META-strategy that allocates between asset classes
    based on market regime, not individual stock signals.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Adaptive Ensemble",
            description="Regime-switching: momentum in bulls, defensive in bears, quality in transitions",
            risk_tolerance=0.5,
            max_position_size=0.20,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                # Momentum/growth sleeve
                "QQQ", "NVDA", "MSFT", "AMZN",
                # Defensive/staples sleeve
                "XLP", "XLV", "XLU",
                # Dividend/quality sleeve
                "VIG", "SCHD", "DVY",
                # Bonds
                "TLT", "IEF", "SHY",
                # Gold
                "GLD",
                # Regime detection
                "SPY",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        spy_sma200 = self._get_indicator(data, "SPY", "sma_200", date)
        spy_sma50 = self._get_indicator(data, "SPY", "sma_50", date)
        spy_price = prices.get("SPY")
        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)
        spy_rsi = self._get_indicator(data, "SPY", "rsi_14", date)

        # Determine regime
        if spy_sma200 and spy_price and spy_sma50:
            ann_vol = spy_vol * (252 ** 0.5) if spy_vol else 0.15
            if spy_price > spy_sma50 > spy_sma200 and ann_vol < 0.20:
                regime = "bull"
            elif spy_price < spy_sma200 or ann_vol > 0.28:
                regime = "bear"
            else:
                regime = "transition"
        else:
            regime = "transition"

        if regime == "bull":
            return {
                "QQQ": 0.25, "NVDA": 0.15, "MSFT": 0.15, "AMZN": 0.15,
                "VIG": 0.10, "GLD": 0.05, "SHY": 0.05,
            }
        elif regime == "bear":
            return {
                "TLT": 0.20, "IEF": 0.15, "SHY": 0.10,
                "GLD": 0.20,
                "XLP": 0.10, "XLV": 0.10, "XLU": 0.05,
                "QQQ": 0.0, "NVDA": 0.0,
            }
        else:  # transition
            return {
                "VIG": 0.15, "SCHD": 0.10, "DVY": 0.05,
                "XLP": 0.10, "XLV": 0.10,
                "TLT": 0.10, "IEF": 0.10,
                "GLD": 0.10,
                "QQQ": 0.10,
            }

    def _filter_tradeable(self, weights, prices):
        return {k: v for k, v in weights.items() if k in prices and k != "SPY"}


# ---------------------------------------------------------------------------
# 5. Core-Satellite Portfolio
# ---------------------------------------------------------------------------
class CoreSatellite(BasePersona):
    """60% passive core + 40% active satellite.

    Core (60%): SPY/VTI + BND/AGG — boring, cheap, always-on
    Satellite (40%): Momentum + thematic + contrarian — active alpha

    Satellite changes based on momentum signals.
    Core stays constant.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Core-Satellite Portfolio",
            description="60% passive core (SPY+BND) + 40% active satellite (momentum+themes)",
            risk_tolerance=0.4,
            max_position_size=0.30,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "SPY", "BND",  # Core
                "NVDA", "AVGO", "LLY", "PLTR", "AMZN", "MSFT",  # Satellite: momentum
                "GLD", "XLE",  # Satellite: alternatives
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        # Core: always on
        weights["SPY"] = 0.40
        weights["BND"] = 0.20

        # Satellite: momentum-filtered
        satellite_candidates = []
        for sym in ["NVDA", "AVGO", "LLY", "PLTR", "GLD", "XLE"]:
            if sym not in prices:
                continue
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            price = prices[sym]
            if sma50 and price > sma50 and (rsi is None or rsi < 75):
                satellite_candidates.append(sym)

        if satellite_candidates:
            per_sat = 0.35 / len(satellite_candidates)
            for sym in satellite_candidates:
                weights[sym] = min(per_sat, 0.12)
        else:
            weights["GLD"] = 0.20
            weights["SPY"] = 0.50  # Increase core if no satellites

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 6. Income Shield
# ---------------------------------------------------------------------------
class IncomeShield(BasePersona):
    """High-dividend equities + bond income for downside protection.

    Combines dividend aristocrats, high-yield bond ETFs, and REITs
    for maximum income generation with lower drawdowns.

    Target: 4-5% yield, max drawdown < 15%.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Income Shield",
            description="High-dividend + bond income: 4-5% yield target, low drawdown",
            risk_tolerance=0.2,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                # High-dividend stocks
                "VIG", "SCHD", "DVY", "HDV",
                # Dividend aristocrats
                "JNJ", "PG", "KO", "ABBV", "XOM", "CVX", "MMM",
                # Bond income
                "BND", "LQD", "HYG", "TIP",
                # REITs
                "VNQ", "O",
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
            # Income: buy near or below SMA200, hold steady
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            if discount > -0.10:
                score = max(discount + 0.10, 0.01) + 0.3
                if rsi and rsi < 45:
                    score += 0.1
                candidates.append((sym, score))

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 7. Bond & Fixed Income Portfolio
# ---------------------------------------------------------------------------
class BondFixedIncome(BasePersona):
    """Diversified bond and fixed income portfolio.

    Thesis: Bonds provide income, diversification, and crisis protection.
    Allocate across duration ladder (short to long), credit spectrum
    (investment grade to high yield), and geography (US + EM).
    Shift duration based on volatility regime.

    Target: 3-5% yield, max drawdown < 8%.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Bond & Fixed Income Portfolio",
            description="Diversified bonds: duration ladder + credit spectrum + EM, 3-5% yield target",
            risk_tolerance=0.15,
            max_position_size=0.20,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "FBND", "SPBO",  # Core bond / corporate
                "SCHI",  # Intermediate corporate
                "VWOB",  # EM sovereign bonds
                "VTEB",  # Tax-exempt munis
                "AGG", "BND",  # Broad US aggregate
                "TLT",  # Long-duration treasuries
                "HYG",  # High yield corporate
                "LQD",  # Investment grade corporate
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Use AGG volatility as regime indicator
        agg_vol = self._get_indicator(data, "AGG", "vol_20", date)
        agg_rsi = self._get_indicator(data, "AGG", "rsi_14", date)

        if agg_vol is not None:
            ann_vol = agg_vol * (252 ** 0.5)
        else:
            ann_vol = 0.05  # Default bond vol assumption

        if ann_vol > 0.10:
            # High bond vol: shorten duration, reduce credit risk
            # Overweight short-duration and high-quality
            weights["FBND"] = 0.15
            weights["SPBO"] = 0.10
            weights["SCHI"] = 0.10
            weights["AGG"] = 0.15
            weights["BND"] = 0.15
            weights["VTEB"] = 0.10
            weights["TLT"] = 0.05  # Reduce long duration
            weights["HYG"] = 0.05  # Reduce credit risk
            weights["LQD"] = 0.10
            weights["VWOB"] = 0.05  # Reduce EM exposure
        elif ann_vol < 0.04:
            # Very low vol: extend duration for yield, add credit
            weights["TLT"] = 0.15
            weights["HYG"] = 0.12
            weights["LQD"] = 0.15
            weights["VWOB"] = 0.12
            weights["SCHI"] = 0.10
            weights["VTEB"] = 0.10
            weights["AGG"] = 0.08
            weights["BND"] = 0.08
            weights["FBND"] = 0.05
            weights["SPBO"] = 0.05
        else:
            # Normal vol: balanced allocation
            weights["AGG"] = 0.12
            weights["BND"] = 0.12
            weights["LQD"] = 0.12
            weights["FBND"] = 0.10
            weights["SCHI"] = 0.10
            weights["VTEB"] = 0.10
            weights["TLT"] = 0.10
            weights["VWOB"] = 0.08
            weights["HYG"] = 0.08
            weights["SPBO"] = 0.08

        # Oversold bonds = accumulate (income strategy always buys dips)
        if agg_rsi is not None and agg_rsi < 30:
            # Boost allocation across the board on bond selloff
            for sym in weights:
                weights[sym] = min(weights[sym] * 1.1, self.config.max_position_size)

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 8. High-Yield REIT, BDC & Real Estate Income
# ---------------------------------------------------------------------------
class HighYieldREITBDCIncome(BasePersona):
    """High-yield REIT, BDC, and real estate income strategy.

    Thesis: REITs and BDCs provide 6-12% dividend yields with monthly
    or quarterly distributions. Realty Income (O) is the "Monthly
    Dividend Company" with 30+ years of increases. AGNC and NLY are
    agency mortgage REITs yielding 12-15% (interest rate sensitive).
    MAIN and HTGC are BDCs lending to middle-market companies at 10%+
    yields. ARCC (Ares Capital) is the largest BDC by AUM.
    STAG Industrial is a logistics/e-commerce REIT beneficiary.
    Zillow and Redfin provide real estate tech exposure as a growth
    kicker alongside the income core.

    Target: 6-8% yield portfolio, max drawdown < 20%.

    Signal: Income-oriented. Buy on dips below SMA200 for yield
    accumulation. Hold in uptrend for total return. Trim overbought.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="High-Yield REIT, BDC & Real Estate",
            description="REITs + BDCs + RE tech: 6-8% yield, monthly income, dip accumulation",
            risk_tolerance=0.3,
            max_position_size=0.10,
            max_positions=14,
            rebalance_frequency="monthly",
            universe=universe or [
                # Equity REITs
                "O",      # Realty Income (monthly dividend, net lease)
                "STAG",   # STAG Industrial (logistics / e-commerce REIT)
                # Mortgage REITs (high yield, rate sensitive)
                "AGNC",   # AGNC Investment (agency MBS, 12-15% yield)
                "ARR",    # ARMOUR Residential (agency MBS REIT)
                "NLY",    # Annaly Capital (largest mortgage REIT)
                "DX",     # Dynex Capital (agency + non-agency MBS)
                # BDCs (Business Development Companies)
                "MAIN",   # Main Street Capital (premium BDC, internal)
                "HTGC",   # Horizon Technology Finance (venture lending)
                "ARCC",   # Ares Capital (largest BDC by AUM)
                # Real Estate Tech (growth kicker)
                "Z",      # Zillow Group (RE marketplace + tech)
                "RDFN",   # Redfin (discount brokerage + tech)
                # Broad REIT exposure
                "VNQ",    # Vanguard Real Estate ETF (diversified)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        # Classify tickers by type for different allocation logic
        income_core = {"O", "STAG", "MAIN", "ARCC", "VNQ"}
        mortgage_reits = {"AGNC", "ARR", "NLY", "DX"}
        bdcs = {"HTGC"}
        growth = {"Z", "RDFN"}

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_200", "sma_50", "rsi_14"], date)
            sma200, sma50, rsi = inds["sma_200"], inds["sma_50"], inds["rsi_14"]

            if sma200 is None or (sma200 != sma200):
                continue

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            if sym in income_core:
                # Income core: always allocate, buy dips aggressively
                if discount > 0.08:
                    score = 3.0 + discount * 5
                    candidates.append((sym, score, 0.10))
                elif discount > -0.05:
                    candidates.append((sym, 2.0, 0.08))
                elif discount > -0.15:
                    candidates.append((sym, 1.0, 0.06))
                elif rsi is not None and rsi > 78:
                    weights[sym] = 0.0

            elif sym in mortgage_reits:
                # Mortgage REITs: yield-seekers, very rate sensitive
                # Buy on oversold, trim on overbought
                if rsi is not None and rsi < 35 and discount > 0:
                    candidates.append((sym, 2.5 + discount * 3, 0.08))
                elif rsi is not None and rsi < 50 and discount > -0.05:
                    candidates.append((sym, 1.5, 0.06))
                elif rsi is not None and rsi > 75:
                    weights[sym] = 0.0
                else:
                    candidates.append((sym, 1.0, 0.05))

            elif sym in bdcs:
                # BDCs: steady income, accumulate on dips
                if discount > 0.05:
                    candidates.append((sym, 2.5, 0.08))
                elif discount > -0.10:
                    candidates.append((sym, 1.5, 0.06))
                elif rsi is not None and rsi > 75:
                    weights[sym] = 0.0

            elif sym in growth:
                # RE tech: momentum-driven growth kicker
                if sma50 is not None and price > sma50 and (rsi is None or rsi < 75):
                    score = 1.5
                    if sma200 is not None and price > sma50 > sma200:
                        score = 2.5
                    candidates.append((sym, score, 0.06))
                elif rsi is not None and rsi > 78:
                    weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        for sym, _, wt in top:
            weights[sym] = min(wt, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 9. Dividend Aristocrat Blue Chips
# ---------------------------------------------------------------------------
class DividendAristocratBlueChips(BasePersona):
    """Dividend aristocrat blue chip income portfolio.

    Thesis: Dividend aristocrats have raised dividends 25+ consecutive
    years — proof of business quality and capital discipline. Altria (MO)
    yields 8%+ with pricing power. Philip Morris (PM) is the global
    tobacco leader with IQOS growth. 3M (MMM) is restructuring post-
    litigation. UPS/FDX are logistics duopoly. JNJ is the healthcare
    conglomerate gold standard. Enbridge (ENB) is North America's
    largest pipeline operator (6%+ yield). ABBV (AbbVie) has the best
    pharma pipeline. XOM generates $50B+ operating cash flow.
    SCHD ETF provides diversified dividend exposure.

    Signal: Income accumulation. Buy on dips below SMA200 (yield
    pickup). Inverse volatility weighting for stability. Trim
    overbought to lock in capital gains.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Dividend Aristocrat Blue Chips",
            description="25+ year dividend growers: 4-8% yield, income + capital appreciation",
            risk_tolerance=0.2,
            max_position_size=0.10,
            max_positions=14,
            rebalance_frequency="monthly",
            universe=universe or [
                "MO",     # Altria (8%+ yield, pricing power)
                "PM",     # Philip Morris International (IQOS growth + 5% yield)
                "MMM",    # 3M (restructuring, 65yr dividend streak)
                "UPS",    # UPS (logistics duopoly, 4%+ yield)
                "FDX",    # FedEx (logistics duopoly, restructuring)
                "KHC",    # Kraft Heinz (consumer staples, 4%+ yield)
                "JNJ",    # Johnson & Johnson (healthcare gold standard)
                "PG",     # Procter & Gamble (69yr dividend streak)
                "KO",     # Coca-Cola (62yr dividend streak)
                "PEP",    # PepsiCo (52yr dividend streak)
                "ENB",    # Enbridge (pipeline, 6%+ yield)
                "ABBV",   # AbbVie (pharma pipeline + 4% yield)
                "XOM",    # Exxon Mobil (energy cash machine)
                "SCHD",   # Schwab US Dividend Equity ETF (diversified)
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
            inds = self._get_indicators(data, sym, ["sma_200", "sma_50", "rsi_14", "vol_20"], date)
            sma200, sma50, rsi, vol20 = inds["sma_200"], inds["sma_50"], inds["rsi_14"], inds["vol_20"]

            if sma200 is None or (sma200 != sma200):
                continue

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            # Income: always maintain some allocation (aristocrats are core)
            base_weight = 0.06
            score = 1.0

            # Buy dips below SMA200 (yield pickup on aristocrats)
            if discount > 0.10:
                score = 3.0 + discount * 5
                base_weight = 0.10
            elif discount > 0.03:
                score = 2.0
                base_weight = 0.08
            elif discount > -0.05:
                score = 1.5
                base_weight = 0.07
            elif discount > -0.15:
                score = 1.0
                base_weight = 0.05

            # RSI bonus for oversold aristocrats
            if rsi is not None and rsi < 35:
                score += 1.5
            elif rsi is not None and rsi < 45:
                score += 0.5

            # Overbought aristocrats: trim (not sell — they're income)
            if rsi is not None and rsi > 78 and discount < -0.15:
                base_weight = 0.03

            # Low vol bonus (stable dividend payers = more allocation)
            if vol20 is not None and vol20 < 0.015:
                score += 0.5

            candidates.append((sym, score, base_weight))

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        total_weight = sum(wt for _, _, wt in top)
        # Scale to ~95% invested
        scale = 0.95 / total_weight if total_weight > 0 else 1.0
        for sym, _, wt in top:
            scaled = min(wt * scale, self.config.max_position_size)
            weights[sym] = scaled
        return weights


# ---------------------------------------------------------------------------
# 10. Buffett Buy-and-Hold Forever (Wide Moat HODL)
# ---------------------------------------------------------------------------
class BuffettHODL(BasePersona):
    """Buffett-style buy-and-hold forever strategy.

    Research basis: Buffett's alpha comes from quality + concentration.
    "Buy wonderful companies at fair prices, not fair companies at wonderful
    prices." Wide moat companies with pricing power, high ROE, low debt.

    Universe: Berkshire Hathaway top holdings + wide-moat blue chips.
    Signal: Only buy when below intrinsic value proxy (below SMA200 or
    RSI < 45 — unloved quality). Max 15% per position.
    Exit: ONLY if price drops 40%+ below SMA200 (thesis broken, not a dip).
    Rebalance: Monthly (check entry signals), but extremely low turnover.

    Target: 12-15% CAGR over 10+ years with concentrated quality.
    Historical: Buffett achieved ~20% CAGR over 50+ years; this proxy
    targets the public equity portion of that approach.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Buffett Buy-and-Hold Forever",
            description="Wide moat companies at fair prices, NEVER sell unless thesis breaks",
            risk_tolerance=0.3,
            max_position_size=0.15,
            max_positions=13,
            rebalance_frequency="monthly",
            universe=universe or [
                "BRK-B",  # Berkshire Hathaway (the Buffett vehicle itself)
                "AAPL",   # Apple (ecosystem moat, 30% of BRK portfolio)
                "KO",     # Coca-Cola (brand moat, 62yr dividend streak)
                "AXP",    # American Express (network effect moat)
                "BAC",    # Bank of America (scale moat)
                "OXY",    # Occidental Petroleum (Buffett's energy bet)
                "CVX",    # Chevron (integrated energy moat)
                "MCO",    # Moody's (duopoly moat with S&P Global)
                "AMZN",   # Amazon (scale + network + switching cost moat)
                "V",      # Visa (payment network moat)
                "MA",     # Mastercard (payment network moat)
                "JNJ",    # Johnson & Johnson (diversified healthcare moat)
                "PG",     # Procter & Gamble (brand portfolio moat)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym, ["sma_200", "rsi_14", "sma_50"], date
            )
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            sma50 = inds["sma_50"]

            if sma200 is None:
                # No data yet — small starter position in quality names
                weights[sym] = 0.05
                continue

            # Thesis broken check: price 40%+ below SMA200 = exit
            discount_from_sma200 = (sma200 - price) / sma200 if sma200 > 0 else 0
            if discount_from_sma200 > 0.40:
                weights[sym] = 0.0  # Thesis broken — sell
                continue

            # Entry signal: buy when below intrinsic value proxy
            # Below SMA200 OR RSI < 45 (unloved quality = best entry)
            if price < sma200 or (rsi is not None and rsi < 45):
                # Aggressive buy — great entry for wide moat stock
                weights[sym] = 0.12
                # Extra conviction if both signals agree
                if price < sma200 and rsi is not None and rsi < 40:
                    weights[sym] = 0.15
            elif price < sma200 * 1.05:
                # Near fair value — standard position
                weights[sym] = 0.09
            else:
                # Above fair value — hold existing, smaller new allocation
                # Buffett: "hold forever" means don't sell, but also don't
                # chase prices above fair value with new money
                weights[sym] = 0.06

        # Normalize to ~95% invested (5% cash buffer)
        total = sum(weights.values())
        if total > 0.95:
            scale = 0.95 / total
            weights = {k: v * scale for k, v in weights.items()}

        return weights


# ---------------------------------------------------------------------------
# 11. Bogleheads Three-Fund Portfolio (Passive Baseline)
# ---------------------------------------------------------------------------
class BogleThreeFund(BasePersona):
    """Bogleheads Three-Fund Portfolio — the passive investing baseline.

    Research basis: 10.36% annualized over 10 years, beats ~90% of
    professional fund managers. Expense ratio: 0.03% blended.
    Alpha: 0.81% vs S&P 500 with beta 0.77 (lower risk).

    Composition: Total US Market + Total International + Total Bond.
    Rebalance: Annually (Bogleheads say less trading = better).
    Signal: Target allocation is fixed. Only trade to rebalance back
    to targets when drift exceeds 5% from target.

    This is the BASELINE — every other strategy should beat this.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Bogleheads Three-Fund Portfolio",
            description="VTI+VXUS+BND passive baseline — beats 90% of pros",
            risk_tolerance=0.3,
            max_position_size=0.55,
            max_positions=6,
            rebalance_frequency="monthly",  # Check monthly, but only act on drift
            universe=universe or [
                "VTI",    # Vanguard Total US Stock Market
                "VXUS",   # Vanguard Total International Stock
                "BND",    # Vanguard Total Bond Market
                # Alternatives if primary unavailable
                "VOO",    # S&P 500 (substitute for VTI)
                "VEU",    # FTSE All-World ex-US (substitute for VXUS)
                "AGG",    # iShares Core US Aggregate Bond (substitute for BND)
            ],
        )
        super().__init__(config)
        # Target allocations (classic 60/20/20 split)
        self._targets = {
            "VTI": 0.50, "VXUS": 0.20, "BND": 0.30,
            "VOO": 0.50, "VEU": 0.20, "AGG": 0.30,
        }

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Use primary ETFs if available, fallback to alternatives
        us_sym = "VTI" if "VTI" in prices else ("VOO" if "VOO" in prices else None)
        intl_sym = "VXUS" if "VXUS" in prices else ("VEU" if "VEU" in prices else None)
        bond_sym = "BND" if "BND" in prices else ("AGG" if "AGG" in prices else None)

        if us_sym:
            weights[us_sym] = self._targets.get(us_sym, 0.50)
        if intl_sym:
            weights[intl_sym] = self._targets.get(intl_sym, 0.20)
        if bond_sym:
            weights[bond_sym] = self._targets.get(bond_sym, 0.30)

        # Normalize in case some ETFs are missing
        total = sum(weights.values())
        if total > 0 and abs(total - 1.0) > 0.01:
            scale = 0.95 / total
            weights = {k: v * scale for k, v in weights.items()}

        return weights


# ---------------------------------------------------------------------------
# 12. Harry Browne Permanent Portfolio (All-Weather 25/25/25/25)
# ---------------------------------------------------------------------------
class PermanentPortfolio(BasePersona):
    """Harry Browne Permanent Portfolio — all-weather 25/25/25/25.

    Research basis: 9.7% CAGR from 1972-2020, only 6.8% volatility.
    7.21% CAGR over 30 years with max drawdown of just -15.92%.
    Sharpe ratio in top 25% of all portfolios.

    Composition: 25% stocks, 25% long bonds, 25% gold, 25% cash/T-bills.
    Rebalance: When any asset drifts beyond 15-35% band from 25% target
    (i.e., drops below 15% or rises above 35% of portfolio).

    Works in ALL economic regimes:
    - Prosperity: stocks rise
    - Recession: bonds rise (flight to safety)
    - Inflation: gold rises
    - Deflation: cash preserves purchasing power + bonds rise
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Harry Browne Permanent Portfolio",
            description="25/25/25/25 stocks/bonds/gold/cash — works in ALL regimes",
            risk_tolerance=0.2,
            max_position_size=0.30,
            max_positions=4,
            rebalance_frequency="monthly",  # Check monthly for band violations
            universe=universe or [
                "VTI",    # Stocks (total US market)
                "TLT",    # Long-term Treasury bonds (20+ year)
                "GLD",    # Gold
                "SHY",    # Short-term Treasury (cash proxy)
            ],
        )
        super().__init__(config)
        self._target = 0.25  # Each asset gets 25%

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        available = [sym for sym in ["VTI", "TLT", "GLD", "SHY"] if sym in prices]

        if not available:
            return weights

        # Equal 25% allocation to each available asset
        # If one asset is missing, redistribute its share equally
        per_asset = 0.96 / len(available)  # 4% cash buffer
        for sym in available:
            weights[sym] = per_asset

        return weights


# ---------------------------------------------------------------------------
# 13. Dividend Growth Compounding (DRIP Strategy)
# ---------------------------------------------------------------------------
class DividendGrowthCompounding(BasePersona):
    """Dividend Growth + DRIP compounding strategy.

    Research basis: DRIP achieves ~75% more assets over 20 years vs
    taking cash dividends. $10K at 8% dividend + 4% growth + 5% price
    appreciation = $32,469 in 10 years. Dividend aristocrats have
    raised dividends 25+ consecutive years.

    Universe: Stocks with 10+ years of dividend growth + dividend ETFs.
    Signal: Only add on dips (below SMA200 or RSI < 50); never sell winners.
    Rebalance: Monthly, equal weight across holdings.
    Exit: None for quality dividend growers — hold forever and reinvest.

    Target: 10-12% total return (4-5% yield + 6-7% appreciation).
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Dividend Growth Compounding (DRIP)",
            description="10+ year dividend growers, reinvest all dividends, never sell winners",
            risk_tolerance=0.2,
            max_position_size=0.10,
            max_positions=13,
            rebalance_frequency="monthly",
            universe=universe or [
                "JNJ",    # Johnson & Johnson (62yr dividend streak)
                "PG",     # Procter & Gamble (69yr dividend streak)
                "KO",     # Coca-Cola (62yr dividend streak)
                "PEP",    # PepsiCo (52yr dividend streak)
                "ABBV",   # AbbVie (52yr including ABT history)
                "MO",     # Altria (55yr dividend streak, 8%+ yield)
                "PM",     # Philip Morris International (16yr, 5% yield)
                "XOM",    # Exxon Mobil (41yr dividend streak)
                "CVX",    # Chevron (37yr dividend streak)
                "O",      # Realty Income (29yr monthly dividend)
                "SCHD",   # Schwab US Dividend Equity ETF
                "VIG",    # Vanguard Dividend Appreciation ETF
                "NOBL",   # ProShares S&P 500 Dividend Aristocrats ETF
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        buy_candidates = []
        hold_candidates = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym, ["sma_200", "sma_50", "rsi_14"], date
            )
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]

            if sma200 is None:
                # No data — equal weight starter
                hold_candidates.append((sym, 1.0))
                continue

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            # Dividend growers: NEVER sell winners
            # Only modulate allocation based on value opportunity
            if discount > 0.10:
                # Deep discount on dividend grower = aggressive buy
                buy_candidates.append((sym, 3.0 + discount * 5))
            elif discount > 0.0 or (rsi is not None and rsi < 50):
                # Below SMA200 or RSI < 50 = add on dip
                buy_candidates.append((sym, 2.0))
            elif discount > -0.10:
                # Near fair value — hold and reinvest
                hold_candidates.append((sym, 1.5))
            else:
                # Above fair value — still hold (never sell), smaller add
                hold_candidates.append((sym, 1.0))

        # Allocate: buy candidates get more weight than hold
        all_candidates = [(s, sc, "buy") for s, sc in buy_candidates] + \
                         [(s, sc, "hold") for s, sc in hold_candidates]

        if not all_candidates:
            return weights

        total_score = sum(sc for _, sc, _ in all_candidates)
        for sym, score, action in all_candidates:
            w = (score / total_score) * 0.95  # 5% cash buffer
            weights[sym] = min(w, self.config.max_position_size)

        return weights


# ---------------------------------------------------------------------------
# 14. Greenblatt Magic Formula (Earnings Yield + ROIC)
# ---------------------------------------------------------------------------
class MagicFormula(BasePersona):
    """Joel Greenblatt's Magic Formula strategy.

    Research basis: 23.8% CAGR (1988-2009) vs 9.6% S&P 500.
    11.4% CAGR (2003-2015) vs 8.7% S&P 500. Works globally.

    Method: Rank stocks by (1) earnings yield (high = cheap) and
    (2) return on capital (high = quality). Buy the top-ranked.

    Proxy implementation: Since we can't compute live ROIC/earnings yield
    in the backtester, we use quality+value factor stocks as proxies —
    high-quality companies (high ROE, strong margins) at reasonable prices
    (below SMA200 or low RSI).

    Universe: Large-cap quality companies with strong ROIC profiles.
    Rebalance: Annually (Greenblatt says hold minimum 1 year).
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Greenblatt Magic Formula",
            description="High earnings yield + high ROIC: quality companies at value prices",
            risk_tolerance=0.4,
            max_position_size=0.10,
            max_positions=14,
            rebalance_frequency="monthly",  # Check monthly, annual-ish turnover
            universe=universe or [
                # High ROIC + reasonable valuations (Magic Formula proxies)
                "AAPL",   # Apple (40%+ ROIC, brand moat)
                "MSFT",   # Microsoft (35%+ ROIC, cloud moat)
                "GOOGL",  # Alphabet (25%+ ROIC, search/ad moat)
                "BRK-B",  # Berkshire (capital allocation excellence)
                "JNJ",    # J&J (consistent 25%+ ROE, healthcare moat)
                "UNH",    # UnitedHealth (managed care dominance)
                "V",      # Visa (80%+ margins, network moat)
                "MA",     # Mastercard (80%+ margins, network moat)
                "HD",     # Home Depot (high ROIC, scale moat)
                "COST",   # Costco (high asset turns, membership moat)
                "MCO",    # Moody's (duopoly, 40%+ margins)
                "SPGI",   # S&P Global (duopoly, 35%+ margins)
                "TXN",    # Texas Instruments (analog chip monopoly)
                "QCOM",   # Qualcomm (IP licensing, high ROIC)
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
            inds = self._get_indicators(
                data, sym, ["sma_200", "sma_50", "rsi_14", "vol_20"], date
            )
            sma200 = inds["sma_200"]
            sma50 = inds["sma_50"]
            rsi = inds["rsi_14"]
            vol = inds["vol_20"]

            if sma200 is None:
                continue

            # Magic Formula scoring proxy:
            # Value score: how cheap relative to SMA200 (earnings yield proxy)
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            value_score = max(discount + 0.10, 0.01)  # Shift so fair value gets some score

            # Quality score: low volatility + above SMA50 = quality proxy
            quality_score = 1.0
            if vol is not None and vol > 0:
                # Lower vol = higher quality (stable earnings proxy)
                quality_score = max(0.02 / vol, 0.5) if vol > 0 else 1.0
                quality_score = min(quality_score, 3.0)
            if sma50 is not None and price > sma50:
                quality_score *= 1.2  # Momentum bonus (quality trends up)

            # RSI bonus: oversold quality = best Magic Formula entry
            if rsi is not None and rsi < 40:
                value_score *= 1.5
            elif rsi is not None and rsi > 75:
                value_score *= 0.5  # Overvalued — reduce

            # Combined Magic Formula score
            combined = value_score * quality_score
            candidates.append((sym, combined))

        # Rank by combined score, take top positions
        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]

        if not top:
            return weights

        total_score = sum(sc for _, sc in top)
        for sym, score in top:
            w = (score / total_score) * 0.95  # 5% cash buffer
            weights[sym] = min(w, self.config.max_position_size)

        return weights


# ---------------------------------------------------------------------------
# 15. Equal Weight S&P 500 Top Holdings
# ---------------------------------------------------------------------------
class EqualWeightSP500(BasePersona):
    """Equal Weight S&P 500 strategy.

    Research basis: Equal weight beat cap-weight by 1.05% annually until
    2023. Since 1990, +63bps/year with 742% cumulative total return
    difference. Equal weight grew earnings 12% annualized vs 9% for
    cap-weight. After peaks in market concentration, equal weight
    tends to outperform dramatically.

    Method: Instead of market-cap weighting (where AAPL/MSFT/NVDA dominate),
    equal-weight the top S&P 500 holdings. Include RSP (equal weight ETF)
    as core + top 15 individual stocks equally weighted.
    Rebalance: Quarterly (to maintain equal weights as prices diverge).
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Equal Weight S&P 500",
            description="Equal weight top S&P 500 holdings — beats cap-weight by ~1%/year long term",
            risk_tolerance=0.4,
            max_position_size=0.10,
            max_positions=16,
            rebalance_frequency="monthly",  # Quarterly intent, monthly checks
            universe=universe or [
                "RSP",    # Invesco S&P 500 Equal Weight ETF (core)
                # Top 15 S&P 500 stocks (equally weighted, not cap-weighted)
                "AAPL",   # Apple
                "MSFT",   # Microsoft
                "NVDA",   # NVIDIA
                "AMZN",   # Amazon
                "GOOGL",  # Alphabet
                "META",   # Meta
                "BRK-B",  # Berkshire Hathaway
                "LLY",    # Eli Lilly
                "UNH",    # UnitedHealth
                "V",      # Visa
                "JNJ",    # Johnson & Johnson
                "XOM",    # Exxon Mobil
                "JPM",    # JPMorgan Chase
                "PG",     # Procter & Gamble
                "HD",     # Home Depot
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        available = [sym for sym in self.config.universe if sym in prices]

        if not available:
            return weights

        # Pure equal weight: each stock gets 1/N allocation
        # RSP gets slightly more as it's already the equal-weight index
        per_stock = 0.95 / len(available)  # 5% cash buffer
        for sym in available:
            if sym == "RSP":
                weights[sym] = min(per_stock * 1.5, 0.10)
            else:
                weights[sym] = min(per_stock, 0.10)

        # Normalize to 95% invested
        total = sum(weights.values())
        if total > 0.95:
            scale = 0.95 / total
            weights = {k: v * scale for k, v in weights.items()}

        return weights


# ---------------------------------------------------------------------------
# 16. Ray Dalio All Weather Passive (Simplified)
# ---------------------------------------------------------------------------
class AllWeatherPassive(BasePersona):
    """Ray Dalio All Weather portfolio — simplified passive version.

    Research basis: 7.33% CAGR over 30 years, 7.49% std dev.
    Designed for risk parity: each asset class contributes equal risk.
    Works in any economic environment. Max drawdown much lower than stocks.

    Composition: 30% stocks, 40% long bonds, 15% intermediate bonds,
    7.5% gold, 7.5% commodities.
    ETFs: VTI, TLT, IEF, GLD, DBC.
    Rebalance: Annually (passive = less frequent).

    Difference from AllWeatherModern (strategy #3): This is the ORIGINAL
    Dalio allocation with no momentum filters or regime detection. Pure
    passive risk parity for 10+ year holding periods.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Ray Dalio All Weather Passive",
            description="30/40/15/7.5/7.5 stocks/long bonds/mid bonds/gold/commodities",
            risk_tolerance=0.2,
            max_position_size=0.42,
            max_positions=5,
            rebalance_frequency="monthly",  # Check monthly, rebalance on drift
            universe=universe or [
                "VTI",    # 30% — Total US Stock Market (stocks)
                "TLT",    # 40% — 20+ Year Treasury Bond (long bonds)
                "IEF",    # 15% — 7-10 Year Treasury Bond (intermediate bonds)
                "GLD",    # 7.5% — Gold
                "DBC",    # 7.5% — Commodities (Invesco DB Commodity Index)
            ],
        )
        super().__init__(config)
        # Fixed Dalio target allocations
        self._targets = {
            "VTI": 0.30,
            "TLT": 0.40,
            "IEF": 0.15,
            "GLD": 0.075,
            "DBC": 0.075,
        }

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        available_targets = {
            sym: w for sym, w in self._targets.items() if sym in prices
        }

        if not available_targets:
            return weights

        # Redistribute missing allocation proportionally
        total_target = sum(available_targets.values())
        if total_target > 0:
            scale = 0.95 / total_target  # 5% cash buffer
            for sym, target in available_targets.items():
                weights[sym] = target * scale

        return weights


# ---------------------------------------------------------------------------
# 17. Quality + Dividend Aristocrats (HODL)
# ---------------------------------------------------------------------------
class QualityDividendAristocrats(BasePersona):
    """Quality factor + Dividend Aristocrats HODL strategy.

    Research basis: Quality factor outperforms by 2.6%/year (MSCI, 1975-2018).
    Dividend Aristocrats have 25+ years of consecutive dividend increases.
    Combining quality (high ROE, stable earnings) with dividend growth
    creates a powerful compounding engine.

    Quality outperforms by 23-31 bps/month during high-volatility periods
    (defensive behavior). Profitability (ROE) is the strongest quality signal.

    Universe: Only companies with 25+ years of consecutive dividend
    increases AND evidence of high quality (strong brands, pricing power).
    Signal: Buy the dip, hold forever, reinvest dividends.
    Exit: None — these are permanent holdings.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Quality Dividend Aristocrats",
            description="25+ year dividend growers with high ROE — buy dips, hold forever",
            risk_tolerance=0.2,
            max_position_size=0.10,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                "NOBL",   # S&P 500 Dividend Aristocrats ETF (core)
                "JNJ",    # Johnson & Johnson (62yr, healthcare)
                "PG",     # Procter & Gamble (69yr, consumer staples)
                "KO",     # Coca-Cola (62yr, beverages)
                "MMM",    # 3M (65yr, industrial conglomerate)
                "EMR",    # Emerson Electric (67yr, industrial automation)
                "ABT",    # Abbott Laboratories (52yr, medical devices)
                "ADP",    # Automatic Data Processing (49yr, payroll/HR)
                "SHW",    # Sherwin-Williams (46yr, paint/coatings moat)
                "CTAS",   # Cintas (41yr, uniform services moat)
                "ITW",    # Illinois Tool Works (50yr, diversified industrial)
                "GPC",    # Genuine Parts Company (68yr, auto parts distribution)
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
            inds = self._get_indicators(
                data, sym, ["sma_200", "sma_50", "rsi_14", "vol_20"], date
            )
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            vol = inds["vol_20"]

            if sma200 is None:
                # No data yet — equal weight starter for aristocrats
                candidates.append((sym, 1.0, 0.07))
                continue

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            score = 1.0
            base_weight = 0.07

            # Quality aristocrats: always hold, buy dips aggressively
            if discount > 0.15:
                # Deep value on a dividend aristocrat = best opportunity
                score = 4.0 + discount * 5
                base_weight = 0.10
            elif discount > 0.05:
                # Moderate dip — accumulate
                score = 2.5
                base_weight = 0.09
            elif discount > -0.05:
                # Near fair value — standard hold
                score = 1.5
                base_weight = 0.07
            else:
                # Above SMA200 — still hold (never sell aristocrats)
                score = 1.0
                base_weight = 0.06

            # RSI: oversold aristocrats are rare gifts
            if rsi is not None and rsi < 30:
                score += 2.0
                base_weight = min(base_weight + 0.02, 0.10)
            elif rsi is not None and rsi < 40:
                score += 1.0

            # Low volatility bonus (quality signal)
            if vol is not None and vol < 0.012:
                score += 0.5

            # NOBL ETF gets a baseline larger allocation as diversified core
            if sym == "NOBL":
                base_weight = min(base_weight + 0.02, 0.10)

            candidates.append((sym, score, base_weight))

        if not candidates:
            return weights

        # Score-weighted allocation
        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        total_weight = sum(wt for _, _, wt in top)
        # Scale to ~95% invested
        if total_weight > 0:
            scale = 0.95 / total_weight if total_weight > 0.95 else 1.0
            for sym, _, wt in top:
                weights[sym] = min(wt * scale, self.config.max_position_size)

        return weights


PORTFOLIO_STRATEGIES = {
    "staples_hedged_growth": StaplesHedgedGrowth,
    "barbell_portfolio": BarbellPortfolio,
    "all_weather_modern": AllWeatherModern,
    "adaptive_ensemble": AdaptiveEnsemble,
    "core_satellite": CoreSatellite,
    "income_shield": IncomeShield,
    "bond_fixed_income": BondFixedIncome,
    "high_yield_reit_bdc": HighYieldREITBDCIncome,
    "dividend_aristocrat_blue_chips": DividendAristocratBlueChips,
    # --- Passive / HODL strategies (10+ year holding periods) ---
    "buffett_hodl": BuffettHODL,
    "bogle_three_fund": BogleThreeFund,
    "permanent_portfolio": PermanentPortfolio,
    "dividend_growth_compounding": DividendGrowthCompounding,
    "magic_formula": MagicFormula,
    "equal_weight_sp500": EqualWeightSP500,
    "all_weather_passive": AllWeatherPassive,
    "quality_dividend_aristocrats": QualityDividendAristocrats,
}


# ---------------------------------------------------------------------------
# 18. Bond Duration Trade (yield curve steepening/flattening)
# ---------------------------------------------------------------------------
class BondDurationTrade(BasePersona):
    """Yield curve duration strategy: rotate between long and short duration bonds.

    Source: CFA Institute yield curve strategies, CME Group yield curve research.
    Duration measures bond price sensitivity to yield changes. TLT (duration ~17)
    moves aggressively with rate expectations. SHY (duration ~2) is defensive.

    When yield curve steepens (long rates rise faster than short rates, i.e.
    TLT underperforms SHY): long-duration bonds are cheap -> buy TLT.
    When curve flattens/inverts (TLT outperforms SHY or short rates rise):
    short-duration bonds are safer -> buy SHY/BIL.

    We detect the regime by comparing TLT vs SHY relative momentum.
    Steepening = TLT weakening relative to SHY (TLT below its SMA, SHY above).
    Flattening = TLT strengthening relative to SHY.

    Implementation:
    - Compute TLT momentum (price vs SMA50) and SHY momentum (price vs SMA50)
    - If TLT > SMA50 and TLT momentum > SHY momentum: curve flattening, long TLT
    - If SHY > SMA50 and SHY momentum > TLT momentum: curve steepening, short
      duration (SHY, BIL)
    - Include IEF, TIP, GOVT for diversification in the intermediate space
    - Monthly rebalance
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Bond Duration Trade",
            description="Yield curve regime: long duration in flattening, short duration in steepening",
            risk_tolerance=0.3,
            max_position_size=0.40,
            max_positions=4,
            rebalance_frequency="monthly",
            universe=universe or [
                "TLT",   # Long duration (~17y)
                "IEF",   # Intermediate duration (~7y)
                "SHY",   # Short duration (~2y)
                "BIL",   # Ultra-short (T-bills)
                "TIP",   # TIPS (inflation protected)
                "GOVT",  # Broad Treasury
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Get momentum for TLT and SHY
        tlt_price = prices.get("TLT")
        shy_price = prices.get("SHY")
        tlt_sma50 = self._get_indicator(data, "TLT", "sma_50", date)
        shy_sma50 = self._get_indicator(data, "SHY", "sma_50", date)
        tlt_sma200 = self._get_indicator(data, "TLT", "sma_200", date)

        if tlt_price is None or shy_price is None:
            # Missing data — equal weight available bonds
            available = [s for s in self.config.universe if s in prices]
            if available:
                per = min(0.90 / len(available), self.config.max_position_size)
                for s in available:
                    weights[s] = per
            return weights

        # Determine curve regime from TLT vs SHY momentum
        tlt_mom = 0.0
        shy_mom = 0.0
        if not _is_missing(tlt_sma50) and tlt_sma50 > 0:
            tlt_mom = (tlt_price - tlt_sma50) / tlt_sma50
        if not _is_missing(shy_sma50) and shy_sma50 > 0:
            shy_mom = (shy_price - shy_sma50) / shy_sma50

        # Additional trend check: TLT above/below SMA200
        tlt_uptrend = (
            not _is_missing(tlt_sma200)
            and tlt_sma200 > 0
            and tlt_price > tlt_sma200
        )

        if tlt_mom > shy_mom and tlt_mom > 0 and tlt_uptrend:
            # Flattening / rates falling — long duration wins
            weights["TLT"] = 0.40
            weights["IEF"] = 0.25
            weights["TIP"] = 0.15
            # Close short duration
            weights["SHY"] = 0.0
            weights["BIL"] = 0.0
        elif shy_mom > tlt_mom or tlt_mom < -0.01:
            # Steepening / rates rising — short duration safer
            weights["SHY"] = 0.35
            weights["BIL"] = 0.25
            weights["IEF"] = 0.15
            weights["TIP"] = 0.10
            # Close long duration
            weights["TLT"] = 0.0
        else:
            # Neutral — balanced across curve
            weights["IEF"] = 0.30
            weights["TIP"] = 0.20
            weights["SHY"] = 0.15
            weights["TLT"] = 0.15

        # Zero out any universe members not allocated
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0

        return weights


PORTFOLIO_STRATEGIES["bond_duration_trade"] = BondDurationTrade


# ---------------------------------------------------------------------------
# 19. Credit Spread Trade (high yield vs investment grade rotation)
# ---------------------------------------------------------------------------
class CreditSpreadTrade(BasePersona):
    """Credit spread rotation: risk-on high yield vs risk-off investment grade.

    Source: SSRN "Credit-Spread Timing between High-Yield Bonds and Treasuries"
    (Situ, 2024). Monthly rotation between HYG and IEF using price-ratio and
    return-spread signals improved long-run growth with controlled drawdowns
    vs a 50/50 benchmark.

    When credit spreads widen (HYG drops relative to LQD): risk-off signal,
    buy quality bonds (LQD, AGG, BND). When spreads tighten (HYG outperforms
    LQD): risk-on signal, buy high yield (HYG, JNK).

    We detect the regime by comparing HYG vs LQD momentum.
    HYG outperforming LQD = spreads tightening = risk-on.
    LQD outperforming HYG = spreads widening = risk-off.

    Note: LQD has ~8.4y duration vs HYG ~4.1y, so we also check the
    absolute trend of HYG to avoid false signals from duration mismatch.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Credit Spread Trade",
            description="Rotate high yield vs investment grade based on credit spread regime",
            risk_tolerance=0.4,
            max_position_size=0.40,
            max_positions=4,
            rebalance_frequency="monthly",
            universe=universe or [
                "HYG",   # High yield corporate
                "LQD",   # Investment grade corporate
                "JNK",   # High yield (SPDR)
                "AGG",   # Broad aggregate bond
                "BND",   # Total bond market
                "VCIT",  # Intermediate corporate
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        hyg_price = prices.get("HYG")
        lqd_price = prices.get("LQD")

        if hyg_price is None or lqd_price is None:
            # Fallback: balanced bond allocation
            available = [s for s in self.config.universe if s in prices]
            if available:
                per = min(0.90 / len(available), self.config.max_position_size)
                for s in available:
                    weights[s] = per
            return weights

        # Get momentum indicators for HYG and LQD
        hyg_sma50 = self._get_indicator(data, "HYG", "sma_50", date)
        lqd_sma50 = self._get_indicator(data, "LQD", "sma_50", date)
        hyg_sma200 = self._get_indicator(data, "HYG", "sma_200", date)
        hyg_rsi = self._get_indicator(data, "HYG", "rsi_14", date)

        hyg_mom = 0.0
        lqd_mom = 0.0
        if not _is_missing(hyg_sma50) and hyg_sma50 > 0:
            hyg_mom = (hyg_price - hyg_sma50) / hyg_sma50
        if not _is_missing(lqd_sma50) and lqd_sma50 > 0:
            lqd_mom = (lqd_price - lqd_sma50) / lqd_sma50

        # Absolute trend check for HYG
        hyg_uptrend = (
            not _is_missing(hyg_sma200)
            and hyg_sma200 > 0
            and hyg_price > hyg_sma200
        )

        if hyg_mom > lqd_mom and hyg_uptrend:
            # Risk-on: credit spreads tightening, HYG outperforming
            weights["HYG"] = 0.40
            weights["JNK"] = 0.25
            weights["VCIT"] = 0.15
            # Close quality
            weights["LQD"] = 0.0
            weights["AGG"] = 0.0
            weights["BND"] = 0.0
        elif lqd_mom > hyg_mom or (not _is_missing(hyg_rsi) and hyg_rsi < 40):
            # Risk-off: credit spreads widening or HYG oversold
            weights["LQD"] = 0.35
            weights["AGG"] = 0.25
            weights["BND"] = 0.20
            # Close high yield
            weights["HYG"] = 0.0
            weights["JNK"] = 0.0
            weights["VCIT"] = 0.0
        else:
            # Neutral — blended allocation
            weights["LQD"] = 0.25
            weights["VCIT"] = 0.20
            weights["HYG"] = 0.15
            weights["AGG"] = 0.15
            weights["BND"] = 0.05

        # Zero out any unallocated
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0

        return weights


PORTFOLIO_STRATEGIES["credit_spread_trade"] = CreditSpreadTrade


# ---------------------------------------------------------------------------
# 20. Covered Call Income
# ---------------------------------------------------------------------------
class CoveredCallIncome(BasePersona):
    """Covered call income strategy using ETF proxies.

    Source: CBOE BuyWrite Index research, JPM JEPI methodology.

    Uses covered call ETFs (JEPI, JEPQ, QYLD, XYLD) as proxies for
    writing calls against equity positions. Adds SVXY for vol-selling
    exposure.

    VIX regime filter (using SPY realized vol as proxy):
    - High vol (VIX > 25 proxy): overweight QYLD (higher premiums)
    - Low vol (VIX < 15 proxy): underweight (low premiums not worth it)
    - Normal: equal weight across all covered call ETFs

    Rebalance quarterly.

    ## Passive Investor View
    Buy-and-hold JEPI + JEPQ equal weight for steady monthly income.
    Suitable for retirees or income-focused portfolios. Expect 7-10%
    yield with equity-like participation in up markets.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Covered Call Income",
            description="Covered call ETF income with VIX regime overlay",
            risk_tolerance=0.3,
            max_position_size=0.30,
            max_positions=6,
            rebalance_frequency="monthly",
            universe=universe or [
                "JEPI", "JEPQ", "QYLD", "XYLD",  # Covered call ETFs
                "SVXY",  # Vol-selling exposure
                "SPY",   # Regime detection
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Estimate VIX regime from SPY 20-day realized vol
        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)

        # vol_20 is typically daily std dev; annualize: vol*sqrt(252)*100 ~ VIX
        high_vol = False
        low_vol = False
        if spy_vol is not None and not _is_missing(spy_vol):
            annualized_vol = spy_vol * 15.87 * 100  # sqrt(252) ~ 15.87
            if annualized_vol > 25:
                high_vol = True
            elif annualized_vol < 15:
                low_vol = True

        cc_etfs = ["JEPI", "JEPQ", "QYLD", "XYLD"]
        available = [s for s in cc_etfs if s in prices]

        if not available:
            return weights

        if high_vol:
            # High vol: overweight QYLD (higher premiums from covered calls)
            for sym in available:
                if sym == "QYLD":
                    weights[sym] = 0.35
                else:
                    weights[sym] = 0.15
            # Add SVXY (vol selling profits from mean reversion)
            if "SVXY" in prices:
                weights["SVXY"] = 0.10
        elif low_vol:
            # Low vol: underweight covered calls, shift to cash-like
            for sym in available:
                weights[sym] = 0.10
            # SVXY less attractive when vol already low
            if "SVXY" in prices:
                weights["SVXY"] = 0.05
        else:
            # Normal vol: equal weight
            per_etf = min(0.20, 0.80 / len(available))
            for sym in available:
                weights[sym] = per_etf
            if "SVXY" in prices:
                weights["SVXY"] = 0.10

        # Zero non-allocated universe symbols
        for sym in self.config.universe:
            if sym in prices and sym not in weights and sym != "SPY":
                weights[sym] = 0.0

        return weights


PORTFOLIO_STRATEGIES["covered_call_income"] = CoveredCallIncome


# ---------------------------------------------------------------------------
# 21. Dual Momentum Global
# ---------------------------------------------------------------------------
class DualMomentumGlobal(BasePersona):
    """Antonacci Dual Momentum with global asset classes.

    Source: Gary Antonacci "Dual Momentum Investing" (2014).

    Compare SPY (US equities) vs EFA (international equities) vs AGG
    (bonds) on 12-month return (SMA200 distance as proxy).
    Hold the top performer if its return > 0 (absolute momentum filter).
    If top performer return < 0, hold SHY (cash proxy).

    Classic documented strategy with historical 0.7+ Sharpe ratio.
    Similar to existing DualMomentum but adds AGG as third horse.

    ## Passive Investor View
    Simple rules-based rotation between 3 asset classes. Low turnover
    (monthly rebalance). Historically avoids major drawdowns by moving
    to bonds/cash when all assets negative.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Dual Momentum Global",
            description="Antonacci dual momentum: SPY vs EFA vs AGG, SHY fallback",
            risk_tolerance=0.5,
            max_position_size=0.90,
            max_positions=2,
            rebalance_frequency="monthly",
            universe=universe or ["SPY", "EFA", "AGG", "SHY"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = ["SPY", "EFA", "AGG"]

        # Calculate 12-month momentum for each candidate (price vs SMA200)
        momentums = {}
        for sym in candidates:
            if sym not in prices:
                continue
            price = prices[sym]
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            if price is None or _is_missing(sma200) or sma200 <= 0:
                continue
            momentums[sym] = (price - sma200) / sma200

        if not momentums:
            # No data: park in cash proxy
            if "SHY" in prices:
                weights["SHY"] = 0.90
            return weights

        # Find top performer
        winner = max(momentums, key=momentums.get)
        winner_mom = momentums[winner]

        # Absolute momentum filter: only invest if return > 0
        if winner_mom > 0:
            weights[winner] = 0.90
        else:
            # All negative: hold cash proxy
            if "SHY" in prices:
                weights["SHY"] = 0.90

        # Zero out non-winners
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0

        return weights


PORTFOLIO_STRATEGIES["dual_momentum_global"] = DualMomentumGlobal


# ---------------------------------------------------------------------------
# 22. Preferred Equity Income
# ---------------------------------------------------------------------------
class PreferredEquityIncome(BasePersona):
    """Preferred stock income strategy with rate sensitivity filter.

    Source: iShares Preferred & Income Securities research.

    Uses PFF, PGX, PFFD for preferred stock exposure. Preferreds are
    rate-sensitive (like bonds but with equity-like yield).

    Rate sensitivity filter:
    - When TLT trending down (10Y yield rising): underweight preferreds,
      shift to SHY (short duration protects against rising rates)
    - When TLT trending up (rates falling): overweight preferreds
      (rate tailwind + high yield)

    ## Passive Investor View
    Preferred stocks offer 5-7% yields with lower volatility than common
    equity. Suitable for income portfolios. Combine PFF + PGX for
    diversification across issuers.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Preferred Equity Income",
            description="Preferred stock ETFs with rate sensitivity filter",
            risk_tolerance=0.3,
            max_position_size=0.40,
            max_positions=5,
            rebalance_frequency="monthly",
            universe=universe or [
                "PFF", "PGX", "PFFD",  # Preferred stock ETFs
                "TLT",  # Rate regime detection
                "SHY",  # Cash proxy for rate-rising regime
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Detect rate regime via TLT trend
        tlt_price = prices.get("TLT")
        tlt_sma50 = self._get_indicator(data, "TLT", "sma_50", date)
        tlt_sma200 = self._get_indicator(data, "TLT", "sma_200", date)

        rates_rising = False
        rates_falling = False

        if tlt_price is not None and not _is_missing(tlt_sma50):
            if not _is_missing(tlt_sma200):
                if tlt_price < tlt_sma50 < tlt_sma200:
                    rates_rising = True  # TLT in downtrend = yields rising
                elif tlt_price > tlt_sma50 > tlt_sma200:
                    rates_falling = True  # TLT in uptrend = yields falling
            else:
                if tlt_price < tlt_sma50:
                    rates_rising = True
                elif tlt_price > tlt_sma50:
                    rates_falling = True

        preferred_etfs = ["PFF", "PGX", "PFFD"]
        available = [s for s in preferred_etfs if s in prices]

        if rates_rising:
            # Rates rising: underweight preferreds, shift to short duration
            for sym in available:
                weights[sym] = 0.10
            if "SHY" in prices:
                weights["SHY"] = 0.50
        elif rates_falling:
            # Rates falling: overweight preferreds (rate tailwind)
            if available:
                per_etf = min(0.30, 0.85 / len(available))
                for sym in available:
                    weights[sym] = per_etf
            if "SHY" in prices:
                weights["SHY"] = 0.0
        else:
            # Neutral: moderate allocation
            if available:
                per_etf = min(0.25, 0.70 / len(available))
                for sym in available:
                    weights[sym] = per_etf
            if "SHY" in prices:
                weights["SHY"] = 0.15

        # Zero out non-allocated
        for sym in self.config.universe:
            if sym in prices and sym not in weights and sym != "TLT":
                weights[sym] = 0.0

        return weights


PORTFOLIO_STRATEGIES["preferred_equity_income"] = PreferredEquityIncome


# ---------------------------------------------------------------------------
# 23. Tax Harvest Rotation
# ---------------------------------------------------------------------------
class DrawdownSeverityRotation(BasePersona):
    """Drawdown-severity asset rotation strategy.

    Source: Meb Faber's GTAA research + AQR crisis alpha papers.

    Shifts allocation between equities, bonds, gold, and cash based on
    how deep the S&P 500 drawdown is from its 52-week high:

    - Drawdown < 5% (normal):  80% equities (SPY+QQQ), 10% bonds (TLT), 10% gold (GLD)
    - Drawdown 5-10% (caution): 50% equities, 25% bonds, 15% gold, 10% cash (SHY)
    - Drawdown 10-20% (fear):   20% equities, 30% bonds, 30% gold, 20% cash
    - Drawdown > 20% (crisis):  10% equities, 20% bonds, 40% gold, 30% cash

    As market recovers (drawdown shrinks), shifts back to equities.
    This captures the well-documented pattern that deep drawdowns
    precede further losses, and gold/bonds provide crisis alpha.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Drawdown Severity Rotation",
            description="Shift equities→bonds→gold→cash as drawdown deepens",
            risk_tolerance=0.4,
            max_position_size=0.45,
            max_positions=5,
            rebalance_frequency="weekly",
            universe=universe or ["SPY", "QQQ", "TLT", "GLD", "SHY"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Measure SPY drawdown from 52-week high
        dd_pct = 0.0
        spy_key = "SPY"
        if spy_key in data and not data[spy_key].empty:
            df = data[spy_key]
            try:
                if date in df.index:
                    loc = df.index.get_loc(date)
                elif hasattr(df.index, 'get_indexer'):
                    idx = df.index.get_indexer([date], method="nearest")[0]
                    loc = idx if idx != -1 else None
                else:
                    loc = None

                if loc is not None and loc >= 50:
                    lookback = df.iloc[max(0, loc - 252):loc + 1]
                    col = "High" if "High" in lookback.columns else "Close"
                    high_52w = lookback[col].max()
                    cur_price = prices.get(spy_key, 0)
                    if high_52w > 0 and cur_price > 0:
                        dd_pct = (high_52w - cur_price) / high_52w
            except Exception:
                pass

        # Determine regime
        if dd_pct < 0.05:
            # Normal: heavy equities
            eq, bond, gold, cash = 0.40, 0.10, 0.10, 0.0
        elif dd_pct < 0.10:
            # Caution: reduce equities, add defense
            eq, bond, gold, cash = 0.25, 0.25, 0.15, 0.10
        elif dd_pct < 0.20:
            # Fear: defensive
            eq, bond, gold, cash = 0.10, 0.30, 0.30, 0.20
        else:
            # Crisis: maximum defense
            eq, bond, gold, cash = 0.05, 0.20, 0.40, 0.30

        # Allocate equities between SPY and QQQ
        if "SPY" in prices:
            weights["SPY"] = eq * 0.6
        if "QQQ" in prices:
            weights["QQQ"] = eq * 0.4
        if "TLT" in prices:
            weights["TLT"] = bond
        if "GLD" in prices:
            weights["GLD"] = gold
        if "SHY" in prices:
            weights["SHY"] = cash

        return weights


PORTFOLIO_STRATEGIES["drawdown_severity_rotation"] = DrawdownSeverityRotation


# ---------------------------------------------------------------------------
# Self-Storage REIT Compounders
# ---------------------------------------------------------------------------
class SelfStorageREIT(BasePersona):
    """Self-storage REITs benefiting from the "4 Ds" of demand.

    Source: Death, Divorce, Downsizing, Dislocation drive counter-cyclical demand.
    Supply growth moderating to 1.5% annually (2025-2027) due to high construction
    costs. PSA long-term total returns rival S&P 500. Current yields 4.1-4.4%.

    Implementation:
    - Equal-weight core self-storage REITs
    - Buy at pullbacks (RSI < 40 entry signal)
    - Must be above 200-SMA for trend confirmation (or deep value entry)
    - Monthly rebalance for yield + appreciation
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Self-Storage REIT",
            description="Counter-cyclical REITs with pricing power — PSA, EXR, CUBE, NSA, REXR",
            risk_tolerance=0.4,
            max_position_size=0.25,
            max_positions=5,
            rebalance_frequency="monthly",
            universe=universe or ["PSA", "EXR", "CUBE", "NSA", "REXR"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        base_weight = 0.18

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_200", "sma_50", "rsi_14"], date)
            sma200 = inds["sma_200"]
            sma50 = inds["sma_50"]
            rsi = inds["rsi_14"]

            if _is_missing(sma200):
                weights[sym] = base_weight * 0.8
                continue

            wt = base_weight

            # Trend confirmation
            if price > sma200:
                # Uptrend: full weight
                if not _is_missing(sma50) and sma50 > sma200:
                    wt *= 1.1  # Strong uptrend bonus

                # Pullback entry in uptrend
                if not _is_missing(rsi) and rsi < 40:
                    wt *= 1.25  # Beaten-down in uptrend = buy
            else:
                # Below trend but REITs are yield plays — reduce but don't exit
                discount = (sma200 - price) / sma200 if sma200 > 0 else 0
                if discount > 0.15:
                    # Deep value territory: actually increase (contrarian)
                    wt *= 0.9
                else:
                    wt *= 0.6

            # Don't chase overbought REITs
            if not _is_missing(rsi) and rsi > 70:
                wt *= 0.6

            weights[sym] = min(wt, self.config.max_position_size)

        return weights


PORTFOLIO_STRATEGIES["self_storage_reit"] = SelfStorageREIT


# ---------------------------------------------------------------------------
# Closed-End Fund Discount Arbitrage
# ---------------------------------------------------------------------------
class ClosedEndFundDiscount(BasePersona):
    """Buy CEFs trading at deep discounts to NAV for structural edge.

    Source: CEFs trading at deep discounts historically mean-revert.
    You get NAV appreciation PLUS discount compression. Yields 6-10%.

    Since we cannot access real-time NAV discount data in backtests,
    we use price-based proxies: RSI oversold + below SMA = likely at discount.

    Implementation:
    - Buy CEFs when RSI < 35 AND price below 200-SMA (proxy for deep discount)
    - Reduce when RSI > 65 AND price above 200-SMA (proxy for premium)
    - Collect high yields (6-10%) while waiting for discount compression
    - Monthly rebalance
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Closed-End Fund Discount",
            description="CEF discount arbitrage — PDI, PTY, UTF, UTG, GOF, BST, BSTZ",
            risk_tolerance=0.4,
            max_position_size=0.20,
            max_positions=7,
            rebalance_frequency="monthly",
            universe=universe or ["PDI", "PTY", "UTF", "UTG", "GOF", "BST", "BSTZ"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        base_weight = 0.12

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_200", "sma_50", "rsi_14"], date)
            sma200 = inds["sma_200"]
            sma50 = inds["sma_50"]
            rsi = inds["rsi_14"]

            if _is_missing(sma200):
                weights[sym] = base_weight * 0.7
                continue

            wt = base_weight
            below_sma = price < sma200

            # Deep discount proxy: below 200-SMA and oversold
            if below_sma:
                discount_pct = (sma200 - price) / sma200 if sma200 > 0 else 0
                if not _is_missing(rsi) and rsi < 35:
                    # Strong buy signal: deep discount + oversold
                    wt *= 1.5
                elif discount_pct > 0.10:
                    # Moderate discount
                    wt *= 1.2
                else:
                    wt *= 0.9
            else:
                # Above SMA (proxy for premium territory)
                if not _is_missing(rsi) and rsi > 65:
                    # Premium + overbought: reduce (sell signal)
                    wt *= 0.4
                elif not _is_missing(rsi) and rsi > 55:
                    wt *= 0.7
                else:
                    wt *= 1.0  # Hold at normal weight

            weights[sym] = min(wt, self.config.max_position_size)

        return weights


PORTFOLIO_STRATEGIES["closed_end_fund_discount"] = ClosedEndFundDiscount


# ---------------------------------------------------------------------------
# Canadian Aristocrat Income
# ---------------------------------------------------------------------------
class CanadianAristocratIncome(BasePersona):
    """Canadian Dividend Aristocrats with decades of dividend growth.

    Source: Canadian Dividend Aristocrats returned 19.11% in 2025.
    ENB: 31st consecutive increase. FTS: 51 consecutive years.
    Average yield 4.06% with P/E 15.84x. Geographic diversification
    with CAD currency exposure.

    Implementation:
    - Equal-weight Canadian aristocrats with 20+ year increase streaks
    - Use US-listed ADRs/tickers for backtesting compatibility
    - Trend filter: maintain weight above 200-SMA, reduce below
    - Monthly rebalance, DRIP all dividends
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Canadian Aristocrat Income",
            description="Decades of dividend growth — ENB, TRP, FTS, BNS, CM, BCE, TU",
            risk_tolerance=0.3,
            max_position_size=0.20,
            max_positions=7,
            rebalance_frequency="monthly",
            universe=universe or ["ENB", "TRP", "FTS", "BNS", "CM", "BCE", "TU"],
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

            # Trend filter
            if price > sma200:
                # Above trend: full weight
                if not _is_missing(sma50) and sma50 > sma200:
                    wt *= 1.05  # Gentle momentum bonus
            else:
                # Below trend: reduce but don't exit (income play)
                wt *= 0.65

            # Pullback entry for income stocks
            if not _is_missing(rsi) and rsi < 35:
                wt *= 1.15  # Oversold = accumulate

            # Avoid chasing
            if not _is_missing(rsi) and rsi > 70:
                wt *= 0.8

            weights[sym] = min(wt, self.config.max_position_size)

        return weights


PORTFOLIO_STRATEGIES["canadian_aristocrat_income"] = CanadianAristocratIncome


# ---------------------------------------------------------------------------
# Pre-IPO Innovation Funds (private company exposure via public ETFs)
# ---------------------------------------------------------------------------
class PreIPOInnovationFunds(BasePersona):
    """Private company exposure via public ETFs and closed-end funds.

    Source: CICC/KraneShares AGIX + ARK Venture + Destiny Tech100 research.
    These funds hold stakes in private unicorns (Anthropic, SpaceX, xAI,
    OpenAI, Stripe, Databricks) that are otherwise inaccessible to retail.

    Universe:
    - AGIX (KraneShares AI & Tech -- holds Anthropic, SpaceX, xAI)
    - DXYZ (Destiny Tech100 -- holds unicorn portfolio)
    - BSTZ (BlackRock Science & Tech Trust -- holds Anthropic, NAV discount)
    - ARKK (ARK Innovation -- closest public proxy)
    - ARKW (ARK Next Gen Internet)

    Signal logic:
    - Equal weight across available funds
    - AGIX gets 1.5x weight (best private company exposure per research)
    - BSTZ gets 1.25x weight (trades at NAV discount = margin of safety)
    - Monthly rebalance
    - No momentum filter -- these are buy-and-hold fund positions

    ## Passive Investor Section
    For buy-and-hold: split equally between AGIX (private AI exposure) and
    BSTZ (BlackRock quality + NAV discount). Add ARKK for broader innovation.
    These are the easiest ways to get pre-IPO tech company exposure through
    a regular brokerage account. Hold for 3-5 years through IPO cycles.
    """

    CONVICTION = {
        "AGIX": 1.5,   # Best private company exposure per research
        "BSTZ": 1.25,  # NAV discount = margin of safety
        "DXYZ": 1.0,
        "ARKK": 1.0,
        "ARKW": 1.0,
    }

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Pre-IPO Innovation Funds",
            description="Private company exposure via AGIX, BSTZ, DXYZ, ARKK, ARKW (holds Anthropic, SpaceX, xAI)",
            risk_tolerance=0.7,
            max_position_size=0.30,
            max_positions=5,
            rebalance_frequency="monthly",
            universe=universe or [
                "AGIX",   # KraneShares AI & Tech (Anthropic, SpaceX, xAI)
                "DXYZ",   # Destiny Tech100 (unicorn portfolio)
                "BSTZ",   # BlackRock Science & Tech Trust (Anthropic, NAV discount)
                "ARKK",   # ARK Innovation (closest public proxy)
                "ARKW",   # ARK Next Gen Internet
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        qualified = []  # (sym, conviction_mult)

        for sym in self.config.universe:
            if sym not in prices:
                continue

            # No momentum filter for fund positions -- buy-and-hold thesis
            conviction = self.CONVICTION.get(sym, 1.0)

            # Only basic safety check: skip if data is severely broken
            price = prices[sym]
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            if not _is_missing(sma200) and sma200 > 0 and price < sma200 * 0.50:
                # >50% below SMA200 = something structurally wrong
                weights[sym] = 0.0
                continue

            qualified.append((sym, conviction))

        # Distribute weights proportionally
        total_units = sum(mult for _, mult in qualified)
        if total_units > 0:
            base = 0.90 / total_units
            for sym, mult in qualified:
                w = base * mult
                weights[sym] = min(w, self.config.max_position_size)

        # Zero out unavailable
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)

        return weights


PORTFOLIO_STRATEGIES["pre_ipo_innovation_funds"] = PreIPOInnovationFunds


def get_portfolio_strategy(name: str, **kwargs) -> BasePersona:
    cls = PORTFOLIO_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown: {name}. Available: {list(PORTFOLIO_STRATEGIES.keys())}")
    return cls(**kwargs)
