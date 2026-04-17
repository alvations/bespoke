# WINNING Strategy: adaptive_ensemble

> **What it does:** Regime-switching: momentum in bulls, defensive in bears, quality in transitions
>
> **Hypothesis:** Adaptive Ensemble

**Generated:** 2026-04-12T19:02:47.635631
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 84.05%
- **sharpe_ratio:** 1.22
- **max_drawdown:** -13.24%
- **win_rate:** 56.72%
- **alpha:** -0.50%

## Risk Parameters
- **max_portfolio_allocation:** 12.9%
- **stop_loss:** 13.2%
- **take_profit_target:** 11.3%
- **max_drawdown_tolerance:** 13.2%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** market
- **limit_offset:** market: Auto-managed. No manual entry needed — strategy self-adjusts weekly.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Set it and forget it. Review quarterly.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **GLD** | BUY | 23% | Limit 0.5% below market | 12.7% below entry | 10.9% above entry | 13.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **VIG** | BUY | 14% | Limit 0.5% below market | 7.6% below entry | 6.5% above entry | 22.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VIG) / [Yahoo](https://finance.yahoo.com/quote/VIG/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 12.1% below entry | 10.3% above entry | 14.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 27.0% below entry | 23.1% above entry | 6.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **MSFT** | BUY | 24% | Limit 0.5% below market | 13.5% below entry | 11.6% above entry | 12.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 18.3% below entry | 15.6% above entry | 9.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **SHY** | BUY | 2% | Limit 0.5% below market | 6.6% below entry | 5.7% above entry | 25.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 101.2% |
| **Avg 5Y Sharpe** | 0.81 |
| **10Y Return** | 317.2% |
| **10Y Sharpe** | 0.85 |
| **HODL Composite** | 0.61 |
| **Consistency** | 89% |
| **Suitable for passive** | Yes |

This strategy is **suitable for passive investing**.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -25% drawdown to return 317% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
