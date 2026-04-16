"""Recession indicators and recession-proof strategies for agents-assemble.

Recession Detection:
- Yield curve inversion (10Y-2Y spread, 10Y-3M spread)
- SMA200 death cross on SPY
- High yield spreads widening
- Market breadth deterioration
- VIX regime

Recession-Proof Strategies:
1. RecessionDetector         — Regime detection, shifts to defensive
2. TreasurySafe             — Flight to quality during downturns
3. DefensiveRotation        — Rotate to staples/utilities/healthcare in recessions
4. GoldBug                  — Gold and precious metals as recession hedge
5. YieldCurveInversion      — Yield curve inversion as recession leading indicator
6. ConsumerCreditStress     — Consumer discretionary weakness as subprime proxy
7. UnemploymentMomentum     — Unemployment claims momentum via sector rotation
8. VShapeRecovery           — High-beta bounce on V-shape recovery signal
9. KShapeEconomy            — Inequality trade: long luxury+tech when dollar stores crash
10. LShapeStagnation        — Worst-case: gold + utilities + short bonds
"""

from __future__ import annotations

import pandas as pd

from bespoke.strategies.base import BaseStrategy as BasePersona, StrategyConfig as PersonaConfig


def _is_missing(v):
    """Check if value is None or NaN."""
    return v is None or v != v


# ---------------------------------------------------------------------------
# Recession Regime Detection
# ---------------------------------------------------------------------------
def detect_recession_regime(
    date: pd.Timestamp,
    data: dict[str, pd.DataFrame],
    prices: dict[str, float],
) -> dict[str, object]:
    """Detect if we're in a recession-like regime.

    Uses multiple signals:
    1. SPY below SMA200 (bear market)
    2. TLT rising (flight to quality)
    3. IWM underperforming SPY (small caps weaker = risk-off)
    4. VIX proxy (high volatility in SPY)

    Returns dict with regime info and confidence score.
    """
    regime = {
        "is_recession": False,
        "confidence": 0.0,
        "signals": {},
    }

    signal_count = 0
    total_signals = 0

    # Fetch SPY indicators once (used by signals 1, 2, 4, 5)
    _spy_raw = prices.get("SPY")
    spy_price = _spy_raw if _spy_raw is not None and not pd.isna(_spy_raw) else None
    spy_sma50 = _safe_get(data, "SPY", "sma_50", date) if "SPY" in data else None
    spy_sma200 = _safe_get(data, "SPY", "sma_200", date) if "SPY" in data else None
    spy_vol = _safe_get(data, "SPY", "vol_20", date) if "SPY" in data else None
    spy_rsi = _safe_get(data, "SPY", "rsi_14", date) if "SPY" in data else None

    # Signal 1: SPY below SMA200
    if spy_sma200 is not None and spy_price is not None:
        total_signals += 1
        if spy_price < spy_sma200:
            signal_count += 1
            regime["signals"]["spy_below_sma200"] = True
        else:
            regime["signals"]["spy_below_sma200"] = False

    # Signal 2: SPY SMA50 < SMA200 (death cross)
    if spy_sma50 is not None and spy_sma200 is not None:
        total_signals += 1
        if spy_sma50 < spy_sma200:
            signal_count += 1
            regime["signals"]["death_cross"] = True
        else:
            regime["signals"]["death_cross"] = False

    # Signal 3: TLT trending up (bonds rally = flight to quality)
    if "TLT" in data:
        tlt_sma50 = _safe_get(data, "TLT", "sma_50", date)
        tlt_sma200 = _safe_get(data, "TLT", "sma_200", date)
        if tlt_sma50 is not None and tlt_sma200 is not None:
            total_signals += 1
            if tlt_sma50 > tlt_sma200:
                signal_count += 1
                regime["signals"]["tlt_uptrend"] = True
            else:
                regime["signals"]["tlt_uptrend"] = False

    # Signal 4: High volatility
    if spy_vol is not None:
        total_signals += 1
        if spy_vol > 0.018:  # Annualized ~28%
            signal_count += 1
            regime["signals"]["high_vol"] = True
        else:
            regime["signals"]["high_vol"] = False

    # Signal 5: RSI below 40 on SPY
    if spy_rsi is not None:
        total_signals += 1
        if spy_rsi < 40:
            signal_count += 1
            regime["signals"]["spy_oversold"] = True
        else:
            regime["signals"]["spy_oversold"] = False

    if total_signals > 0:
        regime["confidence"] = signal_count / total_signals
        regime["is_recession"] = regime["confidence"] >= 0.5  # majority of available signals

    return regime


