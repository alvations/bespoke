# WINNING Strategy: santa_claus_rally

> **What it does:** Last 5 days Dec + first 2 Jan: 80% win rate, 1.3% avg. Q1 signal
>
> **Hypothesis:** Santa Claus Rally

**Generated:** 2026-04-12T19:05:49.472503
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 77.35%
- **sharpe_ratio:** 1.52
- **max_drawdown:** -7.68%
- **win_rate:** 55.53%
- **alpha:** -2.01%

## Risk Parameters
- **max_portfolio_allocation:** 16.6%
- **stop_loss:** 8.0%
- **take_profit_target:** 6.3%
- **max_drawdown_tolerance:** 7.7%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** market
- **limit_offset:** market: Enter on calendar date. Timing IS the strategy — don't wait for better price.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Full position on entry date. Exit on exit date. No scaling needed.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SPY** | BUY | 17% | Limit 0.5% below market | 5.7% below entry | 4.5% above entry | 23.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 7.3% below entry | 5.8% above entry | 18.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **IWM** | BUY | 22% | Limit 0.5% below market | 7.5% below entry | 5.9% above entry | 17.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IWM) / [Yahoo](https://finance.yahoo.com/quote/IWM/) |
| **AAPL** | BUY | 29% | Limit 0.5% below market | 9.6% below entry | 7.6% above entry | 13.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **MSFT** | BUY | 24% | Limit 0.5% below market | 8.2% below entry | 6.5% above entry | 16.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 16.3% below entry | 12.9% above entry | 8.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 11.1% below entry | 8.8% above entry | 12.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **META** | BUY | 36% | Market order (volatile) | 12.2% below entry | 9.6% above entry | 10.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 39.0% |
| **Avg 5Y Sharpe** | 0.3 |
| **10Y Return** | 67.3% |
| **10Y Sharpe** | 0.17 |
| **HODL Composite** | 0.13 |
| **Consistency** | 67% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -23% drawdown to return 67% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
