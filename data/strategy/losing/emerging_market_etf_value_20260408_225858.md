# LOSING Strategy: emerging_market_etf_value

> **What it does:** EM country ETFs at value prices: Vietnam, Korea, India, Taiwan, Singapore
>
> **Hypothesis:** Emerging Market ETF Value 4Y (2022-2025)

**Generated:** 2026-04-08T22:58:58.135186
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 9.42%
- **sharpe_ratio:** -0.06
- **max_drawdown:** -22.39%
- **win_rate:** 50.60%
- **alpha:** -8.58%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 22.4%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When target names show MACD reversal from below signal line. STRONG BUY: When RSI < 35 AND price > 10% below SMA200 — deep value entry at maximum pessimism.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **VNM** | BUY | 27% | Limit 0.5% below market | 28.0% below entry | 5.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VNM) / [Yahoo](https://finance.yahoo.com/quote/VNM/) |
| **EWT** | BUY | 25% | Limit 0.5% below market | 26.6% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EWT) / [Yahoo](https://finance.yahoo.com/quote/EWT/) |
| **EWY** | BUY | 32% | Market order (volatile) | 33.2% below entry | 6.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EWY) / [Yahoo](https://finance.yahoo.com/quote/EWY/) |
| **EWS** | BUY | 18% | Limit 0.5% below market | 18.6% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EWS) / [Yahoo](https://finance.yahoo.com/quote/EWS/) |
| **EEM** | BUY | 19% | Limit 0.5% below market | 19.6% below entry | 3.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EEM) / [Yahoo](https://finance.yahoo.com/quote/EEM/) |
| **NU** | BUY | 44% | Market order (volatile) | 40.0% below entry | 9.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NU) / [Yahoo](https://finance.yahoo.com/quote/NU/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.06 (target > 0.5)
- Max drawdown: -22.39% (target > -20%)
- Alpha: -8.58% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 4.7% |
| **Avg 5Y Sharpe** | -0.15 |
| **Avg 5Y Max DD** | -32.1% |
| **10Y Return (2015-2024)** | -6.6% |
| **10Y Sharpe** | -0.27 |
| **10Y Max DD** | -37.7% |
| **HODL Composite** | 0.0 |
| **Windows Tested** | 28 |
| **Consistency** | 35% |

### How to Use This Strategy Passively

This strategy is **NOT recommended for passive investing**. It has low consistency across time periods or negative long-term returns.

**If you still want exposure:** Limit to 5% of your portfolio maximum. Use the strategy orchestrator (conservative_regime) instead for passive allocation.

</details>
