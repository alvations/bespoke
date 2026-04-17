# WINNING Strategy: fifty_two_week_breakout

> **What it does:** Buy new 52-week highs on 1.5x volume. 72% continuation, +11.4%/31d
>
> **Hypothesis:** 52-Week High Breakout

**Generated:** 2026-04-12T19:05:31.126091
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 14.93%
- **sharpe_ratio:** 0.22
- **max_drawdown:** -3.64%
- **win_rate:** 44.74%
- **alpha:** -18.37%

## Risk Parameters
- **max_portfolio_allocation:** 10.8%
- **stop_loss:** 5.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 3.6%
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
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 6.3% below entry | 6.3% above entry | 8.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 26.8% |
| **Avg 5Y Sharpe** | 0.2 |
| **10Y Return** | 59.0% |
| **10Y Sharpe** | 0.19 |
| **HODL Composite** | 0.22 |
| **Consistency** | 75% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Trim 25% of winners at +80%. Rebalance semi-annually.
- **Stop loss:** Review at -5% drawdown. Exit only if fundamentals deteriorated.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
