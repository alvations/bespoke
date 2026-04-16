# WINNING Strategy: dynamic_ensemble

> **What it does:** Multi-strategy ensemble weighted by rolling Sharpe ratio
>
> **Hypothesis:** Dynamic Ensemble

**Generated:** 2026-04-12T19:03:36.283547
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 49.08%
- **sharpe_ratio:** 0.88
- **max_drawdown:** -10.87%
- **win_rate:** 55.13%
- **alpha:** -8.84%

## Risk Parameters
- **max_portfolio_allocation:** 11.0%
- **stop_loss:** 10.9%
- **take_profit_target:** 7.1%
- **max_drawdown_tolerance:** 10.9%
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
| **AAPL** | BUY | 29% | Limit 0.5% below market | 13.1% below entry | 8.6% above entry | 9.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **XOM** | BUY | 24% | Limit 0.5% below market | 10.8% below entry | 7.1% above entry | 11.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 10.5% below entry | 6.9% above entry | 11.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **JPM** | BUY | 25% | Limit 0.5% below market | 11.6% below entry | 7.6% above entry | 10.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **V** | BUY | 22% | Limit 0.5% below market | 9.9% below entry | 6.5% above entry | 12.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=V) / [Yahoo](https://finance.yahoo.com/quote/V/) |
| **ABBV** | BUY | 26% | Limit 0.5% below market | 12.1% below entry | 7.9% above entry | 9.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ABBV) / [Yahoo](https://finance.yahoo.com/quote/ABBV/) |
| **MRK** | BUY | 27% | Limit 0.5% below market | 12.5% below entry | 8.2% above entry | 9.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MRK) / [Yahoo](https://finance.yahoo.com/quote/MRK/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 22.2% below entry | 14.6% above entry | 5.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 15.0% below entry | 9.9% above entry | 7.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 7.8% below entry | 5.1% above entry | 15.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 9.9% below entry | 6.5% above entry | 12.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 13.7% below entry | 9.0% above entry | 8.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 94.4% |
| **Avg 5Y Sharpe** | 0.71 |
| **10Y Return** | 248.2% |
| **10Y Sharpe** | 0.69 |
| **HODL Composite** | 0.42 |
| **Consistency** | 92% |
| **Suitable for passive** | Yes |

This strategy is **suitable for passive investing**.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -20% drawdown to return 248% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
