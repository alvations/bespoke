# LOSING Strategy: l_shape_stagnation

> **What it does:** Persistent crash with no recovery (Japan 1990s). Gold + utilities + short bonds + dividends only.
>
> **Hypothesis:** L-Shape Stagnation Hedge (Worst Case) 4Y (2022-2025)

**Generated:** 2026-04-08T23:09:23.083266
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 14.66%
- **sharpe_ratio:** -0.06
- **max_drawdown:** -10.31%
- **win_rate:** 55.49%
- **alpha:** -7.38%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 12.4%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 10.3%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: Always hold 10-15% in GLD + short-duration bonds as insurance. STRONG BUY: When SPY death cross persists (SMA50 < SMA200 for 3+ months) — max defensive.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **GLD** | BUY | 23% | Limit 0.5% below market | 11.9% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SCHD** | BUY | 14% | Limit 0.5% below market | 7.3% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SCHD) / [Yahoo](https://finance.yahoo.com/quote/SCHD/) |
| **XLU** | BUY | 16% | Limit 0.5% below market | 8.2% below entry | 3.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLU) / [Yahoo](https://finance.yahoo.com/quote/XLU/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.06 (target > 0.5)
- Max drawdown: -10.31% (target > -20%)
- Alpha: -7.38% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 24.5% |
| **Avg 5Y Sharpe** | 0.13 |
| **Avg 5Y Max DD** | -8.0% |
| **10Y Return (2015-2024)** | 47.0% |
| **10Y Sharpe** | 0.01 |
| **10Y Max DD** | -10.3% |
| **HODL Composite** | 0.12 |
| **Windows Tested** | 28 |
| **Consistency** | 57% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance quarterly to target weights. Take 25% off any position up 100%+.
- **Stop loss:** Review if drawdown exceeds 15% — but dont auto-sell. Assess if fundamentals changed.
- **Exit rule:** Exit if the strategy thesis breaks: sector structural decline, regulation change, or management quality deterioration.

</details>
