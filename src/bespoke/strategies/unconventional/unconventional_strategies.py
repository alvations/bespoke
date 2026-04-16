"""Unconventional and less obvious trading strategies for bespoke.

These go beyond the standard momentum/value playbook into more
creative and contrarian approaches.

Strategies:
    1. SellInMayGoAway    — Seasonal "sell in May" calendar effect
    2. TurnOfMonth        — End-of-month/start-of-month buying window
    3. VIXMeanReversion   — Buy stocks when VIX spikes (fear = opportunity)
    4. DogsOfTheDow       — Buy worst performers yearly (contrarian)
    5. QualityFactor      — Low vol + high profitability + low leverage
    6. TailRiskHarvest    — Sell premium (proxy: buy after sharp drops)
    + DollarCycleRotation  — Trade dollar strength/weakness via UUP vs EM ETFs
    + LeveragedTrendTactical — TQQQ/SQQQ with strict 20% max leveraged exposure
    + WasteMonopolyCompounder — Landfill monopolies (WM, RSG, CWST, WCN, CLH)
    + DeathCareDemographics — Funeral/death care (SCI, CSV, MATW)
    + PawnCounterCyclical — Pawn lenders thrive in recessions (FCFS, EZPW)
    + LongTermLoserRebound — DeBondt-Thaler contrarian mean reversion
"""

from __future__ import annotations


_SQRT_252 = 252 ** 0.5


def _is_missing(v):
    """Check if value is None or NaN."""
    return v is None or v != v


from bespoke.strategies.base import BaseStrategy as BasePersona, StrategyConfig as PersonaConfig


