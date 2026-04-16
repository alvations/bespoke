"""Strategy Orchestrator — Meta-strategy that activates/deactivates strategies by regime.

Instead of running inverse strategies standalone (where they sit idle most of the time),
the orchestrator detects the current market regime and activates the RIGHT strategies:

    BULL (growth) → AI token economy, subscription monopoly, momentum
    BEAR (defensive) → L-shape stagnation, gold bug, treasury safe
    ROTATION (sector shift) → oil-down-tech-up, bonds-down-banks-up
    CRISIS (panic) → VIX spike buyback, NVIDIA domino hedge
    K-SHAPE (inequality) → wealth barometer, K-shape economy

The orchestrator runs as a single strategy in the Backtester, but internally
it delegates to multiple sub-strategies and blends their weights.

Usage:
    from strategy_orchestrator import get_orchestrated_strategy

    # Get the meta-strategy
    strategy = get_orchestrated_strategy("adaptive_regime")

    # Run in backtester like any other strategy
    bt = Backtester(strategy=strategy, symbols=strategy.config.universe, ...)
    results = bt.run()
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import pandas as pd

from bespoke.strategies.base import BaseStrategy as BasePersona, StrategyConfig as PersonaConfig


def _is_missing(v):
    return v is None or v != v


# ---------------------------------------------------------------------------
# Regime Detection
# ---------------------------------------------------------------------------
@dataclass
class RegimeSignal:
    """Market regime detected from macro indicators."""
    regime: str          # "bull", "bear", "rotation", "crisis", "k_shape"
    confidence: float    # 0-1, how confident we are in the regime
    signals: dict        # Individual signal readings


def detect_regime(date, prices, data) -> RegimeSignal:
    """Detect current market regime from macro indicators.

    Checks:
    - SPY trend (bull/bear)
    - VIX level via VXX (crisis)
    - Dollar stores vs luxury (K-shape)
    - Energy vs tech divergence (rotation)
    - Bond trend (rate regime)
    """
    signals = {}
    scores = {"bull": 0, "bear": 0, "rotation": 0, "crisis": 0, "k_shape": 0}

    def _get_sma(sym, period_name):
        if sym not in data:
            return None
        df = data[sym]
        if date not in df.index:
            try:
                idx = df.index.get_indexer([date], method="nearest")[0]
                if idx == -1:
                    return None
                row = df.iloc[idx]
            except Exception:
                return None
        else:
            row = df.loc[date]
            if isinstance(row, pd.DataFrame):
                row = row.iloc[-1]
        val = row.get(period_name)
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return None
        return float(val)

    # 1. SPY trend → bull vs bear
    if "SPY" in prices:
        spy_sma200 = _get_sma("SPY", "sma_200")
        spy_sma50 = _get_sma("SPY", "sma_50")
        if spy_sma200 is not None:
            spy_price = prices["SPY"]
            if spy_price > spy_sma200:
                scores["bull"] += 3
                signals["spy_above_200"] = True
            else:
                scores["bear"] += 3
                signals["spy_above_200"] = False
            if spy_sma50 is not None:
                if spy_sma50 > spy_sma200:
                    scores["bull"] += 2  # Golden cross
                    signals["spy_golden_cross"] = True
                else:
                    scores["bear"] += 2  # Death cross
                    signals["spy_golden_cross"] = False

    # 2. VIX proxy via VXX → crisis
    if "VXX" in prices and "VXX" in data:
        vxx_sma200 = _get_sma("VXX", "sma_200")
        if vxx_sma200 is not None:
            vxx_price = prices["VXX"]
            if vxx_price > vxx_sma200 * 1.5:
                scores["crisis"] += 5  # Strong crisis signal
                signals["vix_extreme"] = True
            elif vxx_price > vxx_sma200 * 1.2:
                scores["crisis"] += 2
                signals["vix_elevated"] = True

    # 3. Dollar store vs luxury → K-shape
    dltr_weak = False
    cost_strong = False
    for sym in ["DLTR", "DG"]:
        if sym in prices and sym in data:
            sma = _get_sma(sym, "sma_200")
            if sma is not None and prices[sym] < sma:
                dltr_weak = True
    for sym in ["COST", "LVMUY"]:
        if sym in prices and sym in data:
            sma = _get_sma(sym, "sma_200")
            if sma is not None and prices[sym] > sma:
                cost_strong = True
    if dltr_weak and cost_strong:
        scores["k_shape"] += 4
        signals["k_shape_divergence"] = True

    # 4. Energy vs tech → rotation
    energy_weak = False
    tech_strong = False
    if "XLE" in prices and "XLE" in data:
        sma = _get_sma("XLE", "sma_200")
        if sma is not None and prices["XLE"] < sma:
            energy_weak = True
    if "QQQ" in prices and "QQQ" in data:
        sma = _get_sma("QQQ", "sma_200")
        if sma is not None and prices["QQQ"] > sma:
            tech_strong = True
    if energy_weak and tech_strong:
        scores["rotation"] += 3
        signals["energy_tech_divergence"] = True

    # 5. Bond trend → rate regime
    if "TLT" in prices and "TLT" in data:
        tlt_sma = _get_sma("TLT", "sma_200")
        if tlt_sma is not None:
            if prices["TLT"] < tlt_sma:
                scores["rotation"] += 1  # Rising rates → sector rotation
                signals["bonds_falling"] = True
            else:
                signals["bonds_falling"] = False

    # Pick highest-scoring regime
    best = max(scores, key=scores.get)
    total = sum(scores.values()) or 1
    confidence = scores[best] / total

    return RegimeSignal(regime=best, confidence=confidence, signals=signals)


# ---------------------------------------------------------------------------
# Strategy Orchestrator
# ---------------------------------------------------------------------------
class AdaptiveRegimeOrchestrator(BasePersona):
    """Meta-strategy: detects regime, activates appropriate sub-strategies.

    Regimes and their strategy allocations:
    - BULL: 70% growth (AI token, subscription monopoly) + 20% momentum + 10% hedge
    - BEAR: 50% defensive (treasury, gold) + 30% L-shape stagnation + 20% cash
    - ROTATION: 40% oil-down-tech-up + 30% bonds-down-banks-up + 30% balanced
    - CRISIS: 40% VIX buyback + 30% gold/bonds + 30% cash
    - K_SHAPE: 40% K-shape economy + 30% wealth barometer + 30% quality
    """

    def __init__(self, universe=None):
        # Combine universes from all sub-strategies we might activate
        combined_universe = list(set([
            # Regime indicators (always loaded)
            "SPY", "QQQ", "VXX", "XLE", "TLT", "DLTR", "DG", "COST",
            # Bull/growth
            "NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "CRM", "NOW", "NFLX", "ADP",
            # Defensive
            "GLD", "SHY", "XLU", "SCHD", "JNJ", "PG",
            # Rotation
            "JPM", "GS", "BAC", "PGR", "ALL",
            # K-shape
            "LVMUY", "LULU", "RH", "UNH", "BX",
            # Crisis/buyback
            "BRK-B", "V", "MA",
            # Midstream (top performer)
            "EPD", "ET", "MPLX", "WMB", "OKE",
        ]))
        config = PersonaConfig(
            name="Adaptive Regime Orchestrator",
            description="Meta-strategy: detects bull/bear/rotation/crisis/K-shape regime, activates best sub-strategies",
            risk_tolerance=0.5,
            max_position_size=0.12,
            max_positions=15,
            rebalance_frequency="weekly",
            universe=universe or combined_universe,
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        regime = detect_regime(date, prices, data)
        weights = {}

        if regime.regime == "bull":
            # Growth + momentum core
            growth_targets = ["NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "CRM", "NOW", "NFLX", "ADP"]
            # Midstream for income
            income_targets = ["EPD", "ET", "MPLX"]
            # Small hedge
            hedge = ["GLD"]

            scored = []
            for sym in growth_targets:
                if sym not in prices:
                    continue
                inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
                if _is_missing(inds.get("sma_200")) or _is_missing(inds.get("rsi_14")):
                    continue
                sc = 0.0
                if prices[sym] > inds["sma_200"]:
                    sc += 2.0
                if inds["sma_50"] is not None and inds["sma_50"] > inds["sma_200"]:
                    sc += 1.0
                if 35 < inds["rsi_14"] < 70:
                    sc += 1.0
                if sc >= 2:
                    scored.append((sym, sc))
            scored.sort(key=lambda x: -x[1])
            if scored:
                total = sum(s for _, s in scored[:10])
                for sym, sc in scored[:10]:
                    weights[sym] = min((sc / total) * 0.70, self.config.max_position_size)
            # Add income + hedge
            for sym in income_targets:
                if sym in prices:
                    weights[sym] = 0.07
            for sym in hedge:
                if sym in prices:
                    weights[sym] = 0.05

        elif regime.regime == "bear":
            # Maximum defense
            defense = {"GLD": 0.20, "SHY": 0.15, "XLU": 0.15, "SCHD": 0.15, "JNJ": 0.10, "PG": 0.10}
            weights = {s: w for s, w in defense.items() if s in prices}

        elif regime.regime == "rotation":
            # Sector rotation: tech + banks (depending on sub-signals)
            if regime.signals.get("energy_tech_divergence"):
                # Oil down → tech up
                tech = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "CRM", "NOW"]
                for sym in tech:
                    if sym in prices:
                        inds = self._get_indicators(data, sym, ["sma_200"], date)
                        if not _is_missing(inds.get("sma_200")) and prices[sym] > inds["sma_200"]:
                            weights[sym] = 0.08
            if regime.signals.get("bonds_falling"):
                # Rates up → banks benefit
                banks = ["JPM", "GS", "BAC", "PGR", "ALL"]
                for sym in banks:
                    if sym in prices:
                        inds = self._get_indicators(data, sym, ["sma_200"], date)
                        if not _is_missing(inds.get("sma_200")) and prices[sym] > inds["sma_200"]:
                            weights[sym] = 0.06

        elif regime.regime == "crisis":
            # Crisis: buyback machines + safe havens
            buyback = ["AAPL", "GOOGL", "META", "MSFT", "BRK-B", "V", "MA"]
            for sym in buyback:
                if sym in prices:
                    inds = self._get_indicators(data, sym, ["rsi_14"], date)
                    rsi = inds.get("rsi_14")
                    if rsi is not None and not _is_missing(rsi) and rsi < 40:
                        weights[sym] = 0.10  # Oversold buyback machine = best entry
                    elif rsi is not None and not _is_missing(rsi) and rsi < 50:
                        weights[sym] = 0.06
            # Safe havens
            weights["GLD"] = weights.get("GLD", 0) + 0.15
            weights["SHY"] = weights.get("SHY", 0) + 0.10

        elif regime.regime == "k_shape":
            # K-shape: long the top arm
            k_targets = ["COST", "LVMUY", "AAPL", "AMZN", "UNH", "BX", "LULU", "RH"]
            scored = []
            for sym in k_targets:
                if sym not in prices:
                    continue
                inds = self._get_indicators(data, sym, ["sma_200", "rsi_14"], date)
                if _is_missing(inds.get("sma_200")) or _is_missing(inds.get("rsi_14")):
                    continue
                sc = 0.0
                if prices[sym] > inds["sma_200"]:
                    sc += 2.0
                if 35 < inds["rsi_14"] < 65:
                    sc += 1.0
                if sc >= 2:
                    scored.append((sym, sc))
            scored.sort(key=lambda x: -x[1])
            if scored:
                total = sum(s for _, s in scored[:8])
                for sym, sc in scored[:8]:
                    weights[sym] = min((sc / total) * 0.80, self.config.max_position_size)
            # Small gold hedge
            if "GLD" in prices:
                weights["GLD"] = 0.10

        # Cap total allocation at 95%
        total_weight = sum(weights.values())
        if total_weight > 0.95:
            scale = 0.95 / total_weight
            weights = {s: w * scale for s, w in weights.items()}

        return weights


# ---------------------------------------------------------------------------
# Conservative version — always keeps 30% in defensive assets
# ---------------------------------------------------------------------------
class ConservativeOrchestrator(BasePersona):
    """Conservative meta-strategy: 70% regime-adaptive + 30% permanent defense.

    Always holds 30% in GLD/SHY/SCHD regardless of regime.
    Remaining 70% allocated by regime detection.
    Lower returns but much lower drawdown.
    """

    def __init__(self, universe=None):
        combined = list(set([
            "SPY", "QQQ", "VXX", "XLE", "TLT", "DLTR", "DG", "COST",
            "NVDA", "AAPL", "MSFT", "GOOGL", "META", "CRM",
            "GLD", "SHY", "SCHD", "XLU", "JNJ", "PG",
            "JPM", "GS", "PGR",
            "EPD", "ET", "MPLX",
            "LVMUY", "UNH", "BRK-B", "V",
        ]))
        config = PersonaConfig(
            name="Conservative Regime Orchestrator",
            description="70% regime-adaptive + 30% permanent defense (GLD/SHY/SCHD). Lower DD, steadier returns.",
            risk_tolerance=0.3,
            max_position_size=0.12,
            max_positions=15,
            rebalance_frequency="weekly",
            universe=universe or combined,
        )
        super().__init__(config)
        self._adaptive = AdaptiveRegimeOrchestrator(universe=combined)

    def generate_signals(self, date, prices, portfolio, data):
        # 30% permanent defense
        defense = {}
        for sym, w in [("GLD", 0.10), ("SHY", 0.10), ("SCHD", 0.10)]:
            if sym in prices:
                defense[sym] = w

        # 70% regime-adaptive
        adaptive_weights = self._adaptive.generate_signals(date, prices, portfolio, data)

        # Scale adaptive to 70%
        total_adaptive = sum(adaptive_weights.values()) or 1
        if total_adaptive > 0.70:
            scale = 0.70 / total_adaptive
            adaptive_weights = {s: w * scale for s, w in adaptive_weights.items()}

        # Merge
        combined = dict(defense)
        for sym, w in adaptive_weights.items():
            combined[sym] = combined.get(sym, 0) + w

        return combined


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
ORCHESTRATOR_STRATEGIES = {
    "adaptive_regime": AdaptiveRegimeOrchestrator,
    "conservative_regime": ConservativeOrchestrator,
}


def get_orchestrated_strategy(name: str, **kwargs) -> BasePersona:
    cls = ORCHESTRATOR_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown orchestrator: {name}. Available: {list(ORCHESTRATOR_STRATEGIES.keys())}")
    return cls(**kwargs)


if __name__ == "__main__":
    print("=== Strategy Orchestrators ===\n")
    for key, cls in ORCHESTRATOR_STRATEGIES.items():
        inst = cls()
        print(f"  {key:25s} | {inst.config.name}")
        print(f"  {'':25s} | {inst.config.description}")
        print(f"  {'':25s} | Universe: {len(inst.config.universe)} tickers")
        print()
