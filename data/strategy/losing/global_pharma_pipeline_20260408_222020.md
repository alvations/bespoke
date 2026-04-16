# LOSING Strategy: global_pharma_pipeline

> **What it does:** Global pharma at value: Roche, AZN, MRK, GSK, TAK — deep pipelines, patent cliff fears
>
> **Hypothesis:** Global Pharma Pipeline 3Y

**Generated:** 2026-04-08T22:20:20.317261
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -4.51%
- **sharpe_ratio:** -0.40
- **max_drawdown:** -23.24%
- **win_rate:** 50.40%
- **alpha:** -10.20%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 23.2%
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
| **RHHBY** | BUY | 26% | Limit 0.5% below market | 27.5% below entry | 5.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=RHHBY) / [Yahoo](https://finance.yahoo.com/quote/RHHBY/) |
| **MRK** | BUY | 27% | Limit 0.5% below market | 28.6% below entry | 5.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MRK) / [Yahoo](https://finance.yahoo.com/quote/MRK/) |
| **NVS** | BUY | 20% | Limit 0.5% below market | 21.1% below entry | 4.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVS) / [Yahoo](https://finance.yahoo.com/quote/NVS/) |
| **AZN** | BUY | 25% | Limit 0.5% below market | 25.8% below entry | 5.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AZN) / [Yahoo](https://finance.yahoo.com/quote/AZN/) |
| **GSK** | BUY | 26% | Limit 0.5% below market | 27.8% below entry | 5.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GSK) / [Yahoo](https://finance.yahoo.com/quote/GSK/) |
| **SNY** | BUY | 25% | Limit 0.5% below market | 26.7% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SNY) / [Yahoo](https://finance.yahoo.com/quote/SNY/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.40 (target > 0.5)
- Max drawdown: -23.24% (target > -20%)
- Alpha: -10.20% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 39.7% |
| **Avg 5Y Sharpe** | 0.27 |
| **Avg 5Y Max DD** | -20.1% |
| **10Y Return (2015-2024)** | 68.3% |
| **10Y Sharpe** | 0.16 |
| **10Y Max DD** | -21.4% |
| **HODL Composite** | 0.24 |
| **Windows Tested** | 28 |
| **Consistency** | 82% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -21% drawdown to return 68% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Review annually. Exit if the strategy underperforms its benchmark for 3 consecutive years with no clear reason to hold.

</details>
