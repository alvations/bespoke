# LOSING Strategy: merger_arbitrage

> **What it does:** M&A deal spread capture: buy targets at discount to deal price
>
> **Hypothesis:** Merger Arbitrage (M&A Spread)

**Generated:** 2026-04-12T19:04:13.083369
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -8.27%
- **sharpe_ratio:** -2.22
- **max_drawdown:** -8.27%
- **win_rate:** 18.51%
- **alpha:** -25.98%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 10.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 8.3%
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
| **IEX** | BUY | 27% | Limit 0.5% below market | 11.3% below entry | 5.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IEX) / [Yahoo](https://finance.yahoo.com/quote/IEX/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -2.22 (target > 0.5)
- Max drawdown: -8.27% (target > -20%)
- Alpha: -25.98% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 1.4% |
| **Avg 5Y Sharpe** | -1.3 |
| **10Y Return** | -0.8% |
| **10Y Sharpe** | -1.24 |
| **HODL Composite** | 0.0 |
| **Consistency** | 10% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Take profit at +50%. This strategy is inconsistent — capture gains when available.
- **Stop loss:** Reduce position by 50% at -25% drawdown. Consistency is only 10%.
- **Exit rule:** Review semi-annually. Exit if strategy thesis no longer holds based on fundamental analysis.

</details>
