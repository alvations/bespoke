"""Trading persona agents for bespoke.

Each persona implements a trading strategy inspired by a famous trader archetype.
All personas return target portfolio weights via a common interface compatible
with the Backtester.

Personas:
    1. BuffettValue         — Warren Buffett / Benjamin Graham value investing
    2. MomentumTrader       — Trend-following momentum (Druckenmiller style)
    3. MemeStockTrader      — Social sentiment / meme stock (WSB / Reddit style)
    4. DividendInvestor     — Dividend growth (old-school income investing)
    5. QuantStrategist      — Statistical arbitrage / mean reversion (Renaissance style)
    6. FixedIncomeStrat     — Bond / yield curve strategies (PIMCO style)
    7. GrowthInvestor       — Cathie Wood / ARK style high-growth disruptors
    8. SectorRotation       — Sector ETF rotation by momentum
    9. PairsTrader          — Relative value / pairs trading
   10. EnsembleStrategist   — Multi-strategy consensus
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


# ---------------------------------------------------------------------------
# Base persona
# ---------------------------------------------------------------------------

from bespoke.strategies.base import BaseStrategy as BasePersona, StrategyConfig as PersonaConfig

# ---------------------------------------------------------------------------
# 1. Buffett Value Investor
# ---------------------------------------------------------------------------
class BuffettValue(BasePersona):
    """Warren Buffett / Benjamin Graham style value investing.

    Philosophy:
    - Buy wonderful companies at fair prices
    - Low P/E, low P/B, strong moat indicators
    - Use SMA200 as a margin-of-safety filter
    - Concentrate in high-conviction picks
    - Hold for the long term, low turnover

    Signals:
    - BUY: Price below SMA200 AND RSI < 40 (unloved + below long-term avg)
    - HOLD: Price within 10% of SMA200
    - SELL: RSI > 75 (overheated)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Buffett Value",
            description="Deep value investing: buy great companies when they're cheap",
            risk_tolerance=0.3,
            max_position_size=0.20,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "BRK-B", "AAPL", "KO", "JNJ", "PG", "JPM", "BAC",
                "CVX", "XOM", "MRK", "ABBV", "V", "MA", "AXP",
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
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]

            if sma200 is None or rsi is None:
                continue

            # Value score: how far below SMA200 (discount to intrinsic value proxy)
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            # Only buy if trading below long-term average and not overbought
            if discount > 0.0 and rsi < 50:
                score = discount * (50 - rsi) / 50  # Combine discount + RSI
                candidates.append((sym, score))
            elif rsi > 75:
                # Sell overheated positions
                weights[sym] = 0.0

        # Rank by value score, take top N
        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]

        if top:
            # Equal weight among top picks, capped at max_position_size
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, score in top:
                weights[sym] = per_stock
        # Close stale positions for symbols not allocated
        for sym in self.config.universe:
            if sym in prices:
                weights.setdefault(sym, 0.0)

        return weights


