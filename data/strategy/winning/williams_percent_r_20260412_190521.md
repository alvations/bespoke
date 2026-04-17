# WINNING Strategy: williams_percent_r

> **What it does:** Buy %R<-90 above SMA200, exit close>prev high. 77% win SPY, 22% invested
>
> **Hypothesis:** Williams %R(2) Mean Reversion

**Generated:** 2026-04-12T19:05:21.278231
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 18.89%
- **sharpe_ratio:** 0.37
- **max_drawdown:** -5.89%
- **win_rate:** 23.83%
- **alpha:** -17.17%

## Risk Parameters
- **max_portfolio_allocation:** 6.5%
- **stop_loss:** 5.9%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 5.9%
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
| **NVDA** | BUY | 49% | Market order (volatile) | 12.0% below entry | 10.2% above entry | 3.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 4.2% below entry | 3.6% above entry | 9.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 5.4% below entry | 4.6% above entry | 7.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **AAPL** | BUY | 29% | Limit 0.5% below market | 7.1% below entry | 6.0% above entry | 5.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **DIA** | BUY | 15% | Limit 0.5% below market | 3.8% below entry | 3.2% above entry | 10.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DIA) / [Yahoo](https://finance.yahoo.com/quote/DIA/) |
| **MSFT** | BUY | 24% | Limit 0.5% below market | 6.0% below entry | 5.1% above entry | 6.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 19.2% |
| **Avg 5Y Sharpe** | -0.04 |
| **10Y Return** | 35.7% |
| **10Y Sharpe** | -0.11 |
| **HODL Composite** | 0.27 |
| **Consistency** | 46% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Take profit at +50%. This strategy is inconsistent — capture gains when available.
- **Stop loss:** Reduce position by 50% at -25% drawdown. Consistency is only 46%.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
