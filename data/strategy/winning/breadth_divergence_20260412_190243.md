# WINNING Strategy: breadth_divergence

> **What it does:** Defensive when breadth narrows (QQQ >> RSP), offensive when broad participation
>
> **Hypothesis:** Breadth Divergence

**Generated:** 2026-04-12T19:02:43.478605
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 84.81%
- **sharpe_ratio:** 1.38
- **max_drawdown:** -14.45%
- **win_rate:** 56.06%
- **alpha:** -0.33%

## Risk Parameters
- **max_portfolio_allocation:** 16.0%
- **stop_loss:** 14.4%
- **take_profit_target:** 11.4%
- **max_drawdown_tolerance:** 14.4%
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
| **GLD** | BUY | 23% | Limit 0.5% below market | 13.9% below entry | 11.0% above entry | 16.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SCHD** | BUY | 14% | Limit 0.5% below market | 8.6% below entry | 6.8% above entry | 26.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SCHD) / [Yahoo](https://finance.yahoo.com/quote/SCHD/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 7.6% below entry | 6.0% above entry | 30.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **AAPL** | BUY | 29% | Limit 0.5% below market | 17.4% below entry | 13.7% above entry | 13.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **MSFT** | BUY | 24% | Limit 0.5% below market | 14.8% below entry | 11.7% above entry | 15.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 29.5% below entry | 23.3% above entry | 7.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 13.2% below entry | 10.4% above entry | 17.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 132.3% |
| **Avg 5Y Sharpe** | 1.0 |
| **10Y Return** | 407.3% |
| **10Y Sharpe** | 0.97 |
| **HODL Composite** | 1.46 |
| **Consistency** | 96% |
| **Suitable for passive** | Yes |

This strategy is **suitable for passive investing**.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -20% drawdown to return 407% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
