# LOSING Strategy: equal_risk_contrib

> **What it does:** Each asset contributes equal risk, with momentum filter
>
> **Hypothesis:** Equal Risk Contribution (ERC) 4Y (2022-2025)

**Generated:** 2026-04-08T23:11:03.439800
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 5.06%
- **sharpe_ratio:** -0.22
- **max_drawdown:** -25.70%
- **win_rate:** 52.50%
- **alpha:** -9.62%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 25.7%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When holdings above SMA200 on weekly rebalance. STRONG BUY: On RSI pullback to 35-50 in confirmed uptrend — buy the dip in quality.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SPY** | BUY | 17% | Limit 0.5% below market | 17.9% below entry | 3.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **EFA** | BUY | 16% | Limit 0.5% below market | 16.9% below entry | 3.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EFA) / [Yahoo](https://finance.yahoo.com/quote/EFA/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 22.7% below entry | 4.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **EEM** | BUY | 19% | Limit 0.5% below market | 19.6% below entry | 3.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EEM) / [Yahoo](https://finance.yahoo.com/quote/EEM/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 24.1% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **IEF** | BUY | 6% | Limit 0.5% below market | 12.5% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IEF) / [Yahoo](https://finance.yahoo.com/quote/IEF/) |
| **IWM** | BUY | 22% | Limit 0.5% below market | 23.3% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IWM) / [Yahoo](https://finance.yahoo.com/quote/IWM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.22 (target > 0.5)
- Max drawdown: -25.70% (target > -20%)
- Alpha: -9.62% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 17.3% |
| **Avg 5Y Sharpe** | -0.04 |
| **Avg 5Y Max DD** | -22.5% |
| **10Y Return (2015-2024)** | 16.6% |
| **10Y Sharpe** | -0.22 |
| **10Y Max DD** | -29.8% |
| **HODL Composite** | 0.04 |
| **Windows Tested** | 28 |
| **Consistency** | 42% |

### How to Use This Strategy Passively

This strategy is **NOT recommended for passive investing**. It has low consistency across time periods or negative long-term returns.

**If you still want exposure:** Limit to 5% of your portfolio maximum. Use the strategy orchestrator (conservative_regime) instead for passive allocation.

</details>
