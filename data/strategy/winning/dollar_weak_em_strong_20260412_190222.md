# WINNING Strategy: dollar_weak_em_strong

> **What it does:** USD weakens → EM stocks + commodities + gold outperform. Inverse dollar-to-EM signal.
>
> **Hypothesis:** Dollar Weak → EM Strong (Currency Rotation)

**Generated:** 2026-04-12T19:02:22.585770
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 36.75%
- **sharpe_ratio:** 0.85
- **max_drawdown:** -13.03%
- **win_rate:** 57.52%
- **alpha:** -12.09%

## Risk Parameters
- **max_portfolio_allocation:** 14.1%
- **stop_loss:** 11.7%
- **take_profit_target:** 8.0%
- **max_drawdown_tolerance:** 13.0%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** market
- **limit_offset:** market: Enter immediately when trigger fires. Speed matters more than price.
- **timing:** WAIT FOR SIGNAL: Only enter when US dollar is weakening. Long emerging markets + gold. Exit when dollar strengthens.
- **scaling:** Full position at trigger. No scaling — the signal is binary.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **GLD** | BUY | 23% | Limit 0.5% below market | 11.3% below entry | 7.7% above entry | 14.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **EEM** | BUY | 19% | Limit 0.5% below market | 9.4% below entry | 6.4% above entry | 17.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EEM) / [Yahoo](https://finance.yahoo.com/quote/EEM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 58.5% |
| **Avg 5Y Sharpe** | 0.53 |
| **10Y Return** | 142.9% |
| **10Y Sharpe** | 0.53 |
| **HODL Composite** | 0.40 |
| **Consistency** | 71% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -13% drawdown to return 143% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
