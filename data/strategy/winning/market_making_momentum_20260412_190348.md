# WINNING Strategy: market_making_momentum

> **What it does:** Multi-factor momentum + short-term mean-reversion entry, Citadel-inspired
>
> **Hypothesis:** Market-Making Momentum (Citadel-style)

**Generated:** 2026-04-12T19:03:48.098022
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 11.84%
- **sharpe_ratio:** 0.04
- **max_drawdown:** -13.98%
- **win_rate:** 51.93%
- **alpha:** -19.32%

## Risk Parameters
- **max_portfolio_allocation:** 3.3%
- **stop_loss:** 11.2%
- **take_profit_target:** 12.0%
- **max_drawdown_tolerance:** 14.0%
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
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 14.1% below entry | 15.1% above entry | 2.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **ABBV** | BUY | 26% | Limit 0.5% below market | 12.4% below entry | 13.3% above entry | 2.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ABBV) / [Yahoo](https://finance.yahoo.com/quote/ABBV/) |
| **XOM** | BUY | 24% | Limit 0.5% below market | 11.1% below entry | 11.9% above entry | 3.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 8.0% below entry | 8.6% above entry | 4.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 22.8% below entry | 24.5% above entry | 1.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **JPM** | BUY | 25% | Limit 0.5% below market | 12.0% below entry | 12.8% above entry | 3.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **CVX** | BUY | 23% | Limit 0.5% below market | 11.0% below entry | 11.8% above entry | 3.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CVX) / [Yahoo](https://finance.yahoo.com/quote/CVX/) |
| **TSLA** | BUY | 62% | Market order (volatile) | 29.2% below entry | 31.3% above entry | 1.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TSLA) / [Yahoo](https://finance.yahoo.com/quote/TSLA/) |
| **GS** | BUY | 31% | Market order (volatile) | 14.7% below entry | 15.8% above entry | 2.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GS) / [Yahoo](https://finance.yahoo.com/quote/GS/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 30.2% |
| **Avg 5Y Sharpe** | 0.15 |
| **10Y Return** | 65.3% |
| **10Y Sharpe** | 0.15 |
| **HODL Composite** | 0.83 |
| **Consistency** | 60% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -23% drawdown to return 65% long-term.
- **Exit rule:** Exit if 3+ holdings break below their long-term trend simultaneously.

</details>
