# WINNING Strategy: leveraged_trend_tactical

> **What it does:** TQQQ/SQQQ with strict 20% max leveraged exposure

**Generated:** 2026-04-14T07:24:11.577239
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 82.35%
- **sharpe_ratio:** 1.07
- **max_drawdown:** -16.19%
- **win_rate:** 56.59%
- **alpha:** -44.12%

## Risk Parameters
- **max_portfolio_allocation:** 11.6%
- **stop_loss:** 16.2%
- **take_profit_target:** 11.1%
- **max_drawdown_tolerance:** 16.2%
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
| **SHY** | BUY | 2% | Limit 0.5% below market | 8.1% below entry | 5.6% above entry | 23.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 14.7% below entry | 10.1% above entry | 12.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **TQQQ** | BUY | 64% | Market order (volatile) | 40.0% below entry | 30.1% above entry | 4.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TQQQ) / [Yahoo](https://finance.yahoo.com/quote/TQQQ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.


<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 123.4% |
| **Avg 5Y Sharpe** | 0.76 |
| **Avg 5Y Max DD** | -23.4% |
| **10Y Return (2015-2024)** | 285.7% |
| **10Y Sharpe** | 0.66 |
| **10Y Max DD** | -27.5% |
| **HODL Composite** | 0.49 |
| **Windows Tested** | 28 |
| **Consistency** | 89% |

### How to Use This Strategy Passively

This strategy has decent long-term performance. **Consider allocating 5-10% of portfolio.** Rebalance quarterly. Use the strategy orchestrator for regime-aware allocation.

</details>