# ---------------------------------------------------------------------------
# 2. Momentum Trader
# ---------------------------------------------------------------------------
class MomentumTrader(BasePersona):
    """Trend-following momentum strategy (Druckenmiller / O'Neil style).

    Philosophy:
    - Buy strength, sell weakness
    - Follow the trend — "the trend is your friend"
    - Use MACD crossovers and moving average alignment
    - Cut losses quickly, let winners run

    Signals:
    - BUY: MACD > signal AND price > SMA50 > SMA200 (uptrend alignment)
    - SELL: MACD < signal AND price < SMA50 (momentum breakdown)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Momentum Trader",
            description="Trend-following: buy strength, cut losers fast",
            risk_tolerance=0.7,
            max_position_size=0.20,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN", "TSLA",
                "AVGO", "NFLX", "CRM", "AMD", "PLTR", "CRWD", "SNOW",
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
                ["sma_50", "sma_200", "macd", "macd_signal", "rsi_14"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            rsi = inds["rsi_14"]

            if any(v is None for v in [sma50, sma200, macd, macd_sig, rsi]):
                continue

            # Trend alignment score
            trend_score = 0.0
            if price > sma50:
                trend_score += 1
            if sma50 > sma200:
                trend_score += 1
            if macd > macd_sig:
                trend_score += 1
            if rsi > 50 and rsi < 80:  # Momentum but not overbought
                trend_score += 1

            if trend_score >= 3:
                # Use RSI/100 as tiebreaker for same discrete trend_score
                scored.append((sym, trend_score + rsi / 100))
            elif trend_score <= 1:
                weights[sym] = 0.0  # Exit weak positions

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]

        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        # Close stale positions for symbols not allocated
        for sym in self.config.universe:
            if sym in prices:
                weights.setdefault(sym, 0.0)

        return weights


# ---------------------------------------------------------------------------
# 3. Meme Stock Trader
# ---------------------------------------------------------------------------
class MemeStockTrader(BasePersona):
    """Social sentiment / meme stock trading (WSB / Reddit style).

    Philosophy:
    - High volume surges signal retail interest
    - RSI extremes as entry points (contrarian on dips, momentum on breakouts)
    - Short squeeze candidates: high short interest + volume spike
    - YOLO concentrated positions

    Signals:
    - BUY: Volume > 2x average AND RSI recovering from <30 (dip buy)
          OR Volume > 3x average AND price breaking above SMA20 (breakout)
    - SELL: RSI > 80 OR price drops below SMA20
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Meme Stock Trader",
            description="YOLO: volume spikes, dip buys, short squeezes",
            risk_tolerance=0.95,
            max_position_size=0.30,
            max_positions=5,
            rebalance_frequency="daily",
            universe=universe or [
                "GME", "AMC", "PLTR", "SOFI", "HOOD", "RIVN",
                "COIN", "MARA", "RIOT", "MSTR", "TSLA", "NVDA",
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
                ["rsi_14", "sma_20", "Volume", "volume_sma_20"],
                date,
            )
            rsi = inds["rsi_14"]
            sma20 = inds["sma_20"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]

            if any(v is None for v in [rsi, sma20, volume, vol_avg]):
                continue

            vol_ratio = volume / vol_avg if vol_avg > 0 else 1

            score = 0.0

            # Dip buy: volume spike + oversold
            if vol_ratio > 2 and rsi < 35:
                score = 3.0 + vol_ratio

            # Breakout: massive volume + price above SMA20
            elif vol_ratio > 3 and price > sma20:
                score = 2.0 + vol_ratio

            # Moderate interest
            elif vol_ratio > 1.5 and rsi < 45 and price > sma20:
                score = 1.0 + vol_ratio

            # Exit overheated (takes priority over buy signals)
            if rsi > 80 or (price < sma20 and rsi > 60):
                weights[sym] = 0.0
            elif score > 0:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]

        if top:
            total_score = sum(s for _, s in top)
            cap = self.config.max_position_size
            raw = {sym: (score / total_score) * 0.90 for sym, score in top}
            # Iteratively redistribute clipped excess so budget isn't lost
            remaining = dict(raw)
            while remaining:
                over = {s: w for s, w in remaining.items() if w > cap}
                if not over:
                    break
                excess = sum(w - cap for w in over.values())
                for sym in over:
                    weights[sym] = cap
                    del remaining[sym]
                if not remaining:
                    break
                under_total = sum(remaining.values())
                if under_total <= 0:
                    break
                for sym in remaining:
                    remaining[sym] += excess * (remaining[sym] / under_total)
            for sym, w in remaining.items():
                weights[sym] = min(w, cap)
        # Close stale positions for symbols not allocated
        for sym in self.config.universe:
            if sym in prices:
                weights.setdefault(sym, 0.0)

        return weights


