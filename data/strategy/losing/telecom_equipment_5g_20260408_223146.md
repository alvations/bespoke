# LOSING Strategy: telecom_equipment_5g

> **What it does:** 5G infrastructure: equipment oligopoly + semiconductor + test & measurement
>
> **Hypothesis:** Telecom Equipment & 5G 3Y

**Generated:** 2026-04-08T22:31:45.861678
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -4.92%
- **sharpe_ratio:** -0.30
- **max_drawdown:** -21.20%
- **win_rate:** 41.62%
- **alpha:** -10.34%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 21.2%
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
| **ANET** | BUY | 53% | Market order (volatile) | 40.0% below entry | 11.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ANET) / [Yahoo](https://finance.yahoo.com/quote/ANET/) |
| **LITE** | BUY | 77% | Market order (volatile) | 40.0% below entry | 15.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LITE) / [Yahoo](https://finance.yahoo.com/quote/LITE/) |
| **MRVL** | BUY | 65% | Market order (volatile) | 40.0% below entry | 13.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MRVL) / [Yahoo](https://finance.yahoo.com/quote/MRVL/) |
| **VIAV** | BUY | 49% | Market order (volatile) | 40.0% below entry | 10.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VIAV) / [Yahoo](https://finance.yahoo.com/quote/VIAV/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.30 (target > 0.5)
- Max drawdown: -21.20% (target > -20%)
- Alpha: -10.34% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 24.6% |
| **Avg 5Y Sharpe** | 0.08 |
| **Avg 5Y Max DD** | -24.8% |
| **10Y Return (2015-2024)** | 23.2% |
| **10Y Sharpe** | -0.05 |
| **10Y Max DD** | -27.4% |
| **HODL Composite** | 0.08 |
| **Windows Tested** | 28 |
| **Consistency** | 57% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -27% drawdown to return 23% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Review annually. Exit if the strategy underperforms its benchmark for 3 consecutive years with no clear reason to hold.

</details>
