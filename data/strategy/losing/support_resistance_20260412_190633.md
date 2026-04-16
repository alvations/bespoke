# LOSING Strategy: support_resistance

> **What it does:** Breakout trading on commodity ETFs with defined S/R levels and ATR stops
>
> **Hypothesis:** Support/Resistance Commodity

**Generated:** 2026-04-12T19:06:32.847060
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -8.34%
- **sharpe_ratio:** -0.39
- **max_drawdown:** -29.62%
- **win_rate:** 49.27%
- **alpha:** -26.00%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 29.6%
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
| **CPER** | BUY | 31% | Market order (volatile) | 33.0% below entry | 6.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CPER) / [Yahoo](https://finance.yahoo.com/quote/CPER/) |
| **XLE** | BUY | 23% | Limit 0.5% below market | 23.9% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLE) / [Yahoo](https://finance.yahoo.com/quote/XLE/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 24.1% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **NEM** | BUY | 41% | Market order (volatile) | 40.0% below entry | 8.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NEM) / [Yahoo](https://finance.yahoo.com/quote/NEM/) |
| **SLV** | BUY | 46% | Market order (volatile) | 40.0% below entry | 9.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SLV) / [Yahoo](https://finance.yahoo.com/quote/SLV/) |
| **COPX** | BUY | 39% | Market order (volatile) | 40.0% below entry | 8.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=COPX) / [Yahoo](https://finance.yahoo.com/quote/COPX/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.39 (target > 0.5)
- Max drawdown: -29.62% (target > -20%)
- Alpha: -26.00% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | -9.5% |
| **Avg 5Y Sharpe** | -0.44 |
| **10Y Return** | -26.4% |
| **10Y Sharpe** | -0.41 |
| **HODL Composite** | -0.01 |
| **Consistency** | 35% |
| **Suitable for passive** | No |

This strategy is **NOT recommended for passive investing**.

- **Take profit:** Take profit at +50%. This strategy is inconsistent — capture gains when available.
- **Stop loss:** Reduce position by 50% at -25% drawdown. Consistency is only 35%.
- **Exit rule:** Review semi-annually. Exit if strategy thesis no longer holds based on fundamental analysis.

</details>
