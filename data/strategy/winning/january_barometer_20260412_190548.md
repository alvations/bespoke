# WINNING Strategy: january_barometer

> **What it does:** As January goes, so goes the year. 86% accuracy when Jan positive
>
> **Hypothesis:** January Barometer

**Generated:** 2026-04-12T19:05:48.336996
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 87.17%
- **sharpe_ratio:** 1.34
- **max_drawdown:** -11.53%
- **win_rate:** 56.72%
- **alpha:** 0.20%

## Risk Parameters
- **max_portfolio_allocation:** 14.1%
- **stop_loss:** 8.0%
- **take_profit_target:** 7.0%
- **max_drawdown_tolerance:** 11.5%
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
| **TLT** | BUY | 13% | Limit 0.5% below market | 4.2% below entry | 3.7% above entry | 26.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 7.7% below entry | 6.7% above entry | 14.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 5.7% below entry | 5.0% above entry | 19.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 7.3% below entry | 6.4% above entry | 15.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **IWM** | BUY | 22% | Limit 0.5% below market | 7.5% below entry | 6.5% above entry | 15.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IWM) / [Yahoo](https://finance.yahoo.com/quote/IWM/) |
| **AAPL** | BUY | 29% | Limit 0.5% below market | 9.6% below entry | 8.4% above entry | 11.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 117.1% |
| **Avg 5Y Sharpe** | 0.82 |
| **10Y Return** | 263.9% |
| **10Y Sharpe** | 0.69 |
| **HODL Composite** | 0.58 |
| **Consistency** | 89% |
| **Suitable for passive** | Yes |

This strategy is **suitable for passive investing**.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -24% drawdown to return 264% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
