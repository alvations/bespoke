# LOSING Strategy: geopolitical_crisis

> **What it does:** War/crisis beneficiaries: energy + defense spike when vol rises
>
> **Hypothesis:** Geopolitical Crisis Alpha

**Generated:** 2026-04-12T19:03:07.067781
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 0.08%
- **sharpe_ratio:** -0.34
- **max_drawdown:** -21.37%
- **win_rate:** 51.80%
- **alpha:** -23.10%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 21.4%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 21.4%
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
| **HAL** | BUY | 38% | Market order (volatile) | 34.5% below entry | 8.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=HAL) / [Yahoo](https://finance.yahoo.com/quote/HAL/) |
| **XLE** | BUY | 23% | Limit 0.5% below market | 20.4% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLE) / [Yahoo](https://finance.yahoo.com/quote/XLE/) |
| **DVN** | BUY | 37% | Market order (volatile) | 33.0% below entry | 7.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DVN) / [Yahoo](https://finance.yahoo.com/quote/DVN/) |
| **RTX** | BUY | 25% | Limit 0.5% below market | 22.3% below entry | 5.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=RTX) / [Yahoo](https://finance.yahoo.com/quote/RTX/) |
| **ITA** | BUY | 21% | Limit 0.5% below market | 19.2% below entry | 4.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ITA) / [Yahoo](https://finance.yahoo.com/quote/ITA/) |
| **LMT** | BUY | 25% | Limit 0.5% below market | 22.5% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LMT) / [Yahoo](https://finance.yahoo.com/quote/LMT/) |
| **NOC** | BUY | 26% | Limit 0.5% below market | 23.0% below entry | 5.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NOC) / [Yahoo](https://finance.yahoo.com/quote/NOC/) |
| **SLV** | BUY | 46% | Market order (volatile) | 40.0% below entry | 9.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SLV) / [Yahoo](https://finance.yahoo.com/quote/SLV/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 20.6% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.34 (target > 0.5)
- Max drawdown: -21.37% (target > -20%)
- Alpha: -23.10% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 21.6% |
| **Avg 5Y Sharpe** | 0.08 |
| **10Y Return** | 26.2% |
| **10Y Sharpe** | -0.03 |
| **HODL Composite** | 0.06 |
| **Consistency** | 60% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -32% drawdown to return 26% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
