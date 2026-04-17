# LOSING Strategy: risk_parity_momentum

> **What it does:** Risk parity allocation with momentum tilt across asset classes
>
> **Hypothesis:** Risk Parity + Momentum 3Y

**Generated:** 2026-04-08T14:15:53.261504
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 1.25%
- **sharpe_ratio:** -0.26
- **max_drawdown:** -18.33%
- **win_rate:** 52.79%
- **alpha:** -8.25%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 22.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 18.3%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When trend leaders above SMA50 > SMA200 (golden cross). STRONG BUY: On RSI pullback to 40-55 in confirmed uptrend — ride the trend, don't fight it.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SPY** | BUY | 17% | Limit 0.5% below market | 15.7% below entry | 3.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **XLE** | BUY | 23% | Limit 0.5% below market | 20.9% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLE) / [Yahoo](https://finance.yahoo.com/quote/XLE/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 11.6% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.26 (target > 0.5)
- Max drawdown: -18.33% (target > -20%)
- Alpha: -8.25% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 16.6% |
| **Avg 5Y Sharpe** | -0.03 |
| **Avg 5Y Max DD** | -19.5% |
| **10Y Return (2015-2024)** | 15.3% |
| **10Y Sharpe** | -0.19 |
| **10Y Max DD** | -24.6% |
| **HODL Composite** | 0.05 |
| **Windows Tested** | 28 |
| **Consistency** | 50% |

### How to Use This Strategy Passively

**Weak long-term profile.** Not recommended for passive buy-and-hold. May still work as a tactical or hedged position — see main body.

</details>
