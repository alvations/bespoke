# LOSING Strategy: volatility_premium

> **What it does:** Long low-vol stocks, avoid high-vol: harvesting the low-volatility anomaly

**Generated:** 2026-04-13T13:47:54.331764
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 10.68%
- **sharpe_ratio:** -0.06
- **max_drawdown:** -6.92%
- **win_rate:** 53.26%
- **alpha:** -19.68%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 6.9%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 6.9%
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
| **SPLV** | BUY | 12% | Limit 0.5% below market | 3.5% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPLV) / [Yahoo](https://finance.yahoo.com/quote/SPLV/) |
| **JNJ** | BUY | 18% | Limit 0.5% below market | 5.2% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |
| **PEP** | BUY | 21% | Limit 0.5% below market | 6.0% below entry | 4.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PEP) / [Yahoo](https://finance.yahoo.com/quote/PEP/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.06 (target > 0.5)
- Max drawdown: -6.92% (target > -20%)
- Alpha: -19.68% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 23.8% |
| **Avg 5Y Sharpe** | 0.08 |
| **Avg 5Y Max DD** | -12.5% |
| **10Y Return (2015-2024)** | 46.3% |
| **10Y Sharpe** | 0.02 |
| **10Y Max DD** | -14.0% |
| **HODL Composite** | 0.08 |
| **Windows Tested** | 28 |
| **Consistency** | 64% |

### How to Use This Strategy Passively

This strategy is **NOT recommended for passive investing**. It has low consistency across time periods or negative long-term returns.

**If you still want exposure:** Limit to 5% of your portfolio maximum. Use the strategy orchestrator (conservative_regime) instead for passive allocation.

</details>
