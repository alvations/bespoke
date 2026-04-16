# LOSING Strategy: activist_distressed

> **What it does:** Deep-value activist targets: buy >20% below SMA200, catalyst-driven recovery
>
> **Hypothesis:** Activist Distressed (Elliott-style)

**Generated:** 2026-04-12T19:03:51.408581
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 7.88%
- **sharpe_ratio:** -0.07
- **max_drawdown:** -20.94%
- **win_rate:** 37.95%
- **alpha:** -20.56%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 20.9%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 20.9%
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
| **BA** | FLAT | 35% | Market order (volatile) | 31.2% below entry | 7.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BA) / [Yahoo](https://finance.yahoo.com/quote/BA/) |
| **INTC** | FLAT | 65% | Market order (volatile) | 40.0% below entry | 13.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=INTC) / [Yahoo](https://finance.yahoo.com/quote/INTC/) |
| **PFE** | FLAT | 25% | Limit 0.5% below market | 21.6% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PFE) / [Yahoo](https://finance.yahoo.com/quote/PFE/) |
| **NKE** | FLAT | 40% | Market order (volatile) | 35.6% below entry | 8.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NKE) / [Yahoo](https://finance.yahoo.com/quote/NKE/) |
| **PYPL** | FLAT | 39% | Market order (volatile) | 34.0% below entry | 8.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PYPL) / [Yahoo](https://finance.yahoo.com/quote/PYPL/) |
| **DIS** | FLAT | 27% | Limit 0.5% below market | 24.1% below entry | 5.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DIS) / [Yahoo](https://finance.yahoo.com/quote/DIS/) |
| **WBD** | FLAT | 54% | Market order (volatile) | 40.0% below entry | 11.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WBD) / [Yahoo](https://finance.yahoo.com/quote/WBD/) |
| **PARA** | FLAT | 32% | Market order (volatile) | 27.9% below entry | 6.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PARA) / [Yahoo](https://finance.yahoo.com/quote/PARA/) |
| **HAS** | FLAT | 32% | Market order (volatile) | 28.3% below entry | 6.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=HAS) / [Yahoo](https://finance.yahoo.com/quote/HAS/) |
| **GE** | FLAT | 32% | Market order (volatile) | 28.2% below entry | 6.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GE) / [Yahoo](https://finance.yahoo.com/quote/GE/) |
| **MMM** | FLAT | 49% | Market order (volatile) | 40.0% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MMM) / [Yahoo](https://finance.yahoo.com/quote/MMM/) |
| **DOW** | FLAT | 43% | Market order (volatile) | 37.6% below entry | 9.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DOW) / [Yahoo](https://finance.yahoo.com/quote/DOW/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.07 (target > 0.5)
- Max drawdown: -20.94% (target > -20%)
- Alpha: -20.56% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 10.0% |
| **Avg 5Y Sharpe** | -0.14 |
| **10Y Return** | 19.4% |
| **10Y Sharpe** | -0.14 |
| **HODL Composite** | 0.01 |
| **Consistency** | 28% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -35% drawdown to return 19% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
