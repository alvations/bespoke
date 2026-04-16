# LOSING Strategy: unemployment_momentum

> **What it does:** Staffing stock weakness as unemployment proxy, rotate to defensives
>
> **Hypothesis:** Unemployment Claims Momentum 4Y (2022-2025)

**Generated:** 2026-04-08T23:09:14.526058
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -0.23%
- **sharpe_ratio:** -0.33
- **max_drawdown:** -25.01%
- **win_rate:** 52.69%
- **alpha:** -10.93%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 25.0%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When SaaS/AI names (CRM, NOW, NVDA) are above SMA200. STRONG BUY: When staffing stocks (MAN, RHI, ADP) break below SMA200 — automation acceleration confirmed.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SPY** | BUY | 17% | Limit 0.5% below market | 17.9% below entry | 3.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 13.2% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 24.1% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **XLP** | BUY | 13% | Limit 0.5% below market | 13.5% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLP) / [Yahoo](https://finance.yahoo.com/quote/XLP/) |
| **XLV** | BUY | 15% | Limit 0.5% below market | 16.1% below entry | 3.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLV) / [Yahoo](https://finance.yahoo.com/quote/XLV/) |
| **XLU** | BUY | 16% | Limit 0.5% below market | 16.5% below entry | 3.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLU) / [Yahoo](https://finance.yahoo.com/quote/XLU/) |
| **IEF** | BUY | 6% | Limit 0.5% below market | 12.5% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IEF) / [Yahoo](https://finance.yahoo.com/quote/IEF/) |
| **VNQ** | BUY | 15% | Limit 0.5% below market | 15.8% below entry | 3.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VNQ) / [Yahoo](https://finance.yahoo.com/quote/VNQ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.33 (target > 0.5)
- Max drawdown: -25.01% (target > -20%)
- Alpha: -10.93% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 44.8% |
| **Avg 5Y Sharpe** | 0.35 |
| **Avg 5Y Max DD** | -22.3% |
| **10Y Return (2015-2024)** | 80.9% |
| **10Y Sharpe** | 0.24 |
| **10Y Max DD** | -26.3% |
| **HODL Composite** | 0.23 |
| **Windows Tested** | 28 |
| **Consistency** | 71% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -26% drawdown to return 81% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit if the momentum factor itself stops working — when 6+ of your holdings reverse trend in the same month, momentum regime has changed.

</details>
