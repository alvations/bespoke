# LOSING Strategy: wealth_barometer

> **What it does:** DLTR/DG crash signals K-shaped economy → long Costco + luxury (rich don't care)
>
> **Hypothesis:** Wealth Barometer (Dollar Store vs Costco/Luxury) 4Y (2022-2025)

**Generated:** 2026-04-08T23:03:38.051614
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 10.97%
- **sharpe_ratio:** -0.04
- **max_drawdown:** -22.40%
- **win_rate:** 53.19%
- **alpha:** -8.22%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 22.4%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When COST/luxury are above SMA200. STRONG BUY: When DLTR/DG break below SMA200 while COST stays above — K-shape divergence confirmed.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **COST** | BUY | 20% | Limit 0.5% below market | 21.5% below entry | 4.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=COST) / [Yahoo](https://finance.yahoo.com/quote/COST/) |
| **WMT** | BUY | 23% | Limit 0.5% below market | 24.4% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WMT) / [Yahoo](https://finance.yahoo.com/quote/WMT/) |
| **TJX** | BUY | 18% | Limit 0.5% below market | 18.6% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TJX) / [Yahoo](https://finance.yahoo.com/quote/TJX/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.04 (target > 0.5)
- Max drawdown: -22.40% (target > -20%)
- Alpha: -8.22% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 20.6% |
| **Avg 5Y Sharpe** | 0.03 |
| **Avg 5Y Max DD** | -22.5% |
| **10Y Return (2015-2024)** | 48.1% |
| **10Y Sharpe** | 0.06 |
| **10Y Max DD** | -24.1% |
| **HODL Composite** | 0.09 |
| **Windows Tested** | 28 |
| **Consistency** | 53% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -24% drawdown to return 48% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit Costco/luxury overweight when Dollar Tree comp sales turn positive for 2 quarters — K-shape closing, lower-income recovering.

</details>
