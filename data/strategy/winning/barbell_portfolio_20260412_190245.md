# WINNING Strategy: barbell_portfolio

> **What it does:** Short bonds + long bonds + growth equities — skip the middle
>
> **Hypothesis:** Barbell Portfolio

**Generated:** 2026-04-12T19:02:45.645215
**Assessment:** STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence.

## Performance Summary
- **total_return:** 163.72%
- **sharpe_ratio:** 1.90
- **max_drawdown:** -12.08%
- **win_rate:** 56.99%
- **alpha:** 15.18%

## Risk Parameters
- **max_portfolio_allocation:** 17.5%
- **stop_loss:** 10.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 12.1%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Enter when Z-score exceeds 2.0. Exit when Z returns to 0.
- **timing:** WAIT FOR SIGNAL: Only enter when price spread between paired stocks reaches extreme levels. Exit when spread normalizes.
- **scaling:** Full position at entry. No scaling — it's a convergence trade.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SHY** | BUY | 2% | Limit 0.5% below market | 5.0% below entry | 3.0% above entry | 35.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 5.3% below entry | 3.0% above entry | 33.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 20.4% below entry | 10.2% above entry | 8.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 9.6% below entry | 4.8% above entry | 18.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **MSFT** | BUY | 24% | Limit 0.5% below market | 10.2% below entry | 5.1% above entry | 17.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 12.6% below entry | 6.3% above entry | 13.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 13.8% below entry | 6.9% above entry | 12.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 161.0% |
| **Avg 5Y Sharpe** | 1.1 |
| **10Y Return** | 682.6% |
| **10Y Sharpe** | 1.22 |
| **HODL Composite** | 0.8 |
| **Consistency** | 96% |
| **Suitable for passive** | Yes |

This strategy is **suitable for passive investing**.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -31% drawdown to return 683% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
