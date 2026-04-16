# LOSING Strategy: retail_crash_ecommerce

> **What it does:** Brick-and-mortar crash accelerates e-commerce: XRT↓ = AMZN/SHOP/MELI↑
>
> **Hypothesis:** Retail Crash → E-commerce Boom 4Y (2022-2025)

**Generated:** 2026-04-08T23:03:30.757688
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -14.86%
- **sharpe_ratio:** -0.19
- **max_drawdown:** -47.53%
- **win_rate:** 50.30%
- **alpha:** -14.82%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 47.5%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** market
- **limit_offset:** use market orders in volatile names
- **timing:** BUY: When AMZN/SHOP are above SMA200. STRONG BUY: When XRT (retail ETF) breaks below SMA200 — accelerated shift to e-commerce.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **AMZN** | BUY | 33% | Market order (volatile) | 34.3% below entry | 6.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **SHOP** | BUY | 58% | Market order (volatile) | 40.0% below entry | 12.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHOP) / [Yahoo](https://finance.yahoo.com/quote/SHOP/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.19 (target > 0.5)
- Max drawdown: -47.53% (target > -20%)
- Alpha: -14.82% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 70.0% |
| **Avg 5Y Sharpe** | 0.43 |
| **Avg 5Y Max DD** | -39.0% |
| **10Y Return (2015-2024)** | 135.5% |
| **10Y Sharpe** | 0.34 |
| **10Y Max DD** | -50.5% |
| **HODL Composite** | 0.31 |
| **Windows Tested** | 28 |
| **Consistency** | 67% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -51% drawdown to return 136% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit e-commerce overweight when XRT recovers above SMA200 — retail stabilized, no more accelerated shift.

</details>
