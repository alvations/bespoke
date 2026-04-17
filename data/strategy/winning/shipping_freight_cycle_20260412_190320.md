# WINNING Strategy: shipping_freight_cycle

> **What it does:** Global shipping cycle: container/bulk shippers + freight ETFs
>
> **Hypothesis:** Shipping / Freight Cycle

**Generated:** 2026-04-12T19:03:19.173997
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 29.05%
- **sharpe_ratio:** 0.39
- **max_drawdown:** -20.23%
- **win_rate:** 51.13%
- **alpha:** -14.23%

## Risk Parameters
- **max_portfolio_allocation:** 5.7%
- **stop_loss:** 30.3%
- **take_profit_target:** 15.0%
- **max_drawdown_tolerance:** 20.2%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy on golden cross (SMA50 > SMA200). These are CYCLE trades — timing matters.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter 30% at signal, add 30% on confirmation, hold 40% for cycle peak.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SEA** | BUY | 20% | Limit 0.5% below market | 25.6% below entry | 12.6% above entry | 6.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SEA) / [Yahoo](https://finance.yahoo.com/quote/SEA/) |
| **CHRW** | BUY | 36% | Market order (volatile) | 40.0% below entry | 22.6% above entry | 3.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CHRW) / [Yahoo](https://finance.yahoo.com/quote/CHRW/) |
| **EXPD** | BUY | 28% | Limit 0.5% below market | 35.5% below entry | 17.5% above entry | 4.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EXPD) / [Yahoo](https://finance.yahoo.com/quote/EXPD/) |
| **GNK** | BUY | 34% | Market order (volatile) | 40.0% below entry | 21.6% above entry | 4.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GNK) / [Yahoo](https://finance.yahoo.com/quote/GNK/) |
| **ZIM** | BUY | 68% | Market order (volatile) | 40.0% below entry | 43.0% above entry | 2.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ZIM) / [Yahoo](https://finance.yahoo.com/quote/ZIM/) |
| **EGLE** | BUY | 12% | Limit 0.5% below market | 15.2% below entry | 7.5% above entry | 11.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EGLE) / [Yahoo](https://finance.yahoo.com/quote/EGLE/) |
| **SBLK** | BUY | 34% | Market order (volatile) | 40.0% below entry | 21.3% above entry | 4.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SBLK) / [Yahoo](https://finance.yahoo.com/quote/SBLK/) |
| **MATX** | BUY | 41% | Market order (volatile) | 40.0% below entry | 25.5% above entry | 3.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MATX) / [Yahoo](https://finance.yahoo.com/quote/MATX/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 39.5% |
| **Avg 5Y Sharpe** | 0.17 |
| **10Y Return** | 56.1% |
| **10Y Sharpe** | 0.11 |
| **HODL Composite** | 0.17 |
| **Consistency** | 57% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -30% drawdown to return 56% long-term.
- **Exit rule:** Exit when newbuild orders surge past 15% of fleet.

</details>
