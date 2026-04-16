# LOSING Strategy: nvidia_domino_hedge

> **What it does:** Profit when NVIDIA financing chain breaks: inverse ETFs + safe havens + vol, scaled by supply chain stress
>
> **Hypothesis:** NVIDIA Domino Hedge (Supply Chain Collapse)

**Generated:** 2026-04-12T19:02:29.152189
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -13.67%
- **sharpe_ratio:** -0.83
- **max_drawdown:** -16.27%
- **win_rate:** 47.94%
- **alpha:** -27.93%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 15.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 16.3%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Always hold some. Add more when SPY breaks below SMA200.
- **timing:** WAIT FOR SIGNAL: Hold AI stocks normally. Switch to defensive ONLY when supply chain companies start breaking down.
- **scaling:** Maintain 5-15% allocation. Add during fear, trim during euphoria.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **GLD** | BUY | 23% | Limit 0.5% below market | 14.4% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SHY** | BUY | 2% | Limit 0.5% below market | 7.5% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **SQQQ** | BUY | 65% | Market order (volatile) | 40.0% below entry | 13.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SQQQ) / [Yahoo](https://finance.yahoo.com/quote/SQQQ/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 7.9% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **UVXY** | BUY | 122% | Market order (volatile) | 40.0% below entry | 15.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UVXY) / [Yahoo](https://finance.yahoo.com/quote/UVXY/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.83 (target > 0.5)
- Max drawdown: -16.27% (target > -20%)
- Alpha: -27.93% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | -14.7% |
| **Avg 5Y Sharpe** | -1.06 |
| **10Y Return** | -27.8% |
| **10Y Sharpe** | -1.17 |
| **HODL Composite** | -0.0 |
| **Consistency** | 0% |
| **Suitable for passive** | No |

This strategy is **NOT recommended for passive investing**.

- **Take profit:** Take profit at +50%. This strategy is inconsistent — capture gains when available.
- **Stop loss:** Reduce position by 50% at -25% drawdown. Consistency is only 0%.
- **Exit rule:** Review semi-annually. Exit if strategy thesis no longer holds based on fundamental analysis.

</details>
