# WINNING Strategy: vix_spike_buyback

> **What it does:** Fear spikes → buy companies with massive buyback programs. They buy themselves cheap in panics.
>
> **Hypothesis:** VIX Spike → Cash-Rich Buyback

**Generated:** 2026-04-12T19:02:25.310782
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 48.72%
- **sharpe_ratio:** 1.14
- **max_drawdown:** -6.88%
- **win_rate:** 56.19%
- **alpha:** -8.93%

## Risk Parameters
- **max_portfolio_allocation:** 19.6%
- **stop_loss:** 6.2%
- **take_profit_target:** 8.0%
- **max_drawdown_tolerance:** 6.9%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** market
- **limit_offset:** market: Enter immediately when trigger fires. Speed matters more than price.
- **timing:** SAFE TO BUY. Even better: add more during market panic — these cash-rich companies buy back their own stock at discount prices.
- **scaling:** Full position at trigger. No scaling — the signal is binary.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **AAPL** | BUY | 29% | Limit 0.5% below market | 7.4% below entry | 9.6% above entry | 16.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 7.8% below entry | 10.1% above entry | 15.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **META** | BUY | 36% | Market order (volatile) | 9.4% below entry | 12.2% above entry | 12.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |
| **V** | BUY | 22% | Limit 0.5% below market | 5.6% below entry | 7.3% above entry | 21.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=V) / [Yahoo](https://finance.yahoo.com/quote/V/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 39.2% |
| **Avg 5Y Sharpe** | 0.32 |
| **10Y Return** | 89.8% |
| **10Y Sharpe** | 0.29 |
| **HODL Composite** | 0.18 |
| **Consistency** | 89% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -21% drawdown to return 90% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
