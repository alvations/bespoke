# LOSING Strategy: dividend_capture

> **What it does:** Dividend capture: hold high-yield low-vol stocks, harvest dividends
>
> **Hypothesis:** Dividend Capture (Ex-Date)

**Generated:** 2026-04-12T19:04:14.637317
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -0.75%
- **sharpe_ratio:** -0.40
- **max_drawdown:** -14.52%
- **win_rate:** 49.53%
- **alpha:** -23.38%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 20.0%
- **take_profit_target:** 8.0%
- **max_drawdown_tolerance:** 14.5%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy on ex-dividend date dips or when yield exceeds 5-year average.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Build position over 4-6 weeks. Reinvest all dividends.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **XOM** | BUY | 24% | Limit 0.5% below market | 19.8% below entry | 7.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **MCD** | BUY | 18% | Limit 0.5% below market | 15.2% below entry | 6.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MCD) / [Yahoo](https://finance.yahoo.com/quote/MCD/) |
| **IBM** | BUY | 30% | Market order (volatile) | 25.5% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IBM) / [Yahoo](https://finance.yahoo.com/quote/IBM/) |
| **VYM** | BUY | 14% | Limit 0.5% below market | 11.5% below entry | 4.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VYM) / [Yahoo](https://finance.yahoo.com/quote/VYM/) |
| **KO** | BUY | 16% | Limit 0.5% below market | 13.8% below entry | 5.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=KO) / [Yahoo](https://finance.yahoo.com/quote/KO/) |
| **JNJ** | BUY | 18% | Limit 0.5% below market | 14.9% below entry | 6.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |
| **HDV** | BUY | 12% | Limit 0.5% below market | 10.0% below entry | 4.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=HDV) / [Yahoo](https://finance.yahoo.com/quote/HDV/) |
| **SCHD** | BUY | 14% | Limit 0.5% below market | 11.9% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SCHD) / [Yahoo](https://finance.yahoo.com/quote/SCHD/) |
| **VZ** | BUY | 22% | Limit 0.5% below market | 18.9% below entry | 7.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VZ) / [Yahoo](https://finance.yahoo.com/quote/VZ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.40 (target > 0.5)
- Max drawdown: -14.52% (target > -20%)
- Alpha: -23.38% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 5.9% |
| **Avg 5Y Sharpe** | -0.23 |
| **10Y Return** | -0.9% |
| **10Y Sharpe** | -0.36 |
| **HODL Composite** | 0.01 |
| **Consistency** | 32% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Take profit at +50%. This strategy is inconsistent — capture gains when available.
- **Stop loss:** Reduce position by 50% at -25% drawdown. Consistency is only 32%.
- **Exit rule:** Exit if any holding cuts its dividend. Price drops with maintained payments are buying opportunities.

</details>
