# LOSING Strategy: cointegration_pairs

> **What it does:** Long laggard in cointegrated pairs when spread Z > 2
>
> **Hypothesis:** Cointegration Pairs Trading

**Generated:** 2026-04-12T19:04:56.407993
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 6.21%
- **sharpe_ratio:** -0.47
- **max_drawdown:** -6.16%
- **win_rate:** 48.60%
- **alpha:** -21.09%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 10.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 6.2%
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
| **UPS** | BUY | 30% | Market order (volatile) | 12.6% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UPS) / [Yahoo](https://finance.yahoo.com/quote/UPS/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.47 (target > 0.5)
- Max drawdown: -6.16% (target > -20%)
- Alpha: -21.09% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 5.7% |
| **Avg 5Y Sharpe** | -0.57 |
| **10Y Return** | 7.0% |
| **10Y Sharpe** | -0.7 |
| **HODL Composite** | 0.0 |
| **Consistency** | 7% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Take profit at +50%. This strategy is inconsistent — capture gains when available.
- **Stop loss:** Reduce position by 50% at -25% drawdown. Consistency is only 7%.
- **Exit rule:** Exit when spread Z-score returns to 0. The convergence trade is done.

</details>
