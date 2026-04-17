# WINNING Strategy: triple_witching_momentum

> **What it does:** Options expiration week bias: reduce exposure during triple witching
>
> **Hypothesis:** Triple Witching Momentum

**Generated:** 2026-04-12T19:05:50.274419
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 49.82%
- **sharpe_ratio:** 1.03
- **max_drawdown:** -8.33%
- **win_rate:** 53.53%
- **alpha:** -8.65%

## Risk Parameters
- **max_portfolio_allocation:** 11.5%
- **stop_loss:** 8.0%
- **take_profit_target:** 12.0%
- **max_drawdown_tolerance:** 8.3%
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
| **TLT** | BUY | 13% | Limit 0.5% below market | 4.2% below entry | 6.3% above entry | 21.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 7.7% below entry | 11.5% above entry | 12.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 5.7% below entry | 8.6% above entry | 16.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 7.3% below entry | 10.9% above entry | 12.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **IWM** | BUY | 22% | Limit 0.5% below market | 7.5% below entry | 11.2% above entry | 12.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IWM) / [Yahoo](https://finance.yahoo.com/quote/IWM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 48.1% |
| **Avg 5Y Sharpe** | 0.4 |
| **10Y Return** | 62.3% |
| **10Y Sharpe** | 0.14 |
| **HODL Composite** | 0.46 |
| **Consistency** | 67% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -27% drawdown to return 62% long-term.
- **Exit rule:** Exit if 3+ holdings break below their long-term trend simultaneously.

</details>
