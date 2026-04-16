# LOSING Strategy: global_airlines_travel

> **What it does:** Airlines and OTAs: DAL, UAL, BKNG, ABNB — post-pandemic travel demand
>
> **Hypothesis:** Global Airlines & Travel 4Y (2022-2025)

**Generated:** 2026-04-08T22:58:44.521124
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -17.37%
- **sharpe_ratio:** -0.28
- **max_drawdown:** -51.92%
- **win_rate:** 49.70%
- **alpha:** -15.54%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 51.9%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** market
- **limit_offset:** use market orders in volatile names
- **timing:** BUY: When holdings above SMA200 on weekly rebalance. STRONG BUY: On RSI pullback to 35-50 in confirmed uptrend — buy the dip in quality.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **EXPE** | BUY | 45% | Market order (volatile) | 40.0% below entry | 9.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EXPE) / [Yahoo](https://finance.yahoo.com/quote/EXPE/) |
| **MAR** | BUY | 27% | Limit 0.5% below market | 28.7% below entry | 5.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MAR) / [Yahoo](https://finance.yahoo.com/quote/MAR/) |
| **DAL** | BUY | 45% | Market order (volatile) | 40.0% below entry | 9.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DAL) / [Yahoo](https://finance.yahoo.com/quote/DAL/) |
| **JBLU** | BUY | 69% | Market order (volatile) | 40.0% below entry | 14.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JBLU) / [Yahoo](https://finance.yahoo.com/quote/JBLU/) |
| **UAL** | BUY | 53% | Market order (volatile) | 40.0% below entry | 11.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UAL) / [Yahoo](https://finance.yahoo.com/quote/UAL/) |
| **AAL** | BUY | 50% | Market order (volatile) | 40.0% below entry | 10.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAL) / [Yahoo](https://finance.yahoo.com/quote/AAL/) |
| **LUV** | BUY | 42% | Market order (volatile) | 40.0% below entry | 8.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LUV) / [Yahoo](https://finance.yahoo.com/quote/LUV/) |
| **TCOM** | BUY | 44% | Market order (volatile) | 40.0% below entry | 9.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TCOM) / [Yahoo](https://finance.yahoo.com/quote/TCOM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.28 (target > 0.5)
- Max drawdown: -51.92% (target > -20%)
- Alpha: -15.54% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | -25.5% |
| **Avg 5Y Sharpe** | -0.41 |
| **Avg 5Y Max DD** | -49.9% |
| **10Y Return (2015-2024)** | -36.4% |
| **10Y Sharpe** | -0.33 |
| **10Y Max DD** | -62.3% |
| **HODL Composite** | -0.04 |
| **Windows Tested** | 28 |
| **Consistency** | 35% |

### How to Use This Strategy Passively

This strategy is **NOT recommended for passive investing**. It has low consistency across time periods or negative long-term returns.

**If you still want exposure:** Limit to 5% of your portfolio maximum. Use the strategy orchestrator (conservative_regime) instead for passive allocation.

</details>
