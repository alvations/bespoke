# WINNING Strategy: equal_risk_contrib

> **What it does:** Each asset contributes equal risk, with momentum filter
>
> **Hypothesis:** Equal Risk Contribution (ERC)

**Generated:** 2026-04-12T19:04:50.771386
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 34.60%
- **sharpe_ratio:** 0.76
- **max_drawdown:** -9.37%
- **win_rate:** 55.13%
- **alpha:** -12.68%

## Risk Parameters
- **max_portfolio_allocation:** 10.1%
- **stop_loss:** 9.4%
- **take_profit_target:** 5.2%
- **max_drawdown_tolerance:** 9.4%
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
| **GLD** | BUY | 23% | Limit 0.5% below market | 9.0% below entry | 5.0% above entry | 10.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **EEM** | BUY | 19% | Limit 0.5% below market | 7.5% below entry | 4.2% above entry | 12.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EEM) / [Yahoo](https://finance.yahoo.com/quote/EEM/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 6.7% below entry | 3.7% above entry | 14.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 8.5% below entry | 4.8% above entry | 11.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **IEF** | BUY | 6% | Limit 0.5% below market | 4.7% below entry | 3.0% above entry | 20.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IEF) / [Yahoo](https://finance.yahoo.com/quote/IEF/) |
| **EFA** | BUY | 16% | Limit 0.5% below market | 6.4% below entry | 3.6% above entry | 14.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EFA) / [Yahoo](https://finance.yahoo.com/quote/EFA/) |
| **IWM** | BUY | 22% | Limit 0.5% below market | 8.8% below entry | 4.9% above entry | 10.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IWM) / [Yahoo](https://finance.yahoo.com/quote/IWM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 17.3% |
| **Avg 5Y Sharpe** | -0.04 |
| **10Y Return** | 16.6% |
| **10Y Sharpe** | -0.22 |
| **HODL Composite** | 0.05 |
| **Consistency** | 42% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -30% drawdown to return 17% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
