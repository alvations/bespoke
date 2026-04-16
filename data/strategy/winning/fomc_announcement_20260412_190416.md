# WINNING Strategy: fomc_announcement

> **What it does:** Pre-FOMC drift: 50 bps excess return, Sharpe 0.75-1.04
>
> **Hypothesis:** FOMC Announcement

**Generated:** 2026-04-12T19:04:16.373404
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 39.87%
- **sharpe_ratio:** 0.98
- **max_drawdown:** -8.16%
- **win_rate:** 55.93%
- **alpha:** -11.25%

## Risk Parameters
- **max_portfolio_allocation:** 12.5%
- **stop_loss:** 8.2%
- **take_profit_target:** 5.9%
- **max_drawdown_tolerance:** 8.2%
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
| **TLT** | BUY | 13% | Limit 0.5% below market | 4.3% below entry | 3.1% above entry | 23.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 5.9% below entry | 4.3% above entry | 17.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 7.9% below entry | 5.7% above entry | 13.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 7.4% below entry | 5.4% above entry | 13.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **SHY** | BUY | 2% | Limit 0.5% below market | 4.1% below entry | 3.0% above entry | 25.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 28.2% |
| **Avg 5Y Sharpe** | 0.16 |
| **10Y Return** | 45.8% |
| **10Y Sharpe** | 0.02 |
| **HODL Composite** | 0.08 |
| **Consistency** | 60% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -21% drawdown to return 46% long-term.
- **Exit rule:** Exit at market close on FOMC announcement day.

</details>
