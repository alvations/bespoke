# LOSING Strategy: market_making_momentum

> **What it does:** Multi-factor momentum + short-term mean-reversion entry, Citadel-inspired
>
> **Hypothesis:** Market-Making Momentum (Citadel-style) 4Y (2022-2025)

**Generated:** 2026-04-08T23:07:08.918419
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -5.28%
- **sharpe_ratio:** -0.38
- **max_drawdown:** -16.77%
- **win_rate:** 50.40%
- **alpha:** -12.22%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 20.1%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 16.8%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When trend leaders above SMA50 > SMA200 (golden cross). STRONG BUY: On RSI pullback to 40-55 in confirmed uptrend — ride the trend, don't fight it.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **ABBV** | BUY | 26% | Limit 0.5% below market | 22.3% below entry | 5.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ABBV) / [Yahoo](https://finance.yahoo.com/quote/ABBV/) |
| **CVX** | BUY | 23% | Limit 0.5% below market | 19.6% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CVX) / [Yahoo](https://finance.yahoo.com/quote/CVX/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 14.4% below entry | 3.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **TSLA** | BUY | 62% | Market order (volatile) | 40.0% below entry | 13.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TSLA) / [Yahoo](https://finance.yahoo.com/quote/TSLA/) |
| **XOM** | BUY | 23% | Limit 0.5% below market | 19.7% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **JPM** | BUY | 25% | Limit 0.5% below market | 21.5% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **GS** | BUY | 31% | Market order (volatile) | 26.4% below entry | 6.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GS) / [Yahoo](https://finance.yahoo.com/quote/GS/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 25.3% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 40.0% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.38 (target > 0.5)
- Max drawdown: -16.77% (target > -20%)
- Alpha: -12.22% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 30.2% |
| **Avg 5Y Sharpe** | 0.15 |
| **Avg 5Y Max DD** | -21.9% |
| **10Y Return (2015-2024)** | 65.3% |
| **10Y Sharpe** | 0.15 |
| **10Y Max DD** | -23.4% |
| **HODL Composite** | 0.15 |
| **Windows Tested** | 28 |
| **Consistency** | 60% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -23% drawdown to return 65% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit if the momentum factor itself stops working — when 6+ of your holdings reverse trend in the same month, momentum regime has changed.

</details>
