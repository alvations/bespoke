# LOSING Strategy: factor_etf_rotation

> **What it does:** Rotate between factor ETFs (momentum, quality, value, low vol) based on trend
>
> **Hypothesis:** Factor ETF Rotation 3Y

**Generated:** 2026-04-08T14:16:02.478407
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -0.48%
- **sharpe_ratio:** -0.25
- **max_drawdown:** -27.42%
- **win_rate:** 49.47%
- **alpha:** -8.82%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 27.4%
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
| **MTUM** | BUY | 22% | Limit 0.5% below market | 23.1% below entry | 4.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MTUM) / [Yahoo](https://finance.yahoo.com/quote/MTUM/) |
| **IWM** | BUY | 22% | Limit 0.5% below market | 23.3% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IWM) / [Yahoo](https://finance.yahoo.com/quote/IWM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.25 (target > 0.5)
- Max drawdown: -27.42% (target > -20%)
- Alpha: -8.82% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 41.9% |
| **Avg 5Y Sharpe** | 0.27 |
| **Avg 5Y Max DD** | -28.6% |
| **10Y Return (2015-2024)** | 82.1% |
| **10Y Sharpe** | 0.21 |
| **10Y Max DD** | -30.8% |
| **HODL Composite** | 0.23 |
| **Windows Tested** | 28 |
| **Consistency** | 79% |

### How to Use This Strategy Passively

**Marginal long-term returns.** Treat as tactical, not core. Small allocation (<2%) if any.

</details>