# ---------------------------------------------------------------------------
# 4. Dividend Investor
# ---------------------------------------------------------------------------
class DividendInvestor(BasePersona):
    """Old-school dividend growth investing.

    Philosophy:
    - Buy companies with long dividend histories (Dividend Aristocrats)
    - Focus on dividend yield + growth rate
    - Reinvest dividends (compounding)
    - Very low turnover — buy and hold forever
    - Use price dips as accumulation opportunities

    Signals:
    - BUY: Price near or below SMA200 (accumulate on weakness)
    - HOLD: Always (unless dividend cut)
    - Rarely SELL: Only if price >30% above SMA200 (take some off table)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Dividend Investor",
            description="Buy and hold dividend aristocrats, compound forever",
            risk_tolerance=0.2,
            max_position_size=0.15,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                "JNJ", "PG", "KO", "PEP", "MMM", "T", "VZ",
                "MO", "ABBV", "O", "XOM", "CVX", "IBM", "HD",
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
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]

            if sma200 is None:
                continue

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            # Accumulate on dips, hold otherwise
            if discount > -0.10:  # Within 10% of or below SMA200
                # Score: prefer deeper discounts
                score = max(0, discount + 0.10)
                if rsi is not None and rsi < 40:
                    score += 0.1  # Bonus for oversold
                candidates.append((sym, score + 0.5))  # Base score ensures we hold
            elif discount < -0.30:
                # Way above SMA200 — trim
                weights[sym] = min(0.05, self.config.max_position_size)

        # Rank by score, take top max_positions, equal weight
        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            # Budget accounts for trim allocations so total doesn't exceed 0.95
            trim_total = sum(v for v in weights.values() if v > 0)
            budget = max(0.90 - trim_total, 0.10)
            per_stock = min(budget / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        # Close stale positions for symbols not allocated
        for sym in self.config.universe:
            if sym in prices:
                weights.setdefault(sym, 0.0)

        return weights


# ---------------------------------------------------------------------------
# 5. Quant Strategist
# ---------------------------------------------------------------------------
class QuantStrategist(BasePersona):
    """Statistical/quantitative mean-reversion strategy (Renaissance style).

    Philosophy:
    - Markets are mostly efficient but mean-revert on short timescales
    - Use Bollinger Bands and RSI for mean-reversion signals
    - Volatility-weighted position sizing
    - High turnover, many small bets

    Signals:
    - BUY: Price below lower Bollinger Band AND RSI < 30
    - SELL: Price above upper Bollinger Band AND RSI > 70
    - Size inversely proportional to volatility
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Quant Strategist",
            description="Mean-reversion: buy oversold, sell overbought, size by vol",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="daily",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "JPM", "BAC", "GS",
                "XOM", "CVX", "JNJ", "PG", "KO", "WMT", "HD",
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
                data, sym,
                ["bb_upper", "bb_lower", "rsi_14", "vol_20", "sma_20"],
                date,
            )
            bb_upper = inds["bb_upper"]
            bb_lower = inds["bb_lower"]
            rsi = inds["rsi_14"]
            vol = inds["vol_20"]
            sma20 = inds["sma_20"]

            if any(v is None for v in [bb_upper, bb_lower, rsi, vol, sma20]):
                continue

            # Multi-factor mean reversion + momentum signals
            z_score = (sma20 - price) / (vol * price) if vol > 0 and price > 0 else 0

            if price < bb_lower and rsi < 35:
                # Strong mean reversion: deeply oversold
                candidates.append((sym, max(z_score, 0.1) + 2.0, vol))
            elif price < bb_lower and rsi < 45:
                # Moderate mean reversion: below lower band, not extreme
                candidates.append((sym, max(z_score, 0.1) + 1.0, vol))
            elif price < sma20 and rsi < 40:
                # Mild reversion: below SMA20, oversold
                candidates.append((sym, max(z_score * 0.5, 0.05) + 0.5, vol))

            elif price > bb_upper and rsi > 70:
                # Overbought — close position
                weights[sym] = 0.0

        # Vol-weighted sizing with cap redistribution
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            top = candidates[:self.config.max_positions]
            total_inv_vol = sum(1 / max(v, 0.005) for _, _, v in top)
            cap = self.config.max_position_size
            raw = {}
            for sym, score, vol in top:
                inv_vol = 1 / max(vol, 0.005)
                raw[sym] = (inv_vol / total_inv_vol) * 0.85
            # Iteratively redistribute clipped excess so budget isn't lost
            remaining = dict(raw)
            while remaining:
                over = {s: w for s, w in remaining.items() if w > cap}
                if not over:
                    break
                excess = sum(w - cap for w in over.values())
                for sym in over:
                    weights[sym] = cap
                    del remaining[sym]
                if not remaining:
                    break
                under_total = sum(remaining.values())
                if under_total <= 0:
                    break
                for sym in remaining:
                    remaining[sym] += excess * (remaining[sym] / under_total)
            for sym, w in remaining.items():
                weights[sym] = min(w, cap)
        # Close stale positions for symbols not allocated
        for sym in self.config.universe:
            if sym in prices:
                weights.setdefault(sym, 0.0)

        return weights


