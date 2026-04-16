# LOSING Strategy: global_financial_infra

> **What it does:** Payment rails + mega-banks + Japanese trading houses + Singapore banks — backbone of world finance
>
> **Hypothesis:** Global Financial Infrastructure 3Y

**Generated:** 2026-04-08T22:04:58.209760
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 0.00%
- **sharpe_ratio:** 0.00
- **max_drawdown:** 0.00%
- **win_rate:** 0.00%
- **alpha:** -8.66%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 2.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 0.0%
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
| **V** | FLAT | 22% | Limit 0.5% below market | 1.8% below entry | 4.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=V) / [Yahoo](https://finance.yahoo.com/quote/V/) |
| **MA** | FLAT | 22% | Limit 0.5% below market | 1.8% below entry | 4.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MA) / [Yahoo](https://finance.yahoo.com/quote/MA/) |
| **AXP** | FLAT | 30% | Limit 0.5% below market | 2.5% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AXP) / [Yahoo](https://finance.yahoo.com/quote/AXP/) |
| **JPM** | FLAT | 25% | Limit 0.5% below market | 2.1% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **GS** | FLAT | 31% | Market order (volatile) | 2.6% below entry | 6.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GS) / [Yahoo](https://finance.yahoo.com/quote/GS/) |
| **BK** | FLAT | 23% | Limit 0.5% below market | 1.9% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BK) / [Yahoo](https://finance.yahoo.com/quote/BK/) |
| **COF** | FLAT | 37% | Market order (volatile) | 3.1% below entry | 7.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=COF) / [Yahoo](https://finance.yahoo.com/quote/COF/) |
| **MRBEY** | FLAT | 32% | Market order (volatile) | 2.7% below entry | 6.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MRBEY) / [Yahoo](https://finance.yahoo.com/quote/MRBEY/) |
| **MITSY** | FLAT | 31% | Market order (volatile) | 2.6% below entry | 6.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MITSY) / [Yahoo](https://finance.yahoo.com/quote/MITSY/) |
| **ITOCY** | FLAT | 29% | Limit 0.5% below market | 2.5% below entry | 6.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ITOCY) / [Yahoo](https://finance.yahoo.com/quote/ITOCY/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: 0.00 (target > 0.5)
- Max drawdown: 0.00% (target > -20%)
- Alpha: -8.66% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 35.4% |
| **Avg 5Y Sharpe** | 0.22 |
| **Avg 5Y Max DD** | -18.6% |
| **10Y Return (2015-2024)** | 93.7% |
| **10Y Sharpe** | 0.29 |
| **10Y Max DD** | -20.2% |
| **HODL Composite** | 0.25 |
| **Windows Tested** | 28 |
| **Consistency** | 75% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -20% drawdown to return 94% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit if global payment volumes decline for 2 consecutive quarters — would signal structural economic contraction, not just a cycle.

</details>
