# WINNING Strategy: buyback_yield_systematic

> **What it does:** Companies reducing share count via buybacks outperform over time
>
> **Hypothesis:** Net stock issuance anomaly — conservative issuance firms outperformed aggressive diluters over 30 years (amplified post-COVID)

**Generated:** 2026-04-13T19:46:23.693712
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 25.15%
- **sharpe_ratio:** 0.66
- **max_drawdown:** -5.46%
- **win_rate:** 53.13%
- **alpha:** -58.58%

## Risk Parameters
- **max_portfolio_allocation:** 10.6%
- **stop_loss:** 5.5%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 5.5%
- **rebalance_frequency:** monthly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy 0.5% below market in uptrend.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter in 3 tranches over 1-2 weeks.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SHY** | BUY | 2% | Limit 0.5% below market | 2.7% below entry | 3.0% above entry | 21.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **PKW** | BUY | 17% | Limit 0.5% below market | 3.9% below entry | 3.6% above entry | 14.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PKW) / [Yahoo](https://finance.yahoo.com/quote/PKW/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.


## Passive Investor Section

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 28.7% |
| **Avg 5Y Sharpe** | 0.20 |
| **10Y Return** | 53.9% |
| **10Y Sharpe** | 0.10 |
| **HODL Composite** | 0.16 |
| **Consistency** | 68% |
| **Suitable for passive** | No |

This strategy is **not recommended for passive investing**.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** Consider a -25% portfolio-level stop loss.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
