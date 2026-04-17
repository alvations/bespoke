# WINNING Strategy: sector_monthly_rotation

> **What it does:** Top 3 of 11 sector ETFs by 3-month momentum. 13.94% CAGR
>
> **Hypothesis:** Sector Monthly Rotation

**Generated:** 2026-04-12T19:05:31.698646
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 45.33%
- **sharpe_ratio:** 0.74
- **max_drawdown:** -13.20%
- **win_rate:** 52.06%
- **alpha:** -9.81%

## Risk Parameters
- **max_portfolio_allocation:** 8.8%
- **stop_loss:** 13.2%
- **take_profit_target:** 6.7%
- **max_drawdown_tolerance:** 13.2%
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
| **XLV** | BUY | 15% | Limit 0.5% below market | 8.5% below entry | 4.3% above entry | 13.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLV) / [Yahoo](https://finance.yahoo.com/quote/XLV/) |
| **XLE** | BUY | 23% | Limit 0.5% below market | 12.6% below entry | 6.4% above entry | 9.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLE) / [Yahoo](https://finance.yahoo.com/quote/XLE/) |
| **XLP** | BUY | 13% | Limit 0.5% below market | 7.2% below entry | 3.6% above entry | 16.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLP) / [Yahoo](https://finance.yahoo.com/quote/XLP/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 13.0% |
| **Avg 5Y Sharpe** | -0.06 |
| **10Y Return** | 17.1% |
| **10Y Sharpe** | -0.11 |
| **HODL Composite** | 0.06 |
| **Consistency** | 50% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -28% drawdown to return 17% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