# ---------------------------------------------------------------------------
# 6. Fixed Income Strategist
# ---------------------------------------------------------------------------
class FixedIncomeStrat(BasePersona):
    """Bond / yield curve strategy (PIMCO / Gundlach style).

    Philosophy:
    - Use bond ETFs as instruments (TLT, IEF, SHY, LQD, HYG, TIP)
    - Duration management based on yield curve signals
    - Go long duration when curve inverts (recession signal → rates will fall)
    - Go short duration when curve steepens
    - Credit spread trades: HYG vs LQD based on risk appetite

    Signals (using price action of bond ETFs as proxy):
    - Long TLT when SMA50 > SMA200 (bond uptrend = rates falling)
    - Long SHY when TLT trending down (flight to short duration)
    - Long HYG when RSI recovering and momentum positive (risk-on)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Fixed Income Strategist",
            description="Bond duration/credit strategies via ETFs",
            risk_tolerance=0.3,
            max_position_size=0.35,
            max_positions=5,
            rebalance_frequency="weekly",
            universe=universe or ["TLT", "IEF", "SHY", "LQD", "HYG", "TIP", "BND", "AGG"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        tradeable = set(prices.keys())

        # Assess TLT trend (long-term bonds)
        tlt_inds = self._get_indicators(
            data, "TLT", ["sma_50", "sma_200", "rsi_14"], date,
        )
        tlt_sma50 = tlt_inds["sma_50"]
        tlt_sma200 = tlt_inds["sma_200"]
        tlt_price = prices.get("TLT")
        tlt_rsi = tlt_inds["rsi_14"]

        # Assess HYG (high yield = risk appetite)
        hyg_inds = self._get_indicators(
            data, "HYG", ["macd", "macd_signal", "rsi_14"], date,
        )
        hyg_macd = hyg_inds["macd"]
        hyg_sig = hyg_inds["macd_signal"]
        hyg_rsi = hyg_inds["rsi_14"]

        # Rate direction filter: detect if rates are rising aggressively
        # (TLT in strong downtrend = rates rising fast)
        rates_rising_fast = (
            tlt_price is not None and tlt_sma50 is not None
            and tlt_sma200 is not None
            and tlt_price < tlt_sma50 < tlt_sma200
        )

        # Duration allocation
        if tlt_sma50 is not None and tlt_sma200 is not None and tlt_price is not None:
            if tlt_sma50 > tlt_sma200:
                # Bond uptrend — rates falling, go long duration
                weights["TLT"] = 0.35
                weights["IEF"] = 0.20
                weights["SHY"] = 0.10
            elif rates_rising_fast:
                # Rates rising aggressively — heavy short duration + TIPS
                weights["SHY"] = 0.35
                weights["TIP"] = 0.20
                weights["IEF"] = 0.10
                weights["TLT"] = 0.0
            elif tlt_price < tlt_sma50:
                # Rates rising moderately — shorten duration
                weights["SHY"] = 0.35
                weights["IEF"] = 0.20
                weights["TLT"] = 0.05
            else:
                # Neutral — barbell
                weights["TLT"] = 0.15
                weights["SHY"] = 0.25
                weights["IEF"] = 0.15
        else:
            # Fallback when indicators unavailable: balanced allocation
            weights["SHY"] = 0.25
            weights["IEF"] = 0.20
            weights["BND"] = 0.15

        # Credit allocation
        if hyg_macd is not None and hyg_sig is not None:
            if hyg_macd > hyg_sig and hyg_rsi is not None and hyg_rsi > 40:
                # Risk-on: prefer high yield
                weights["HYG"] = 0.15
                weights["LQD"] = 0.10
            else:
                # Risk-off: prefer investment grade
                weights["LQD"] = 0.20
                weights["HYG"] = 0.0
        else:
            # Fallback: modest IG allocation
            weights.setdefault("LQD", 0.10)

        # Inflation protection: always hold some TIPS, more when bonds oversold
        if tlt_rsi is not None and tlt_rsi < 30:
            weights["TIP"] = weights.get("TIP", 0) + 0.10
        else:
            weights.setdefault("TIP", 0.05)

        # Only return weights for symbols in our universe that are actually tradeable
        universe = set(self.config.universe)
        cap = self.config.max_position_size
        result = {sym: min(w, cap) for sym, w in weights.items()
                  if sym in tradeable and sym in universe}
        # Close stale positions for universe symbols not allocated
        for sym in universe:
            if sym in tradeable:
                result.setdefault(sym, 0.0)
        return result


# ---------------------------------------------------------------------------
# 7. Growth Investor
# ---------------------------------------------------------------------------
class GrowthInvestor(BasePersona):
    """Cathie Wood / ARK style growth & disruption investing.

    Philosophy:
    - Invest in disruptive innovation
    - High growth > current profitability
    - Buy on dips in high-conviction names
    - Willing to hold through volatility
    - Concentrated portfolio

    Signals:
    - BUY: Price near SMA50 support + RSI 35-55 (buying the dip in uptrend)
    - HOLD: Price > SMA50
    - SELL: Price breaks below SMA200 (thesis broken)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Growth Investor",
            description="Disruptive innovation: high growth, buy dips in uptrends",
            risk_tolerance=0.8,
            max_position_size=0.20,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "TSLA", "PLTR", "COIN", "SHOP", "SQ", "ROKU", "CRWD",
                "DDOG", "NET", "SNOW", "ENPH", "MELI", "SE", "RBLX",
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
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]

            if any(v is None for v in [sma50, sma200, rsi]):
                continue

            # Thesis broken — full exit
            if price < sma200 * 0.95:
                weights[sym] = 0.0
                continue

            # Overbought — take profits
            if rsi > 80:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Buy the dip in uptrend
            if price > sma200 and 30 < rsi < 55:
                proximity_to_sma50 = abs(price - sma50) / sma50 if sma50 > 0 else 1.0
                if proximity_to_sma50 < 0.05:  # Near SMA50 support
                    score = 3.0
                elif price > sma50:
                    score = 2.0
                else:
                    score = 1.0

                if macd is not None and macd_sig is not None and macd > macd_sig:
                    score += 1.0

            if score > 0:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]

        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        # Close stale positions for symbols not allocated
        for sym in self.config.universe:
            if sym in prices:
                weights.setdefault(sym, 0.0)

        return weights


