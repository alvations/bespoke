# WINNING Strategy: momentum_crash_hedge

> **What it does:** Momentum with vol-scaling: reduce exposure when volatility spikes
>
> **Hypothesis:** Momentum Crash-Hedged 3Y

**Generated:** 2026-04-08T14:15:50.318880
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 78.30%
- **sharpe_ratio:** 0.86
- **max_drawdown:** -21.11%
- **win_rate:** 46.14%
- **alpha:** 12.68%

## Risk Parameters
- **max_portfolio_allocation:** 8.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 10.7%
- **max_drawdown_tolerance:** 21.1%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** market
- **limit_offset:** use market orders in volatile names
- **timing:** BUY: When top momentum names above SMA200. STRONG BUY: On pullback to SMA50 in uptrend — crash-hedged momentum rides trends but cuts losers fast.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **TSLA** | BUY | 62% | Market order (volatile) | 40.0% below entry | 27.9% above entry | 3.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TSLA) / [Yahoo](https://finance.yahoo.com/quote/TSLA/) |
| **AVGO** | BUY | 55% | Market order (volatile) | 40.0% below entry | 24.6% above entry | 3.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AVGO) / [Yahoo](https://finance.yahoo.com/quote/AVGO/) |
| **AAPL** | BUY | 29% | Limit 0.5% below market | 30.1% below entry | 12.9% above entry | 6.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **META** | BUY | 36% | Market order (volatile) | 37.8% below entry | 16.1% above entry | 5.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |
| **CRWD** | BUY | 48% | Market order (volatile) | 40.0% below entry | 21.4% above entry | 4.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CRWD) / [Yahoo](https://finance.yahoo.com/quote/CRWD/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 31.4% below entry | 13.4% above entry | 6.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 34.3% below entry | 14.6% above entry | 5.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **CRM** | BUY | 33% | Market order (volatile) | 34.9% below entry | 14.9% above entry | 5.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CRM) / [Yahoo](https://finance.yahoo.com/quote/CRM/) |
| **PLTR** | BUY | 64% | Market order (volatile) | 40.0% below entry | 28.5% above entry | 3.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PLTR) / [Yahoo](https://finance.yahoo.com/quote/PLTR/) |
| **NFLX** | BUY | 33% | Market order (volatile) | 34.4% below entry | 14.7% above entry | 5.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NFLX) / [Yahoo](https://finance.yahoo.com/quote/NFLX/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 187.8% |
| **Avg 5Y Sharpe** | 1.01 |
| **Avg 5Y Max DD** | -20.9% |
| **10Y Return (2015-2024)** | 839.7% |
| **10Y Sharpe** | 1.09 |
| **10Y Max DD** | -24.8% |
| **HODL Composite** | 2.21 |
| **Windows Tested** | 28 |
| **Consistency** | 96% |

### How to Use This Strategy Passively

**Strong long-horizon compounder.** Suitable as a core or satellite holding (5-15% of portfolio). Rebalance quarterly or annually.

</details>
