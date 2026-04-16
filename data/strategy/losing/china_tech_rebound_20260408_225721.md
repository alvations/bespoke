# LOSING Strategy: china_tech_rebound

> **What it does:** China tech ADR recovery: deep value after regulatory crackdown
>
> **Hypothesis:** China Tech Rebound 4Y (2022-2025)

**Generated:** 2026-04-08T22:57:20.909871
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** -5.42%
- **sharpe_ratio:** 0.00
- **max_drawdown:** -39.21%
- **win_rate:** 42.42%
- **alpha:** -12.25%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 39.2%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** market
- **limit_offset:** use market orders in volatile names
- **timing:** BUY: When holdings above SMA200 on weekly rebalance. STRONG BUY: On RSI pullback to 35-50 in confirmed uptrend — buy the dip in quality.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **ZTO** | BUY | 33% | Market order (volatile) | 34.8% below entry | 7.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ZTO) / [Yahoo](https://finance.yahoo.com/quote/ZTO/) |
| **BIDU** | BUY | 46% | Market order (volatile) | 40.0% below entry | 9.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BIDU) / [Yahoo](https://finance.yahoo.com/quote/BIDU/) |
| **FXI** | BUY | 46% | Market order (volatile) | 40.0% below entry | 9.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=FXI) / [Yahoo](https://finance.yahoo.com/quote/FXI/) |
| **TME** | BUY | 53% | Market order (volatile) | 40.0% below entry | 11.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TME) / [Yahoo](https://finance.yahoo.com/quote/TME/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: 0.00 (target > 0.5)
- Max drawdown: -39.21% (target > -20%)
- Alpha: -12.25% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 31.6% |
| **Avg 5Y Sharpe** | 0.2 |
| **Avg 5Y Max DD** | -49.1% |
| **10Y Return (2015-2024)** | 67.7% |
| **10Y Sharpe** | 0.18 |
| **10Y Max DD** | -61.9% |
| **HODL Composite** | 0.15 |
| **Windows Tested** | 28 |
| **Consistency** | 75% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -62% drawdown to return 68% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Review annually. Exit if the strategy underperforms its benchmark for 3 consecutive years with no clear reason to hold.

</details>
