# LOSING Strategy: global_consumer_staples

> **What it does:** Global pricing power: Unilever, Nestle, P&G, KO, Deere — income + stability
>
> **Hypothesis:** Global Consumer Staples

**Generated:** 2026-04-12T19:01:03.311546
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -3.24%
- **sharpe_ratio:** -0.40
- **max_drawdown:** -16.63%
- **win_rate:** 49.27%
- **alpha:** -24.23%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 16.6%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 16.6%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy 0.5% below market in uptrend.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter in 3 tranches over 1-2 weeks.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **NVO** | BUY | 49% | Market order (volatile) | 33.9% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVO) / [Yahoo](https://finance.yahoo.com/quote/NVO/) |
| **CL** | BUY | 21% | Limit 0.5% below market | 14.4% below entry | 4.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CL) / [Yahoo](https://finance.yahoo.com/quote/CL/) |
| **MKC** | BUY | 25% | Limit 0.5% below market | 17.7% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MKC) / [Yahoo](https://finance.yahoo.com/quote/MKC/) |
| **PG** | BUY | 18% | Limit 0.5% below market | 12.9% below entry | 3.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PG) / [Yahoo](https://finance.yahoo.com/quote/PG/) |
| **COST** | BUY | 21% | Limit 0.5% below market | 14.4% below entry | 4.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=COST) / [Yahoo](https://finance.yahoo.com/quote/COST/) |
| **UL** | BUY | 20% | Limit 0.5% below market | 13.9% below entry | 4.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UL) / [Yahoo](https://finance.yahoo.com/quote/UL/) |
| **DE** | BUY | 29% | Limit 0.5% below market | 20.1% below entry | 6.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DE) / [Yahoo](https://finance.yahoo.com/quote/DE/) |
| **KO** | BUY | 16% | Limit 0.5% below market | 11.4% below entry | 3.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=KO) / [Yahoo](https://finance.yahoo.com/quote/KO/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.40 (target > 0.5)
- Max drawdown: -16.63% (target > -20%)
- Alpha: -24.23% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 49.2% |
| **Avg 5Y Sharpe** | 0.37 |
| **10Y Return** | 101.1% |
| **10Y Sharpe** | 0.33 |
| **HODL Composite** | 0.16 |
| **Consistency** | 71% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -21% drawdown to return 101% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
