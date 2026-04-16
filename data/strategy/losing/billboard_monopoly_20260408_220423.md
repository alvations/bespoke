# LOSING Strategy: billboard_monopoly

> **What it does:** Irreplaceable physical ad assets: billboards, airports, transit — frozen permits = moat
>
> **Hypothesis:** Billboard & Outdoor Media Monopoly 3Y

**Generated:** 2026-04-08T22:04:22.434288
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -7.63%
- **sharpe_ratio:** -0.27
- **max_drawdown:** -32.47%
- **win_rate:** 52.39%
- **alpha:** -11.28%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 32.5%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When LAMR/CCO are above SMA50. STRONG BUY: On RSI pullback to 35-50 — billboard permits are frozen, digital conversion doubles revenue.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **CCO** | BUY | 53% | Market order (volatile) | 40.0% below entry | 11.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CCO) / [Yahoo](https://finance.yahoo.com/quote/CCO/) |
| **OUT** | BUY | 35% | Market order (volatile) | 36.4% below entry | 7.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=OUT) / [Yahoo](https://finance.yahoo.com/quote/OUT/) |
| **LAMR** | BUY | 24% | Limit 0.5% below market | 25.1% below entry | 5.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LAMR) / [Yahoo](https://finance.yahoo.com/quote/LAMR/) |
| **LYV** | BUY | 30% | Limit 0.5% below market | 31.4% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LYV) / [Yahoo](https://finance.yahoo.com/quote/LYV/) |
| **MSGS** | BUY | 26% | Limit 0.5% below market | 27.3% below entry | 5.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSGS) / [Yahoo](https://finance.yahoo.com/quote/MSGS/) |
| **MGNI** | BUY | 60% | Market order (volatile) | 40.0% below entry | 12.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MGNI) / [Yahoo](https://finance.yahoo.com/quote/MGNI/) |
| **SPOT** | BUY | 43% | Market order (volatile) | 40.0% below entry | 9.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPOT) / [Yahoo](https://finance.yahoo.com/quote/SPOT/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.27 (target > 0.5)
- Max drawdown: -32.47% (target > -20%)
- Alpha: -11.28% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 48.9% |
| **Avg 5Y Sharpe** | 0.31 |
| **Avg 5Y Max DD** | -25.8% |
| **10Y Return (2015-2024)** | 65.7% |
| **10Y Sharpe** | 0.15 |
| **10Y Max DD** | -33.9% |
| **HODL Composite** | 0.18 |
| **Windows Tested** | 28 |
| **Consistency** | 60% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -34% drawdown to return 66% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit if municipalities start revoking billboard permits at scale OR if autonomous vehicles eliminate the value of roadside advertising.

</details>
