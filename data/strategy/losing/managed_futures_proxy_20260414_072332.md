# LOSING Strategy: managed_futures_proxy

> **What it does:** DBMF + KMLM trend-following with crisis alpha overlay

**Generated:** 2026-04-14T07:23:32.378394
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 2.26%
- **sharpe_ratio:** -0.61
- **max_drawdown:** -6.99%
- **win_rate:** 53.93%
- **alpha:** -64.69%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 7.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 7.0%
- **rebalance_frequency:** monthly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy 0.5% below market in uptrend.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter in 3 tranches over 1-2 weeks.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **DBMF** | BUY | 11% | Limit 0.5% below market | 3.5% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DBMF) / [Yahoo](https://finance.yahoo.com/quote/DBMF/) |
| **KMLM** | BUY | 10% | Limit 0.5% below market | 3.5% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=KMLM) / [Yahoo](https://finance.yahoo.com/quote/KMLM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.61 (target > 0.5)
- Max drawdown: -6.99% (target > -20%)
- Alpha: -64.69% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 15.8% |
| **Avg 5Y Sharpe** | -0.52 |
| **Avg 5Y Max DD** | -9.4% |
| **10Y Return (2015-2024)** | 23.7% |
| **10Y Sharpe** | -0.29 |
| **10Y Max DD** | -14.5% |
| **HODL Composite** | 0.04 |
| **Windows Tested** | 28 |
| **Consistency** | 32% |

### How to Use This Strategy Passively

This strategy is **NOT recommended for passive investing**.

**If you still want exposure:** Limit to 5% of your portfolio maximum.

</details>
