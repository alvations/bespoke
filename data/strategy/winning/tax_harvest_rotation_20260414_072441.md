# WINNING Strategy: tax_harvest_rotation

> ⚠ **Stale data:** This strategy is no longer in the active backtest universe. Numbers below reflect an earlier run under the prior flat-averaged composite formula. Re-run `scripts/update_strategy_composites.py` after adding the strategy back to the registry.

> **What it does:** Tax-loss harvesting via correlated ETF swaps on drawdowns

**Generated:** 2026-04-14T07:24:41.204799
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 210.81%
- **sharpe_ratio:** 0.93
- **max_drawdown:** -18.55%
- **win_rate:** 56.81%
- **alpha:** -19.37%

## Risk Parameters
- **max_portfolio_allocation:** 21.9%
- **stop_loss:** 18.5%
- **take_profit_target:** 23.0%
- **max_drawdown_tolerance:** 18.5%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** market
- **limit_offset:** market: Use market orders for volatile names.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter in 3 tranches over 1-2 weeks.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SPY** | BUY | 17% | Limit 0.5% below market | 13.3% below entry | 16.5% above entry | 30.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **VTI** | BUY | 17% | Limit 0.5% below market | 13.4% below entry | 16.6% above entry | 30.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VTI) / [Yahoo](https://finance.yahoo.com/quote/VTI/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 16.9% below entry | 21.0% above entry | 24.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.


<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 95.4% |
| **Avg 5Y Sharpe** | 0.62 |
| **Avg 5Y Max DD** | -27.5% |
| **10Y Return (2015-2024)** | 241.2% |
| **10Y Sharpe** | 0.58 |
| **10Y Max DD** | -29.6% |
| **HODL Composite** | 0.40 |
| **Windows Tested** | 28 |
| **Consistency** | 93% |

### How to Use This Strategy Passively

This strategy has decent long-term performance. **Consider allocating 5-10% of portfolio.** Rebalance quarterly. Use the strategy orchestrator for regime-aware allocation.

</details>
