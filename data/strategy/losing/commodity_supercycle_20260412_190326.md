# LOSING Strategy: commodity_supercycle

> **What it does:** Ride multi-commodity momentum when commodities outperform stocks
>
> **Hypothesis:** Commodity Supercycle

**Generated:** 2026-04-12T19:03:26.340678
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -8.15%
- **sharpe_ratio:** -0.59
- **max_drawdown:** -22.61%
- **win_rate:** 51.26%
- **alpha:** -25.93%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 33.9%
- **take_profit_target:** 15.0%
- **max_drawdown_tolerance:** 22.6%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy on golden cross (SMA50 > SMA200). These are CYCLE trades — timing matters.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter 30% at signal, add 30% on confirmation, hold 40% for cycle peak.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **DJP** | BUY | 17% | Limit 0.5% below market | 24.8% below entry | 11.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DJP) / [Yahoo](https://finance.yahoo.com/quote/DJP/) |
| **SCCO** | BUY | 43% | Market order (volatile) | 40.0% below entry | 27.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SCCO) / [Yahoo](https://finance.yahoo.com/quote/SCCO/) |
| **MOO** | BUY | 16% | Limit 0.5% below market | 22.5% below entry | 10.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MOO) / [Yahoo](https://finance.yahoo.com/quote/MOO/) |
| **NTR** | BUY | 29% | Limit 0.5% below market | 40.0% below entry | 18.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NTR) / [Yahoo](https://finance.yahoo.com/quote/NTR/) |
| **XME** | BUY | 32% | Market order (volatile) | 40.0% below entry | 20.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XME) / [Yahoo](https://finance.yahoo.com/quote/XME/) |
| **SLV** | BUY | 46% | Market order (volatile) | 40.0% below entry | 29.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SLV) / [Yahoo](https://finance.yahoo.com/quote/SLV/) |
| **COPX** | BUY | 39% | Market order (volatile) | 40.0% below entry | 24.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=COPX) / [Yahoo](https://finance.yahoo.com/quote/COPX/) |
| **GSG** | BUY | 20% | Limit 0.5% below market | 28.2% below entry | 12.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GSG) / [Yahoo](https://finance.yahoo.com/quote/GSG/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 32.6% below entry | 14.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **FCX** | BUY | 45% | Market order (volatile) | 40.0% below entry | 28.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=FCX) / [Yahoo](https://finance.yahoo.com/quote/FCX/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.59 (target > 0.5)
- Max drawdown: -22.61% (target > -20%)
- Alpha: -25.93% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 35.7% |
| **Avg 5Y Sharpe** | 0.19 |
| **10Y Return** | 43.2% |
| **10Y Sharpe** | 0.03 |
| **HODL Composite** | 0.08 |
| **Consistency** | 57% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -30% drawdown to return 43% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
