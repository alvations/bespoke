# WINNING Strategy: drawdown_severity_rotation

> **What it does:** Shift equities→bonds→gold→cash as drawdown deepens

**Generated:** 2026-04-14T07:39:50.640201
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 76.43%
- **sharpe_ratio:** 0.78
- **max_drawdown:** -8.22%
- **win_rate:** 55.24%
- **alpha:** -44.55%

## Risk Parameters
- **max_portfolio_allocation:** 19.2%
- **stop_loss:** 8.2%
- **take_profit_target:** 10.4%
- **max_drawdown_tolerance:** 8.2%
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
| **GLD** | BUY | 23% | Limit 0.5% below market | 7.9% below entry | 10.0% above entry | 20.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 4.3% below entry | 5.5% above entry | 36.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 5.9% below entry | 7.5% above entry | 26.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 7.5% below entry | 9.5% above entry | 21.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 38.7% |
| **Avg 5Y Sharpe** | 0.32 |
| **Avg 5Y Max DD** | -16.3% |
| **10Y Return (2015-2024)** | 97.1% |
| **10Y Sharpe** | 0.27 |
| **10Y Max DD** | -21.7% |
| **HODL Composite** | 0.17 |
| **Windows Tested** | 28 |
| **Consistency** | 79% |

### How to Use This Strategy Passively

This strategy has decent long-term performance. **Consider allocating 5-10% of portfolio.** Rebalance quarterly.

</details>
