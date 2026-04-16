# LOSING Strategy: boring_compounder

> **What it does:** Quiet compounders in boring industries: pool supply, uniforms, fasteners, packaging
>
> **Hypothesis:** Boring Compounder 20% Club 4Y (2022-2025)

**Generated:** 2026-04-08T23:02:07.316748
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 1.61%
- **sharpe_ratio:** -0.17
- **max_drawdown:** -30.24%
- **win_rate:** 50.40%
- **alpha:** -10.47%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 30.2%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When above SMA200 (compounding intact). STRONG BUY: On RSI dip to 30-45 — POOL/ODFL/CTAS never stay down long, best entry is on fear.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **WST** | BUY | 49% | Market order (volatile) | 40.0% below entry | 10.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WST) / [Yahoo](https://finance.yahoo.com/quote/WST/) |
| **IDXX** | BUY | 37% | Market order (volatile) | 39.4% below entry | 7.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IDXX) / [Yahoo](https://finance.yahoo.com/quote/IDXX/) |
| **CLH** | BUY | 28% | Limit 0.5% below market | 29.2% below entry | 5.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CLH) / [Yahoo](https://finance.yahoo.com/quote/CLH/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.17 (target > 0.5)
- Max drawdown: -30.24% (target > -20%)
- Alpha: -10.47% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 116.3% |
| **Avg 5Y Sharpe** | 0.79 |
| **Avg 5Y Max DD** | -28.7% |
| **10Y Return (2015-2024)** | 278.1% |
| **10Y Sharpe** | 0.7 |
| **10Y Max DD** | -32.3% |
| **HODL Composite** | 0.75 |
| **Windows Tested** | 28 |
| **Consistency** | 82% |

### How to Use This Strategy Passively

This strategy is **suitable for passive investing**. It has shown consistent returns across multiple time horizons.

**Entry:** Buy the recommended positions at any time. Use the position sizes above as your target allocation.

**Rebalance:** Check quarterly. If any position has drifted more than 5% from target, rebalance back.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -32% drawdown to return 278% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit if a company acquisition destroys returns — watch for ROIC dropping below 12% post-acquisition for 3+ quarters.

</details>
