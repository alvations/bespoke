# LOSING Strategy: earnings_gap_and_go

> **What it does:** Buy 4%+ gap-up on 3x volume (earnings proxy). 60-70% win, hold 1-5d
>
> **Hypothesis:** Earnings Gap-and-Go 4Y (2022-2025)

**Generated:** 2026-04-08T23:14:47.679015
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 10.30%
- **sharpe_ratio:** -0.26
- **max_drawdown:** -7.98%
- **win_rate:** 22.55%
- **alpha:** -8.38%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 9.6%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 8.0%
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
| **AAPL** | FLAT | 29% | Limit 0.5% below market | 11.5% below entry | 6.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **MSFT** | FLAT | 24% | Limit 0.5% below market | 9.8% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **NVDA** | FLAT | 49% | Market order (volatile) | 19.6% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **GOOGL** | FLAT | 30% | Limit 0.5% below market | 12.0% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **AMZN** | FLAT | 33% | Market order (volatile) | 13.1% below entry | 6.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **META** | FLAT | 36% | Market order (volatile) | 14.5% below entry | 7.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |
| **TSLA** | FLAT | 62% | Market order (volatile) | 25.1% below entry | 13.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TSLA) / [Yahoo](https://finance.yahoo.com/quote/TSLA/) |
| **NFLX** | FLAT | 33% | Market order (volatile) | 13.2% below entry | 6.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NFLX) / [Yahoo](https://finance.yahoo.com/quote/NFLX/) |
| **CRM** | FLAT | 33% | Market order (volatile) | 13.4% below entry | 7.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CRM) / [Yahoo](https://finance.yahoo.com/quote/CRM/) |
| **AVGO** | FLAT | 55% | Market order (volatile) | 22.1% below entry | 11.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AVGO) / [Yahoo](https://finance.yahoo.com/quote/AVGO/) |
| **AMD** | FLAT | 57% | Market order (volatile) | 22.8% below entry | 11.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMD) / [Yahoo](https://finance.yahoo.com/quote/AMD/) |
| **PLTR** | FLAT | 64% | Market order (volatile) | 25.5% below entry | 13.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PLTR) / [Yahoo](https://finance.yahoo.com/quote/PLTR/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.26 (target > 0.5)
- Max drawdown: -7.98% (target > -20%)
- Alpha: -8.38% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 12.0% |
| **Avg 5Y Sharpe** | -0.39 |
| **Avg 5Y Max DD** | -6.9% |
| **10Y Return (2015-2024)** | 28.6% |
| **10Y Sharpe** | -0.31 |
| **10Y Max DD** | -8.3% |
| **HODL Composite** | 0.01 |
| **Windows Tested** | 28 |
| **Consistency** | 10% |

### How to Use This Strategy Passively

This strategy is **NOT recommended for passive investing**. It has low consistency across time periods or negative long-term returns.

**If you still want exposure:** Limit to 5% of your portfolio maximum. Use the strategy orchestrator (conservative_regime) instead for passive allocation.

</details>