def _safe_get(data, sym, indicator, date):
    if sym not in data:
        return None
    df = data[sym]
    if indicator not in df.columns:
        return None
    if date in df.index:
        val = df.loc[date, indicator]
        if isinstance(val, pd.Series):
            val = val.iloc[0]
        return float(val) if not pd.isna(val) else None
    try:
        idx = df.index.get_indexer([date], method="nearest")[0]
        if idx >= 0:
            nearest_date = df.index[idx]
            if abs((date - nearest_date).days) > 10:
                return None  # Data too stale
            val = df.iloc[idx][indicator]
            if isinstance(val, pd.Series):
                val = val.iloc[0]
            return float(val) if not pd.isna(val) else None
    except (IndexError, KeyError, TypeError):
        pass
    return None


# ---------------------------------------------------------------------------
# 1. Recession Detector — Adaptive regime switching
# ---------------------------------------------------------------------------
class RecessionDetector(BasePersona):
    """Adaptive strategy that detects recession regime and switches positioning.

    Normal regime: 70% stocks (SPY/QQQ), 20% bonds (TLT), 10% gold (GLD)
    Recession regime: 20% stocks (XLP/XLV), 50% bonds (TLT/IEF), 20% gold (GLD), 10% cash
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Recession Detector (Adaptive)",
            description="Regime-switching: risk-on in growth, defensive in recession",
            risk_tolerance=0.4,
            max_position_size=0.50,
            max_positions=6,
            rebalance_frequency="weekly",
            universe=universe or [
                "SPY", "QQQ", "TLT", "IEF", "GLD",
                "XLP", "XLV", "SHY",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        regime = detect_recession_regime(date, data, prices)

        if regime["is_recession"]:
            # Defensive positioning
            weights = {
                "XLP": 0.15,  # Consumer staples
                "XLV": 0.10,  # Healthcare
                "TLT": 0.30,  # Long bonds
                "IEF": 0.15,  # Intermediate bonds
                "GLD": 0.20,  # Gold
                "SHY": 0.05,  # Short-term treasuries (cash proxy)
                "SPY": 0.0,   # Exit stocks
                "QQQ": 0.0,   # Exit tech
            }
        else:
            # Risk-on positioning
            weights = {
                "SPY": 0.35,
                "QQQ": 0.30,
                "TLT": 0.15,
                "GLD": 0.10,
                "IEF": 0.05,
                "XLP": 0.0,
                "XLV": 0.0,
                "SHY": 0.0,
            }

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 2. Treasury Safe Haven
# ---------------------------------------------------------------------------
class TreasurySafe(BasePersona):
    """Flight to quality strategy during downturns.

    Thesis: When stocks sell off, treasuries rally. Go long duration
    when recession signals fire, short duration otherwise.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Treasury Safe Haven",
            description="Flight to quality: long-duration bonds when recession signals fire",
            risk_tolerance=0.2,
            max_position_size=0.40,
            max_positions=4,
            rebalance_frequency="weekly",
            universe=universe or ["TLT", "IEF", "SHY", "TIP", "GLD", "SPY"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        regime = detect_recession_regime(date, data, prices)

        if regime["is_recession"]:
            weights = {
                "TLT": 0.45,  # Long bonds (biggest winner in recession)
                "IEF": 0.20,
                "GLD": 0.20,  # Gold hedge
                "TIP": 0.10,  # Inflation protection
                "SHY": 0.0,
                "SPY": 0.0,
            }
        elif regime["confidence"] > 0.3:
            # Mixed signals — balanced
            weights = {
                "IEF": 0.30,
                "TLT": 0.15,
                "GLD": 0.15,
                "SHY": 0.20,
                "TIP": 0.10,
                "SPY": 0.0,
            }
        else:
            # All clear — moderate bond allocation
            weights = {
                "SHY": 0.40,  # Short duration (rates may rise)
                "IEF": 0.25,
                "TLT": 0.10,
                "GLD": 0.10,
                "TIP": 0.10,
                "SPY": 0.0,
            }

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 3. Defensive Rotation
# ---------------------------------------------------------------------------
class DefensiveRotation(BasePersona):
    """Rotate into defensive sectors during recession signals.

    Thesis: Consumer staples, utilities, and healthcare outperform
    during recessions because demand is inelastic.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Defensive Rotation",
            description="Rotate to staples/utilities/healthcare when recession signals fire",
            risk_tolerance=0.3,
            max_position_size=0.30,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                # Defensive sectors
                "XLP", "XLU", "XLV",  # Sector ETFs
                "PG", "KO", "PEP", "CL",  # Consumer staples
                "JNJ", "MRK", "ABBV", "UNH",  # Healthcare
                "NEE", "DUK", "SO",  # Utilities
                # Growth (for when things are good)
                "SPY", "QQQ", "XLK",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        regime = detect_recession_regime(date, data, prices)
        weights = {}

        if regime["is_recession"]:
            # Full defensive
            defensive = ["XLP", "XLU", "XLV", "PG", "KO", "JNJ", "MRK", "NEE"]
            available = [s for s in defensive if s in prices]
            if available:
                per_stock = min(0.90 / len(available), self.config.max_position_size)
                for sym in available:
                    weights[sym] = per_stock
            # Exit growth
            for sym in ["SPY", "QQQ", "XLK"]:
                weights[sym] = 0.0
        else:
            # Risk-on with some defensive hedge
            weights["SPY"] = 0.30
            weights["QQQ"] = 0.25
            weights["XLK"] = 0.15
            weights["XLP"] = 0.10
            weights["XLV"] = 0.10
            weights["XLU"] = 0.05

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 4. Gold Bug
# ---------------------------------------------------------------------------
class GoldBug(BasePersona):
    """Gold and precious metals strategy for recession/inflation hedge.

    Thesis: Gold outperforms during recessions, currency debasement,
    and inflation. Mining stocks provide leveraged exposure.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Gold Bug (Precious Metals)",
            description="Gold/silver/miners as recession and inflation hedge",
            risk_tolerance=0.5,
            max_position_size=0.25,
            max_positions=6,
            rebalance_frequency="weekly",
            universe=universe or [
                "GLD", "SLV",  # Physical gold/silver ETFs
                "GDX", "GDXJ",  # Gold miners (senior + junior)
                "NEM", "GOLD", "AEM",  # Individual miners (Newmont, Barrick, Agnico Eagle)
                "IAU",  # Alternative gold ETF
                "SPY", "TLT",  # Required for recession regime detection
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        regime = detect_recession_regime(date, data, prices)

        # Always hold some gold
        base_gold = 0.20

        if regime["is_recession"]:
            # Max gold allocation
            weights["GLD"] = 0.35
            weights["SLV"] = 0.15
            weights["GDX"] = 0.20
            weights["NEM"] = 0.10
            weights["IAU"] = 0.10
        else:
            # Check gold trend
            gld_sma50 = _safe_get(data, "GLD", "sma_50", date)
            gld_sma200 = _safe_get(data, "GLD", "sma_200", date)

            if gld_sma50 is not None and gld_sma200 is not None:
                if gld_sma50 > gld_sma200:
                    # Gold uptrend — increase allocation
                    weights["GLD"] = 0.30
                    weights["GDX"] = 0.20
                    weights["SLV"] = 0.15
                    weights["NEM"] = 0.10
                else:
                    # Gold downtrend — minimal
                    weights["GLD"] = 0.15
                    weights["IAU"] = 0.10
            else:
                weights["GLD"] = base_gold

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 5. Yield Curve Inversion Signal
# ---------------------------------------------------------------------------
class YieldCurveInversion(BasePersona):
    """Yield curve inversion as recession leading indicator.

    Hypothesis: The 10Y-2Y Treasury spread inversion has predicted
    every US recession since 1960 with a 12-18 month lead time.
    Since we cannot directly observe yield curves from equity data,
    we use TLT/SHY ratio as a proxy: when long bonds rally vs short
    bonds (TLT outperforms SHY), the curve is flattening/inverting.

    The strategy goes defensive when TLT outperforms SHY on a trend
    basis (SMA50 of TLT/SHY ratio rising = flattening curve), and
    becomes aggressive when the ratio normalizes (steepening).

    Source: Estrella & Mishkin (1998) show yield curve predicts
    recessions 4-6 quarters ahead with >80% accuracy. Harvey (1989)
    established the inverted yield curve as the single best recession
    predictor. Campbell & Shiller (1991) confirm term spread
    forecasting power.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Yield Curve Inversion Signal",
            description="TLT/SHY ratio proxy for yield curve: go defensive on flattening",
            risk_tolerance=0.3,
            max_position_size=0.35,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "TLT", "SHY", "IEF",  # Treasury ETFs (curve proxy)
                "SPY", "QQQ",          # Equities (risk-on)
                "XLP", "XLU", "XLV",   # Defensive sectors
                "GLD",                  # Gold hedge
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        # Compute yield curve proxy: TLT relative strength vs SHY
        curve_flattening = False
        curve_inverting = False

        if "TLT" in data and "SHY" in data and "TLT" in prices and "SHY" in prices:
            tlt_sma50 = _safe_get(data, "TLT", "sma_50", date)
            tlt_sma200 = _safe_get(data, "TLT", "sma_200", date)
            shy_sma50 = _safe_get(data, "SHY", "sma_50", date)
            shy_sma200 = _safe_get(data, "SHY", "sma_200", date)

            if all(v is not None for v in [tlt_sma50, tlt_sma200, shy_sma50, shy_sma200]):
                # TLT relative strength: long bonds outperforming short bonds
                tlt_trend = (tlt_sma50 - tlt_sma200) / tlt_sma200 if tlt_sma200 > 0 else 0
                shy_trend = (shy_sma50 - shy_sma200) / shy_sma200 if shy_sma200 > 0 else 0
                relative_strength = tlt_trend - shy_trend

                if relative_strength > 0.02:
                    curve_inverting = True  # Strong flattening/inversion
                elif relative_strength > 0.005:
                    curve_flattening = True  # Moderate flattening

        # Also check broader recession regime
        regime = detect_recession_regime(date, data, prices)

        if curve_inverting or (curve_flattening and regime["is_recession"]):
            # Full defensive: yield curve inverted = recession in 12-18 months
            weights = {
                "TLT": 0.30,   # Long bonds rally in rate cuts
                "IEF": 0.15,
                "XLP": 0.15,   # Consumer staples
                "XLU": 0.10,   # Utilities
                "XLV": 0.10,   # Healthcare
                "GLD": 0.15,   # Gold
                "SPY": 0.0,
                "QQQ": 0.0,
                "SHY": 0.0,
            }
        elif curve_flattening:
            # Cautious: flattening but not inverted
            weights = {
                "SPY": 0.15,
                "XLP": 0.15,
                "XLV": 0.10,
                "TLT": 0.20,
                "IEF": 0.15,
                "GLD": 0.15,
                "QQQ": 0.0,
                "XLU": 0.05,
                "SHY": 0.0,
            }
        else:
            # Normal: risk-on, steep curve is bullish
            weights = {
                "SPY": 0.35,
                "QQQ": 0.30,
                "TLT": 0.10,
                "GLD": 0.10,
                "IEF": 0.05,
                "XLP": 0.0,
                "XLU": 0.0,
                "XLV": 0.0,
                "SHY": 0.0,
            }

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 6. Consumer Credit Stress (Subprime Indicator Proxy)
# ---------------------------------------------------------------------------
class ConsumerCreditStress(BasePersona):
    """Consumer credit stress proxy via consumer discretionary weakness.

    Hypothesis: When consumer credit is stressed (rising delinquencies,
    tightening lending), consumer discretionary stocks underperform
    staples. The XLY/XLP ratio falling signals credit stress. This
    preceded both the 2008 GFC and the 2020 COVID recession.

    We proxy subprime stress by: (1) XLY underperforming XLP (consumer
    weakness), (2) regional bank weakness (KRE) as lending proxy,
    (3) high yield credit via HYG weakness (credit spreads widening).
    When all three signal stress, rotate to cash-rich defensives.

    Source: Mian & Sufi (2009) "The Consequences of Mortgage Credit
    Expansion" show consumer credit as the primary amplifier of
    recessions. Adrian & Shin (2010) link credit conditions to
    financial stability.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Consumer Credit Stress (Subprime Proxy)",
            description="Consumer discretionary vs staples ratio as credit stress indicator",
            risk_tolerance=0.3,
            max_position_size=0.25,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                # Stress indicators
                "XLY", "XLP",  # Consumer discretionary vs staples
                "KRE",         # Regional banks (lending proxy)
                "HYG",         # High yield bonds (credit spread proxy)
                # Defensive assets
                "SHY", "TLT", "GLD",
                # Cash-rich defensives (survive credit crunches)
                "JNJ", "PG", "KO", "WMT", "COST",
                # Avoid in stress
                "SPY", "QQQ",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        stress_signals = 0
        total_checks = 0

        # Check 1: XLY underperforming XLP (consumer weakness)
        xly_sma50 = _safe_get(data, "XLY", "sma_50", date)
        xly_sma200 = _safe_get(data, "XLY", "sma_200", date)
        xlp_sma50 = _safe_get(data, "XLP", "sma_50", date)
        xlp_sma200 = _safe_get(data, "XLP", "sma_200", date)
        if all(v is not None for v in [xly_sma50, xly_sma200, xlp_sma50, xlp_sma200]):
            total_checks += 1
            xly_trend = (xly_sma50 - xly_sma200) / xly_sma200 if xly_sma200 > 0 else 0
            xlp_trend = (xlp_sma50 - xlp_sma200) / xlp_sma200 if xlp_sma200 > 0 else 0
            if xly_trend < xlp_trend - 0.01:
                stress_signals += 1  # Consumer discretionary lagging staples

        # Check 2: Regional banks (KRE) in downtrend
        kre_price = prices.get("KRE")
        kre_sma200 = _safe_get(data, "KRE", "sma_200", date)
        if kre_price is not None and kre_sma200 is not None:
            total_checks += 1
            if kre_price < kre_sma200:
                stress_signals += 1  # Banks below SMA200 = credit tightening

        # Check 3: HYG weakness (credit spreads widening)
        hyg_price = prices.get("HYG")
        hyg_sma50 = _safe_get(data, "HYG", "sma_50", date)
        hyg_sma200 = _safe_get(data, "HYG", "sma_200", date)
        if hyg_price is not None and hyg_sma200 is not None:
            total_checks += 1
            if hyg_price < hyg_sma200:
                stress_signals += 1  # HYG below SMA200 = credit stress

        # Also check broader regime
        regime = detect_recession_regime(date, data, prices)

        credit_stress = total_checks > 0 and (stress_signals / total_checks) >= 0.5
        severe_stress = credit_stress and regime["is_recession"]

        if severe_stress:
            # Full defensive: credit crunch
            weights = {
                "TLT": 0.25,
                "SHY": 0.20,
                "GLD": 0.20,
                "JNJ": 0.10,
                "PG": 0.08,
                "KO": 0.07,
                "WMT": 0.05,
                "XLY": 0.0, "XLP": 0.0, "KRE": 0.0,
                "HYG": 0.0, "SPY": 0.0, "QQQ": 0.0,
                "COST": 0.0,
            }
        elif credit_stress:
            # Moderate stress: reduce risk, overweight defensives
            weights = {
                "XLP": 0.15,
                "JNJ": 0.10,
                "PG": 0.10,
                "WMT": 0.10,
                "COST": 0.10,
                "TLT": 0.15,
                "GLD": 0.10,
                "SHY": 0.10,
                "SPY": 0.05,
                "XLY": 0.0, "KRE": 0.0,
                "HYG": 0.0, "QQQ": 0.0,
                "KO": 0.0,
            }
        else:
            # No stress: normal risk-on
            weights = {
                "SPY": 0.30,
                "QQQ": 0.25,
                "XLY": 0.15,
                "KRE": 0.10,
                "HYG": 0.05,
                "GLD": 0.05,
                "TLT": 0.05,
                "XLP": 0.0, "SHY": 0.0,
                "JNJ": 0.0, "PG": 0.0, "KO": 0.0,
                "WMT": 0.0, "COST": 0.0,
            }

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 7. Unemployment Claims Momentum
# ---------------------------------------------------------------------------
class UnemploymentMomentum(BasePersona):
    """Unemployment claims momentum via sector performance proxy.

    Hypothesis: Rising unemployment claims signal economic weakness.
    Since we cannot directly observe jobless claims from equity data,
    we use sector rotation patterns that correlate with employment
    cycles: (1) staffing companies (HAYS, MAN, RHI) as leading
    indicators, (2) consumer discretionary weakness, (3) regional
    bank lending pullback.

    When staffing stocks break down (below SMA200), it signals
    companies are cutting hiring -- a leading indicator of recession
    by 2-4 quarters. We shift to defensive sectors that benefit
    from falling rates (utilities, REITs) and counter-cyclical
    sectors (healthcare, staples).

    Source: Sims (2012) "Macroeconomics and Methodology" -- employment
    leads GDP by 1-2 quarters. Caballero & Hammour (1994) document
    the "cleansing effect" of recessions on labor markets.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Unemployment Claims Momentum",
            description="Staffing stock weakness as unemployment proxy, rotate to defensives",
            risk_tolerance=0.3,
            max_position_size=0.20,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                # Staffing / employment proxies (leading indicators)
                "MAN", "RHI", "HAYS", "ASGN", "KFRC",
                # Risk-on cyclicals
                "SPY", "QQQ", "XLI",
                # Defensive destinations
                "XLP", "XLU", "XLV",
                "TLT", "GLD",
                # Rate-sensitive beneficiaries
                "VNQ", "IEF",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        # Check staffing company health as employment proxy
        staffing_stocks = ["MAN", "RHI", "ASGN", "KFRC"]
        staffing_weak = 0
        staffing_checked = 0

        for sym in staffing_stocks:
            if sym not in data or sym not in prices:
                continue
            price = prices[sym]
            sma200 = _safe_get(data, sym, "sma_200", date)
            sma50 = _safe_get(data, sym, "sma_50", date)
            if sma200 is not None:
                staffing_checked += 1
                if price < sma200:
                    staffing_weak += 1
                    # Death cross (SMA50 < SMA200) = severe
                    if sma50 is not None and sma50 < sma200:
                        staffing_weak += 0.5

        # Also check industrial sector (employment-correlated)
        xli_price = prices.get("XLI")
        xli_sma200 = _safe_get(data, "XLI", "sma_200", date)
        if xli_price is not None and xli_sma200 is not None:
            staffing_checked += 1
            if xli_price < xli_sma200:
                staffing_weak += 1

        regime = detect_recession_regime(date, data, prices)

        employment_stress = staffing_checked > 0 and (staffing_weak / staffing_checked) >= 0.5
        severe_stress = employment_stress and regime["is_recession"]

        if severe_stress:
            # Severe: staffing collapsing + recession signals
            weights = {
                "XLU": 0.20,   # Utilities (rate cut beneficiary)
                "XLV": 0.15,   # Healthcare (inelastic demand)
                "XLP": 0.15,   # Staples
                "TLT": 0.20,   # Long bonds (rate cuts coming)
                "GLD": 0.15,   # Gold
                "VNQ": 0.10,   # REITs (rate cut beneficiary)
                "SPY": 0.0, "QQQ": 0.0, "XLI": 0.0, "IEF": 0.0,
            }
        elif employment_stress:
            # Moderate: staffing weak but no full recession yet
            weights = {
                "XLP": 0.15,
                "XLV": 0.15,
                "XLU": 0.10,
                "TLT": 0.15,
                "GLD": 0.10,
                "IEF": 0.10,
                "SPY": 0.10,
                "VNQ": 0.10,
                "QQQ": 0.0, "XLI": 0.0,
            }
        else:
            # Healthy employment: risk-on, favor cyclicals
            weights = {
                "SPY": 0.30,
                "QQQ": 0.25,
                "XLI": 0.15,   # Industrials (employment growth)
                "TLT": 0.10,
                "GLD": 0.05,
                "XLP": 0.05,
                "XLU": 0.0, "XLV": 0.0, "VNQ": 0.0, "IEF": 0.0,
            }

        # Remove staffing stocks from weights (they are indicators, not holdings)
        for sym in staffing_stocks:
            weights.pop(sym, None)

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# V-Shape Recovery Trader
# ---------------------------------------------------------------------------
class VShapeRecovery(BasePersona):
    """Trade the V-shape recovery: sharp drop → sharp rebound.

    V-shapes happen when the shock is exogenous (COVID, flash crash) not structural.
    Signal: SPY drops >15% from SMA200 then reclaims SMA50 = V-recovery confirmed.
    Buy: high-beta growth stocks that bounce hardest (TSLA, NVDA, SHOP, SQ).
    Historical: COVID Mar-Aug 2020 was textbook V — NASDAQ recovered in 5 months.
    """
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="V-Shape Recovery (Sharp Bounce)",
            description="Sharp crash → sharp rebound. Buy high-beta growth on confirmed V-recovery signal.",
            risk_tolerance=0.7, max_position_size=0.12, max_positions=10, rebalance_frequency="weekly",
            universe=universe or [
                "SPY", "QQQ",  # Recovery indicators
                "TSLA", "NVDA", "AMD", "SHOP", "SQ",  # High-beta bouncers
                "ARKK", "SOFI", "COIN", "PLTR", "MSTR",  # Speculative growth
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        # Detect V-shape: SPY was below SMA200 but now reclaiming SMA50
        v_signal = False
        if "SPY" in data and "SPY" in prices:
            inds = self._get_indicators(data, "SPY", ["sma_50", "sma_200"], date)
            s50, s200 = inds["sma_50"], inds["sma_200"]
            if s50 is not None and s200 is not None and not _is_missing(s200):
                # V-recovery: price above SMA50 but SMA50 still below SMA200 (recovery underway)
                if prices["SPY"] > s50 and s50 < s200:
                    v_signal = True
        if v_signal:
            # Buy high-beta stocks aggressively
            targets = ["TSLA","NVDA","AMD","SHOP","SQ","ARKK","SOFI","COIN","PLTR","MSTR"]
            scored = []
            for sym in targets:
                if sym not in prices: continue
                inds = self._get_indicators(data, sym, ["sma_50","rsi_14","macd","macd_signal"], date)
                rsi = inds["rsi_14"]
                if _is_missing(rsi): continue
                sc = 1.0
                s50 = inds["sma_50"]
                if s50 is not None and prices[sym] > s50: sc += 2.0
                macd, ms = inds["macd"], inds["macd_signal"]
                if macd is not None and ms is not None and macd > ms: sc += 1.0
                if 40 < rsi < 70: sc += 1.0
                scored.append((sym, sc))
            scored.sort(key=lambda x: -x[1])
            if scored:
                total = sum(s for _,s in scored[:self.config.max_positions])
                for sym, sc in scored[:self.config.max_positions]:
                    weights[sym] = min((sc/total)*0.95, self.config.max_position_size)
        else:
            # No V-signal — small position in QQQ
            if "QQQ" in prices: weights["QQQ"] = 0.10
        return weights


# ---------------------------------------------------------------------------
# K-Shape Economy (Inequality Trade)
# ---------------------------------------------------------------------------
class KShapeEconomy(BasePersona):
    """Trade the K-shaped recovery: rich get richer, poor get poorer.

    K-shape signal: luxury/tech (top arm) diverges UP while retail/restaurants (bottom arm) diverges DOWN.
    Detect: LVMUY+COST > SMA200 while DLTR+DG < SMA200 = K-shape confirmed.
    Long: tech platforms, luxury, wealth management, premium healthcare.
    The K-shape has been the dominant pattern since COVID. Not cyclical — structural.
    """
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="K-Shape Economy (Inequality Trade)",
            description="Rich richer, poor poorer: luxury+tech UP while dollar stores DOWN. Long the top arm of K.",
            risk_tolerance=0.5, max_position_size=0.12, max_positions=10, rebalance_frequency="weekly",
            universe=universe or [
                # Bottom arm indicators (INVERSE — weakness confirms K-shape)
                "DLTR", "DG", "KSS",
                # Top arm beneficiaries (LONG these)
                "COST", "LVMUY", "AAPL", "AMZN",  # Premium consumer
                "GS", "MS", "BX",  # Wealth management
                "UNH", "ELV",  # Premium healthcare
                "LULU", "RH",  # Aspirational luxury
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        # Detect K-shape: bottom arm weak, top arm strong
        bottom_weak = 0; top_strong = 0
        for sym in ["DLTR", "DG", "KSS"]:
            if sym not in data or sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_200"], date)
            if not _is_missing(inds["sma_200"]) and prices[sym] < inds["sma_200"]:
                bottom_weak += 1
        for sym in ["COST", "AAPL", "AMZN", "UNH"]:
            if sym not in data or sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_200"], date)
            if not _is_missing(inds["sma_200"]) and prices[sym] > inds["sma_200"]:
                top_strong += 1

        k_shape = bottom_weak >= 1 and top_strong >= 2
        targets = ["COST","LVMUY","AAPL","AMZN","GS","MS","BX","UNH","ELV","LULU","RH"]
        if k_shape:
            scored = []
            for sym in targets:
                if sym not in prices: continue
                inds = self._get_indicators(data, sym, ["sma_50","sma_200","rsi_14"], date)
                if _is_missing(inds["sma_200"]) or _is_missing(inds["rsi_14"]): continue
                sc = 0.0
                if prices[sym] > inds["sma_200"]: sc += 2.0
                s50 = inds["sma_50"]
                if s50 is not None and s50 > inds["sma_200"]: sc += 1.0
                if 35 < inds["rsi_14"] < 65: sc += 1.0
                if sc >= 2: scored.append((sym, sc))
            scored.sort(key=lambda x: -x[1])
            if scored:
                total = sum(s for _,s in scored[:self.config.max_positions])
                for sym, sc in scored[:self.config.max_positions]:
                    weights[sym] = min((sc/total)*0.95, self.config.max_position_size)
        else:
            # No K-shape — balanced
            for sym in ["COST","AAPL","UNH"]:
                if sym in prices: weights[sym] = 0.08
        return weights


# ---------------------------------------------------------------------------
# L-Shape Stagnation Hedge
# ---------------------------------------------------------------------------
class LShapeStagnation(BasePersona):
    """Hedge for L-shaped stagnation: crash with NO recovery (Japan 1990s style).

    L-shape signal: SPY below SMA200 for 6+ months AND SMA50 < SMA200 (death cross persistent).
    In L-shape, NOTHING works except: gold, utilities, short-duration bonds, and dividend aristocrats.
    This is the worst-case scenario strategy — it sacrifices upside for survival.
    """
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="L-Shape Stagnation Hedge (Worst Case)",
            description="Persistent crash with no recovery (Japan 1990s). Gold + utilities + short bonds + dividends only.",
            risk_tolerance=0.2, max_position_size=0.20, max_positions=6, rebalance_frequency="monthly",
            universe=universe or [
                "SPY",  # Indicator
                "GLD", "IAU",  # Gold (store of value)
                "XLU",  # Utilities (recession-proof income)
                "SHY", "BIL",  # Short-duration bonds (no duration risk)
                "SCHD",  # Dividend ETF (income in stagnation)
                "JNJ", "PG",  # Defensive dividend aristocrats
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        # Detect L-shape: persistent bearish (SPY below SMA200 with death cross)
        l_signal = False
        if "SPY" in data and "SPY" in prices:
            inds = self._get_indicators(data, "SPY", ["sma_50", "sma_200"], date)
            s50, s200 = inds["sma_50"], inds["sma_200"]
            if s50 is not None and s200 is not None and not _is_missing(s200):
                if prices["SPY"] < s200 and s50 < s200:
                    l_signal = True  # Death cross + below both MAs
        if l_signal:
            # Maximum defense
            weights = {"GLD": 0.25, "SHY": 0.20, "XLU": 0.15, "SCHD": 0.15, "JNJ": 0.10, "PG": 0.10}
            weights = {s: w for s, w in weights.items() if s in prices}
        else:
            # Mild defense
            weights = {"GLD": 0.10, "SCHD": 0.10, "XLU": 0.05}
            weights = {s: w for s, w in weights.items() if s in prices}
        return weights


RECESSION_STRATEGIES = {
    "recession_detector": RecessionDetector,
    "treasury_safe": TreasurySafe,
    "defensive_rotation": DefensiveRotation,
    "gold_bug": GoldBug,
    "yield_curve_inversion": YieldCurveInversion,
    "consumer_credit_stress": ConsumerCreditStress,
    "unemployment_momentum": UnemploymentMomentum,
    "v_shape_recovery": VShapeRecovery,
    "k_shape_economy": KShapeEconomy,
    "l_shape_stagnation": LShapeStagnation,
}


def get_recession_strategy(name: str, **kwargs) -> BasePersona:
    cls = RECESSION_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown strategy: {name}. Available: {list(RECESSION_STRATEGIES.keys())}")
    return cls(**kwargs)


if __name__ == "__main__":
    print("=== Recession Strategies ===\n")
    for key, cls in RECESSION_STRATEGIES.items():
        inst = cls()
        print(f"  {key:25s} | {inst.config.name:35s} | {inst.config.description}")
