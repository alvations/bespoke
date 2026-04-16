# LOSING Strategy: small_cap_value_rotation

> **What it does:** Small caps at 50-year cheap: AVUV + momentum picks, 18% YTD 2026
>
> **Hypothesis:** Small Cap Value Rotation 4Y (2022-2025)

**Generated:** 2026-04-08T23:04:41.431366
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -3.85%
- **sharpe_ratio:** -0.16
- **max_drawdown:** -27.41%
- **win_rate:** 48.60%
- **alpha:** -11.85%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 27.4%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When target names show MACD reversal from below signal line. STRONG BUY: When RSI < 35 AND price > 10% below SMA200 — deep value entry at maximum pessimism.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **AVUV** | BUY | 23% | Limit 0.5% below market | 23.7% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AVUV) / [Yahoo](https://finance.yahoo.com/quote/AVUV/) |
| **VBR** | BUY | 19% | Limit 0.5% below market | 20.1% below entry | 4.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VBR) / [Yahoo](https://finance.yahoo.com/quote/VBR/) |
| **IWN** | BUY | 21% | Limit 0.5% below market | 22.3% below entry | 4.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IWN) / [Yahoo](https://finance.yahoo.com/quote/IWN/) |
| **SAIA** | BUY | 57% | Market order (volatile) | 40.0% below entry | 12.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SAIA) / [Yahoo](https://finance.yahoo.com/quote/SAIA/) |
| **IWM** | BUY | 22% | Limit 0.5% below market | 23.3% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IWM) / [Yahoo](https://finance.yahoo.com/quote/IWM/) |
| **DFSV** | BUY | 22% | Limit 0.5% below market | 23.5% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DFSV) / [Yahoo](https://finance.yahoo.com/quote/DFSV/) |
| **DECK** | BUY | 49% | Market order (volatile) | 40.0% below entry | 10.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DECK) / [Yahoo](https://finance.yahoo.com/quote/DECK/) |
| **GRC** | BUY | 30% | Market order (volatile) | 31.7% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GRC) / [Yahoo](https://finance.yahoo.com/quote/GRC/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.16 (target > 0.5)
- Max drawdown: -27.41% (target > -20%)
- Alpha: -11.85% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 98.6% |
| **Avg 5Y Sharpe** | 0.59 |
| **Avg 5Y Max DD** | -31.7% |
| **10Y Return (2015-2024)** | 188.0% |
| **10Y Sharpe** | 0.47 |
| **10Y Max DD** | -37.9% |
| **HODL Composite** | 0.52 |
| **Windows Tested** | 28 |
| **Consistency** | 78% |

### How to Use This Strategy Passively

This strategy is **suitable for passive investing**. It has shown consistent returns across multiple time horizons.

**Entry:** Buy the recommended positions at any time. Use the position sizes above as your target allocation.

**Rebalance:** Check quarterly. If any position has drifted more than 5% from target, rebalance back.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -38% drawdown to return 188% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit individual ETFs only if they close or change methodology. The rotation framework, not individual ETFs, is the strategy.

</details>
