# LOSING Strategy: contrastive_pairs

> **What it does:** Long the cheap stock in every hot sector: WDC not NVDA, HRB not SNOW, ADP not WDAY
>
> **Hypothesis:** Contrastive Pairs (Value Side of Hype Sectors) 3Y

**Generated:** 2026-04-08T22:04:55.045941
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 0.00%
- **sharpe_ratio:** 0.00
- **max_drawdown:** 0.00%
- **win_rate:** 0.00%
- **alpha:** -8.66%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 2.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 0.0%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When spread Z-score > 1.5 (divergence starting). STRONG BUY: When Z-score > 2.0 — statistical mean reversion at extreme levels.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **WDC** | FLAT | 57% | Market order (volatile) | 4.8% below entry | 12.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WDC) / [Yahoo](https://finance.yahoo.com/quote/WDC/) |
| **MU** | FLAT | 63% | Market order (volatile) | 5.3% below entry | 13.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MU) / [Yahoo](https://finance.yahoo.com/quote/MU/) |
| **ON** | FLAT | 55% | Market order (volatile) | 4.6% below entry | 11.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ON) / [Yahoo](https://finance.yahoo.com/quote/ON/) |
| **HRB** | FLAT | 30% | Market order (volatile) | 2.6% below entry | 6.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=HRB) / [Yahoo](https://finance.yahoo.com/quote/HRB/) |
| **ADP** | FLAT | 20% | Limit 0.5% below market | 1.7% below entry | 4.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ADP) / [Yahoo](https://finance.yahoo.com/quote/ADP/) |
| **PAYX** | FLAT | 24% | Limit 0.5% below market | 2.0% below entry | 5.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PAYX) / [Yahoo](https://finance.yahoo.com/quote/PAYX/) |
| **NFLX** | FLAT | 33% | Market order (volatile) | 2.8% below entry | 6.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NFLX) / [Yahoo](https://finance.yahoo.com/quote/NFLX/) |
| **WBD** | FLAT | 55% | Market order (volatile) | 4.6% below entry | 11.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WBD) / [Yahoo](https://finance.yahoo.com/quote/WBD/) |
| **ORCL** | FLAT | 53% | Market order (volatile) | 4.5% below entry | 11.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ORCL) / [Yahoo](https://finance.yahoo.com/quote/ORCL/) |
| **IBM** | FLAT | 30% | Market order (volatile) | 2.6% below entry | 6.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IBM) / [Yahoo](https://finance.yahoo.com/quote/IBM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: 0.00 (target > 0.5)
- Max drawdown: 0.00% (target > -20%)
- Alpha: -8.66% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 105.3% |
| **Avg 5Y Sharpe** | 0.55 |
| **Avg 5Y Max DD** | -34.1% |
| **10Y Return (2015-2024)** | 255.3% |
| **10Y Sharpe** | 0.51 |
| **10Y Max DD** | -36.1% |
| **HODL Composite** | 0.71 |
| **Windows Tested** | 28 |
| **Consistency** | 89% |

### How to Use This Strategy Passively

This strategy is **suitable for passive investing**. It has shown consistent returns across multiple time horizons.

**Entry:** Buy the recommended positions at any time. Use the position sizes above as your target allocation.

**Rebalance:** Check quarterly. If any position has drifted more than 5% from target, rebalance back.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -36% drawdown to return 255% over the long term. Stopping out would have locked in losses.
- **Exit rule:** This strategy returned 255% over 10 years despite -36% max drawdown. Exit the value side if it fails to close the gap with the hype side within 18 months — mean reversion thesis expired.

</details>
