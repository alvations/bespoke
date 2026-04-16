# LOSING Strategy: stat_arb_medallion

> **What it does:** Short-term mean reversion across sector pairs, Renaissance-inspired
>
> **Hypothesis:** Stat Arb (Medallion-style)

**Generated:** 2026-04-12T19:03:42.877649
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 10.20%
- **sharpe_ratio:** -0.14
- **max_drawdown:** -3.64%
- **win_rate:** 50.47%
- **alpha:** -19.83%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 10.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 3.6%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Enter when Z-score exceeds 2.0. Exit when Z returns to 0.
- **timing:** WAIT FOR SIGNAL: Only enter when price spread between paired stocks reaches extreme levels. Exit when spread normalizes.
- **scaling:** Full position at entry. No scaling — it's a convergence trade.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **PG** | BUY | 18% | Limit 0.5% below market | 7.7% below entry | 3.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PG) / [Yahoo](https://finance.yahoo.com/quote/PG/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.14 (target > 0.5)
- Max drawdown: -3.64% (target > -20%)
- Alpha: -19.83% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 12.6% |
| **Avg 5Y Sharpe** | -0.34 |
| **10Y Return** | 22.6% |
| **10Y Sharpe** | -0.43 |
| **HODL Composite** | 0.02 |
| **Consistency** | 35% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Take profit at +50%. This strategy is inconsistent — capture gains when available.
- **Stop loss:** Reduce position by 50% at -25% drawdown. Consistency is only 35%.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