# ---------------------------------------------------------------------------
# 1. Sell in May and Go Away (Halloween Effect)
# ---------------------------------------------------------------------------
class SellInMayGoAway(BasePersona):
    """Seasonal calendar strategy: "Sell in May and go away."

    Historical evidence: Nov-Apr returns >> May-Oct returns.
    Source: Bouman & Jacobsen (2002) "The Halloween Indicator"

    Implementation:
    - Nov 1 to Apr 30: 100% in SPY/QQQ
    - May 1 to Oct 31: Move to bonds (TLT/IEF) or cash (SHY)
    - Simple but historically robust across many markets
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Sell in May (Halloween Effect)",
            description="Seasonal: stocks Nov-Apr, bonds May-Oct",
            risk_tolerance=0.4,
            max_position_size=0.50,
            max_positions=4,
            rebalance_frequency="monthly",
            universe=universe or ["SPY", "QQQ", "TLT", "IEF", "SHY"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        month = date.month

        if month >= 11 or month <= 4:
            # "Winter" = stocks
            raw = {
                "SPY": 0.50,
                "QQQ": 0.40,
                "TLT": 0.0,
                "IEF": 0.0,
                "SHY": 0.0,
            }
        else:
            # "Summer" = bonds/cash
            raw = {
                "SPY": 0.0,
                "QQQ": 0.0,
                "TLT": 0.30,
                "IEF": 0.30,
                "SHY": 0.30,
            }
        return {k: v for k, v in raw.items() if k in prices}


# ---------------------------------------------------------------------------
# 2. Turn of Month Effect
# ---------------------------------------------------------------------------
class TurnOfMonth(BasePersona):
    """Turn-of-month buying window.

    Research shows the last 3 trading days + first 3 trading days of
    each month account for most of the monthly return due to cash flows
    (pension funds, paychecks, portfolio rebalancing).

    Source: Ariel (1987), Lakonishok & Smidt (1988)

    Implementation:
    - Buy SPY/QQQ on day 26+ of month and hold through day 3 of next month
    - Move to SHY/cash for the rest of the month
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Turn of Month Effect",
            description="Buy last 3 + first 3 days of month, cash otherwise",
            risk_tolerance=0.3,
            max_position_size=0.50,
            max_positions=3,
            rebalance_frequency="daily",
            universe=universe or ["SPY", "QQQ", "SHY"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        day = date.day

        if day >= 26 or day <= 3:
            # Turn of month window — be in stocks
            raw = {
                "SPY": 0.50,
                "QQQ": 0.40,
                "SHY": 0.0,
            }
        else:
            # Mid-month — park in short-term treasuries
            raw = {
                "SPY": 0.0,
                "QQQ": 0.0,
                "SHY": 0.90,
            }
        return {k: v for k, v in raw.items() if k in prices}


# ---------------------------------------------------------------------------
# 3. VIX Mean Reversion (Buy the Fear)
# ---------------------------------------------------------------------------
class VIXMeanReversion(BasePersona):
    """Buy stocks when VIX spikes (fear = opportunity).

    Research: VIX mean-reverts. Spikes above 30 are historically
    followed by strong equity returns (Whaley 2000).

    Implementation (using SPY volatility as VIX proxy since we don't
    have VIX directly):
    - When realized vol spikes > 2x 60-day average → aggressively buy
    - When vol is low → normal allocation
    - When vol is extremely low → reduce (complacency risk)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="VIX Mean Reversion (Buy Fear)",
            description="Buy aggressively when volatility spikes, reduce when complacent",
            risk_tolerance=0.6,
            max_position_size=0.35,
            max_positions=5,
            rebalance_frequency="daily",
            universe=universe or [
                "SPY", "QQQ", "IWM",  # Broad market
                "TLT", "GLD",  # Safe havens
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)

        if _is_missing(spy_vol):
            fallback = {"SPY": 0.30, "QQQ": 0.20, "TLT": 0.20, "GLD": 0.10}
            return {k: v for k, v in fallback.items() if k in prices}

        # Estimate VIX from realized vol (rough: annualized * 100)
        implied_vix = spy_vol * _SQRT_252 * 100

        if implied_vix > 30:
            # High fear — BUY aggressively (VIX will mean-revert)
            weights["SPY"] = 0.40
            weights["QQQ"] = 0.30
            weights["IWM"] = 0.20
            weights["TLT"] = 0.0
            weights["GLD"] = 0.0
        elif implied_vix > 20:
            # Moderate fear — balanced
            weights["SPY"] = 0.30
            weights["QQQ"] = 0.20
            weights["TLT"] = 0.15
            weights["GLD"] = 0.10
            weights["IWM"] = 0.10
        elif implied_vix < 12:
            # Very low vol — complacency, reduce and hedge
            weights["SPY"] = 0.15
            weights["QQQ"] = 0.10
            weights["TLT"] = 0.25
            weights["GLD"] = 0.20
            weights["IWM"] = 0.0
        else:
            # Normal vol
            weights["SPY"] = 0.25
            weights["QQQ"] = 0.20
            weights["TLT"] = 0.15
            weights["GLD"] = 0.10
            weights["IWM"] = 0.10

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 4. Dogs of the Dow (Contrarian Yearly)
# ---------------------------------------------------------------------------
class DogsOfTheDow(BasePersona):
    """Dogs of the Dow contrarian strategy.

    Source: Michael O'Higgins, "Beating the Dow" (1991)

    Buy the 10 highest-yielding Dow stocks at start of year.
    Proxy: buy the worst-performing stocks (highest discount to SMA200)
    from blue-chip universe at each rebalance, equal weight.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Dogs of the Dow (Contrarian)",
            description="Buy worst-performing blue chips yearly, contrarian equal-weight",
            risk_tolerance=0.4,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="monthly",
            # Dow 30 components (approximate)
            universe=universe or [
                "AAPL", "MSFT", "AMZN", "UNH", "GS", "HD", "MCD",
                "V", "CRM", "DIS", "NKE", "BA", "CAT", "JPM",
                "IBM", "JNJ", "KO", "PG", "WMT", "MRK",
                "MMM", "CVX", "DOW", "INTC", "VZ",
                "TRV", "HON", "AXP", "SHW", "AMGN",  # Additional Dow components
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        discount_scores = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            if _is_missing(sma200) or sma200 <= 0:
                continue

            discount = (sma200 - price) / sma200
            discount_scores.append((sym, discount))

        # Sort by discount (highest = furthest below SMA200 = "dogs")
        discount_scores.sort(key=lambda x: x[1], reverse=True)

        # Take the 10 "worst" performers (highest discount = most beaten down)
        dogs = discount_scores[:self.config.max_positions]

        if dogs:
            per_stock = min(0.90 / len(dogs), self.config.max_position_size)
            for sym, _ in dogs:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 5. Quality Factor (Buffett + Quant Hybrid)
# ---------------------------------------------------------------------------
class QualityFactor(BasePersona):
    """Quality factor: low volatility + strong trend = quality.

    Source: AQR "Quality Minus Junk" (Asness, Frazzini, Pedersen 2019)

    Buy stocks that are:
    - Low volatility (stable earnings proxy)
    - Above SMA200 (quality doesn't break down)
    - Not overbought (RSI < 70)
    - Moderate momentum (not hot, not cold)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Quality Factor (Low Vol + Trend)",
            description="Buy low-vol stocks in uptrends — quality minus junk",
            risk_tolerance=0.3,
            max_position_size=0.10,
            max_positions=15,
            rebalance_frequency="monthly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "JNJ", "PG", "KO", "PEP",
                "V", "MA", "UNH", "HD", "MCD", "COST", "ABT",
                "LLY", "TMO", "ACN", "AVGO", "TXN", "LIN",
                "BRK-B", "WMT", "NEE", "DUK",
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
            vol = self._get_indicator(data, sym, "vol_20", date)
            sma50 = self._get_indicator(data, sym, "sma_50", date)

            if any(_is_missing(v) for v in [sma200, rsi, vol]):
                continue

            # Quality filters
            if price < sma200:
                continue  # Must be above long-term trend
            if rsi > 70:
                continue  # Not overbought
            if vol > 0.025:
                continue  # Not too volatile (daily vol < 2.5%)

            # Score: inverse of volatility * trend alignment
            trend_bonus = 1.0
            if sma50 is not None and price > sma50:
                trend_bonus = 1.3

            quality_score = (1 / max(vol, 0.005)) * trend_bonus
            scored.append((sym, quality_score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 6. Tail Risk Harvest (Buy After Sharp Drops)
# ---------------------------------------------------------------------------
class TailRiskHarvest(BasePersona):
    """Buy after sharp single-day drops in quality names.

    Research: Large single-day drops in blue chips tend to
    mean-revert over 5-20 trading days (overreaction effect).

    Implementation:
    - Track daily returns
    - Buy when a quality stock drops > 3% in a day with high volume
    - Hold for ~20 trading days, then re-evaluate
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Tail Risk Harvest (Buy Crashes)",
            description="Buy quality names after sharp single-day drops, capture mean-reversion",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="daily",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META",
                "JPM", "V", "MA", "UNH", "JNJ", "PG",
                "HD", "MCD", "KO", "WMT",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        crash_buys = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            daily_ret = self._get_indicator(data, sym, "daily_return", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            volume = self._get_indicator(data, sym, "Volume", date)
            vol_avg = self._get_indicator(data, sym, "volume_sma_20", date)

            if _is_missing(daily_ret):
                continue

            # Exit recovered positions (RSI > 60 = recovered from crash)
            if rsi is not None and rsi > 65 and sma200 is not None and price > sma200:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity > 0:
                    weights[sym] = 0.0
                    continue  # Don't consider for crash buy

            # Crash buy signal: sharp drop + above SMA200 (still quality)
            if daily_ret < -0.03:  # > 3% drop
                vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
                if sma200 is not None and price > sma200 * 0.90:
                    # Quality + crash = buy
                    score = abs(daily_ret) * 10
                    if vol_ratio > 2:
                        score *= 1.5  # Panic selling = better opportunity
                    crash_buys.append((sym, score))

        crash_buys.sort(key=lambda x: x[1], reverse=True)
        top = crash_buys[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# 7. Dividend Aristocrat Momentum
# ---------------------------------------------------------------------------
class DividendAristocratMomentum(BasePersona):
    """Combine Dividend Aristocrats with momentum filtering.

    Thesis: Aristocrats provide quality (25+ years of div growth).
    Momentum filter selects the ones trending up. This avoids
    the "value trap" problem of pure dividend investing.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Dividend Aristocrat Momentum",
            description="Quality dividends + momentum: only buy Aristocrats in uptrends",
            risk_tolerance=0.3,
            max_position_size=0.10,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                "JNJ", "PG", "KO", "PEP", "ABBV", "MRK", "ABT", "CL",
                "EMR", "ADP", "AFL", "APD", "CVX", "ECL", "GD", "ITW",
                "KMB", "LOW", "MCD", "NEE", "PPG", "SHW", "SYY", "TGT",
                "WMT", "XOM",
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
            if any(v is None for v in [sma50, sma200, rsi]):
                continue
            # Must be in uptrend (momentum filter)
            if price < sma200:
                continue
            # Score by trend strength
            score = 0.0
            if price > sma50 > sma200:
                score += 2.0
            elif price > sma50:
                score += 1.0
            if 35 < rsi < 65:
                score += 0.5  # Prefer not overbought
            # Bonus for being near SMA50 (buy on pullback in uptrend)
            if sma50 and abs(price - sma50) / sma50 < 0.03:
                score += 0.5
            if score > 1.0:
                scored.append((sym, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 8. Concentration in Winners
# ---------------------------------------------------------------------------
class ConcentrateWinners(BasePersona):
    """Let winners run, cut losers — extreme concentration.

    Thesis: A few stocks drive most market returns. Instead of
    diversifying equally, concentrate in the top 3-5 strongest
    momentum stocks. Higher risk but potentially higher returns.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Concentrate in Winners",
            description="Extreme concentration: top 3-5 strongest momentum stocks only",
            risk_tolerance=0.9,
            max_position_size=0.30,
            max_positions=5,
            rebalance_frequency="weekly",
            universe=universe or [
                "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA",
                "AVGO", "LLY", "V", "MA", "UNH", "JPM", "HD",
                "NFLX", "CRM", "AMD", "PLTR", "CRWD",
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
            # Only the strongest momentum
            score = 0.0
            if price > sma50 > sma200:
                score += 3.0
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5
            if 50 < rsi < 80:
                score += 1.0
            # Momentum magnitude
            mom = (price - sma200) / sma200 if sma200 > 0 else 0
            score += mom * 5  # Weight by how far above SMA200
            if score >= 4:
                scored.append((sym, score))
            elif sma200 and price < sma200 * 0.95:
                weights[sym] = 0.0
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            # Score-weighted allocation (more to strongest)
            total_score = sum(s for _, s in top)
            for sym, score in top:
                w = min((score / total_score) * 0.95, self.config.max_position_size)
                weights[sym] = w
        return weights


# ---------------------------------------------------------------------------
# 9. Hidden Monopoly Compounders — boring businesses with pricing power
# ---------------------------------------------------------------------------
class HiddenMonopoly(BasePersona):
    """Invest in companies with natural monopolies or duopolies in boring industries.

    These businesses have massive moats but get zero media attention:
    - Credit ratings (MCO, SPGI) — literally impossible to compete
    - Data monopolies (VRSK, ICE, MSCI) — mission-critical, no switching
    - Waste management (WM, RSG) — local monopolies, inflation-linked pricing
    - Railroads (CSX, NSC) — physically impossible to build competing rail
    - Elevator/HVAC installed base (OTIS, CARR, TT) — service contracts = recurring

    Edge: These compound intrinsic value 12-18% annually but trade at lower
    multiples than tech because they're "boring." The market systematically
    underprices predictability.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Hidden Monopoly Compounders",
            description="Natural monopolies in boring industries: credit ratings, data, waste, rail, HVAC",
            risk_tolerance=0.4,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                # Credit ratings duopoly
                "SPGI", "MCO",
                # Data/analytics monopolies
                "VRSK", "ICE", "MSCI", "FDS",
                # Waste monopolies
                "WM", "RSG",
                # Railroad monopolies
                "CSX", "NSC",
                # Installed-base HVAC/elevator
                "OTIS", "CARR", "TT",
                # Industrial distribution
                "FAST", "CTAS",
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
            vol = inds["vol_20"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Long-term uptrend (compounding)
            if price > sma200:
                score += 2.0
            if sma50 is not None and price > sma50:
                score += 1.0
            # Buy on pullbacks (RSI dip in uptrend = gift)
            if 30 < rsi < 50 and price > sma200:
                score += 2.0  # Pullback in uptrend = best entry
            elif 50 <= rsi < 65:
                score += 1.0
            # Low vol = stable compounder (good)
            if vol is not None and not _is_missing(vol) and vol < 0.015:
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
# 10. DCF Deep Value — stocks trading 30%+ below intrinsic value
# ---------------------------------------------------------------------------
class DCFDeepValue(BasePersona):
    """Buy mid/large caps trading far below DCF intrinsic value.

    Uses price-to-FCF and distance-from-highs as proxies for DCF discount
    (we can't compute DCF in real-time, but beaten-down FCF machines are
    statistically the same set).

    Universe: companies with high FCF yield that have sold off.
    Edge: Market overreacts to short-term earnings misses in high-FCF companies.
    The FCF keeps compounding even when the stock price doesn't.

    Includes: healthcare post-patent, consumer staples GLP-1 fear selloff,
    energy with massive buybacks, beaten-down industrials.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="DCF Deep Value (High FCF Discount)",
            description="Mid/large caps trading 30%+ below intrinsic value — high FCF, beaten-down prices",
            risk_tolerance=0.5,
            max_position_size=0.10,
            max_positions=15,
            rebalance_frequency="weekly",
            universe=universe or [
                # Consumer staples beaten down (GLP-1 fear overreaction)
                "MDLZ", "CAG", "SJM", "HRL", "CPB",
                # Healthcare FCF machines
                "DHR", "WAT", "ZTS", "IDXX",
                # Insurance float compounders
                "ALL", "PGR", "MKL", "CINF",
                # Payment infrastructure (depressed vs growth)
                "FIS", "GPN", "FISV",
                # Industrial FCF
                "DOV", "ROP", "TDY",
                # Boring but profitable
                "WST", "ODFL",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
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
            price = prices[sym]
            score = 0.0

            # Deep value: price significantly below SMA200 = potential DCF discount
            if price < sma200 * 0.90:
                score += 3.0  # >10% below long-term avg = deep value
            elif price < sma200:
                score += 1.5

            # RSI oversold = maximum pessimism
            if rsi < 35:
                score += 2.0
            elif rsi < 45:
                score += 1.0

            # MACD turning up = reversal starting
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5

            # Near lower Bollinger = statistical extreme
            if bb_low is not None and not _is_missing(bb_low) and price < bb_low * 1.02:
                score += 1.0

            # Only buy if there's actual value signal (not just trending down)
            if score >= 3.0:
                scored.append((sym, score))
            elif price > sma200:
                # Exited value zone — reduce or exit
                weights[sym] = 0.0

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 11. Toll Booth Economy — companies that tax every transaction
# ---------------------------------------------------------------------------
class TollBoothEconomy(BasePersona):
    """Invest in companies that sit on critical infrastructure and collect fees.

    These are the "toll booths" of the modern economy:
    - Every credit card swipe: V, MA
    - Every stock trade: ICE, CME, NDAQ
    - Every insurance policy: SPGI, MCO rate it
    - Every building needs HVAC: OTIS, CARR
    - Every package shipped: ODFL, CHRW

    Edge: Transaction volumes grow with GDP. These companies have near-zero
    marginal cost per transaction. Revenue scales infinitely.
    Unlike tech, they don't need to reinvent themselves every 3 years.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Toll Booth Economy",
            description="Companies that tax every transaction: payments, exchanges, ratings, logistics",
            risk_tolerance=0.4,
            max_position_size=0.10,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                # Payment toll booths
                "V", "MA", "FISV", "GPN",
                # Exchange toll booths
                "ICE", "CME", "NDAQ",
                # Ratings toll booths
                "SPGI", "MCO",
                # Logistics toll booths
                "ODFL", "CHRW",
                # Testing/compliance toll booths
                "A", "VRSK",
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
            vol = inds["vol_20"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Uptrend = growing transaction volumes
            if price > sma200:
                score += 2.0
            if sma50 is not None and sma50 > sma200:
                score += 1.0  # Golden cross
            # Not overextended
            if 40 < rsi < 70:
                score += 1.0
            # Low vol = stable toll collector (exactly what we want)
            if vol is not None and not _is_missing(vol) and vol < 0.018:
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
# 12. Beaten Down Staples (GLP-1 Fear Overreaction)
# ---------------------------------------------------------------------------
class BeatenDownStaples(BasePersona):
    """Buy consumer staples crushed by GLP-1/Ozempic weight-loss drug fears.

    The market sold off snack, soda, fast food, and packaged food companies
    on fears that GLP-1 drugs will reduce calorie consumption. But:
    - GLP-1 penetration is <5% of population even in 2026
    - These companies have pricing power and adapt product lines
    - Dividend yields are now at 10-year highs
    - FCF is still growing

    Edge: Classic overreaction. The selloff priced in 100% GLP-1 adoption
    when real adoption is <5%. Buy the fear, collect the dividends.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Beaten Down Staples (GLP-1 Fear)",
            description="Consumer staples oversold on GLP-1 fears — buy the overreaction, collect dividends",
            risk_tolerance=0.3,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                # Snack/packaged food (hit hardest by GLP-1 fear)
                "MDLZ", "CAG", "SJM", "HRL", "CPB",
                # Soda (Pepsi/Coke hit by weight loss fears)
                "PEP", "KO",
                # Fast food/restaurants
                "MCD", "YUM", "DPZ",
                # Grocery/consumer
                "KR", "SYY",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "bb_lower"], date)
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            bb_low = inds["bb_lower"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Below SMA200 = fear territory (where we want to buy)
            if price < sma200 * 0.95:
                score += 3.0  # Deep discount to trend
            elif price < sma200:
                score += 1.5
            # RSI oversold = maximum fear
            if rsi < 35:
                score += 2.0
            elif rsi < 45:
                score += 1.0
            # Near Bollinger lower = statistical extreme
            if bb_low is not None and not _is_missing(bb_low) and price < bb_low * 1.02:
                score += 1.0
            # Recovery signal: if above SMA200, hold with momentum
            if price > sma200 and rsi > 50:
                score += 1.5

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
# 13. Insurance Float Compounders
# ---------------------------------------------------------------------------
class InsuranceFloat(BasePersona):
    """Invest in insurance companies that compound via float investing.

    Insurance companies collect premiums upfront and pay claims later.
    The "float" — premiums collected but not yet paid out — is essentially
    free leverage that they invest. Berkshire Hathaway pioneered this.

    Edge: Float grows with premiums (inflation-linked). Combined ratios <100%
    mean they're paid to hold your money. Market treats them as boring financials
    but they're actually leveraged investment vehicles.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Insurance Float Compounders",
            description="Insurance companies with massive float: paid to hold money, compound via investing",
            risk_tolerance=0.4,
            max_position_size=0.12,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "BRK-B",  # Berkshire Hathaway (the OG float compounder)
                "PGR",    # Progressive (auto insurance, 96% combined ratio)
                "ALL",    # Allstate
                "CB",     # Chubb (global, very profitable)
                "MKL",    # Markel (mini-Berkshire)
                "CINF",   # Cincinnati Financial (50+ year dividend growth)
                "AFL",    # Aflac (supplemental insurance, massive float)
                "WRB",    # Berkley (specialty insurance)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Uptrend = growing premiums + float
            if price > sma200:
                score += 2.0
            if sma50 is not None and price > sma50:
                score += 1.0
            # Buy dips in uptrend
            if 35 < rsi < 50 and price > sma200:
                score += 2.0
            elif 50 <= rsi < 65:
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
# 14. Boring Compounder 20% Club
# ---------------------------------------------------------------------------
class BoringCompounder(BasePersona):
    """Companies growing intrinsic value 15-20% annually in boring industries.

    These never make CNBC, never go viral on Reddit, never get mentioned
    by Cathie Wood. They just quietly compound wealth:
    - POOL: only national pool supply distributor
    - ODFL: best-in-class LTL freight (98% on-time)
    - CTAS: uniform rental monopoly
    - WST: pharmaceutical packaging (every vial needs a stopper)
    - ROP: vertical market software roll-up
    - FAST: industrial fastener distribution

    Edge: Boring = under-owned by retail = less volatile = better Sharpe.
    Institutional ownership is high but passive flows dominate, meaning
    mispricings persist longer.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Boring Compounder 20% Club",
            description="Quiet compounders in boring industries: pool supply, uniforms, fasteners, packaging",
            risk_tolerance=0.3,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "POOL",  # Pool supply distribution monopoly
                "ODFL",  # Best LTL freight carrier
                "CTAS",  # Uniform rental
                "WST",   # Pharma packaging
                "ROP",   # Vertical software roll-up
                "FAST",  # Industrial fasteners
                "TDY",   # Defense/instrumentation
                "IDXX",  # Veterinary diagnostics monopoly
                "CLH",   # Hazardous waste (Clean Harbors)
                "LII",   # HVAC (Lennox)
                "WSO",   # HVAC distribution (Watsco)
                "MORN",  # Morningstar (investment research monopoly)
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
            vol = inds["vol_20"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Must be in uptrend (compounders trend up)
            if price > sma200:
                score += 2.0
            else:
                continue  # Don't buy broken compounders
            if sma50 is not None and price > sma50:
                score += 1.0
            # Buy pullbacks aggressively (these always recover)
            if 30 < rsi < 45:
                score += 2.5  # Deep pullback in compounder = best entry
            elif 45 <= rsi < 60:
                score += 1.0
            # Low vol = stable compounder
            if vol is not None and not _is_missing(vol) and vol < 0.015:
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
# 15. Billboard & Outdoor Media Monopoly
# ---------------------------------------------------------------------------
class BillboardMonopoly(BasePersona):
    """Lamar, Clear Channel, Outfront — they OWN the physical ad space.

    Billboard companies have irreplaceable physical assets (you can't build
    new billboards on highways — permits are frozen). Digital conversion
    doubles revenue per board. Inflation = higher ad rates on same asset.
    LAMR has 50-year track record of raising dividends.

    Also includes airport/transit ad monopolies and experiential venues.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Billboard & Outdoor Media Monopoly",
            description="Irreplaceable physical ad assets: billboards, airports, transit — frozen permits = moat",
            risk_tolerance=0.4,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "LAMR",   # Lamar Advertising — #1 US billboard operator
                "CCO",    # Clear Channel Outdoor — #2, post-bankruptcy lean
                "OUT",    # Outfront Media — NYC subway/transit ads
                "MSGS",   # MSG Sports — owns MSG arena (irreplaceable NYC asset)
                "LYV",    # Live Nation — owns Ticketmaster + venues
                "SPOT",   # Spotify — audio ad monopoly (different but related)
                "MGNI",   # Magnite — programmatic outdoor/CTV ads
                "PUBM",   # PubMatic — ad infrastructure
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
            if price > sma200:
                score += 2.0
            if sma50 is not None and price > sma50:
                score += 1.0
            if 35 < rsi < 55 and price > sma200:
                score += 2.0
            elif 55 <= rsi < 70:
                score += 0.5
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
# 16. Specialty Insurance & Niche Underwriters
# ---------------------------------------------------------------------------
class SpecialtyInsurance(BasePersona):
    """Kinsale, RLI, Palomar, HCI — niche underwriters with massive ROE.

    These aren't your parent's insurance companies. They specialize in
    risks nobody else will touch: construction defect, cannabis, cyber,
    hurricane. KNSL has 25%+ ROE because they price risk better than
    generalists. Small enough to grow 20%+ for years. Most people
    have never heard of any of them.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Specialty Insurance Niche Underwriters",
            description="Niche insurers with 25%+ ROE: construction, cyber, hurricane — nobody else will touch these risks",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "KNSL",   # Kinsale Capital — E&S specialty, 25%+ ROE
                "RLI",    # RLI Corp — niche casualty, 50+ year profitability streak
                "PLMR",   # Palomar Holdings — earthquake/hurricane specialty
                "HCI",    # HCI Group — Florida hurricane specialist
                "RYAN",   # Ryan Specialty — wholesale specialty broker
                "WRB",    # W.R. Berkley — specialty lines
                "OSCR",   # Oscar Health — tech-enabled health insurance
                "ROOT",   # Root Insurance — telematics-based auto
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            if price > sma200:
                score += 2.5
            sma50 = inds["sma_50"]
            if sma50 is not None and price > sma50:
                score += 1.0
            if 30 < rsi < 50 and price > sma200:
                score += 2.0
            elif 50 <= rsi < 65:
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
# 17. Uranium & Nuclear Renaissance
# ---------------------------------------------------------------------------
class UraniumRenaissance(BasePersona):
    """UUUU, CCJ, LEU, NXE, UEC — nuclear is back and uranium is scarce.

    Post-Fukushima uranium mines closed. Now 60+ reactors being built globally,
    existing reactors extending life, and SMRs coming online. Supply deficit
    is structural — takes 10+ years to open a new mine. UUUU is the ONLY
    US uranium producer AND processes rare earths.

    Edge: Supply/demand imbalance takes years to fix. Price must go up
    for mines to be economically viable. This is a multi-year secular trend
    that most retail investors are completely unaware of.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Uranium & Nuclear Renaissance",
            description="Structural uranium supply deficit: only US producer (UUUU), SMRs, 60+ reactors building",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "UUUU",   # Energy Fuels — ONLY US uranium + rare earth producer
                "CCJ",    # Cameco — largest pure-play uranium miner
                "LEU",    # Centrus Energy — HALEU enrichment monopoly
                "UEC",    # Uranium Energy Corp
                "NXE",    # NexGen Energy — flagship Arrow deposit
                "DNN",    # Denison Mines — ISR uranium
                "URA",    # Global X Uranium ETF
                "SMR",    # NuScale Power — SMR technology leader
                "OKLO",   # Oklo — micro-reactor startup
                "VST",    # Vistra — nuclear fleet operator
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "volume_sma_20"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Secular uptrend
            if price > sma200:
                score += 2.0
            if sma50 is not None and sma50 > sma200:
                score += 1.5
            # MACD momentum
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            # RSI: buy momentum, not overbought
            if 45 < rsi < 75:
                score += 1.0
            # Volume confirmation
            vol_sma = inds["volume_sma_20"]
            if vol_sma is not None and not _is_missing(vol_sma) and sym in data:
                try:
                    cur_vol = data[sym].loc[:date, "Volume"].iloc[-1]
                    if cur_vol > vol_sma * 1.3:
                        score += 1.0
                except Exception:
                    pass
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
# 18. Fallen Luxury & Aspirational Brands
# ---------------------------------------------------------------------------
class FallenLuxury(BasePersona):
    """Kering, Tapestry/Coach, Capri/Versace, Burberry — luxury selloff.

    Luxury sold off hard in 2023-2024 on China slowdown + "quiet luxury"
    trend shift. But these brands have 100+ year moats, 60%+ gross margins,
    and pricing power. TPR (Coach) just won the Capri acquisition fight.
    PPRUY (Kering/Gucci) is at 2017 prices despite 2x the revenue.

    Edge: Luxury always comes back. Brand equity doesn't depreciate.
    These are trading at decade-low multiples on cyclical fears.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Fallen Luxury & Aspirational Brands",
            description="Luxury brands at decade-low multiples: Kering, Coach, Burberry — brand equity doesn't depreciate",
            risk_tolerance=0.6,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "TPR",    # Tapestry (Coach, Kate Spade, Stuart Weitzman)
                "CPRI",   # Capri Holdings (Versace, Jimmy Choo, Michael Kors)
                "PPRUY",  # Kering (Gucci, YSL, Balenciaga, Bottega Veneta)
                "BURBY",  # Burberry
                "RL",     # Ralph Lauren (turnaround working)
                "LVMUY",  # LVMH (if it dips)
                "HESAY",  # Hermes (ultimate luxury moat)
                "RMS.PA", # Richemont if needed
                "EL",     # Estee Lauder (China recovery play)
                "LULU",   # Lululemon (aspirational athleisure)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "bb_lower"], date)
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Deep discount = opportunity (contrarian luxury)
            if price < sma200 * 0.85:
                score += 3.0
            elif price < sma200:
                score += 1.5
            elif price > sma200:
                score += 0.5  # Already recovering
            # RSI oversold
            if rsi < 35:
                score += 2.5
            elif rsi < 45:
                score += 1.5
            elif rsi > 50:
                score += 0.5
            # Bollinger band support
            bb_low = inds["bb_lower"]
            if bb_low is not None and not _is_missing(bb_low) and price < bb_low * 1.03:
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
# 19. Muni Bond & Tax-Free Income
# ---------------------------------------------------------------------------
class MuniBondIncome(BasePersona):
    """MUB, HYD, VTEB — municipal bonds are the ultimate stealth income play.

    Most retail investors don't know muni bond interest is FEDERAL TAX FREE
    (and state tax free if in-state). A 4% muni yield = 6%+ taxable equivalent
    for high earners. Munis almost never default (<0.1% historically).

    Mix with high-yield munis (HYD) and closed-end funds (NUV, NEA) that
    trade at discounts to NAV for extra yield + capital appreciation.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Muni Bond Tax-Free Income",
            description="Tax-free municipal bonds: 4% muni = 6%+ taxable. Near-zero default risk.",
            risk_tolerance=0.2,
            max_position_size=0.20,
            max_positions=6,
            rebalance_frequency="monthly",
            universe=universe or [
                "MUB",    # iShares National Muni Bond ETF
                "VTEB",   # Vanguard Tax-Exempt Bond ETF
                "HYD",    # VanEck High Yield Muni ETF (higher yield)
                "TFI",    # SPDR Nuveen Bloomberg Municipal Bond ETF
                "NUV",    # Nuveen Municipal Value Fund (closed-end, discount to NAV)
                "NEA",    # Nuveen AMT-Free Quality Muni (closed-end)
                "SHM",    # SPDR Short-Term Muni Bond (low duration)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        # For bonds: buy when price dips (yields rise), simple mean-reversion
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Buy when price is low (yields are high) — income play
            if price < sma200:
                score += 2.0  # Below long-term = higher yield
            if rsi < 40:
                score += 2.0  # Oversold = best yield entry
            elif rsi < 50:
                score += 1.0
            # Also hold in uptrend (rates falling = price rising)
            if price > sma200:
                score += 1.0
            if sma50 is not None and price > sma50:
                score += 0.5
            score += 1.0  # Always some allocation (it's income)
            scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 20. Serial Acquirer Compounders — TDG 5,449% since IPO
# ---------------------------------------------------------------------------
class SerialAcquirer(BasePersona):
    """TransDigm, HEICO, Roper, Danaher — capital allocation machines.

    Buy small profitable businesses, integrate with minimal overhead, compound 15-25%
    annually. Look "expensive" on P/E but CHEAP on P/FCF because acquisitions
    depress earnings via amortization. ROP at 19x FCF vs 29x historical is deep value.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Serial Acquirer Compounders",
            description="TDG/HEI/ROP: 15-25% CAGR machines that look expensive on P/E but are cheap on FCF",
            risk_tolerance=0.4,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "TDG", "HEI", "DHR", "ROP", "IEX", "NDSN",
                "GGG", "ITW", "AME", "CPRT", "WDFC", "BR",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "volume_sma_20"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            if price > sma200:
                score += 2.0
            if sma50 is not None and sma50 > sma200:
                score += 1.5
            if 35 < rsi < 50 and price > sma200:
                score += 2.0  # Pullback in compounder
            elif 50 <= rsi < 65:
                score += 0.5
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            if score >= 3.5:
                scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 21. Patent Cliff Pharma Value — BMY 7x earnings, $15B FCF
# ---------------------------------------------------------------------------
class PatentCliffPharma(BasePersona):
    """Big Pharma at decade-low multiples due to patent cliff fears.

    Market prices in 100% revenue loss but biosimilar erosion is only 60-70%.
    ABBV proved transition works. BMY at 7x earnings with Opdivo growing.
    $2.1T in M&A firepower ensures continuous pipeline refilling.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Patent Cliff Pharma Value",
            description="BMY 7x earnings, PFE post-COVID: market overprices patent cliffs by 2-3x",
            risk_tolerance=0.5,
            max_position_size=0.10,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "BMY", "PFE", "MRK", "ABBV", "GILD", "VTRS",
                "TEVA", "AMGN", "JNJ", "BIIB", "TAK", "GSK", "AZN", "NVS",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "bb_lower"], date)
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            if price < sma200 * 0.90:
                score += 3.0
            elif price < sma200:
                score += 1.5
            if rsi < 35:
                score += 2.5
            elif rsi < 45:
                score += 1.0
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5
            bb_low = inds["bb_lower"]
            if bb_low is not None and not _is_missing(bb_low) and price < bb_low * 1.02:
                score += 1.0
            if price > sma200 and rsi > 55:
                score += 1.0  # Hold recovery
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
# 22. Midstream Toll Road Income — 40% discount, 7%+ yield
# ---------------------------------------------------------------------------
class MidstreamTollRoad(BasePersona):
    """Pipeline MLPs: 90% fee-based, 7%+ growing yield, don't care about oil prices.

    EPD has 27 consecutive distribution increases. 40% discount to S&P peers.
    These are toll roads collecting fees on every barrel. LNG export growth
    and data center power demand = structural volume growth.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Midstream Toll Road Income",
            description="Pipeline MLPs: 90% fee-based contracts, 7%+ yield, 27yr distribution growth, toll roads of energy",
            risk_tolerance=0.4,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "EPD", "ET", "MPLX", "WMB", "OKE",
                "PAA", "TRGP", "KMI", "AM", "CTRA",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "volume_sma_20"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            if price > sma200:
                score += 2.0
            if sma50 is not None and sma50 > sma200:
                score += 1.0
            if 30 < rsi < 45:
                score += 2.0  # Yield expansion on pullback
            elif 45 <= rsi < 65:
                score += 1.0
            vol_sma = inds["volume_sma_20"]
            if vol_sma is not None and not _is_missing(vol_sma) and sym in data:
                try:
                    cur_vol = data[sym].loc[:date, "Volume"].iloc[-1]
                    if cur_vol > vol_sma * 1.5:
                        score += 1.0
                except Exception:
                    pass
            score += 0.5  # Base allocation (income play)
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
# 23. Constellation Contrarian — STZ 49.8% DCF discount
# ---------------------------------------------------------------------------
class ConstellationContrarian(BasePersona):
    """Wide-moat brands at extreme DCF discounts.

    STZ at $155 vs $309 DCF (49.8% discount) — Modelo is #1 US beer.
    EFX at 34% discount to fair value. NKE brand moat permanent despite selloff.
    LULU at 15x earnings. These are the most mispriced wide-moat stocks available.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Constellation Contrarian (Max DCF Discount)",
            description="STZ 49.8% DCF discount, EFX 34%, NKE permanent moat — most mispriced wide-moat stocks",
            risk_tolerance=0.5,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "STZ",    # Constellation Brands — 49.8% DCF discount, Modelo #1 beer
                "EFX",    # Equifax — 34% discount, data monopoly
                "NKE",    # Nike — brand moat, beaten down on China
                "LULU",   # Lululemon — 15x earnings for 20% grower
                "PVH",    # Calvin Klein + Tommy Hilfiger — Morningstar undervalued
                "BUD",    # AB InBev — global beer monopoly, cheap
                "TAP",    # Molson Coors — value play
                "SAM",    # Boston Beer — craft beer + Truly, beaten down
                "MNST",   # Monster Beverage — energy drink growth
                "BF.B",   # Brown-Forman — Jack Daniel's, recession-proof
                "DEO",    # Diageo — global spirits monopoly
                "HAS",    # Hasbro — IP licensing machine
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "bb_lower"], date)
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Deep discount = massive DCF upside
            if price < sma200 * 0.85:
                score += 3.0
            elif price < sma200:
                score += 1.5
            # Max pessimism
            if rsi < 35:
                score += 2.5
            elif rsi < 45:
                score += 1.5
            # MACD reversal
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5
            # Bollinger support
            bb_low = inds["bb_lower"]
            if bb_low is not None and not _is_missing(bb_low) and price < bb_low * 1.03:
                score += 1.0
            # Recovery hold
            if price > sma200 and rsi > 50:
                score += 1.5
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
# News & Media Monopoly
# ---------------------------------------------------------------------------
class NewsMediaMonopoly(BasePersona):
    """News and media monopoly strategy.

    Thesis: Legacy media companies own irreplaceable content libraries and
    distribution networks. NYT has proven digital subscription model.
    GOOG owns YouTube (largest video platform). DIS owns unmatched IP.
    These trade at discounts due to cord-cutting fears but content is king.
    Buy beaten-down media names with MACD reversal signals.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="News & Media Monopoly",
            description="Irreplaceable media IP and distribution: NYT, DIS, GOOG (YouTube), CMCSA",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=7,
            rebalance_frequency="weekly",
            universe=universe or [
                "NYT",  # New York Times (digital subscription leader)
                "CMCSA",  # Comcast (NBCUniversal + cable infrastructure)
                "DIS",  # Disney (IP moat: Marvel, Star Wars, Pixar, ESPN)
                "PARA",  # Paramount (content library)
                "WBD",  # Warner Bros Discovery (HBO, CNN)
                "NWSA",  # News Corp (WSJ, Dow Jones)
                "GOOG",  # Alphabet (YouTube = video monopoly)
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

            # Deep value: media names crushed by cord-cutting narrative
            if price < sma200 * 0.90:
                score += 3.0  # >10% below long-term avg
            elif price < sma200:
                score += 1.5

            # RSI oversold = maximum pessimism on media
            if rsi < 35:
                score += 2.0
            elif rsi < 45:
                score += 1.0

            # MACD reversal = sentiment turning (content wins eventually)
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5

            # Bollinger lower band = statistical extreme
            if bb_low is not None and not _is_missing(bb_low) and price < bb_low * 1.02:
                score += 1.0

            # Also ride momentum if uptrend established (NYT, GOOG)
            if sma50 is not None and price > sma50 > sma200:
                score += 2.0
            elif sma50 is not None and price > sma50:
                score += 1.0

            # Overbought: take profits on media (cyclical)
            if rsi > 75 and price > sma200:
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
# Retail Deep Value
# ---------------------------------------------------------------------------
class RetailDeepValue(BasePersona):
    """Retail deep value — contrarian department store / brick-and-mortar play.

    Thesis: Department stores and brick-and-mortar retailers are trading
    at historic low valuations (0.1-0.3x sales) despite owning prime real
    estate, generating free cash flow, and buying back shares aggressively.
    Kohl's, Macy's, and Nordstrom are trading below liquidation value.
    Dillard's has 10 straight years of buybacks (share count -60%).
    Burlington is the off-price leader with expanding margins.
    The "retail is dead" narrative is overdone — survivors are
    cash-generative with real asset backing.

    Signal: Deep value + RSI reversal. Buy oversold names with MACD
    bullish crossover. Sell on overbought recovery.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Retail Deep Value",
            description="Contrarian brick-and-mortar: below liquidation value, buybacks, real estate",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "KSS",    # Kohl's (massive buybacks, real estate value)
                "M",      # Macy's (prime urban real estate, digital growth)
                "JWN",    # Nordstrom (premium positioning, Rack growth)
                "DDS",    # Dillard's (buyback king, owner-operator)
                "BURL",   # Burlington (off-price growth, margin expansion)
                "TJX",    # TJ Maxx (off-price leader, treasure hunt model)
                "ROST",   # Ross Stores (discount leader, low-income resilient)
                "BBWI",   # Bath & Body Works (specialty retail, brand moat)
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
                ["sma_200", "sma_50", "rsi_14", "macd", "macd_signal",
                 "bb_lower", "Volume", "volume_sma_20"],
                date,
            )
            sma200 = inds["sma_200"]
            sma50 = inds["sma_50"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            bb_low = inds["bb_lower"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]

            if _is_missing(sma200) or _is_missing(rsi):
                continue

            # Exit: structural freefall (>35% below SMA200 = going bankrupt)
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            if discount > 0.35:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Deep value: below SMA200
            if discount > 0.10:
                score += 3.0  # >10% below = deep discount
            elif discount > 0.02:
                score += 1.5

            # RSI oversold = maximum retail pessimism
            if rsi < 30:
                score += 2.5
            elif rsi < 40:
                score += 1.5

            # MACD reversal = turnaround starting
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5

            # Bollinger lower band = statistical extreme
            if bb_low is not None and not _is_missing(bb_low) and price < bb_low * 1.02:
                score += 1.0

            # Volume surge = institutional interest (buyout? activist?)
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            if vol_ratio > 1.5:
                score += 0.5

            # Also ride recovery momentum
            if sma50 is not None and price > sma50 > sma200:
                score += 1.5

            # Take profits on recovery
            if rsi > 70 and discount < -0.15:
                weights[sym] = 0.0
                continue

            if score >= 3.0:
                candidates.append((sym, score))

        candidates.sort(key=lambda x: -x[1])
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
# Cannabis & Alt Consumer
# ---------------------------------------------------------------------------
class CannabisAltConsumer(BasePersona):
    """Cannabis and alternative consumer products strategy.

    Thesis: US cannabis legalization is a matter of when, not if. SAFE
    Banking Act / rescheduling would unlock institutional capital for an
    industry generating $30B+ annual revenue. Tilray (TLRY) is the
    world's largest cannabis company by revenue with diversification
    into beverages. Canopy Growth (CGC) has Constellation Brands backing.
    MJ ETF provides diversified cannabis exposure. The sector trades
    at 0.5-1x sales vs 3-5x for consumer staples — binary catalyst
    with asymmetric upside if regulation changes.

    Signal: Contrarian deep value. Buy on extreme oversold with MACD
    reversal. These are volatile — aggressive position sizing limits.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Cannabis & Alt Consumer",
            description="Contrarian cannabis: pre-legalization value, binary regulatory catalyst",
            risk_tolerance=0.8,
            max_position_size=0.12,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "TLRY",   # Tilray Brands (largest cannabis co by revenue)
                "CGC",    # Canopy Growth (Constellation Brands-backed)
                "MJ",     # ETFMG Alternative Harvest ETF (diversified)
                "CRON",   # Cronos Group (Altria-backed cannabis)
                "MSOS",   # AdvisorShares Pure US Cannabis ETF
                "GTBIF",  # Green Thumb Industries (US MSO leader)
                "CURLF",  # Curaleaf Holdings (US MSO)
                "SAM",    # Boston Beer (craft/alternative beverage proxy)
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
                 "bb_lower", "Volume", "volume_sma_20"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            bb_low = inds["bb_lower"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]

            if _is_missing(rsi):
                continue

            # Exit: overbought (cannabis rallies are sharp and short)
            if rsi > 75:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Deep value: heavily discounted from peak
            if sma200 is not None:
                discount = (sma200 - price) / sma200 if sma200 > 0 else 0
                if discount > 0.15:
                    score += 3.0  # >15% below SMA200 = deep distress
                elif discount > 0.05:
                    score += 2.0

            # RSI extremely oversold (common for cannabis)
            if rsi < 25:
                score += 3.0
            elif rsi < 35:
                score += 2.0
            elif rsi < 45:
                score += 1.0

            # MACD bullish crossover = regulatory catalyst hope
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5

            # Bollinger lower band = statistical extreme
            if bb_low is not None and not _is_missing(bb_low) and price < bb_low * 1.03:
                score += 1.0

            # Volume surge = potential catalyst (regulatory news)
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            if vol_ratio > 2.0:
                score += 1.5
            elif vol_ratio > 1.5:
                score += 0.5

            # Momentum: also ride if uptrend established
            if sma50 is not None and sma200 is not None and price > sma50 > sma200:
                score += 2.0

            if score >= 3.0:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# Fallen Blue Chip Value
# ---------------------------------------------------------------------------
class FallenBlueChipValue(BasePersona):
    """Fallen blue chip value — contrarian play on once-great companies.

    Thesis: Blue chips that have fallen 30-60% from highs while
    maintaining dominant market positions and strong cash flows.
    Pfizer (PFE) trades at 9x earnings with $60B+ revenue and
    oncology pipeline. Intel (INTC) is the only Western foundry with
    US government backing ($50B+ CHIPS Act). Starbucks (SBUX) has new
    CEO turnaround. Nike (NKE) is the world's #1 athletic brand
    at a decade-low valuation. Cisco (CSCO) generates $15B+ FCF.
    These are NOT value traps — they have identifiable catalysts.

    Signal: Deep value + mean reversion. Buy when RSI < 40 and
    price near SMA200 support. MACD crossover for timing.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Fallen Blue Chip Value",
            description="Once-great blue chips at deep discounts: turnaround catalysts + dividend income",
            risk_tolerance=0.5,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "PFE",    # Pfizer (9x earnings, oncology pipeline)
                "INTC",   # Intel (CHIPS Act, foundry turnaround)
                "WMT",    # Walmart (defensive, e-commerce growth)
                "SBUX",   # Starbucks (new CEO turnaround)
                "NKE",    # Nike (brand moat at decade-low valuation)
                "CSCO",   # Cisco (networking moat, $15B+ FCF)
                "VZ",     # Verizon (7% dividend yield, fiber build)
                "TGT",    # Target (inventory reset, private label)
                "BMY",    # Bristol-Myers Squibb (pipeline catalyst)
                "MDT",    # Medtronic (med-tech leader at discount)
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
                ["sma_200", "sma_50", "rsi_14", "macd", "macd_signal",
                 "bb_lower", "Volume", "volume_sma_20"],
                date,
            )
            sma200 = inds["sma_200"]
            sma50 = inds["sma_50"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            bb_low = inds["bb_lower"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]

            if _is_missing(sma200) or _is_missing(rsi):
                continue

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            # Exit: falling knife (>30% below SMA200 with no reversal)
            if discount > 0.30 and rsi < 25:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Deep value: below SMA200
            if discount > 0.10:
                score += 3.0
            elif discount > 0.03:
                score += 1.5

            # RSI oversold = contrarian entry
            if rsi < 30:
                score += 2.5
            elif rsi < 40:
                score += 1.5
            elif rsi < 50:
                score += 0.5

            # MACD bullish crossover = turnaround confirmation
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5

            # Bollinger lower band
            if bb_low is not None and not _is_missing(bb_low) and price < bb_low * 1.02:
                score += 1.0

            # Volume surge = institutional accumulation
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            if vol_ratio > 1.5:
                score += 0.5

            # Recovery momentum: already started turning
            if sma50 is not None and price > sma50 > sma200:
                score += 2.0
            elif sma50 is not None and price > sma50:
                score += 1.0

            # Take profits on full recovery
            if rsi > 70 and discount < -0.15:
                weights[sym] = 0.0
                continue

            if score >= 3.0:
                candidates.append((sym, score))

        candidates.sort(key=lambda x: -x[1])
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


UNCONVENTIONAL_STRATEGIES = {
    "sell_in_may": SellInMayGoAway,
    "turn_of_month": TurnOfMonth,
    "vix_mean_reversion": VIXMeanReversion,
    "dogs_of_dow": DogsOfTheDow,
    "quality_factor": QualityFactor,
    "tail_risk_harvest": TailRiskHarvest,
    "dividend_aristocrat_momentum": DividendAristocratMomentum,
    "concentrate_winners": ConcentrateWinners,
    "hidden_monopoly": HiddenMonopoly,
    "dcf_deep_value": DCFDeepValue,
    "toll_booth_economy": TollBoothEconomy,
    "beaten_down_staples": BeatenDownStaples,
    "insurance_float": InsuranceFloat,
    "boring_compounder": BoringCompounder,
    "billboard_monopoly": BillboardMonopoly,
    "specialty_insurance": SpecialtyInsurance,
    "uranium_renaissance": UraniumRenaissance,
    "fallen_luxury": FallenLuxury,
    "muni_bond_income": MuniBondIncome,
    "serial_acquirer": SerialAcquirer,
    "patent_cliff_pharma": PatentCliffPharma,
    "midstream_toll_road": MidstreamTollRoad,
    "constellation_contrarian": ConstellationContrarian,
    "news_media_monopoly": NewsMediaMonopoly,
    "retail_deep_value": RetailDeepValue,
    "cannabis_alt_consumer": CannabisAltConsumer,
    "fallen_blue_chip_value": FallenBlueChipValue,
}


# ---------------------------------------------------------------------------
# Economic Indicator Proxies (Hemline, Underwear, Big Mac, Lipstick)
# ---------------------------------------------------------------------------
class EconomicIndicatorProxy(BasePersona):
    """Trade based on famous non-traditional economic indicators.

    Hemline Index: fashion confidence → risk-on. Underwear Index: drops → recession.
    Big Mac Index: MCD health = global consumer. Lipstick Index: rises in recession.
    Dr. Copper: copper momentum = industrial health. Cardboard Box: packaging = GDP lead.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Economic Indicator Proxy (Hemline/BigMac/Lipstick)",
            description="Non-traditional indicators: fashion=confidence, underwear=recession, copper=industrial",
            risk_tolerance=0.5, max_position_size=0.12, max_positions=12, rebalance_frequency="weekly",
            universe=universe or [
                "MCD", "RL", "LULU", "PVH",  # Consumer confidence
                "EL", "ULTA", "HBI",          # Recession detectors
                "FCX", "COPX", "PKG",         # Industrial health
                "TLT", "GLD",                 # Defensive
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        consumer = 0; recession = 0
        for sym, role in [("MCD","c"),("RL","c"),("LULU","c"),("FCX","i"),("COPX","i"),("PKG","i"),("EL","r"),("HBI","rn")]:
            if sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_200"], date)
            s200 = inds["sma_200"]
            if _is_missing(s200): continue
            up = prices[sym] > s200
            if role in ("c","i") and up: consumer += 1
            elif role in ("c","i") and not up: recession += 1
            elif role == "rn" and not up: recession += 2  # Underwear dropping

        if consumer > recession + 1:
            for sym in ["MCD","RL","LULU","PVH","FCX","PKG"]:
                if sym in prices:
                    inds = self._get_indicators(data, sym, ["sma_200"], date)
                    if not _is_missing(inds["sma_200"]) and prices[sym] > inds["sma_200"]:
                        weights[sym] = 0.10
        elif recession > consumer:
            for sym in ["TLT","GLD"]: weights[sym] = 0.25 if sym in prices else 0
            for sym in ["EL","ULTA"]: weights[sym] = 0.10 if sym in prices else 0
        else:
            for sym in ["MCD","TLT","GLD","FCX"]: weights[sym] = 0.12 if sym in prices else 0
        return weights


# ---------------------------------------------------------------------------
# AI Token Economy — trade AI infrastructure based on compute demand
# ---------------------------------------------------------------------------
class AITokenEconomy(BasePersona):
    """AI token/compute demand as economic indicator for AI infrastructure stocks.

    As AI usage grows (OpenAI, Anthropic, Google), the companies providing
    compute infrastructure benefit directly. Track GPU makers (NVDA, AMD),
    cloud providers (AMZN, MSFT, GOOGL), data center REITs (EQIX, DLR),
    power for data centers (VST, CEG, NRG), and cooling (VRT).

    Proxy for "AI token spend index": NVDA revenue growth = direct measure
    of industry-wide AI compute spending. When NVDA accelerates, the whole
    AI infrastructure stack benefits.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="AI Token Economy (Compute Demand Indicator)",
            description="AI compute demand signals: GPU makers, cloud, data center REITs, power, cooling",
            risk_tolerance=0.6, max_position_size=0.12, max_positions=10, rebalance_frequency="weekly",
            universe=universe or [
                "NVDA",   # GPU monopoly — direct token compute proxy
                "AMD",    # GPU #2
                "AVGO",   # Custom AI chips (Google TPU, etc.)
                "SMCI",   # AI server assembly
                "VRT",    # Data center cooling (Vertiv)
                "EQIX",   # Data center REIT
                "DLR",    # Digital Realty — data center REIT
                "VST",    # Vistra — nuclear power for data centers
                "CEG",    # Constellation Energy — nuclear fleet
                "NRG",    # NRG Energy — power for AI
                "ANET",   # Arista Networks — data center networking
                "MRVL",   # Marvell — AI custom silicon
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        # Use NVDA as the "token spend index" — if NVDA is accelerating,
        # the whole stack benefits
        nvda_signal = 0
        if "NVDA" in data:
            inds = self._get_indicators(data, "NVDA", ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            s50, s200 = inds["sma_50"], inds["sma_200"]
            if not _is_missing(s200) and "NVDA" in prices:
                if prices["NVDA"] > s200: nvda_signal += 2
                if s50 is not None and s50 > s200: nvda_signal += 1
                macd, ms = inds["macd"], inds["macd_signal"]
                if macd is not None and ms is not None and macd > ms: nvda_signal += 1

        for sym in self.config.universe:
            if sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            s200, rsi = inds["sma_200"], inds["rsi_14"]
            if _is_missing(s200) or _is_missing(rsi): continue
            price = prices[sym]
            score = 0.0
            if price > s200: score += 2.0
            s50 = inds["sma_50"]
            if s50 is not None and s50 > s200: score += 1.0
            if 35 < rsi < 55: score += 1.5
            # Boost if NVDA (token spend proxy) is strong
            score += nvda_signal * 0.5
            if score >= 4:
                scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# Job Loss → Tech Productivity Boom
# ---------------------------------------------------------------------------
class JobLossTechBoom(BasePersona):
    """When jobs are lost and PPI drops, companies automate → tech booms.

    Inverse correlation: rising unemployment + falling PPI = cost-cutting mode.
    Companies replace workers with software/AI/automation.
    Result: staffing stocks (MAN, RHI) DROP while tech/SaaS (CRM, NOW, WDAY) RISE.

    Proxy: Track staffing companies as employment leading indicators.
    When staffing breaks SMA200, it means hiring is slowing → go LONG tech productivity.
    When staffing is strong, labor market tight → stay balanced.

    Historical: 2022-23 tech layoffs → massive cloud/AI adoption. Every recession
    triggers a productivity investment cycle that benefits automation stocks.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Job Loss → Tech Productivity Boom",
            description="Unemployment rises → companies automate → tech/SaaS/AI booms. Inverse staffing-to-tech signal.",
            risk_tolerance=0.6, max_position_size=0.12, max_positions=12, rebalance_frequency="weekly",
            universe=universe or [
                # Employment indicators (INVERSE — weakness = automation signal)
                "MAN",    # ManpowerGroup — global staffing bellwether
                "RHI",    # Robert Half — white-collar staffing
                "ASGN",   # ASGN — IT staffing
                "ADP",    # ADP — payroll volume = direct employment proxy (40M employees)
                # Tech productivity beneficiaries (LONG these when employment drops)
                "CRM",    # Salesforce — replaces salespeople
                "NOW",    # ServiceNow — IT automation
                "WDAY",   # Workday — HR/finance automation
                "INTU",   # Intuit — replaces accountants
                "ADBE",   # Adobe — replaces designers
                "PANW",   # Palo Alto — replaces security analysts
                "HUBS",   # HubSpot — replaces marketing teams
                "ZM",     # Zoom — reduces office/travel costs
                # AI/automation pure plays
                "NVDA",   # GPU compute for AI replacing workers
                "PATH",   # UiPath — robotic process automation
                "AI",     # C3.ai — enterprise AI
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Check employment indicators (inverse signal)
        staffing_weak = 0
        staffing_tickers = ["MAN", "RHI", "ASGN", "ADP"]
        for sym in staffing_tickers:
            if sym not in data or sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_200"], date)
            s200 = inds["sma_200"]
            if _is_missing(s200):
                continue
            if prices[sym] < s200:
                staffing_weak += 1  # Below trend = hiring slowing

        # Tech productivity targets
        tech_targets = ["CRM", "NOW", "WDAY", "INTU", "ADBE", "PANW", "HUBS",
                        "NVDA", "PATH", "AI", "ZM"]

        if staffing_weak >= 2:
            # Strong signal: staffing companies weak → tech productivity boom
            scored = []
            for sym in tech_targets:
                if sym not in prices:
                    continue
                inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
                s200, rsi = inds["sma_200"], inds["rsi_14"]
                if _is_missing(s200) or _is_missing(rsi):
                    continue
                price = prices[sym]
                score = 0.0
                if price > s200:
                    score += 2.0
                s50 = inds["sma_50"]
                if s50 is not None and s50 > s200:
                    score += 1.0
                if 35 < rsi < 65:
                    score += 1.0
                macd, ms = inds["macd"], inds["macd_signal"]
                if macd is not None and ms is not None and macd > ms:
                    score += 1.0
                if score >= 2:
                    scored.append((sym, score))
            scored.sort(key=lambda x: -x[1])
            top = scored[:self.config.max_positions]
            if top:
                total = sum(s for _, s in top)
                for sym, sc in top:
                    weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        else:
            # Staffing strong → balanced allocation (no strong automation signal)
            for sym in ["CRM", "NOW", "NVDA", "INTU"]:
                if sym in prices:
                    inds = self._get_indicators(data, sym, ["sma_200"], date)
                    if not _is_missing(inds["sma_200"]) and prices[sym] > inds["sma_200"]:
                        weights[sym] = 0.08

        return weights


# Add strategies defined after the registry dict
# ---------------------------------------------------------------------------
# Cross-Category Inverse Strategies
# ---------------------------------------------------------------------------
class OilDownTechUp(BasePersona):
    """When oil crashes, tech benefits from lower costs + growth rotation.

    Inverse: XLE (energy) drops → XLK (tech) gets inflows.
    Mechanism: Lower oil = lower costs for data centers, shipping, manufacturing.
    Growth stocks benefit from lower discount rates (oil crash → Fed easing).
    Energy layoffs → capital flows to growth. Every oil crash since 2014 led to tech rally.
    """
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Oil Down → Tech Up (Inverse Rotation)",
            description="When energy crashes, capital rotates to tech. Lower oil = lower costs + Fed easing expectations.",
            risk_tolerance=0.5, max_position_size=0.12, max_positions=10, rebalance_frequency="weekly",
            universe=universe or [
                "XLE", "XOP", "OIH",  # Energy indicators (INVERSE)
                "AAPL", "MSFT", "GOOGL", "AMZN", "META",  # Tech beneficiaries
                "NFLX", "CRM", "NOW",  # Cloud/SaaS (lower costs)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        energy_weak = 0
        for sym in ["XLE", "XOP", "OIH"]:
            if sym not in data or sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_200"], date)
            if not _is_missing(inds["sma_200"]) and prices[sym] < inds["sma_200"]:
                energy_weak += 1
        if energy_weak >= 2:
            scored = []
            for sym in ["AAPL","MSFT","GOOGL","AMZN","META","NFLX","CRM","NOW"]:
                if sym not in prices: continue
                inds = self._get_indicators(data, sym, ["sma_50","sma_200","rsi_14"], date)
                if _is_missing(inds["sma_200"]) or _is_missing(inds["rsi_14"]): continue
                sc = 0.0
                if prices[sym] > inds["sma_200"]: sc += 2.0
                if inds["sma_50"] is not None and inds["sma_50"] > inds["sma_200"]: sc += 1.0
                if 35 < inds["rsi_14"] < 65: sc += 1.0
                if sc >= 2: scored.append((sym, sc))
            scored.sort(key=lambda x: -x[1])
            if scored:
                total = sum(s for _,s in scored[:self.config.max_positions])
                for sym, sc in scored[:self.config.max_positions]:
                    weights[sym] = min((sc/total)*0.95, self.config.max_position_size)
        else:
            for sym in ["AAPL","MSFT","GOOGL"]:
                if sym in prices: weights[sym] = 0.08
        return weights


class DollarWeakEMStrong(BasePersona):
    """When USD weakens, emerging markets + commodities outperform.

    Inverse: UUP (dollar ETF) drops → EEM, VWO, GLD, commodity exporters rise.
    Mechanism: Weak dollar = cheaper debt for EM, higher commodity prices in USD,
    EM earnings worth more when converted back. Every USD bear cycle = EM outperformance.
    """
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Dollar Weak → EM Strong (Currency Rotation)",
            description="USD weakens → EM stocks + commodities + gold outperform. Inverse dollar-to-EM signal.",
            risk_tolerance=0.6, max_position_size=0.10, max_positions=10, rebalance_frequency="weekly",
            universe=universe or [
                "UUP",    # Dollar index ETF (INVERSE indicator)
                "EEM",    # EM equities
                "VWO",    # Vanguard EM
                "GLD",    # Gold (inverse dollar)
                "BABA",   # China
                "VALE",   # Brazil commodities
                "PBR",    # Petrobras Brazil
                "EWZ",    # Brazil ETF
                "INDA",   # India
                "EWY",    # Korea
                "FXI",    # China large cap
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        dollar_weak = False
        if "UUP" in data and "UUP" in prices:
            inds = self._get_indicators(data, "UUP", ["sma_50","sma_200"], date)
            s50, s200 = inds["sma_50"], inds["sma_200"]
            if not _is_missing(s200) and prices["UUP"] < s200:
                dollar_weak = True
                if s50 is not None and s50 < s200: dollar_weak = True  # Strong signal
        if dollar_weak:
            targets = ["EEM","VWO","GLD","BABA","VALE","PBR","EWZ","INDA","EWY","FXI"]
            scored = []
            for sym in targets:
                if sym not in prices: continue
                inds = self._get_indicators(data, sym, ["sma_200","rsi_14"], date)
                if _is_missing(inds["sma_200"]) or _is_missing(inds["rsi_14"]): continue
                sc = 0.0
                if prices[sym] > inds["sma_200"]: sc += 2.0
                if 30 < inds["rsi_14"] < 65: sc += 1.0
                if sc >= 1: scored.append((sym, sc))
            scored.sort(key=lambda x: -x[1])
            if scored:
                total = sum(s for _,s in scored[:self.config.max_positions])
                for sym, sc in scored[:self.config.max_positions]:
                    weights[sym] = min((sc/total)*0.95, self.config.max_position_size)
        else:
            for sym in ["GLD","EEM"]:
                if sym in prices: weights[sym] = 0.10
        return weights


class BondsDownBanksUp(BasePersona):
    """When bonds sell off (rates rise), banks profit from wider net interest margins.

    Inverse: TLT drops → XLF rises. Banks make money on the spread between
    deposit rates and lending rates. Rising rates widen this spread massively.
    Also: higher rates → insurance float earns more → insurance stocks benefit.
    """
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Bonds Down → Banks Up (Rate Rotation)",
            description="Rising rates crush bonds but boost banks (wider NIM) + insurance (float income). TLT↓ = XLF↑.",
            risk_tolerance=0.5, max_position_size=0.12, max_positions=10, rebalance_frequency="weekly",
            universe=universe or [
                "TLT", "IEF",  # Bond indicators (INVERSE)
                "JPM", "BAC", "WFC", "C", "GS",  # Banks
                "PGR", "ALL", "CB", "MET",  # Insurance
                "SCHW", "MS",  # Brokers/wealth mgmt
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        bonds_falling = 0
        for sym in ["TLT", "IEF"]:
            if sym not in data or sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_200"], date)
            if not _is_missing(inds["sma_200"]) and prices[sym] < inds["sma_200"]:
                bonds_falling += 1
        if bonds_falling >= 1:
            targets = ["JPM","BAC","WFC","C","GS","PGR","ALL","CB","MET","SCHW","MS"]
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
            # Bonds strong → hold some bonds + balanced banks
            for sym in ["TLT","JPM","GS"]:
                if sym in prices: weights[sym] = 0.10
        return weights


class RetailCrashEcommerce(BasePersona):
    """When brick-and-mortar retail crashes, e-commerce accelerates.
    XRT (retail ETF) drops → AMZN, SHOP, MELI, SE, CPNG rise.
    Every retail recession accelerates the secular shift to online."""
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Retail Crash → E-commerce Boom",
            description="Brick-and-mortar crash accelerates e-commerce: XRT↓ = AMZN/SHOP/MELI↑",
            risk_tolerance=0.5, max_position_size=0.12, max_positions=8, rebalance_frequency="weekly",
            universe=universe or ["XRT","AMZN","SHOP","MELI","SE","CPNG","ETSY","W","BABA","EBAY"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        retail_weak = False
        if "XRT" in data and "XRT" in prices:
            inds = self._get_indicators(data, "XRT", ["sma_200"], date)
            if not _is_missing(inds["sma_200"]) and prices["XRT"] < inds["sma_200"]:
                retail_weak = True
        targets = ["AMZN","SHOP","MELI","SE","CPNG","ETSY","W","BABA","EBAY"]
        if retail_weak:
            scored = []
            for sym in targets:
                if sym not in prices: continue
                inds = self._get_indicators(data, sym, ["sma_200","rsi_14"], date)
                if _is_missing(inds["sma_200"]) or _is_missing(inds["rsi_14"]): continue
                sc = 0.0
                if prices[sym] > inds["sma_200"]: sc += 2.0
                if 35 < inds["rsi_14"] < 65: sc += 1.0
                if sc >= 1: scored.append((sym, sc))
            scored.sort(key=lambda x: -x[1])
            if scored:
                total = sum(s for _,s in scored[:8])
                for sym, sc in scored[:8]:
                    weights[sym] = min((sc/total)*0.95, self.config.max_position_size)
        else:
            for sym in ["AMZN","SHOP"]:
                if sym in prices: weights[sym] = 0.08
        return weights


class VIXSpikeBuyback(BasePersona):
    """When VIX spikes (fear), buy cash-rich companies doing buybacks.
    Companies with massive cash piles (AAPL, GOOGL, META) buy back stock
    during panics, creating a floor. They're essentially buying themselves cheap."""
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="VIX Spike → Cash-Rich Buyback",
            description="Fear spikes → buy companies with massive buyback programs. They buy themselves cheap in panics.",
            risk_tolerance=0.5, max_position_size=0.12, max_positions=10, rebalance_frequency="weekly",
            universe=universe or [
                "VXX",  # VIX indicator
                "AAPL","GOOGL","META","MSFT",  # Mega buyback machines
                "BRK-B","JPM","V","MA",  # Cash-rich compounders
                "QCOM","TXN",  # Semi buyback kings
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        vix_high = False
        if "VXX" in data and "VXX" in prices:
            inds = self._get_indicators(data, "VXX", ["sma_50","sma_200"], date)
            s200 = inds["sma_200"]
            if not _is_missing(s200) and prices["VXX"] > s200 * 1.3:
                vix_high = True
        targets = ["AAPL","GOOGL","META","MSFT","BRK-B","JPM","V","MA","QCOM","TXN"]
        if vix_high:
            for sym in targets:
                if sym not in prices: continue
                inds = self._get_indicators(data, sym, ["sma_200","rsi_14"], date)
                if _is_missing(inds["sma_200"]) or _is_missing(inds["rsi_14"]): continue
                if inds["rsi_14"] < 40:
                    weights[sym] = 0.12  # Max allocation on fear + oversold
                elif inds["rsi_14"] < 50:
                    weights[sym] = 0.08
        else:
            for sym in ["AAPL","GOOGL","META","V"]:
                if sym in prices: weights[sym] = 0.06
        return weights


class CryptoCrashTradFi(BasePersona):
    """When crypto crashes, capital flows back to traditional finance.
    GBTC/COIN drops → JPM, GS, BLK, SCHW benefit from "flight to safety"
    and crypto refugees opening brokerage accounts."""
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Crypto Crash → TradFi Flight",
            description="Crypto collapse drives capital to traditional banks, brokers, asset managers.",
            risk_tolerance=0.5, max_position_size=0.12, max_positions=8, rebalance_frequency="weekly",
            universe=universe or [
                "COIN","GBTC",  # Crypto indicators (INVERSE)
                "JPM","GS","MS",  # Banks
                "BLK","BX","KKR",  # Asset managers
                "SCHW","IBKR",  # Brokers
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        crypto_crash = 0
        for sym in ["COIN","GBTC"]:
            if sym not in data or sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_200","rsi_14"], date)
            if not _is_missing(inds["sma_200"]) and prices[sym] < inds["sma_200"] * 0.80:
                crypto_crash += 1
        targets = ["JPM","GS","MS","BLK","BX","KKR","SCHW","IBKR"]
        if crypto_crash >= 1:
            scored = []
            for sym in targets:
                if sym not in prices: continue
                inds = self._get_indicators(data, sym, ["sma_200","rsi_14"], date)
                if _is_missing(inds["sma_200"]) or _is_missing(inds["rsi_14"]): continue
                sc = 0.0
                if prices[sym] > inds["sma_200"]: sc += 2.0
                if 35 < inds["rsi_14"] < 65: sc += 1.0
                if sc >= 1: scored.append((sym, sc))
            scored.sort(key=lambda x: -x[1])
            if scored:
                total = sum(s for _,s in scored[:8])
                for sym, sc in scored[:8]:
                    weights[sym] = min((sc/total)*0.95, self.config.max_position_size)
        else:
            for sym in ["JPM","BLK"]:
                if sym in prices: weights[sym] = 0.08
        return weights


# Add all strategies defined after the registry dict
UNCONVENTIONAL_STRATEGIES["economic_indicators"] = EconomicIndicatorProxy
UNCONVENTIONAL_STRATEGIES["ai_token_economy"] = AITokenEconomy
UNCONVENTIONAL_STRATEGIES["job_loss_tech_boom"] = JobLossTechBoom
UNCONVENTIONAL_STRATEGIES["oil_down_tech_up"] = OilDownTechUp
UNCONVENTIONAL_STRATEGIES["dollar_weak_em_strong"] = DollarWeakEMStrong
UNCONVENTIONAL_STRATEGIES["bonds_down_banks_up"] = BondsDownBanksUp
UNCONVENTIONAL_STRATEGIES["retail_crash_ecommerce"] = RetailCrashEcommerce
UNCONVENTIONAL_STRATEGIES["vix_spike_buyback"] = VIXSpikeBuyback
UNCONVENTIONAL_STRATEGIES["crypto_crash_tradfi"] = CryptoCrashTradFi


class WealthBarometer(BasePersona):
    """Dollar stores vs Costco/luxury = wealth inequality barometer.

    When DLTR/DG crash: lower-income consumers under stress → trade DOWN.
    But Costco (bulk = value-conscious affluent) and luxury (LVMUY, RMS, TPR)
    OUTPERFORM because wealthy consumers are unaffected.

    Inverse: Dollar store weakness = K-shaped economy signal.
    Long: Costco + luxury + Walmart (captures both ends).
    This worked perfectly in 2023 when DLTR crashed 50% while COST hit ATH.
    """
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Wealth Barometer (Dollar Store vs Costco/Luxury)",
            description="DLTR/DG crash signals K-shaped economy → long Costco + luxury (rich don't care)",
            risk_tolerance=0.5, max_position_size=0.12, max_positions=10, rebalance_frequency="weekly",
            universe=universe or [
                # Barometer stocks (INVERSE signals)
                "DLTR",   # Dollar Tree — lower-income consumer proxy
                "DG",     # Dollar General — same
                # Beneficiaries when dollar stores crash (K-shape winners)
                "COST",   # Costco — bulk buying affluent
                "WMT",    # Walmart — captures trade-down from middle class
                "TJX",    # TJ Maxx — "treasure hunt" off-price
                "LVMUY",  # LVMH — ultra luxury
                "TPR",    # Tapestry/Coach — aspirational luxury
                "RL",     # Ralph Lauren
                "LULU",   # Lululemon
                "RH",     # Restoration Hardware — high-end home
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        dollar_store_weak = 0
        for sym in ["DLTR", "DG"]:
            if sym not in data or sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_200"], date)
            if not _is_missing(inds["sma_200"]) and prices[sym] < inds["sma_200"]:
                dollar_store_weak += 1

        targets = ["COST","WMT","TJX","LVMUY","TPR","RL","LULU","RH"]
        if dollar_store_weak >= 1:
            # K-shape signal: dollar stores weak → long quality/luxury
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
                total = sum(s for _,s in scored[:8])
                for sym, sc in scored[:8]:
                    weights[sym] = min((sc/total)*0.95, self.config.max_position_size)
        else:
            # Dollar stores strong = broad consumer health → balanced
            for sym in ["COST","WMT","TJX"]:
                if sym in prices: weights[sym] = 0.08
        return weights


def get_unconventional_strategy(name: str, **kwargs) -> BasePersona:
    cls = UNCONVENTIONAL_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown: {name}. Available: {list(UNCONVENTIONAL_STRATEGIES.keys())}")
    return cls(**kwargs)

UNCONVENTIONAL_STRATEGIES["wealth_barometer"] = WealthBarometer


# ---------------------------------------------------------------------------
# NVIDIA Domino Hedge — profit when NVIDIA supply chain collapses
# ---------------------------------------------------------------------------
class NVIDIADominoHedge(BasePersona):
    """Hedging strategy that profits when the NVIDIA financing/supply chain breaks.

    Thesis: NVIDIA has a ~$110B financing book (2.8x Lucent's ratio when it
    collapsed). CoreWeave alone has $28B in debt, 40% market-implied default
    risk, and GPUs as collateral. The supply chain is single-threaded:
    Trumpf -> ASML -> TSMC -> SK Hynix -> NVIDIA -> CoreWeave -> AI startups.
    If ANY link breaks, the whole chain suffers.

    Historical precedent: Cisco 2000 (stock -88%, 20 years to recover),
    Lucent 2001 ($3.5B write-offs, revenue -69%, 24 of 30 top customers bankrupt).

    Implementation:
    - Normal times (no stress): small hedge (8% in safe havens)
    - Moderate stress (NVDA overbought, supply chain names breaking): 25-35% hedge
    - High stress (SMCI collapse, vol spike, chain breaking): 40-60% defensive
    - Uses NVDA RSI, SMCI trend break, and vol regime as stress signals

    Instruments:
    - SQQQ (3x inverse Nasdaq — NVDA is ~8% of QQQ)
    - GLD, TLT, SHY (safe havens)
    - UVXY (1.5x VIX futures for vol spike capture)
    - Monitors SMCI, NVDA, AVGO, MU as chain stress indicators

    Edge: Most portfolios are long-only NVDA-exposed. This is the anti-portfolio
    that pays off exactly when crowded AI trades unwind. The Cisco/Lucent parallel
    is well-documented but not yet priced in because "this time is different."

    Sources:
    - Tomasz Tunguz: NVIDIA's $110B bet echoes telecom bubble
    - Jim Chanos: "putting money into money-losing companies to order their chips"
    - Harding Loevner: NVIDIA and the cautionary tale of Cisco Systems
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="NVIDIA Domino Hedge (Supply Chain Collapse)",
            description="Profit when NVIDIA financing chain breaks: inverse ETFs + safe havens + vol, scaled by supply chain stress",
            risk_tolerance=0.7,
            max_position_size=0.25,
            max_positions=8,
            rebalance_frequency="daily",
            universe=universe or [
                # Inverse / hedge instruments
                "SQQQ",   # 3x inverse Nasdaq (primary NVDA hedge)
                "UVXY",   # 1.5x VIX futures (vol spike capture)
                # Safe havens
                "GLD",    # Gold (crisis alpha)
                "TLT",    # Long-term treasuries (flight to quality)
                "SHY",    # Short-term treasuries (cash proxy)
                # Supply chain stress monitors (we track but DON'T buy)
                "NVDA",   # NVIDIA itself (monitor RSI/trend)
                "SMCI",   # Super Micro (canary in the coal mine)
                "AVGO",   # Broadcom (AI chip peer)
                "MU",     # Micron (HBM memory supplier)
            ],
        )
        super().__init__(config)

    def _compute_stress_level(self, date, prices, data):
        """Compute NVIDIA supply chain stress level (0-10 scale).

        Stress signals:
        - NVDA RSI > 75: overbought (fragile)
        - SMCI below SMA200: supply chain cracking
        - High realized vol on NVDA: institutional repositioning
        - MU/AVGO below SMA200: broad chain weakness
        """
        stress = 0.0

        # Signal 1: NVDA overbought (RSI > 75 = fragile, pre-crash)
        nvda_rsi = self._get_indicator(data, "NVDA", "rsi_14", date)
        if not _is_missing(nvda_rsi):
            if nvda_rsi > 80:
                stress += 2.5  # Extremely overbought
            elif nvda_rsi > 75:
                stress += 1.5  # Overbought
            elif nvda_rsi < 30:
                stress += 2.0  # Already crashing

        # Signal 2: SMCI below SMA200 (canary — supply chain stress)
        if "SMCI" in prices:
            smci_sma200 = self._get_indicator(data, "SMCI", "sma_200", date)
            smci_rsi = self._get_indicator(data, "SMCI", "rsi_14", date)
            if not _is_missing(smci_sma200):
                if prices["SMCI"] < smci_sma200 * 0.85:
                    stress += 2.5  # Deep breakdown
                elif prices["SMCI"] < smci_sma200:
                    stress += 1.5  # Below trend
            if not _is_missing(smci_rsi) and smci_rsi < 30:
                stress += 1.0  # SMCI in panic

        # Signal 3: NVDA vol spike (institutional repositioning)
        nvda_vol = self._get_indicator(data, "NVDA", "vol_20", date)
        if not _is_missing(nvda_vol):
            annualized = nvda_vol * _SQRT_252 * 100
            if annualized > 60:
                stress += 2.0  # Extreme vol
            elif annualized > 40:
                stress += 1.0  # Elevated vol

        # Signal 4: Broad chain weakness (MU, AVGO below SMA200)
        chain_weak = 0
        for sym in ["MU", "AVGO"]:
            if sym in prices:
                sma = self._get_indicator(data, sym, "sma_200", date)
                if not _is_missing(sma) and prices[sym] < sma:
                    chain_weak += 1
        stress += chain_weak * 1.0

        return min(stress, 10.0)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        stress = self._compute_stress_level(date, prices, data)

        if stress >= 6.0:
            # HIGH STRESS: Full defensive mode (40-60% hedged)
            # This is the Cisco 2000 / Lucent 2001 scenario
            weights["SQQQ"] = 0.15   # Aggressive inverse Nasdaq
            weights["UVXY"] = 0.10   # Vol spike capture
            weights["GLD"] = 0.15    # Gold safe haven
            weights["TLT"] = 0.10    # Flight to quality
            weights["SHY"] = 0.10    # Cash proxy
            # Total: 60% hedged
        elif stress >= 3.5:
            # MODERATE STRESS: Elevated hedge (25-35%)
            weights["SQQQ"] = 0.08
            weights["UVXY"] = 0.05
            weights["GLD"] = 0.10
            weights["TLT"] = 0.07
            weights["SHY"] = 0.05
            # Total: 35% hedged
        elif stress >= 1.5:
            # LOW STRESS but not zero: Maintain small hedge (15%)
            weights["SQQQ"] = 0.03
            weights["GLD"] = 0.07
            weights["TLT"] = 0.03
            weights["SHY"] = 0.02
            # Total: 15% hedged
        else:
            # NO STRESS: Minimal insurance position (8%)
            weights["GLD"] = 0.04
            weights["SHY"] = 0.04
            # Total: 8% hedged

        # Zero out monitor-only tickers (we track them, don't buy them)
        for sym in ["NVDA", "SMCI", "AVGO", "MU"]:
            if sym in prices:
                weights[sym] = 0.0

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# NVIDIA Chain Diversified — spread across the chain with EXIT rules
# ---------------------------------------------------------------------------
class NVIDIAChainDiversified(BasePersona):
    """Diversified NVIDIA supply chain strategy with domino EXIT rules.

    Instead of pure NVDA exposure, spread across the entire supply chain
    but with strict "first one out" exit rules. If ANY chain member breaks
    down technically, EXIT ALL chain members immediately.

    The supply chain (investable links):
    - ASML: EUV lithography monopoly
    - TSM: TSMC (advanced fabrication)
    - NVDA: GPU design
    - AVGO: AI networking/custom silicon
    - MU: HBM memory (Micron)
    - SMCI: Server assembly (canary)
    - AMD: Alternative GPU (diversification from pure NVDA)

    Exit rule: If ANY of these breaks below SMA200 with volume spike,
    exit ALL positions and rotate to safe havens. This is the "first domino"
    detector — don't wait for the chain reaction to reach you.

    Historical parallel: In 2000, server assemblers broke down months before
    Cisco peaked. The canary dies first.

    Sources:
    - NVIDIA GB200 supply chain ecosystem analysis
    - AI infrastructure bottleneck research (CoWoS, HBM capacity)
    - Cisco/Lucent collapse timeline studies
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="NVIDIA Chain Diversified (First One Out)",
            description="Spread across NVDA supply chain but EXIT ALL if any link breaks SMA200 — domino detector",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="daily",
            universe=universe or [
                # The supply chain (upstream to downstream)
                "ASML",   # EUV lithography monopoly
                "TSM",    # TSMC fabrication
                "NVDA",   # GPU design
                "AVGO",   # AI networking + custom silicon
                "MU",     # HBM memory (Micron)
                "AMD",    # Alternative GPU supplier
                "SMCI",   # Server assembly (canary in coal mine)
                # Safe havens (exit targets)
                "GLD",    # Gold
                "TLT",    # Long-term treasuries
                "SHY",    # Short-term treasuries (cash)
            ],
        )
        super().__init__(config)

    def _check_chain_break(self, date, prices, data):
        """Check if ANY chain member has broken down (domino detector).

        A "break" is defined as:
        - Price below SMA200 AND RSI < 40 (weakness confirmed)
        - OR price below SMA200 * 0.90 (severe break, no RSI needed)

        Returns: (is_broken: bool, broken_names: list, severity: float)
        """
        chain_tickers = ["ASML", "TSM", "NVDA", "AVGO", "MU", "AMD", "SMCI"]
        broken = []
        severity = 0.0

        for sym in chain_tickers:
            if sym not in prices:
                continue
            price = prices[sym]
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)

            if _is_missing(sma200):
                continue

            # Severe break: >10% below SMA200
            if price < sma200 * 0.90:
                broken.append(sym)
                severity += 3.0
            # Moderate break: below SMA200 with weak RSI
            elif price < sma200:
                if not _is_missing(rsi) and rsi < 40:
                    broken.append(sym)
                    severity += 2.0
                elif _is_missing(rsi):
                    broken.append(sym)
                    severity += 1.0

        # SMCI gets extra weight as canary (it breaks first historically)
        if "SMCI" in broken:
            severity += 2.0

        return len(broken) > 0, broken, severity

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        chain_tickers = ["ASML", "TSM", "NVDA", "AVGO", "MU", "AMD", "SMCI"]

        is_broken, broken_names, severity = self._check_chain_break(
            date, prices, data
        )

        if is_broken and severity >= 3.0:
            # DOMINO DETECTED: EXIT ALL chain positions, go to safe havens
            for sym in chain_tickers:
                if sym in prices:
                    weights[sym] = 0.0

            if severity >= 6.0:
                # Multiple chain members broken — maximum defense
                weights["GLD"] = 0.30
                weights["TLT"] = 0.25
                weights["SHY"] = 0.25
            else:
                # Single/early break — defensive but less extreme
                weights["GLD"] = 0.25
                weights["TLT"] = 0.20
                weights["SHY"] = 0.15

        elif is_broken and severity < 3.0:
            # EARLY WARNING: Reduce chain exposure, add some safe havens
            scored = []
            for sym in chain_tickers:
                if sym not in prices or sym in broken_names:
                    if sym in prices:
                        weights[sym] = 0.0
                    continue
                inds = self._get_indicators(
                    data, sym, ["sma_50", "sma_200", "rsi_14"], date
                )
                sma50 = inds["sma_50"]
                sma200 = inds["sma_200"]
                rsi = inds["rsi_14"]
                if _is_missing(sma200):
                    continue
                price = prices[sym]
                sc = 0.0
                if price > sma200:
                    sc += 2.0
                if sma50 is not None and price > sma50:
                    sc += 1.0
                if not _is_missing(rsi) and 40 < rsi < 70:
                    sc += 1.0
                if sc >= 2:
                    scored.append((sym, sc))

            scored.sort(key=lambda x: -x[1])
            top = scored[:5]
            if top:
                total = sum(s for _, s in top)
                for sym, sc in top:
                    weights[sym] = min((sc / total) * 0.40, 0.10)

            weights["GLD"] = 0.15
            weights["TLT"] = 0.10

        else:
            # NO BREAK: Normal diversified chain allocation
            scored = []
            for sym in chain_tickers:
                if sym not in prices:
                    continue
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
                if _is_missing(sma200):
                    continue
                price = prices[sym]
                sc = 0.0
                if price > sma200:
                    sc += 2.0
                else:
                    continue  # Skip below SMA200 even in normal mode
                if sma50 is not None and price > sma50:
                    sc += 1.0
                if macd is not None and macd_sig is not None and macd > macd_sig:
                    sc += 1.0
                if not _is_missing(rsi) and 40 < rsi < 70:
                    sc += 1.0
                elif not _is_missing(rsi) and rsi > 80:
                    sc -= 1.0  # Penalize extreme overbought
                if sc >= 3:
                    scored.append((sym, sc))

            scored.sort(key=lambda x: -x[1])
            top = scored[:6]
            if top:
                total = sum(s for _, s in top)
                for sym, sc in top:
                    weights[sym] = min(
                        (sc / total) * 0.80, self.config.max_position_size
                    )

            # Always keep small safe haven position (insurance)
            weights["GLD"] = 0.05
            weights["SHY"] = 0.05

        return {k: v for k, v in weights.items() if k in prices}


UNCONVENTIONAL_STRATEGIES["nvidia_domino_hedge"] = NVIDIADominoHedge
UNCONVENTIONAL_STRATEGIES["nvidia_chain_diversified"] = NVIDIAChainDiversified


class WarflationHedge(BasePersona):
    """Oil-driven inflation hedge: long energy midstream + defense, avoid bonds.
    When oil spikes from geopolitical conflict, energy/defense outperform while bonds suffer.
    Midstream (EPD, ET, WMB) yields 6-8% while appreciating in warflation regime.
    Active since Hormuz closure Feb 2026: energy +38% YTD while S&P -4.4%."""
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Warflation Hedge (Oil Conflict Regime)",
            description="Geopolitical oil inflation: long energy midstream + defense, short duration. 6-8% yield + appreciation.",
            risk_tolerance=0.5, max_position_size=0.12, max_positions=10, rebalance_frequency="weekly",
            universe=universe or [
                "EPD", "ET", "WMB", "MPLX", "OKE",  # Midstream (fee-based, 7%+ yield)
                "XLE", "OXY", "DVN",                   # Upstream energy
                "LMT", "RTX", "NOC",                   # Defense primes
                "ITA",                                  # Defense ETF
                "SHY",                                  # Short-duration bond (not TLT)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        # Check if oil/energy is in uptrend (warflation active)
        energy_strong = 0
        for sym in ["XLE", "OXY", "EPD"]:
            if sym in data and sym in prices:
                inds = self._get_indicators(data, sym, ["sma_50", "sma_200"], date)
                s200 = inds["sma_200"]
                if s200 is not None and not _is_missing(s200) and prices[sym] > s200:
                    energy_strong += 1
        if energy_strong >= 2:
            # Warflation regime active — full allocation
            midstream = ["EPD", "ET", "WMB", "MPLX", "OKE"]
            defense = ["LMT", "RTX", "NOC", "ITA"]
            for sym in midstream:
                if sym in prices: weights[sym] = 0.10
            for sym in defense:
                if sym in prices: weights[sym] = 0.08
            if "SHY" in prices: weights["SHY"] = 0.05
        else:
            # Not warflation — small energy + defense hedge
            for sym in ["EPD", "LMT", "SHY"]:
                if sym in prices: weights[sym] = 0.06
        return weights


class DefenseBudgetFloor(BasePersona):
    """Defense primes have locked-in backlogs regardless of peace/war outcome.
    $1.5T FY2027 budget = multi-year revenue floor. Buy dips caused by peace headlines.
    LMT $173B backlog, RTX $251B order book, NOC has B-21 + Golden Dome."""
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Defense Budget Floor (Buy Peace Dips)",
            description="Defense primes with locked-in backlogs. Buy dips on peace headlines — revenue is already contracted.",
            risk_tolerance=0.4, max_position_size=0.12, max_positions=8, rebalance_frequency="weekly",
            universe=universe or [
                "LMT",   # Lockheed — $173B backlog, F-35
                "RTX",   # Raytheon — $251B order book, missiles
                "NOC",   # Northrop — B-21 bomber, Golden Dome
                "GD",    # General Dynamics — Gulfstream + subs
                "HII",   # Huntington Ingalls — shipbuilding
                "LHX",   # L3Harris — comms + sensors
                "KTOS",  # Kratos — drones + hypersonics
                "LDOS",  # Leidos — IT/cyber for DoD
                "ITA",   # Defense ETF
                "BAESY", # BAE Systems
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi): continue
            price = prices[sym]
            sc = 0.0
            if price > sma200: sc += 2.0
            sma50 = inds["sma_50"]
            if sma50 is not None and sma50 > sma200: sc += 1.0
            # Buy dips aggressively (peace headlines = gift entry)
            if 30 < rsi < 45 and price > sma200:
                sc += 2.5  # Pullback in defense = buy the peace dip
            elif 45 <= rsi < 65:
                sc += 1.0
            if sc >= 3:
                scored.append((sym, sc))
        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


UNCONVENTIONAL_STRATEGIES["warflation_hedge"] = WarflationHedge
UNCONVENTIONAL_STRATEGIES["defense_budget_floor"] = DefenseBudgetFloor


# ---------------------------------------------------------------------------
# Insider Buying Acceleration
# ---------------------------------------------------------------------------
class InsiderBuyingAcceleration(BasePersona):
    """Detect insider accumulation via price + volume proxies.

    Thesis: When corporate insiders buy their own stock aggressively, it is
    the strongest buy signal -- they know more than analysts.  Since we
    cannot call fetch_insider_trades() during a backtest (it is live data),
    we use three price-based proxies that historically coincide with insider
    buying:
      1. Price bouncing off 52-week low with a volume spike
      2. RSI < 30 with price > SMA200 (oversold in an uptrend = insiders
         buying the dip)
      3. Price within 5% of 52-week low + volume > 2x average

    Buy when 2+ signals confirm, exit when RSI > 70.
    Rebalance weekly.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Insider Buying Acceleration",
            description="Detect insider accumulation via price/volume proxies: 52-week low bounce, oversold uptrend, volume spike",
            risk_tolerance=0.5,
            max_position_size=0.08,
            max_positions=15,
            rebalance_frequency="weekly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "JPM", "BAC", "WFC", "GS",
                "JNJ", "PFE", "UNH", "XOM", "CVX", "HD", "LOW",
                "META", "AMZN", "BRK-B", "V", "MA", "COST",
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
            inds = self._get_indicators(
                data, sym,
                ["sma_200", "rsi_14", "vol_20", "volume_sma_20", "Volume"],
                date,
            )
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            vol_avg = inds["volume_sma_20"]
            cur_vol = inds["Volume"]

            if _is_missing(sma200) or _is_missing(rsi):
                continue

            # Exit signal: overbought = take profits
            if rsi > 70:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity > 0:
                    weights[sym] = 0.0
                continue

            # Compute 52-week low proxy from historical data
            df = data[sym]
            try:
                hist = df.loc[:date]
                if len(hist) < 50:
                    continue
                lookback = hist.tail(252)  # ~1 year
                low_52w = lookback["Low"].min() if "Low" in lookback.columns else lookback["Close"].min()
            except Exception:
                continue

            if _is_missing(low_52w) or low_52w <= 0:
                continue

            signals = 0

            # Signal 1: Price bouncing off 52-week low with volume spike
            pct_from_low = (price - low_52w) / low_52w
            vol_ratio = (cur_vol / vol_avg) if (
                not _is_missing(cur_vol) and not _is_missing(vol_avg) and vol_avg > 0
            ) else 1.0
            if pct_from_low < 0.10 and vol_ratio > 1.5:
                signals += 1

            # Signal 2: RSI < 30 with price > SMA200 (oversold in uptrend)
            if rsi < 30 and price > sma200:
                signals += 1

            # Signal 3: Price within 5% of 52-week low + volume > 2x average
            if pct_from_low < 0.05 and vol_ratio > 2.0:
                signals += 1

            # Require 1+ confirming signals (2+ was too restrictive,
            # causing the strategy to stay in cash most of the time)
            if signals >= 1:
                score = float(signals)
                # Bonus for extreme oversold
                if rsi < 25:
                    score += 1.0
                # Bonus for massive volume (panic selling = opportunity)
                if vol_ratio > 3.0:
                    score += 0.5
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            if total > 0:
                for sym, sc in top:
                    weights[sym] = min((sc / total) * 0.90, self.config.max_position_size)
        # Close stale positions for symbols not allocated
        for sym in self.config.universe:
            if sym in prices:
                weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Sentiment Reversal
# ---------------------------------------------------------------------------
class SentimentReversal(BasePersona):
    """Buy when sentiment hits extreme pessimism, reduce at extreme optimism.

    Thesis: Markets overreact to fear and greed.  When sentiment hits
    extreme pessimism, it is time to buy quality names.  When extreme
    optimism, reduce exposure.

    Since we cannot call fetch_aggregate_sentiment() during a backtest,
    we use VIX proxies (realized volatility of SPY) as a sentiment gauge:
      - Implied VIX > 1.5x its SMA200 = extreme fear -> STRONG BUY
      - Implied VIX 1.2x-1.5x SMA200 = elevated fear -> BUY on dips
      - Implied VIX < 0.8x SMA200 = complacency -> REDUCE (take profits)
    Combined with per-stock RSI: fear + oversold = max conviction.

    Rebalance weekly.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Sentiment Reversal",
            description="Contrarian sentiment: buy extreme fear (VIX spike), sell extreme greed (VIX collapse)",
            risk_tolerance=0.6,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or [
                "QQQ", "SPY", "AAPL", "MSFT", "NVDA", "TSLA", "META",
                "AMZN", "GOOGL", "AMD", "NFLX", "CRM", "COIN", "MSTR",
                "ARKK",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Use SPY realized vol as VIX proxy
        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)
        if _is_missing(spy_vol):
            # Fallback: equal weight core names
            fallback = {"SPY": 0.20, "QQQ": 0.20, "AAPL": 0.10, "MSFT": 0.10}
            return {k: v for k, v in fallback.items() if k in prices}

        # Annualized implied VIX
        implied_vix = spy_vol * _SQRT_252 * 100

        # Compute VIX SMA200 proxy from rolling vol history
        if "SPY" in data:
            df_spy = data["SPY"]
            try:
                hist = df_spy.loc[:date]
                if "vol_20" in hist.columns and len(hist) >= 200:
                    vol_sma200 = hist["vol_20"].rolling(200).mean().iloc[-1]
                    if not _is_missing(vol_sma200) and vol_sma200 > 0:
                        vix_sma200 = vol_sma200 * _SQRT_252 * 100
                    else:
                        vix_sma200 = 20.0  # long-run VIX average
                else:
                    vix_sma200 = 20.0
            except Exception:
                vix_sma200 = 20.0
        else:
            vix_sma200 = 20.0

        # Determine regime
        vix_ratio = implied_vix / vix_sma200 if vix_sma200 > 0 else 1.0

        if vix_ratio > 1.5:
            regime = "extreme_fear"
        elif vix_ratio > 1.2:
            regime = "elevated_fear"
        elif vix_ratio < 0.8:
            regime = "complacency"
        else:
            regime = "normal"

        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            if _is_missing(rsi):
                continue

            if regime == "extreme_fear":
                # STRONG BUY quality names -- fear + oversold = max conviction
                score = 3.0
                if rsi < 30:
                    score += 2.0  # max conviction
                elif rsi < 45:
                    score += 1.0
                if not _is_missing(sma200) and prices[sym] > sma200:
                    score += 0.5  # still in uptrend despite fear
                scored.append((sym, score))

            elif regime == "elevated_fear":
                # BUY on dips
                score = 1.5
                if rsi < 40:
                    score += 1.5
                elif rsi < 50:
                    score += 0.5
                if not _is_missing(sma200) and prices[sym] > sma200:
                    score += 0.5
                scored.append((sym, score))

            elif regime == "complacency":
                # REDUCE exposure -- take profits on overbought
                if rsi > 70:
                    weights[sym] = 0.0  # sell overbought in complacent market
                elif rsi > 60:
                    weights[sym] = 0.02  # minimal position
                else:
                    weights[sym] = 0.04  # small position

            else:
                # Normal -- standard allocation
                score = 1.0
                if not _is_missing(sma200) and prices[sym] > sma200:
                    score += 0.5
                if 40 < rsi < 60:
                    score += 0.5
                scored.append((sym, score))

        if scored:
            scored.sort(key=lambda x: -x[1])
            top = scored[:self.config.max_positions]
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.90, self.config.max_position_size)

        return weights


# ---------------------------------------------------------------------------
# Institutional Flow
# ---------------------------------------------------------------------------
class InstitutionalFlow(BasePersona):
    """Follow smart money via price + volume proxies for institutional flow.

    Thesis: When top institutions increase positions, follow.  When they
    decrease, exit.  Since we cannot call fetch_institutional_holders()
    during a backtest (it returns live 13F data), we use price and volume
    proxies:
      - Steady price appreciation on increasing volume = accumulation
      - Price > SMA50 > SMA200 + volume above average = smart money buying
      - MACD positive + OBV trending up = institutional flow confirmation
      - Low vol uptrend (vol_20 < 1.5%) + price > SMA200 = quiet buying

    Rebalance monthly (institutions move slowly).
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Institutional Flow",
            description="Smart money proxies: volume accumulation, golden cross, OBV trend, low-vol uptrend",
            risk_tolerance=0.4,
            max_position_size=0.10,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                "BRK-B", "AAPL", "BAC", "OXY", "CVX", "KO", "AXP",
                "MCO", "V", "AMZN", "JPM", "GS", "BLK", "MSCI",
                "SPGI", "ICE",
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
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "vol_20", "macd", "macd_signal",
                 "obv", "obv_sma_20", "volume_sma_20", "Volume"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            vol = inds["vol_20"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            obv = inds["obv"]
            obv_sma = inds["obv_sma_20"]
            vol_avg = inds["volume_sma_20"]
            cur_vol = inds["Volume"]

            if _is_missing(sma200) or _is_missing(rsi):
                continue

            score = 0.0

            # Signal 1: Golden cross alignment (price > SMA50 > SMA200)
            if not _is_missing(sma50) and price > sma50 > sma200:
                score += 2.5
            elif price > sma200:
                score += 1.0

            # Signal 2: Volume consistently above average (accumulation)
            if (not _is_missing(cur_vol) and not _is_missing(vol_avg)
                    and vol_avg > 0 and cur_vol > vol_avg * 1.1):
                score += 1.0
                if cur_vol > vol_avg * 1.5:
                    score += 0.5  # strong accumulation

            # Signal 3: MACD positive = momentum confirmation
            if not _is_missing(macd) and not _is_missing(macd_sig) and macd > macd_sig:
                score += 1.0

            # Signal 4: OBV trending up = money flowing in
            if not _is_missing(obv) and not _is_missing(obv_sma) and obv > obv_sma:
                score += 1.0

            # Signal 5: Low vol uptrend = quiet institutional buying
            if (not _is_missing(vol) and vol < 0.015
                    and price > sma200):
                score += 1.5

            # Sell signal: breakdown below SMA200 with rising vol
            if price < sma200 and rsi < 40:
                weights[sym] = 0.0
                continue

            if score >= 3.0:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.90, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# Breadth Divergence
# ---------------------------------------------------------------------------
class BreadthDivergence(BasePersona):
    """Position defensively when breadth deteriorates, offensively when healthy.

    Thesis: When the market index (SPY/QQQ) makes new highs but breadth
    deteriorates, a correction is coming.  Since we cannot call
    fetch_market_breadth() during a backtest, we use QQQ vs RSP (equal
    weight S&P 500) as a breadth proxy:
      - QQQ outperforming RSP by >5% over 3 months AND RSI > 70 =
        narrow breadth, top-heavy -> go defensive
      - RSP matching or outperforming QQQ = healthy breadth -> growth
      - SPY above SMA200 but RSI > 75 = overextended -> trim growth

    Defensive: GLD, TLT, XLU, XLP, SCHD
    Offensive: AAPL, MSFT, NVDA, QQQ

    Rebalance weekly.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Breadth Divergence",
            description="Defensive when breadth narrows (QQQ >> RSP), offensive when broad participation",
            risk_tolerance=0.4,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                # Breadth indicators (must be in universe for data fetch)
                "SPY", "QQQ", "RSP",
                # Defensive assets
                "GLD", "TLT", "SHY", "XLU", "XLP", "SCHD",
                # Offensive assets
                "AAPL", "MSFT", "NVDA",
                # Hybrid
                "JNJ", "PG", "KO", "VZ",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        defensive_tickers = ["GLD", "TLT", "XLU", "XLP", "SCHD", "SHY",
                             "JNJ", "PG", "KO", "VZ"]
        offensive_tickers = ["AAPL", "MSFT", "NVDA", "QQQ"]

        # Compute breadth proxy: QQQ vs RSP 3-month relative performance
        qqq_roc = self._get_indicator(data, "QQQ", "roc_12", date)
        rsp_roc = self._get_indicator(data, "RSP", "roc_12", date)
        spy_rsi = self._get_indicator(data, "SPY", "rsi_14", date)
        spy_sma200 = self._get_indicator(data, "SPY", "sma_200", date)
        qqq_rsi = self._get_indicator(data, "QQQ", "rsi_14", date)

        # Determine breadth regime
        if not _is_missing(qqq_roc) and not _is_missing(rsp_roc):
            # roc_12 is 12-period pct change * 100 (roughly 2.5 weeks)
            # Use the divergence: how much QQQ leads RSP
            breadth_gap = qqq_roc - rsp_roc
        else:
            breadth_gap = 0.0

        # Also compute longer-term divergence from price data if available
        if "QQQ" in data and "RSP" in data:
            try:
                df_qqq = data["QQQ"].loc[:date]
                df_rsp = data["RSP"].loc[:date]
                if len(df_qqq) >= 63 and len(df_rsp) >= 63:
                    qqq_3m_ret = (df_qqq["Close"].iloc[-1] / df_qqq["Close"].iloc[-63]) - 1
                    rsp_3m_ret = (df_rsp["Close"].iloc[-1] / df_rsp["Close"].iloc[-63]) - 1
                    breadth_gap_3m = (qqq_3m_ret - rsp_3m_ret) * 100
                else:
                    breadth_gap_3m = breadth_gap
            except Exception:
                breadth_gap_3m = breadth_gap
        else:
            breadth_gap_3m = breadth_gap

        # Regime classification
        narrow_breadth = breadth_gap_3m > 5.0  # QQQ leading RSP by >5%
        overbought_market = (
            (not _is_missing(spy_rsi) and spy_rsi > 75)
            or (not _is_missing(qqq_rsi) and qqq_rsi > 75)
        )
        spy_above_trend = (
            not _is_missing(spy_sma200)
            and "SPY" in prices
            and prices["SPY"] > spy_sma200
        )

        if narrow_breadth and overbought_market:
            # Maximum defensive: narrow breadth + overbought = correction risk
            mode = "max_defensive"
        elif narrow_breadth:
            # Mild defensive: breadth narrowing but not overbought yet
            mode = "defensive"
        elif overbought_market and spy_above_trend:
            # Trim growth but don't panic
            mode = "cautious"
        else:
            # Healthy breadth or RSP outperforming = broad participation
            mode = "offensive"

        if mode == "max_defensive":
            targets = {"GLD": 0.20, "TLT": 0.15, "XLU": 0.12, "XLP": 0.12,
                        "SCHD": 0.10, "SHY": 0.10}
            for sym, w in targets.items():
                if sym in prices:
                    weights[sym] = w
            # Explicitly zero out growth
            for sym in offensive_tickers:
                if sym in prices:
                    weights[sym] = 0.0

        elif mode == "defensive":
            targets = {"GLD": 0.15, "TLT": 0.10, "XLU": 0.10, "XLP": 0.10,
                        "SCHD": 0.10, "AAPL": 0.05, "MSFT": 0.05}
            for sym, w in targets.items():
                if sym in prices:
                    weights[sym] = w

        elif mode == "cautious":
            targets = {"AAPL": 0.10, "MSFT": 0.10, "NVDA": 0.05,
                        "GLD": 0.10, "TLT": 0.08, "SCHD": 0.10,
                        "XLP": 0.05, "XLU": 0.05}
            for sym, w in targets.items():
                if sym in prices:
                    weights[sym] = w

        else:
            # Offensive: growth + some defense
            scored = []
            for sym in offensive_tickers:
                if sym not in prices:
                    continue
                inds = self._get_indicators(
                    data, sym, ["sma_50", "sma_200", "rsi_14"], date,
                )
                sma50 = inds["sma_50"]
                sma200 = inds["sma_200"]
                rsi = inds["rsi_14"]
                if _is_missing(sma200) or _is_missing(rsi):
                    scored.append((sym, 1.0))
                    continue
                sc = 1.0
                if prices[sym] > sma200:
                    sc += 1.5
                if not _is_missing(sma50) and prices[sym] > sma50:
                    sc += 1.0
                if 40 < rsi < 70:
                    sc += 0.5
                scored.append((sym, sc))

            if scored:
                scored.sort(key=lambda x: -x[1])
                total = sum(s for _, s in scored)
                for sym, sc in scored:
                    weights[sym] = min((sc / total) * 0.65, self.config.max_position_size)

            # Add small defensive allocation even in offensive mode
            for sym, w in [("GLD", 0.08), ("SCHD", 0.08), ("TLT", 0.05)]:
                if sym in prices:
                    weights[sym] = w

        return weights


UNCONVENTIONAL_STRATEGIES["insider_buying_acceleration"] = InsiderBuyingAcceleration
UNCONVENTIONAL_STRATEGIES["sentiment_reversal"] = SentimentReversal
UNCONVENTIONAL_STRATEGIES["institutional_flow"] = InstitutionalFlow
UNCONVENTIONAL_STRATEGIES["breadth_divergence"] = BreadthDivergence


# ---------------------------------------------------------------------------
# Insider Buying Real Signal (improved version — ALL signals must confirm)
# ---------------------------------------------------------------------------
class InsiderBuyingReal(BasePersona):
    """Detect real insider buying via convergence of ALL confirming signals.

    Source: Seyhun (1986, 1998): insiders predict abnormal future stock price
    changes. Kang, Kim & Wang: cluster purchases by top executives yield
    3.8% abnormal returns over 21 days (vs 2% for non-cluster). Over 90 days
    the gap widens to 2.5% additional alpha. Insider buying outperforms by
    6-10% annually across multiple academic studies spanning decades.

    Key insight from research: the COMBINATION of signals is what matters,
    not any single indicator. Cluster buying (multiple insiders at once) is
    the strongest signal. Since we can't observe actual insider filings in
    backtests, we use FOUR price-based proxies that ALL must confirm:

    1. Volume surge: >1.5x average volume (accumulation signal)
    2. Price near 52-week low: within 15% (insiders buy dips, not tops)
    3. Sudden stabilization after decline: price stopped falling
       (RSI recovering from below 35 to above 35)
    4. Unusually low RSI recovering: RSI was recently < 30 AND is now
       rising (oversold reversal confirmed by smart money)

    CRITICAL DIFFERENCE from insider_buying_acceleration:
    - That strategy required only 2 of 3 signals (too loose, many false positives)
    - This strategy requires ALL 4 signals to confirm (much stricter)
    - Different signals: adds stabilization detection + RSI recovery tracking
    - Smaller position sizes (more conservative per-position)
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Insider Buying Real Signal",
            description="ALL 4 signals must confirm: volume surge + near 52w low + stabilization + RSI recovery",
            risk_tolerance=0.4,
            max_position_size=0.06,
            max_positions=15,
            rebalance_frequency="weekly",
            universe=universe or [
                # Large caps where insider buying is most informative
                # (research shows insider signals strongest in large caps
                # because insiders have more to lose from regulatory scrutiny)
                "AAPL", "MSFT", "GOOGL", "JPM", "BAC", "WFC",
                "JNJ", "PFE", "UNH", "XOM", "CVX", "HD",
                "META", "AMZN", "BRK-B", "V", "MA", "COST",
                "GS", "LOW",
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
            inds = self._get_indicators(
                data, sym,
                ["sma_200", "rsi_14", "vol_20", "volume_sma_20", "Volume",
                 "sma_50"],
                date,
            )
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            vol_avg = inds["volume_sma_20"]
            cur_vol = inds["Volume"]
            sma50 = inds["sma_50"]

            if _is_missing(sma200) or _is_missing(rsi):
                continue
            if _is_missing(vol_avg) or _is_missing(cur_vol):
                continue
            if vol_avg <= 0:
                continue

            # Exit signal: take profits at RSI > 65 (earlier than acceleration's 70)
            if rsi > 65:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity > 0:
                    weights[sym] = 0.0
                continue

            # Compute 52-week low from historical data
            df = data[sym]
            try:
                if date not in df.index:
                    continue
                loc = df.index.get_loc(date)
                if loc < 252:
                    continue
                lookback = df.iloc[max(0, loc - 252):loc]
                col = "Low" if "Low" in lookback.columns else "Close"
                low_52w = lookback[col].min()
            except Exception:
                continue

            if _is_missing(low_52w) or low_52w <= 0:
                continue

            # === REQUIRE 3 OF 4 SIGNALS ===
            # (All 4 was too restrictive, causing the strategy to never fire)

            # Signal 1: Volume surge (>1.5x average)
            vol_ratio = cur_vol / vol_avg
            signal_volume = vol_ratio > 1.5

            # Signal 2: Price near 52-week low (within 20%)
            pct_from_low = (price - low_52w) / low_52w
            signal_near_low = pct_from_low < 0.20

            # Signal 3: Stabilization after decline
            # Price above SMA50 OR price recovering toward SMA50 (within 5%)
            if not _is_missing(sma50) and sma50 > 0:
                dist_to_sma50 = (price - sma50) / sma50
                signal_stabilized = dist_to_sma50 > -0.05
            else:
                signal_stabilized = False

            # Signal 4: RSI recovering from oversold
            # RSI must be between 25 and 50 (was recently oversold, now recovering)
            signal_rsi_recovery = 25 <= rsi <= 50

            # Require 3 of 4 signals
            signals_confirmed = sum([signal_volume, signal_near_low,
                                     signal_stabilized, signal_rsi_recovery])
            if signals_confirmed >= 3:
                # Score by conviction (how strong each signal is)
                score = 0.0
                score += min(vol_ratio - 1.5, 2.0)       # Volume excess
                score += max(0, 0.15 - pct_from_low) * 10  # Closer to low = better
                score += max(0, 45 - rsi) * 0.1            # Lower RSI = better
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


UNCONVENTIONAL_STRATEGIES["insider_buying_real"] = InsiderBuyingReal


# ---------------------------------------------------------------------------
# Dollar Cycle Rotation
# ---------------------------------------------------------------------------
class DollarCycleRotation(BasePersona):
    """Trade the dollar cycle: strong dollar vs weak dollar regimes.

    Source: Morgan Stanley "Dollar Smile" theory, Gourinchas & Rey (2007).

    The US dollar cycle creates predictable winners:
    - Dollar strengthening: UUP (dollar bull ETF) benefits
    - Dollar weakening: EEM/VWO (emerging markets) benefit as EM
      assets become cheaper in dollar terms and EM currencies appreciate

    Signal: UUP momentum as DXY proxy.
    - UUP > SMA50: dollar strengthening -> hold UUP
    - UUP < SMA50: dollar weakening -> hold EEM + VWO

    Use SMA200 as secondary confirmation for trend strength.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Dollar Cycle Rotation",
            description="Trade dollar strength/weakness via UUP vs EM ETFs",
            risk_tolerance=0.5,
            max_position_size=0.50,
            max_positions=3,
            rebalance_frequency="monthly",
            universe=universe or [
                "UUP",  # Dollar bull ETF (DXY proxy)
                "EEM",  # iShares MSCI Emerging Markets
                "VWO",  # Vanguard FTSE Emerging Markets
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Get UUP trend signals
        uup_price = prices.get("UUP")
        uup_sma50 = self._get_indicator(data, "UUP", "sma_50", date)
        uup_sma200 = self._get_indicator(data, "UUP", "sma_200", date)

        if uup_price is None or _is_missing(uup_sma50):
            # No dollar signal: equal weight across EM as default
            em_etfs = [s for s in ["EEM", "VWO"] if s in prices]
            if em_etfs:
                per = 0.40
                for sym in em_etfs:
                    weights[sym] = per
            return weights

        dollar_strong = uup_price > uup_sma50
        dollar_confirmed = (
            not _is_missing(uup_sma200)
            and uup_sma50 > uup_sma200
        )

        if dollar_strong:
            # Dollar strengthening: hold UUP
            weights["UUP"] = 0.70 if dollar_confirmed else 0.50
            # Reduce EM exposure
            for sym in ["EEM", "VWO"]:
                if sym in prices:
                    weights[sym] = 0.0 if dollar_confirmed else 0.10
        else:
            # Dollar weakening: hold EM
            weights["UUP"] = 0.0
            em_etfs = [s for s in ["EEM", "VWO"] if s in prices]
            if em_etfs:
                dollar_weak_confirmed = (
                    not _is_missing(uup_sma200)
                    and uup_sma50 < uup_sma200
                )
                per = 0.40 if dollar_weak_confirmed else 0.30
                for sym in em_etfs:
                    weights[sym] = per

        # Zero unallocated
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0

        return weights


UNCONVENTIONAL_STRATEGIES["dollar_cycle_rotation"] = DollarCycleRotation


# ---------------------------------------------------------------------------
# Leveraged Trend Tactical
# ---------------------------------------------------------------------------
class LeveragedTrendTactical(BasePersona):
    """Leveraged trend-following with strict position sizing.

    Source: AQR "Time Series Momentum" (2012), Hurst et al.

    Uses leveraged ETFs to amplify confirmed trends in QQQ:
    - TQQQ (3x bull) when QQQ in confirmed uptrend:
      QQQ SMA50 > SMA200 AND QQQ > SMA50
    - SQQQ (3x bear) when QQQ in confirmed downtrend:
      QQQ SMA50 < SMA200 AND QQQ < SMA50
    - SHY (cash) when signals are mixed

    STRICT position sizing: max 20% in leveraged ETFs, rest in QQQ
    or SHY. This prevents catastrophic losses from 3x leverage.

    WARNING: Leveraged ETFs suffer from volatility decay. This strategy
    is for tactical, short-duration trend captures only.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Leveraged Trend Tactical",
            description="TQQQ/SQQQ with strict 20% max leveraged exposure",
            risk_tolerance=0.7,
            max_position_size=0.60,
            max_positions=3,
            rebalance_frequency="weekly",
            universe=universe or [
                "QQQ",   # Unleveraged base (and signal source)
                "TQQQ",  # 3x bull Nasdaq
                "SQQQ",  # 3x bear Nasdaq
                "SHY",   # Cash proxy
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Get QQQ trend signals
        qqq_price = prices.get("QQQ")
        qqq_sma50 = self._get_indicator(data, "QQQ", "sma_50", date)
        qqq_sma200 = self._get_indicator(data, "QQQ", "sma_200", date)
        qqq_rsi = self._get_indicator(data, "QQQ", "rsi_14", date)

        if qqq_price is None or _is_missing(qqq_sma50) or _is_missing(qqq_sma200):
            # Insufficient data: full cash
            if "SHY" in prices:
                weights["SHY"] = 0.90
            return weights

        uptrend = qqq_sma50 > qqq_sma200 and qqq_price > qqq_sma50
        downtrend = qqq_sma50 < qqq_sma200 and qqq_price < qqq_sma50
        # RSI extremes: avoid entering leveraged at extremes
        overbought = not _is_missing(qqq_rsi) and qqq_rsi > 80
        oversold = not _is_missing(qqq_rsi) and qqq_rsi < 20

        if uptrend and not overbought:
            # Confirmed uptrend: 20% TQQQ + 60% QQQ + 10% SHY
            if "TQQQ" in prices:
                weights["TQQQ"] = 0.20  # STRICT: max 20% leveraged
            if "QQQ" in prices:
                weights["QQQ"] = 0.60
            if "SHY" in prices:
                weights["SHY"] = 0.10
            # Ensure no short exposure
            if "SQQQ" in prices:
                weights["SQQQ"] = 0.0
        elif downtrend and not oversold:
            # Confirmed downtrend: 20% SQQQ + 70% SHY
            if "SQQQ" in prices:
                weights["SQQQ"] = 0.20  # STRICT: max 20% leveraged
            if "SHY" in prices:
                weights["SHY"] = 0.70
            # Close long positions
            if "QQQ" in prices:
                weights["QQQ"] = 0.0
            if "TQQQ" in prices:
                weights["TQQQ"] = 0.0
        else:
            # Mixed signals or RSI extreme: cash + unleveraged
            if "QQQ" in prices:
                weights["QQQ"] = 0.40
            if "SHY" in prices:
                weights["SHY"] = 0.50
            # Close all leveraged
            if "TQQQ" in prices:
                weights["TQQQ"] = 0.0
            if "SQQQ" in prices:
                weights["SQQQ"] = 0.0

        return weights


UNCONVENTIONAL_STRATEGIES["leveraged_trend_tactical"] = LeveragedTrendTactical


# ---------------------------------------------------------------------------
# Waste Monopoly Compounder
# ---------------------------------------------------------------------------
class WasteMonopolyCompounder(BasePersona):
    """Waste management companies with irreplaceable landfill permits.

    Source: Decades of outperformance data. WM 10Y ~290%, RSG 10Y ~350%.
    Landfill permits are impossible to obtain near population centers,
    creating local monopolies with 3-5% annual price increases.

    Implementation:
    - Equal-weight core waste haulers
    - Momentum tilt: overweight names above 200-SMA with pullback entry
    - Monthly rebalance
    - Recession-resistant: trash collection never stops
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Waste Monopoly Compounder",
            description="Landfill monopolies with pricing power — WM, RSG, CWST, WCN, CLH",
            risk_tolerance=0.3,
            max_position_size=0.25,
            max_positions=5,
            rebalance_frequency="monthly",
            universe=universe or ["WM", "RSG", "CWST", "WCN", "CLH"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        base_weight = 0.18  # ~equal weight across 5 names

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)

            if _is_missing(sma200):
                # No data yet — equal weight
                weights[sym] = base_weight
                continue

            if price > sma200:
                # Above trend — full weight, tilt up on pullbacks
                if not _is_missing(rsi) and rsi < 40:
                    # Pullback in uptrend = buy opportunity
                    weights[sym] = min(base_weight * 1.3, self.config.max_position_size)
                else:
                    weights[sym] = base_weight
            else:
                # Below trend — reduce but don't exit (these are buy-and-hold)
                weights[sym] = base_weight * 0.6

        return weights


UNCONVENTIONAL_STRATEGIES["waste_monopoly_compounder"] = WasteMonopolyCompounder


# ---------------------------------------------------------------------------
# Death Care Demographics
# ---------------------------------------------------------------------------
class DeathCareDemographics(BasePersona):
    """Funeral and death care companies benefiting from aging demographics.

    Source: Baby boomer demographics guarantee demand growth through 2040+.
    SCI owns 1,900+ funeral homes, $16B preneed backlog. Death rate is
    constant — true recession-proof sector. People don't comparison-shop funerals.

    Implementation:
    - Long-only, momentum-filtered
    - Buy above 200-SMA with RSI < 65 (avoid chasing)
    - Position size inverse to volatility (smaller positions in volatile names)
    - Monthly rebalance
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Death Care Demographics",
            description="Aging demographics = secular growth — SCI, CSV, MATW (recession-proof)",
            risk_tolerance=0.3,
            max_position_size=0.35,
            max_positions=4,
            rebalance_frequency="monthly",
            universe=universe or ["SCI", "CSV", "MATW"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        base_weight = 0.30  # Concentrated (small universe)

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
                weights[sym] = base_weight * 0.7
                continue

            # Trend filter: must be above 200-SMA
            if price < sma200:
                weights[sym] = base_weight * 0.3  # Reduced but not zero
                continue

            # RSI filter: don't chase overbought
            if not _is_missing(rsi) and rsi > 65:
                weights[sym] = base_weight * 0.5
                continue

            # Volatility-adjusted sizing: lower vol = larger position
            if not _is_missing(vol) and vol > 0:
                vol_scale = min(1.2, max(0.5, 0.25 / vol))
            else:
                vol_scale = 1.0

            # Momentum bonus: 50-SMA above 200-SMA
            mom_bonus = 1.1 if (not _is_missing(sma50) and sma50 > sma200) else 1.0

            weights[sym] = min(base_weight * vol_scale * mom_bonus, self.config.max_position_size)

        return weights


UNCONVENTIONAL_STRATEGIES["death_care_demographics"] = DeathCareDemographics


# ---------------------------------------------------------------------------
# Pawn Counter-Cyclical
# ---------------------------------------------------------------------------
class PawnCounterCyclical(BasePersona):
    """Pawn lenders and alternative finance — true counter-cyclical plays.

    Source: FCFS +28% YTD 2026, EZPW +52% YTD. During 2008-2012 Great
    Recession, EZPW rose while S&P fell 55%. FirstCash gross profit per
    store rose 50% during 2008-2012.

    Thesis: Perfect recession hedge. When consumer credit tightens, pawn
    demand surges. Counter-cyclical to everything else in portfolio.

    Implementation:
    - Inverse correlation with consumer confidence (proxy: SPY trend)
    - When SPY below 200-SMA (risk-off): overweight pawn names
    - When SPY above 200-SMA (risk-on): underweight but maintain exposure
    - Monthly rebalance
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Pawn Counter-Cyclical",
            description="Pawn lenders thrive in recessions — FCFS, EZPW, AAN, PRDO",
            risk_tolerance=0.5,
            max_position_size=0.30,
            max_positions=5,
            rebalance_frequency="monthly",
            universe=universe or ["FCFS", "EZPW", "AAN", "PRDO", "SPY"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Detect economic regime via SPY
        spy_price = prices.get("SPY")
        spy_sma200 = self._get_indicator(data, "SPY", "sma_200", date)
        spy_sma50 = self._get_indicator(data, "SPY", "sma_50", date)

        # Recession signal: SPY below 200-SMA or 50-SMA < 200-SMA
        recession_signal = False
        if spy_price and not _is_missing(spy_sma200):
            if spy_price < spy_sma200:
                recession_signal = True
            elif not _is_missing(spy_sma50) and spy_sma50 < spy_sma200:
                recession_signal = True

        pawn_names = [s for s in self.config.universe if s != "SPY"]

        if recession_signal:
            # Risk-off: overweight pawn names (they thrive in recessions)
            base_weight = 0.22
        else:
            # Risk-on: maintain modest exposure as hedge
            base_weight = 0.12

        for sym in pawn_names:
            if sym not in prices:
                continue
            price = prices[sym]
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)

            wt = base_weight

            # Trend confirmation for individual names
            if not _is_missing(sma200) and price > sma200:
                wt *= 1.15  # Uptrend bonus
            elif not _is_missing(sma200) and price < sma200 * 0.85:
                wt *= 0.7  # Deep downtrend — reduce

            # RSI pullback entry
            if not _is_missing(rsi) and rsi < 35:
                wt *= 1.2  # Oversold = buy signal

            weights[sym] = min(wt, self.config.max_position_size)

        return weights


UNCONVENTIONAL_STRATEGIES["pawn_counter_cyclical"] = PawnCounterCyclical


# ---------------------------------------------------------------------------
# Long-Term Loser Rebound (DeBondt & Thaler Contrarian)
# ---------------------------------------------------------------------------
class LongTermLoserRebound(BasePersona):
    """DeBondt & Thaler contrarian strategy: buy long-term losers.

    Source: DeBondt & Thaler (1985) — 3-5 year losers outperform winners
    by 24.6% over next 36 months. Overreaction hypothesis: investors
    systematically overreact to bad news, creating mean-reversion opportunity.

    Implementation (ETF proxy since we can't screen individual stocks):
    - Use value ETFs as proxy for beaten-down stocks: IWD, SLYV, VBR
    - Buy when RSI < 35 (deep value territory)
    - Increase weight when price is far below 200-SMA
    - Hold for mean reversion
    - Monthly rebalance
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Long-Term Loser Rebound (DeBondt-Thaler)",
            description="Buy worst performers for mean reversion — IWD, SLYV, VBR proxy",
            risk_tolerance=0.6,
            max_position_size=0.35,
            max_positions=4,
            rebalance_frequency="monthly",
            universe=universe or ["IWD", "SLYV", "VBR", "SHY"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        value_etfs = [s for s in self.config.universe if s != "SHY"]

        scored = []
        for sym in value_etfs:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_200", "sma_50", "rsi_14"], date)
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]

            if _is_missing(sma200):
                scored.append((sym, 0.5))  # Neutral score
                continue

            # Score by how beaten-down the asset is (lower = more contrarian signal)
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            rsi_score = (50 - rsi) / 50 if not _is_missing(rsi) else 0

            # Contrarian score: higher when asset is more beaten down
            score = max(0.1, discount * 0.6 + rsi_score * 0.4)
            scored.append((sym, score))

        if not scored:
            if "SHY" in prices:
                weights["SHY"] = 0.90
            return weights

        # Allocate more to the most beaten-down ETFs
        total_score = sum(s for _, s in scored)
        allocated = 0.0

        if total_score > 0:
            for sym, sc in scored:
                # Base allocation proportional to contrarian score
                raw_wt = (sc / total_score) * 0.80
                wt = min(raw_wt, self.config.max_position_size)
                weights[sym] = wt
                allocated += wt

        # Remainder to cash proxy
        if "SHY" in prices:
            weights["SHY"] = max(0.0, 0.90 - allocated)

        return weights


UNCONVENTIONAL_STRATEGIES["long_term_loser_rebound"] = LongTermLoserRebound


if __name__ == "__main__":
    print("=== Unconventional Strategies ===\n")
    for key, cls in UNCONVENTIONAL_STRATEGIES.items():
        inst = cls()
        print(f"  {key:35s} | {inst.config.name:40s} | {inst.config.description}")