# ---------------------------------------------------------------------------
# 8. Sector Rotation Strategist
# ---------------------------------------------------------------------------
class SectorRotation(BasePersona):
    """Sector rotation strategy — rotate into strongest sectors.

    Philosophy:
    - Different sectors lead at different economic cycle stages
    - Momentum in sector ETFs predicts continued outperformance
    - Overweight top 3 sectors, underweight bottom 3
    - Weekly rotation to capture sector trends

    Signals:
    - Rank sectors by 1-month momentum (price / SMA20)
    - Go long top 3 sectors with momentum > 1
    - Exit sectors with momentum < 0.97 (below SMA20 by 3%)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Sector Rotation",
            description="Rotate into strongest sector ETFs, fade weakest",
            risk_tolerance=0.5,
            max_position_size=0.25,
            max_positions=4,
            rebalance_frequency="weekly",
            universe=universe or [
                "XLK", "XLF", "XLE", "XLV", "XLI", "XLP", "XLU",
                "XLRE", "XLC", "XLB", "XLY",
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
                data, sym, ["sma_20", "sma_50", "rsi_14"], date,
            )
            sma20 = inds["sma_20"]
            sma50 = inds["sma_50"]
            rsi = inds["rsi_14"]

            if sma20 is None or sma50 is None:
                continue

            # Overbought — exit overheated sectors
            if rsi is not None and rsi > 75:
                weights[sym] = 0.0
                continue

            # Momentum score: how far above SMA20
            momentum = price / sma20 if sma20 > 0 else 1.0
            trend = 1.0 if price > sma50 else 0.0

            if momentum > 1.0:
                score = momentum + trend
                if rsi is not None and 40 < rsi < 75:
                    score += 0.2  # Bonus for healthy RSI
                scored.append((sym, score))
            elif momentum < 0.97:
                weights[sym] = 0.0  # Exit weak sectors

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]

        if top:
            total_score = sum(s for _, s in top)
            cap = self.config.max_position_size
            raw = {sym: (score / total_score) * 0.90 for sym, score in top}
            # Iteratively redistribute clipped excess so budget isn't lost
            remaining = dict(raw)
            while remaining:
                over = {s: w for s, w in remaining.items() if w > cap}
                if not over:
                    break
                excess = sum(w - cap for w in over.values())
                for sym in over:
                    weights[sym] = cap
                    del remaining[sym]
                if not remaining:
                    break
                under_total = sum(remaining.values())
                if under_total <= 0:
                    break
                for sym in remaining:
                    remaining[sym] += excess * (remaining[sym] / under_total)
            for sym, w in remaining.items():
                weights[sym] = min(w, cap)
        # Close stale positions for symbols not allocated
        for sym in self.config.universe:
            if sym in prices:
                weights.setdefault(sym, 0.0)

        return weights


# ---------------------------------------------------------------------------
# 9. Pairs / Relative Value Trader
# ---------------------------------------------------------------------------
class PairsTrader(BasePersona):
    """Pairs trading / relative value strategy.

    Philosophy:
    - Trade relative performance between correlated assets
    - When the spread deviates, mean-revert by going long the laggard
      and overweighting vs the leader
    - Classic pairs: XOM/CVX, KO/PEP, JPM/BAC, GOOGL/META

    Signals:
    - For each pair, compute relative strength (RSI of ratio)
    - Overweight the underperformer when ratio RSI < 30
    - Overweight the outperformer when ratio RSI > 70 (trend)
    """

    PAIRS = [
        ("XOM", "CVX"),
        ("KO", "PEP"),
        ("JPM", "BAC"),
        ("GOOGL", "META"),
        ("AAPL", "MSFT"),
        ("V", "MA"),
        ("HD", "LOW"),
    ]

    def __init__(self, universe: list[str] | None = None):
        all_syms = list(dict.fromkeys(s for pair in self.PAIRS for s in pair))
        config = PersonaConfig(
            name="Pairs Trader",
            description="Relative value: long laggard vs leader in correlated pairs",
            risk_tolerance=0.4,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or all_syms,
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        universe = set(self.config.universe)

        for sym_a, sym_b in self.PAIRS:
            if sym_a not in prices or sym_b not in prices:
                continue
            if sym_a not in universe or sym_b not in universe:
                continue

            price_a = prices[sym_a]
            price_b = prices[sym_b]
            rsi_a = self._get_indicator(data, sym_a, "rsi_14", date)
            rsi_b = self._get_indicator(data, sym_b, "rsi_14", date)

            if rsi_a is None or rsi_b is None:
                continue

            # Exit overbought symbols
            if rsi_a > 80:
                weights[sym_a] = 0.0
            if rsi_b > 80:
                weights[sym_b] = 0.0
            if rsi_a > 80 or rsi_b > 80:
                continue

            # Mean reversion in the pair — use max() so later pairs don't
            # silently downgrade allocations from earlier pairs
            if rsi_a < 35 and rsi_b > 55:
                # A oversold relative to B — overweight A
                weights[sym_a] = max(weights.get(sym_a, 0), self.config.max_position_size)
                weights[sym_b] = max(weights.get(sym_b, 0), self.config.max_position_size * 0.5)
            elif rsi_b < 35 and rsi_a > 55:
                # B oversold relative to A — overweight B
                weights[sym_b] = max(weights.get(sym_b, 0), self.config.max_position_size)
                weights[sym_a] = max(weights.get(sym_a, 0), self.config.max_position_size * 0.5)
            else:
                # Neutral — equal weight both
                weights[sym_a] = weights.get(sym_a, 0) + 0.06
                weights[sym_b] = weights.get(sym_b, 0) + 0.06

        # Enforce per-position cap
        cap = self.config.max_position_size
        weights = {k: min(v, cap) for k, v in weights.items()}

        # Enforce max_positions: keep top N positive weights + all exits
        positive = [(s, w) for s, w in weights.items() if w > 0]
        if len(positive) > self.config.max_positions:
            positive.sort(key=lambda x: x[1], reverse=True)
            positive = positive[:self.config.max_positions]
        exits = [(s, w) for s, w in weights.items() if w <= 0]
        weights = dict(positive + exits)

        # Cap total exposure
        total = sum(weights.values())
        if total > 0.95:
            scale = 0.95 / total
            weights = {k: v * scale for k, v in weights.items()}

        # Close stale positions for symbols not allocated
        for sym in self.config.universe:
            if sym in prices:
                weights.setdefault(sym, 0.0)

        return weights


# ---------------------------------------------------------------------------
# 10. Ensemble Strategist
# ---------------------------------------------------------------------------
class EnsembleStrategist(BasePersona):
    """Ensemble strategy combining signals from multiple personas.

    Philosophy:
    - Diversification across strategy types reduces drawdowns
    - Weight strategies by their Sharpe ratio (or equal-weight)
    - Only take positions where multiple strategies agree
    - Uses Momentum, Growth, Buffett, and QuantMR for coverage

    Signals:
    - Run all sub-strategies
    - Take consensus positions (2+ strategies agree)
    - Weight by number of agreeing strategies
    """

    def __init__(self, universe: list[str] | None = None):
        # Create sub-strategies once — with custom universe if provided
        subs = [
            (MomentumTrader(universe=universe), 0.35),   # Best Sharpe
            (GrowthInvestor(universe=universe), 0.25),
            (BuffettValue(universe=universe), 0.25),
            (DividendInvestor(universe=universe), 0.15),
        ]
        if universe is None:
            # Build union universe from sub-strategy defaults
            all_syms = list(dict.fromkeys(
                sym for s, _ in subs for sym in s.config.universe
            ))
            # Expand each sub-strategy to the full union universe
            for s, _ in subs:
                s.config.universe = all_syms
        else:
            all_syms = universe
        config = PersonaConfig(
            name="Ensemble Strategist",
            description="Multi-strategy consensus: momentum + value + growth + dividend",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=all_syms,
        )
        super().__init__(config)
        self._sub_strategies = subs

    def generate_signals(self, date, prices, portfolio, data):
        # Collect signals from all sub-strategies
        all_signals = []
        for strategy, weight in self._sub_strategies:
            try:
                signals = strategy.generate_signals(date, prices, portfolio, data)
                all_signals.append((signals, weight))
            except Exception:
                pass

        if not all_signals:
            return {sym: 0.0 for sym in self.config.universe if sym in prices}

        # Aggregate: weighted average of signals
        # Distinguish between explicit exits (strategy returned 0.0 for a
        # symbol it specifically evaluated) and neutral (symbol absent from
        # strategy output means the strategy had no opinion).
        combined = {}
        for signals, weight in all_signals:
            for sym, w in signals.items():
                if sym not in combined:
                    combined[sym] = {"total_weight": 0.0, "signal_count": 0,
                                     "explicit_exit": 0}
                if w > 0:
                    combined[sym]["total_weight"] += w * weight
                    combined[sym]["signal_count"] += 1
                # Only count as explicit exit if the strategy specifically
                # set 0.0 for this symbol (not just absent from output)
                elif w == 0.0:
                    combined[sym]["explicit_exit"] += 1

        # Take positions where 1+ strategies have a buy signal
        # (requiring 2+ consensus was too strict with 4 diverse strategies)
        weights = {}
        n_ran = len(all_signals)
        for sym, info in combined.items():
            if info["signal_count"] >= 1 and info["signal_count"] >= info["explicit_exit"]:
                # Scale weight by consensus strength
                consensus_factor = info["signal_count"] / n_ran
                w = min(info["total_weight"] * consensus_factor,
                        self.config.max_position_size)
                weights[sym] = w
            elif info["explicit_exit"] >= 3:
                weights[sym] = 0.0  # Strong consensus exit (3+ out of 4)

        # Enforce max_positions: keep top N positive weights + all exits
        positive = sorted(
            ((s, w) for s, w in weights.items() if w > 0),
            key=lambda x: x[1], reverse=True,
        )
        exits = [(s, w) for s, w in weights.items() if w <= 0]
        if len(positive) > self.config.max_positions:
            positive = positive[:self.config.max_positions]
        weights = dict(positive + exits)

        # Normalize if over-allocated
        total = sum(v for v in weights.values() if v > 0)
        if total > 0.95:
            scale = 0.95 / total
            weights = {k: v * scale if v > 0 else v for k, v in weights.items()}

        # Close stale positions for symbols not allocated
        for sym in self.config.universe:
            if sym in prices:
                weights.setdefault(sym, 0.0)

        return weights


# ---------------------------------------------------------------------------
# Persona registry
# ---------------------------------------------------------------------------
ALL_PERSONAS = {
    "buffett_value": BuffettValue,
    "momentum": MomentumTrader,
    "meme_stock": MemeStockTrader,
    "dividend": DividendInvestor,
    "quant": QuantStrategist,
    "fixed_income": FixedIncomeStrat,
    "growth": GrowthInvestor,
    "sector_rotation": SectorRotation,
    "pairs": PairsTrader,
    "ensemble": EnsembleStrategist,
}


def get_persona(name: str, **kwargs) -> BasePersona:
    """Get a persona by name."""
    cls = ALL_PERSONAS.get(name)
    if cls is None:
        raise ValueError(f"Unknown persona: {name}. Available: {list(ALL_PERSONAS.keys())}")
    return cls(**kwargs)


def list_personas() -> list[dict[str, object]]:
    """List all available personas."""
    result = []
    for key, cls in ALL_PERSONAS.items():
        instance = cls()
        result.append({
            "key": key,
            "name": instance.config.name,
            "description": instance.config.description,
            "risk_tolerance": instance.config.risk_tolerance,
            "rebalance_frequency": instance.config.rebalance_frequency,
            "universe_size": len(instance.config.universe),
        })
    return result


if __name__ == "__main__":
    print("=== Available Trading Personas ===\n")
    for p in list_personas():
        print(f"  {p['key']:20s} | {p['name']:25s} | Risk: {p['risk_tolerance']:.1f} | {p['description']}")
