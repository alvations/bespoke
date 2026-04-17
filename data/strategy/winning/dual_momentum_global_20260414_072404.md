# WINNING Strategy: dual_momentum_global

> **What it does:** Antonacci dual momentum: SPY vs EFA vs AGG, SHY fallback

**Generated:** 2026-04-14T07:24:04.569278
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 37.34%
- **sharpe_ratio:** 0.56
- **max_drawdown:** -14.32%
- **win_rate:** 53.27%
- **alpha:** -54.26%

## Risk Parameters
- **max_portfolio_allocation:** 7.6%
- **stop_loss:** 11.5%
- **take_profit_target:** 12.0%
- **max_drawdown_tolerance:** 14.3%
- **rebalance_frequency:** monthly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy on RSI pullback to 40-50 in confirmed uptrend. Never chase.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter 50% initial, add 25% on first pullback, final 25% on trend confirmation.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SPY** | BUY | 17% | Limit 0.5% below market | 8.2% below entry | 8.6% above entry | 10.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.


<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 36.5% |
| **Avg 5Y Sharpe** | 0.23 |
| **Avg 5Y Max DD** | -20.8% |
| **10Y Return (2015-2024)** | 66.4% |
| **10Y Sharpe** | 0.16 |
| **10Y Max DD** | -21.4% |
| **HODL Composite** | 0.09 |
| **Windows Tested** | 28 |
| **Consistency** | 68% |

### How to Use This Strategy Passively

This strategy has decent long-term performance. **Consider allocating 5-10% of portfolio.** Rebalance quarterly. Use the strategy orchestrator for regime-aware allocation.

</details>
