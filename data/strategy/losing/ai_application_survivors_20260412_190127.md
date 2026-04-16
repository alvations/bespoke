# LOSING Strategy: ai_application_survivors

> **What it does:** The Amazons of AI: real-revenue application companies that survive the bust
>
> **Hypothesis:** AI Application Survivors

**Generated:** 2026-04-12T19:01:27.253640
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 3.59%
- **sharpe_ratio:** -0.25
- **max_drawdown:** -19.28%
- **win_rate:** 36.35%
- **alpha:** -21.94%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 17.4%
- **take_profit_target:** 10.0%
- **max_drawdown_tolerance:** 19.3%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy when NVDA above SMA50 (demand signal). Don't buy if NVDA below SMA200.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter 40% initial, add on NVDA pullback to SMA50, full position on confirmation.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **CRM** | BUY | 33% | Market order (volatile) | 24.3% below entry | 14.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CRM) / [Yahoo](https://finance.yahoo.com/quote/CRM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.25 (target > 0.5)
- Max drawdown: -19.28% (target > -20%)
- Alpha: -21.94% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 31.9% |
| **Avg 5Y Sharpe** | 0.16 |
| **10Y Return** | 49.5% |
| **10Y Sharpe** | 0.06 |
| **HODL Composite** | 0.07 |
| **Consistency** | 50% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -19% drawdown to return 50% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
