# LOSING Strategy: crypto_crash_tradfi

> **What it does:** Crypto collapse drives capital to traditional banks, brokers, asset managers.
>
> **Hypothesis:** Crypto Crash → TradFi Flight 4Y (2022-2025)

**Generated:** 2026-04-08T23:03:35.176132
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 1.74%
- **sharpe_ratio:** -0.25
- **max_drawdown:** -17.51%
- **win_rate:** 54.79%
- **alpha:** -10.43%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 21.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 17.5%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When banks (JPM, GS) are above SMA50. STRONG BUY: When COIN/GBTC drop >20% below SMA200 — crypto refugees rotate to TradFi.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **JPM** | BUY | 25% | Limit 0.5% below market | 22.4% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **BLK** | BUY | 26% | Limit 0.5% below market | 22.6% below entry | 5.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BLK) / [Yahoo](https://finance.yahoo.com/quote/BLK/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.25 (target > 0.5)
- Max drawdown: -17.51% (target > -20%)
- Alpha: -10.43% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 12.1% |
| **Avg 5Y Sharpe** | -0.15 |
| **Avg 5Y Max DD** | -18.0% |
| **10Y Return (2015-2024)** | 25.6% |
| **10Y Sharpe** | -0.14 |
| **10Y Max DD** | -18.8% |
| **HODL Composite** | 0.04 |
| **Windows Tested** | 28 |
| **Consistency** | 39% |

### How to Use This Strategy Passively

This strategy is **NOT recommended for passive investing**. It has low consistency across time periods or negative long-term returns.

**If you still want exposure:** Limit to 5% of your portfolio maximum. Use the strategy orchestrator (conservative_regime) instead for passive allocation.

</details>
