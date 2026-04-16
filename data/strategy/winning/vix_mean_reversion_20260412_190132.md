# WINNING Strategy: vix_mean_reversion

> **What it does:** Buy aggressively when volatility spikes, reduce when complacent
>
> **Hypothesis:** VIX Mean Reversion (Buy Fear)

**Generated:** 2026-04-12T19:01:32.275213
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 56.21%
- **sharpe_ratio:** 1.06
- **max_drawdown:** -10.64%
- **win_rate:** 55.93%
- **alpha:** -7.04%

## Risk Parameters
- **max_portfolio_allocation:** 13.6%
- **stop_loss:** 10.6%
- **take_profit_target:** 8.0%
- **max_drawdown_tolerance:** 10.6%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy 0.5% below market in uptrend.
- **timing:** WAIT FOR SIGNAL: Only enter when price spread between paired stocks reaches extreme levels. Exit when spread normalizes.
- **scaling:** Enter in 3 tranches over 1-2 weeks.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SPY** | BUY | 17% | Limit 0.5% below market | 7.6% below entry | 5.8% above entry | 19.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 9.7% below entry | 7.3% above entry | 15.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 5.6% below entry | 4.2% above entry | 25.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 10.2% below entry | 7.7% above entry | 14.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 45.5% |
| **Avg 5Y Sharpe** | 0.34 |
| **10Y Return** | 88.0% |
| **10Y Sharpe** | 0.25 |
| **HODL Composite** | 0.16 |
| **Consistency** | 75% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -27% drawdown to return 88% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
