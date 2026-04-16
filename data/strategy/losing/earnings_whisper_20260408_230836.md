# LOSING Strategy: earnings_whisper

> **What it does:** Pre-earnings drift: accumulation patterns predict positive surprises
>
> **Hypothesis:** Earnings Whisper (Pre-Drift) 4Y (2022-2025)

**Generated:** 2026-04-08T23:08:36.656730
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 2.44%
- **sharpe_ratio:** -0.20
- **max_drawdown:** -23.60%
- **win_rate:** 46.31%
- **alpha:** -10.26%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 23.6%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When holdings above SMA200 on weekly rebalance. STRONG BUY: On RSI pullback to 35-50 in confirmed uptrend — buy the dip in quality.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **META** | BUY | 36% | Market order (volatile) | 37.8% below entry | 7.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |
| **JPM** | BUY | 25% | Limit 0.5% below market | 26.7% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **CRM** | BUY | 33% | Market order (volatile) | 34.9% below entry | 7.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CRM) / [Yahoo](https://finance.yahoo.com/quote/CRM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.20 (target > 0.5)
- Max drawdown: -23.60% (target > -20%)
- Alpha: -10.26% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 24.3% |
| **Avg 5Y Sharpe** | 0.09 |
| **Avg 5Y Max DD** | -22.1% |
| **10Y Return (2015-2024)** | 59.2% |
| **10Y Sharpe** | 0.12 |
| **10Y Max DD** | -28.8% |
| **HODL Composite** | 0.14 |
| **Windows Tested** | 28 |
| **Consistency** | 64% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -29% drawdown to return 59% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Review annually. Exit if the strategy underperforms its benchmark for 3 consecutive years with no clear reason to hold.

</details>
