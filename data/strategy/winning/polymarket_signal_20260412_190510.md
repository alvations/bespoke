# WINNING Strategy: polymarket_signal

> **What it does:** Political uncertainty→defensive, stability→risk-on (Polymarket proxy)
>
> **Hypothesis:** Polymarket Signal (Uncertainty Proxy)

**Generated:** 2026-04-12T19:05:10.255153
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 41.38%
- **sharpe_ratio:** 0.86
- **max_drawdown:** -11.44%
- **win_rate:** 57.26%
- **alpha:** -10.85%

## Risk Parameters
- **max_portfolio_allocation:** 11.1%
- **stop_loss:** 11.4%
- **take_profit_target:** 6.1%
- **max_drawdown_tolerance:** 11.4%
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
| **TLT** | BUY | 13% | Limit 0.5% below market | 6.0% below entry | 3.2% above entry | 21.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 11.0% below entry | 5.9% above entry | 11.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 8.2% below entry | 4.4% above entry | 15.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 10.4% below entry | 5.6% above entry | 12.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 50.3% |
| **Avg 5Y Sharpe** | 0.44 |
| **10Y Return** | 109.5% |
| **10Y Sharpe** | 0.38 |
| **HODL Composite** | 0.51 |
| **Consistency** | 89% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -19% drawdown to return 110% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
