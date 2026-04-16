# LOSING Strategy: williams_percent_r

> **What it does:** Buy %R<-90 above SMA200, exit close>prev high. 77% win SPY, 22% invested
>
> **Hypothesis:** Williams %R(2) Mean Reversion 4Y (2022-2025)

**Generated:** 2026-04-08T23:12:54.715166
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 15.11%
- **sharpe_ratio:** -0.05
- **max_drawdown:** -5.90%
- **win_rate:** 20.46%
- **alpha:** -7.28%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 7.1%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 5.9%
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
| **SPY** | BUY | 17% | Limit 0.5% below market | 5.1% below entry | 3.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 6.4% below entry | 4.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **DIA** | BUY | 15% | Limit 0.5% below market | 4.5% below entry | 3.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DIA) / [Yahoo](https://finance.yahoo.com/quote/DIA/) |
| **MSFT** | BUY | 24% | Limit 0.5% below market | 7.3% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 14.5% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **AAPL** | BUY | 29% | Limit 0.5% below market | 8.5% below entry | 6.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.05 (target > 0.5)
- Max drawdown: -5.90% (target > -20%)
- Alpha: -7.28% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 19.2% |
| **Avg 5Y Sharpe** | -0.04 |
| **Avg 5Y Max DD** | -7.8% |
| **10Y Return (2015-2024)** | 35.7% |
| **10Y Sharpe** | -0.11 |
| **10Y Max DD** | -9.2% |
| **HODL Composite** | 0.08 |
| **Windows Tested** | 28 |
| **Consistency** | 46% |

### How to Use This Strategy Passively

This strategy is **NOT recommended for passive investing**. It has low consistency across time periods or negative long-term returns.

**If you still want exposure:** Limit to 5% of your portfolio maximum. Use the strategy orchestrator (conservative_regime) instead for passive allocation.

</details>
