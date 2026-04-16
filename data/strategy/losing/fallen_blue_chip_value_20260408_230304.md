# LOSING Strategy: fallen_blue_chip_value

> **What it does:** Once-great blue chips at deep discounts: turnaround catalysts + dividend income
>
> **Hypothesis:** Fallen Blue Chip Value 4Y (2022-2025)

**Generated:** 2026-04-08T23:03:04.090496
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 3.08%
- **sharpe_ratio:** -0.13
- **max_drawdown:** -25.59%
- **win_rate:** 48.50%
- **alpha:** -10.10%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 25.6%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When target names show MACD reversal from below signal line. STRONG BUY: When RSI < 35 AND price > 10% below SMA200 — deep value entry at maximum pessimism.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **MDT** | BUY | 20% | Limit 0.5% below market | 21.3% below entry | 4.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MDT) / [Yahoo](https://finance.yahoo.com/quote/MDT/) |
| **PFE** | BUY | 25% | Limit 0.5% below market | 25.8% below entry | 5.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PFE) / [Yahoo](https://finance.yahoo.com/quote/PFE/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.13 (target > 0.5)
- Max drawdown: -25.59% (target > -20%)
- Alpha: -10.10% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 15.7% |
| **Avg 5Y Sharpe** | 0.01 |
| **Avg 5Y Max DD** | -24.9% |
| **10Y Return (2015-2024)** | 24.9% |
| **10Y Sharpe** | -0.06 |
| **10Y Max DD** | -29.7% |
| **HODL Composite** | 0.05 |
| **Windows Tested** | 28 |
| **Consistency** | 46% |

### How to Use This Strategy Passively

This strategy is **NOT recommended for passive investing**. It has low consistency across time periods or negative long-term returns.

**If you still want exposure:** Limit to 5% of your portfolio maximum. Use the strategy orchestrator (conservative_regime) instead for passive allocation.

</details>
