# WINNING Strategy: late_cycle_bubble_hedge

> **What it does:** Dynamic value/growth rotation based on AI froth detection
>
> **Hypothesis:** Late-Cycle Bubble Hedge

**Generated:** 2026-04-12T19:01:29.863924
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 108.28%
- **sharpe_ratio:** 1.31
- **max_drawdown:** -18.54%
- **win_rate:** 54.46%
- **alpha:** 4.68%

## Risk Parameters
- **max_portfolio_allocation:** 13.1%
- **stop_loss:** 15.0%
- **take_profit_target:** 11.1%
- **max_drawdown_tolerance:** 18.5%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Always hold some. Add more when SPY breaks below SMA200.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Maintain 5-15% allocation. Add during fear, trim during euphoria.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **NVDA** | BUY | 49% | Market order (volatile) | 30.6% below entry | 22.7% above entry | 6.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **AVGO** | BUY | 55% | Market order (volatile) | 34.6% below entry | 25.7% above entry | 5.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AVGO) / [Yahoo](https://finance.yahoo.com/quote/AVGO/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 13.7% below entry | 10.1% above entry | 14.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **MSFT** | BUY | 24% | Limit 0.5% below market | 15.3% below entry | 11.4% above entry | 12.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 18.8% below entry | 14.0% above entry | 10.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **AMD** | BUY | 57% | Market order (volatile) | 35.7% below entry | 26.5% above entry | 5.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMD) / [Yahoo](https://finance.yahoo.com/quote/AMD/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 20.7% below entry | 15.4% above entry | 9.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **AAPL** | BUY | 29% | Limit 0.5% below market | 18.0% below entry | 13.4% above entry | 10.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 78.5% |
| **Avg 5Y Sharpe** | 0.65 |
| **10Y Return** | 190.7% |
| **10Y Sharpe** | 0.61 |
| **HODL Composite** | 2.15 |
| **Consistency** | 89% |
| **Suitable for passive** | Yes |

This strategy is **suitable for passive investing**.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -19% drawdown to return 191% long-term.
- **Exit rule:** This IS the exit strategy — it rotates to value when growth gets frothy.

</details>
