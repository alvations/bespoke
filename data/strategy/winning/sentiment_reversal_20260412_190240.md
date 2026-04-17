# WINNING Strategy: sentiment_reversal

> **What it does:** Contrarian sentiment: buy extreme fear (VIX spike), sell extreme greed (VIX collapse)
>
> **Hypothesis:** Sentiment Reversal

**Generated:** 2026-04-12T19:02:39.901312
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 108.25%
- **sharpe_ratio:** 1.10
- **max_drawdown:** -26.10%
- **win_rate:** 56.46%
- **alpha:** 4.68%

## Risk Parameters
- **max_portfolio_allocation:** 12.1%
- **stop_loss:** 25.0%
- **take_profit_target:** 13.9%
- **max_drawdown_tolerance:** 26.1%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** market
- **limit_offset:** market: Use market orders for volatile names.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter in 3 tranches over 1-2 weeks.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **AMZN** | BUY | 33% | Market order (volatile) | 34.6% below entry | 19.2% above entry | 8.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **MSFT** | BUY | 24% | Limit 0.5% below market | 25.5% below entry | 14.2% above entry | 11.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 40.0% below entry | 28.4% above entry | 5.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 22.8% below entry | 12.7% above entry | 13.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 17.9% below entry | 10.0% above entry | 16.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **AAPL** | BUY | 29% | Limit 0.5% below market | 30.1% below entry | 16.7% above entry | 10.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **AMD** | BUY | 57% | Market order (volatile) | 40.0% below entry | 33.1% above entry | 5.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMD) / [Yahoo](https://finance.yahoo.com/quote/AMD/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 31.4% below entry | 17.5% above entry | 9.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **COIN** | BUY | 79% | Market order (volatile) | 40.0% below entry | 41.7% above entry | 4.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=COIN) / [Yahoo](https://finance.yahoo.com/quote/COIN/) |
| **MSTR** | BUY | 86% | Market order (volatile) | 40.0% below entry | 41.7% above entry | 4.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSTR) / [Yahoo](https://finance.yahoo.com/quote/MSTR/) |
| **NFLX** | BUY | 33% | Market order (volatile) | 34.4% below entry | 19.1% above entry | 8.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NFLX) / [Yahoo](https://finance.yahoo.com/quote/NFLX/) |
| **ARKK** | BUY | 41% | Market order (volatile) | 40.0% below entry | 24.1% above entry | 7.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ARKK) / [Yahoo](https://finance.yahoo.com/quote/ARKK/) |
| **META** | BUY | 36% | Market order (volatile) | 38.0% below entry | 21.1% above entry | 8.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |
| **TSLA** | BUY | 62% | Market order (volatile) | 40.0% below entry | 36.3% above entry | 4.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TSLA) / [Yahoo](https://finance.yahoo.com/quote/TSLA/) |
| **CRM** | BUY | 33% | Market order (volatile) | 35.1% below entry | 19.5% above entry | 8.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CRM) / [Yahoo](https://finance.yahoo.com/quote/CRM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 200.8% |
| **Avg 5Y Sharpe** | 0.89 |
| **10Y Return** | 807.7% |
| **10Y Sharpe** | 0.91 |
| **HODL Composite** | 2.48 |
| **Consistency** | 96% |
| **Suitable for passive** | Yes |

This strategy is **suitable for passive investing**.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -40% drawdown to return 808% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
