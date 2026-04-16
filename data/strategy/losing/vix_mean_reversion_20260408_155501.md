# LOSING Strategy: vix_mean_reversion

> **What it does:** Buy aggressively when volatility spikes, reduce when complacent
>
> **Hypothesis:** VIX Mean Reversion (Buy Fear) 3Y

**Generated:** 2026-04-08T15:55:01.264011
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 4.00%
- **sharpe_ratio:** -0.14
- **max_drawdown:** -23.06%
- **win_rate:** 51.33%
- **alpha:** -7.34%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 23.1%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: Small hedge allocation (5-10%) at all times. STRONG BUY: When VIX spikes >25 — crisis alpha: deploy into oversold quality names.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SPY** | BUY | 17% | Limit 0.5% below market | 17.9% below entry | 3.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 22.7% below entry | 4.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 13.2% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 24.1% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **IWM** | BUY | 22% | Limit 0.5% below market | 23.3% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IWM) / [Yahoo](https://finance.yahoo.com/quote/IWM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.14 (target > 0.5)
- Max drawdown: -23.06% (target > -20%)
- Alpha: -7.34% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 45.5% |
| **Avg 5Y Sharpe** | 0.34 |
| **Avg 5Y Max DD** | -23.9% |
| **10Y Return (2015-2024)** | 88.0% |
| **10Y Sharpe** | 0.25 |
| **10Y Max DD** | -26.5% |
| **HODL Composite** | 0.26 |
| **Windows Tested** | 28 |
| **Consistency** | 75% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -27% drawdown to return 88% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Review annually. Exit if the strategy underperforms its benchmark for 3 consecutive years with no clear reason to hold.

</details>
