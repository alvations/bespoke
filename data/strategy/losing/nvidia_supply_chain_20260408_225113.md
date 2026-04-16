# LOSING Strategy: nvidia_supply_chain

> **What it does:** Non-megacap companies NVIDIA depends on: packaging, testing, materials, cooling, power
>
> **Hypothesis:** NVIDIA Supply Chain (Peripheral)

**Generated:** 2026-04-08T22:51:13.334470
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -7.68%
- **sharpe_ratio:** -0.23
- **max_drawdown:** -26.91%
- **win_rate:** 45.48%
- **alpha:** -11.30%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 26.9%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** market
- **limit_offset:** use market orders in volatile names
- **timing:** BUY: When NVDA is above SMA200, hold diversified AI chain. STRONG BUY hedge: When ANY chain member breaks SMA200 with RSI < 35 — first-one-out exit rule.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **AJINY** | BUY | 34% | Market order (volatile) | 35.6% below entry | 7.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AJINY) / [Yahoo](https://finance.yahoo.com/quote/AJINY/) |
| **FORM** | BUY | 64% | Market order (volatile) | 40.0% below entry | 13.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=FORM) / [Yahoo](https://finance.yahoo.com/quote/FORM/) |
| **TTMI** | BUY | 59% | Market order (volatile) | 40.0% below entry | 12.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TTMI) / [Yahoo](https://finance.yahoo.com/quote/TTMI/) |
| **ASX** | BUY | 41% | Market order (volatile) | 40.0% below entry | 8.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ASX) / [Yahoo](https://finance.yahoo.com/quote/ASX/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.23 (target > 0.5)
- Max drawdown: -26.91% (target > -20%)
- Alpha: -11.30% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 56.7% |
| **Avg 5Y Sharpe** | 0.33 |
| **Avg 5Y Max DD** | -31.9% |
| **10Y Return (2015-2024)** | 85.9% |
| **10Y Sharpe** | 0.22 |
| **10Y Max DD** | -37.1% |
| **HODL Composite** | 0.26 |
| **Windows Tested** | 28 |
| **Consistency** | 75% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -37% drawdown to return 86% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit if TSMC announces capacity cuts or if ASML order book declines — these are the irreplaceable links in the chain.

</details>
