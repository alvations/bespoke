# LOSING Strategy: all_weather_modern

> **What it does:** Updated Dalio All-Weather: reduced bonds, added TIPS + crypto exposure
>
> **Hypothesis:** All-Weather Modern (2026) 4Y (2022-2025)

**Generated:** 2026-04-08T23:04:04.900885
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 7.94%
- **sharpe_ratio:** -0.56
- **max_drawdown:** -7.15%
- **win_rate:** 52.69%
- **alpha:** -8.93%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 8.6%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 7.2%
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
| **SHY** | BUY | 2% | Limit 0.5% below market | 4.3% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **TIP** | BUY | 4% | Limit 0.5% below market | 4.3% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TIP) / [Yahoo](https://finance.yahoo.com/quote/TIP/) |
| **VEA** | BUY | 35% | Market order (volatile) | 12.7% below entry | 7.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VEA) / [Yahoo](https://finance.yahoo.com/quote/VEA/) |
| **VTI** | BUY | 17% | Limit 0.5% below market | 6.2% below entry | 3.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VTI) / [Yahoo](https://finance.yahoo.com/quote/VTI/) |
| **XLE** | BUY | 23% | Limit 0.5% below market | 8.2% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLE) / [Yahoo](https://finance.yahoo.com/quote/XLE/) |
| **IEF** | BUY | 6% | Limit 0.5% below market | 4.3% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IEF) / [Yahoo](https://finance.yahoo.com/quote/IEF/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 8.3% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.56 (target > 0.5)
- Max drawdown: -7.15% (target > -20%)
- Alpha: -8.93% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 7.5% |
| **Avg 5Y Sharpe** | -0.94 |
| **Avg 5Y Max DD** | -6.1% |
| **10Y Return (2015-2024)** | 13.9% |
| **10Y Sharpe** | -0.96 |
| **10Y Max DD** | -8.0% |
| **HODL Composite** | 0.01 |
| **Windows Tested** | 28 |
| **Consistency** | 14% |

### How to Use This Strategy Passively

This strategy is **NOT recommended for passive investing**. It has low consistency across time periods or negative long-term returns.

**If you still want exposure:** Limit to 5% of your portfolio maximum. Use the strategy orchestrator (conservative_regime) instead for passive allocation.

</details>
