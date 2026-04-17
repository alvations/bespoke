# WINNING Strategy: long_term_loser_rebound

> **What it does:** DeBondt & Thaler contrarian strategy — buy long-term losers for mean reversion
>
> **Hypothesis:** Investors systematically overreact to bad news. 3-5 year losers outperform winners by 24.6% over next 36 months (DeBondt & Thaler 1985)

**Generated:** 2026-04-13T19:46:17.647919
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 35.11%
- **sharpe_ratio:** 0.51
- **max_drawdown:** -18.67%
- **win_rate:** 51.40%
- **alpha:** -55.78%

## Risk Parameters
- **max_portfolio_allocation:** 6.5%
- **stop_loss:** 18.7%
- **take_profit_target:** 5.3%
- **max_drawdown_tolerance:** 18.7%
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
| **SLYV** | BUY | 22% | Limit 0.5% below market | 17.4% below entry | 4.9% above entry | 7.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SLYV) / [Yahoo](https://finance.yahoo.com/quote/SLYV/) |
| **IWD** | BUY | 14% | Limit 0.5% below market | 11.1% below entry | 3.2% above entry | 10.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IWD) / [Yahoo](https://finance.yahoo.com/quote/IWD/) |
| **VBR** | BUY | 19% | Limit 0.5% below market | 15.0% below entry | 4.3% above entry | 8.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VBR) / [Yahoo](https://finance.yahoo.com/quote/VBR/) |
| **SHY** | BUY | 2% | Limit 0.5% below market | 9.3% below entry | 3.0% above entry | 13.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.


## Passive Investor Section

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 47.6% |
| **Avg 5Y Sharpe** | 0.31 |
| **10Y Return** | 103.0% |
| **10Y Sharpe** | 0.28 |
| **HODL Composite** | 0.31 |
| **Consistency** | 89% |
| **Suitable for passive** | Yes |

This strategy is **suitable for passive investing**.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from 35% drawdown to deliver positive long-term returns.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
