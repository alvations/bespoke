# LOSING Strategy: tail_risk_harvest

> **What it does:** Buy quality names after sharp single-day drops, capture mean-reversion
>
> **Hypothesis:** Tail Risk Harvest (Buy Crashes)

**Generated:** 2026-04-12T19:01:44.979465
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 10.73%
- **sharpe_ratio:** -0.03
- **max_drawdown:** -12.12%
- **win_rate:** 39.28%
- **alpha:** -19.66%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 12.1%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 12.1%
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
| **NVDA** | BUY | 49% | Market order (volatile) | 24.7% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 15.2% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.03 (target > 0.5)
- Max drawdown: -12.12% (target > -20%)
- Alpha: -19.66% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 45.7% |
| **Avg 5Y Sharpe** | 0.32 |
| **10Y Return** | 90.4% |
| **10Y Sharpe** | 0.28 |
| **HODL Composite** | 0.27 |
| **Consistency** | 67% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -22% drawdown to return 90% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
