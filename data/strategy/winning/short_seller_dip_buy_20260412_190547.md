# WINNING Strategy: short_seller_dip_buy

> **What it does:** Buy >5% drops on 3x volume (short report proxy). MSTR +226%, HOOD +168%
>
> **Hypothesis:** Short Seller Dip Buy

**Generated:** 2026-04-12T19:05:47.364497
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 75.40%
- **sharpe_ratio:** 1.05
- **max_drawdown:** -11.38%
- **win_rate:** 52.60%
- **alpha:** -2.45%

## Risk Parameters
- **max_portfolio_allocation:** 12.3%
- **stop_loss:** 11.4%
- **take_profit_target:** 10.3%
- **max_drawdown_tolerance:** 11.4%
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
| **META** | BUY | 36% | Market order (volatile) | 17.3% below entry | 15.7% above entry | 8.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 58.7% |
| **Avg 5Y Sharpe** | 0.46 |
| **10Y Return** | 174.2% |
| **10Y Sharpe** | 0.53 |
| **HODL Composite** | 0.26 |
| **Consistency** | 85% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -28% drawdown to return 174% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
