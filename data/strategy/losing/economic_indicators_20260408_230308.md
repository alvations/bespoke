# LOSING Strategy: economic_indicators

> **What it does:** Non-traditional indicators: fashion=confidence, underwear=recession, copper=industrial
>
> **Hypothesis:** Economic Indicator Proxy (Hemline/BigMac/Lipstick) 4Y (2022-2025)

**Generated:** 2026-04-08T23:03:08.520920
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 2.84%
- **sharpe_ratio:** -0.28
- **max_drawdown:** -14.85%
- **win_rate:** 49.90%
- **alpha:** -10.16%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 17.8%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 14.9%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: Balanced allocation across consumer proxies. STRONG BUY risk-on: When MCD/RL/FCX all above SMA200. STRONG BUY defensive: When HBI drops below SMA200 (underwear index recession signal).
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **MCD** | BUY | 18% | Limit 0.5% below market | 13.6% below entry | 3.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MCD) / [Yahoo](https://finance.yahoo.com/quote/MCD/) |
| **RL** | BUY | 36% | Market order (volatile) | 27.1% below entry | 7.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=RL) / [Yahoo](https://finance.yahoo.com/quote/RL/) |
| **FCX** | BUY | 45% | Market order (volatile) | 33.8% below entry | 9.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=FCX) / [Yahoo](https://finance.yahoo.com/quote/FCX/) |
| **PKG** | BUY | 25% | Limit 0.5% below market | 18.9% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PKG) / [Yahoo](https://finance.yahoo.com/quote/PKG/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.28 (target > 0.5)
- Max drawdown: -14.85% (target > -20%)
- Alpha: -10.16% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 31.6% |
| **Avg 5Y Sharpe** | 0.2 |
| **Avg 5Y Max DD** | -17.7% |
| **10Y Return (2015-2024)** | 62.3% |
| **10Y Sharpe** | 0.14 |
| **10Y Max DD** | -19.9% |
| **HODL Composite** | 0.19 |
| **Windows Tested** | 28 |
| **Consistency** | 75% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -20% drawdown to return 62% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit risk-on positions when 3+ indicators flip to recession (underwear down, copper down, cardboard down simultaneously).

</details>
