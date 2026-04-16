# LOSING Strategy: multi_factor_combined

> **What it does:** Long stocks in top quintile of ALL of quality, momentum, and value

**Generated:** 2026-04-13T13:47:51.367696
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 1.35%
- **sharpe_ratio:** -6.45
- **max_drawdown:** -0.42%
- **win_rate:** 4.93%
- **alpha:** -22.68%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 5.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 0.4%
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
| **AAPL** | FLAT | 29% | Limit 0.5% below market | 6.0% below entry | 6.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **MSFT** | FLAT | 24% | Limit 0.5% below market | 5.1% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **GOOGL** | FLAT | 30% | Limit 0.5% below market | 6.3% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **AMZN** | FLAT | 33% | Market order (volatile) | 6.9% below entry | 6.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **NVDA** | FLAT | 49% | Market order (volatile) | 10.2% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **META** | FLAT | 36% | Market order (volatile) | 7.6% below entry | 7.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |
| **TSLA** | FLAT | 62% | Market order (volatile) | 13.1% below entry | 13.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TSLA) / [Yahoo](https://finance.yahoo.com/quote/TSLA/) |
| **JPM** | FLAT | 25% | Limit 0.5% below market | 5.3% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **V** | FLAT | 22% | Limit 0.5% below market | 4.6% below entry | 4.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=V) / [Yahoo](https://finance.yahoo.com/quote/V/) |
| **MA** | FLAT | 22% | Limit 0.5% below market | 4.5% below entry | 4.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MA) / [Yahoo](https://finance.yahoo.com/quote/MA/) |
| **UNH** | FLAT | 43% | Market order (volatile) | 9.0% below entry | 9.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UNH) / [Yahoo](https://finance.yahoo.com/quote/UNH/) |
| **JNJ** | FLAT | 18% | Limit 0.5% below market | 3.7% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -6.45 (target > 0.5)
- Max drawdown: -0.42% (target > -20%)
- Alpha: -22.68% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | -0.5% |
| **Avg 5Y Sharpe** | -8.39 |
| **Avg 5Y Max DD** | -1.7% |
| **10Y Return (2015-2024)** | 0.1% |
| **10Y Sharpe** | -8.45 |
| **10Y Max DD** | -2.3% |
| **HODL Composite** | -0.00 |
| **Windows Tested** | 28 |
| **Consistency** | 0% |

### How to Use This Strategy Passively

This strategy is **NOT recommended for passive investing**. It has low consistency across time periods or negative long-term returns.

**If you still want exposure:** Limit to 5% of your portfolio maximum. Use the strategy orchestrator (conservative_regime) instead for passive allocation.

</details>
