# LOSING Strategy: news_reaction_momentum

> **What it does:** Buy unusual volume + positive price moves (news proxy)
>
> **Hypothesis:** News Reaction Momentum

**Generated:** 2026-04-12T19:03:56.165391
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 10.39%
- **sharpe_ratio:** -0.09
- **max_drawdown:** -5.97%
- **win_rate:** 9.72%
- **alpha:** -19.77%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 8.0%
- **take_profit_target:** 12.0%
- **max_drawdown_tolerance:** 6.0%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy on RSI pullback to 40-50 in confirmed uptrend. Never chase.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter 50% initial, add 25% on first pullback, final 25% on trend confirmation.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **AAPL** | FLAT | 29% | Limit 0.5% below market | 9.6% below entry | 14.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **MSFT** | FLAT | 24% | Limit 0.5% below market | 8.2% below entry | 12.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **NVDA** | FLAT | 49% | Market order (volatile) | 16.3% below entry | 24.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **GOOGL** | FLAT | 30% | Limit 0.5% below market | 10.1% below entry | 15.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **AMZN** | FLAT | 33% | Market order (volatile) | 11.1% below entry | 16.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **META** | FLAT | 36% | Market order (volatile) | 12.2% below entry | 18.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |
| **TSLA** | FLAT | 62% | Market order (volatile) | 20.9% below entry | 31.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TSLA) / [Yahoo](https://finance.yahoo.com/quote/TSLA/) |
| **JPM** | FLAT | 25% | Limit 0.5% below market | 8.6% below entry | 12.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **V** | FLAT | 22% | Limit 0.5% below market | 7.3% below entry | 10.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=V) / [Yahoo](https://finance.yahoo.com/quote/V/) |
| **UNH** | FLAT | 43% | Market order (volatile) | 14.5% below entry | 21.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UNH) / [Yahoo](https://finance.yahoo.com/quote/UNH/) |
| **LLY** | FLAT | 38% | Market order (volatile) | 12.8% below entry | 19.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LLY) / [Yahoo](https://finance.yahoo.com/quote/LLY/) |
| **AVGO** | FLAT | 55% | Market order (volatile) | 18.5% below entry | 27.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AVGO) / [Yahoo](https://finance.yahoo.com/quote/AVGO/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.09 (target > 0.5)
- Max drawdown: -5.97% (target > -20%)
- Alpha: -19.77% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | -4.4% |
| **Avg 5Y Sharpe** | -1.11 |
| **10Y Return** | -2.8% |
| **10Y Sharpe** | -0.86 |
| **HODL Composite** | -0.0 |
| **Consistency** | 7% |
| **Suitable for passive** | No |

This strategy is **NOT recommended for passive investing**.

- **Take profit:** Take profit at +50%. This strategy is inconsistent — capture gains when available.
- **Stop loss:** Reduce position by 50% at -25% drawdown. Consistency is only 7%.
- **Exit rule:** Exit if 3+ holdings break below their long-term trend simultaneously.

</details>
