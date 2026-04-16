# WINNING Strategy: recession_detector

> **What it does:** Regime-switching: risk-on in growth, defensive in recession
>
> **Hypothesis:** Recession Detector (Adaptive)

**Generated:** 2026-04-12T19:04:23.268753
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 54.95%
- **sharpe_ratio:** 1.04
- **max_drawdown:** -14.31%
- **win_rate:** 56.06%
- **alpha:** -7.36%

## Risk Parameters
- **max_portfolio_allocation:** 11.6%
- **stop_loss:** 14.3%
- **take_profit_target:** 7.9%
- **max_drawdown_tolerance:** 14.3%
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
| **TLT** | BUY | 13% | Limit 0.5% below market | 7.5% below entry | 4.2% above entry | 22.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 13.8% below entry | 7.6% above entry | 12.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **IEF** | BUY | 6% | Limit 0.5% below market | 7.2% below entry | 3.9% above entry | 23.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IEF) / [Yahoo](https://finance.yahoo.com/quote/IEF/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 10.3% below entry | 5.7% above entry | 16.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 13.0% below entry | 7.2% above entry | 12.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 62.1% |
| **Avg 5Y Sharpe** | 0.58 |
| **10Y Return** | 151.9% |
| **10Y Sharpe** | 0.55 |
| **HODL Composite** | 0.27 |
| **Consistency** | 89% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -25% drawdown to return 152% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
