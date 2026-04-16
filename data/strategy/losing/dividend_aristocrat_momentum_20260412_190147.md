# LOSING Strategy: dividend_aristocrat_momentum

> **What it does:** Quality dividends + momentum: only buy Aristocrats in uptrends
>
> **Hypothesis:** Dividend Aristocrat Momentum

**Generated:** 2026-04-12T19:01:46.383521
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -5.13%
- **sharpe_ratio:** -0.53
- **max_drawdown:** -15.46%
- **win_rate:** 50.73%
- **alpha:** -24.88%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 20.1%
- **take_profit_target:** 8.0%
- **max_drawdown_tolerance:** 15.5%
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
| **JNJ** | BUY | 18% | Limit 0.5% below market | 15.0% below entry | 6.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |
| **NEE** | BUY | 26% | Limit 0.5% below market | 22.2% below entry | 8.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NEE) / [Yahoo](https://finance.yahoo.com/quote/NEE/) |
| **XOM** | BUY | 24% | Limit 0.5% below market | 19.9% below entry | 7.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **EMR** | BUY | 31% | Market order (volatile) | 26.0% below entry | 10.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EMR) / [Yahoo](https://finance.yahoo.com/quote/EMR/) |
| **LOW** | BUY | 25% | Limit 0.5% below market | 21.0% below entry | 8.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LOW) / [Yahoo](https://finance.yahoo.com/quote/LOW/) |
| **PEP** | BUY | 21% | Limit 0.5% below market | 17.5% below entry | 7.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PEP) / [Yahoo](https://finance.yahoo.com/quote/PEP/) |
| **ECL** | BUY | 20% | Limit 0.5% below market | 17.2% below entry | 6.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ECL) / [Yahoo](https://finance.yahoo.com/quote/ECL/) |
| **MRK** | BUY | 27% | Limit 0.5% below market | 23.1% below entry | 9.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MRK) / [Yahoo](https://finance.yahoo.com/quote/MRK/) |
| **MCD** | BUY | 18% | Limit 0.5% below market | 15.3% below entry | 6.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MCD) / [Yahoo](https://finance.yahoo.com/quote/MCD/) |
| **WMT** | BUY | 23% | Limit 0.5% below market | 19.8% below entry | 7.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WMT) / [Yahoo](https://finance.yahoo.com/quote/WMT/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.53 (target > 0.5)
- Max drawdown: -15.46% (target > -20%)
- Alpha: -24.88% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 49.1% |
| **Avg 5Y Sharpe** | 0.39 |
| **10Y Return** | 75.9% |
| **10Y Sharpe** | 0.21 |
| **HODL Composite** | 0.15 |
| **Consistency** | 67% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -15% drawdown to return 76% long-term.
- **Exit rule:** Exit if any holding cuts its dividend. Price drops with maintained payments are buying opportunities.

</details>
