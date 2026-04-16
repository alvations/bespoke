# LOSING Strategy: constellation_contrarian

> **What it does:** STZ 49.8% DCF discount, EFX 34%, NKE permanent moat — most mispriced wide-moat stocks
>
> **Hypothesis:** Constellation Contrarian (Max DCF Discount)

**Generated:** 2026-04-12T19:02:09.405839
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -1.87%
- **sharpe_ratio:** -0.19
- **max_drawdown:** -26.51%
- **win_rate:** 48.87%
- **alpha:** -23.76%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 30.0%
- **take_profit_target:** 10.0%
- **max_drawdown_tolerance:** 26.5%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy below SMA200 or at RSI < 35. Value = patience. Don't rush.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter in 3 tranches over 4-6 weeks as price confirms bottom.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **LULU** | BUY | 46% | Market order (volatile) | 40.0% below entry | 19.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LULU) / [Yahoo](https://finance.yahoo.com/quote/LULU/) |
| **NKE** | BUY | 40% | Market order (volatile) | 40.0% below entry | 17.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NKE) / [Yahoo](https://finance.yahoo.com/quote/NKE/) |
| **EFX** | BUY | 35% | Market order (volatile) | 40.0% below entry | 14.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EFX) / [Yahoo](https://finance.yahoo.com/quote/EFX/) |
| **SAM** | BUY | 32% | Market order (volatile) | 39.7% below entry | 13.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SAM) / [Yahoo](https://finance.yahoo.com/quote/SAM/) |
| **DEO** | BUY | 29% | Limit 0.5% below market | 36.5% below entry | 12.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DEO) / [Yahoo](https://finance.yahoo.com/quote/DEO/) |
| **BUD** | BUY | 24% | Limit 0.5% below market | 29.9% below entry | 10.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BUD) / [Yahoo](https://finance.yahoo.com/quote/BUD/) |
| **PVH** | BUY | 46% | Market order (volatile) | 40.0% below entry | 19.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PVH) / [Yahoo](https://finance.yahoo.com/quote/PVH/) |
| **MNST** | BUY | 24% | Limit 0.5% below market | 30.7% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MNST) / [Yahoo](https://finance.yahoo.com/quote/MNST/) |
| **STZ** | BUY | 30% | Limit 0.5% below market | 37.5% below entry | 12.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=STZ) / [Yahoo](https://finance.yahoo.com/quote/STZ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.19 (target > 0.5)
- Max drawdown: -26.51% (target > -20%)
- Alpha: -23.76% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 33.5% |
| **Avg 5Y Sharpe** | 0.18 |
| **10Y Return** | 62.7% |
| **10Y Sharpe** | 0.14 |
| **HODL Composite** | 0.08 |
| **Consistency** | 60% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -40% drawdown to return 63% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
