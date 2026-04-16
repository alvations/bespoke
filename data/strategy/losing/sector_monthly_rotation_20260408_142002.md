# LOSING Strategy: sector_monthly_rotation

> **What it does:** Top 3 of 11 sector ETFs by 3-month momentum. 13.94% CAGR
>
> **Hypothesis:** Sector Monthly Rotation 3Y

**Generated:** 2026-04-08T14:20:02.806560
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 6.86%
- **sharpe_ratio:** -0.05
- **max_drawdown:** -24.10%
- **win_rate:** 49.47%
- **alpha:** -6.42%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 24.1%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When holdings above SMA200 on weekly rebalance. STRONG BUY: On RSI pullback to 35-50 in confirmed uptrend — buy the dip in quality.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **XLF** | BUY | 18% | Limit 0.5% below market | 18.9% below entry | 3.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLF) / [Yahoo](https://finance.yahoo.com/quote/XLF/) |
| **XLY** | BUY | 23% | Limit 0.5% below market | 23.7% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLY) / [Yahoo](https://finance.yahoo.com/quote/XLY/) |
| **XLC** | BUY | 17% | Limit 0.5% below market | 17.8% below entry | 3.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLC) / [Yahoo](https://finance.yahoo.com/quote/XLC/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.05 (target > 0.5)
- Max drawdown: -24.10% (target > -20%)
- Alpha: -6.42% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 13.0% |
| **Avg 5Y Sharpe** | -0.06 |
| **Avg 5Y Max DD** | -23.9% |
| **10Y Return (2015-2024)** | 17.1% |
| **10Y Sharpe** | -0.11 |
| **10Y Max DD** | -27.6% |
| **HODL Composite** | 0.04 |
| **Windows Tested** | 28 |
| **Consistency** | 50% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -28% drawdown to return 17% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit individual ETFs only if they close or change methodology. The rotation framework, not individual ETFs, is the strategy.

</details>
