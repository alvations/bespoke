# LOSING Strategy: bonds_down_banks_up

> **What it does:** Rising rates crush bonds but boost banks (wider NIM) + insurance (float income). TLT↓ = XLF↑.
>
> **Hypothesis:** Bonds Down → Banks Up (Rate Rotation)

**Generated:** 2026-04-08T22:39:52.389940
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 3.96%
- **sharpe_ratio:** -0.14
- **max_drawdown:** -29.00%
- **win_rate:** 52.39%
- **alpha:** -7.35%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 29.0%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When bank stocks (JPM, GS) are above SMA200. STRONG BUY: When TLT breaks below SMA200 — rising rates widen bank net interest margins.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **JPM** | BUY | 25% | Limit 0.5% below market | 26.7% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **WFC** | BUY | 31% | Market order (volatile) | 32.1% below entry | 6.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WFC) / [Yahoo](https://finance.yahoo.com/quote/WFC/) |
| **GS** | BUY | 31% | Market order (volatile) | 32.7% below entry | 6.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GS) / [Yahoo](https://finance.yahoo.com/quote/GS/) |
| **CB** | BUY | 19% | Limit 0.5% below market | 20.0% below entry | 4.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CB) / [Yahoo](https://finance.yahoo.com/quote/CB/) |
| **MS** | BUY | 30% | Market order (volatile) | 31.9% below entry | 6.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MS) / [Yahoo](https://finance.yahoo.com/quote/MS/) |
| **BAC** | BUY | 26% | Limit 0.5% below market | 27.0% below entry | 5.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BAC) / [Yahoo](https://finance.yahoo.com/quote/BAC/) |
| **PGR** | BUY | 24% | Limit 0.5% below market | 24.9% below entry | 5.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PGR) / [Yahoo](https://finance.yahoo.com/quote/PGR/) |
| **MET** | BUY | 27% | Limit 0.5% below market | 28.0% below entry | 5.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MET) / [Yahoo](https://finance.yahoo.com/quote/MET/) |
| **ALL** | BUY | 25% | Limit 0.5% below market | 26.1% below entry | 5.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ALL) / [Yahoo](https://finance.yahoo.com/quote/ALL/) |
| **C** | BUY | 32% | Market order (volatile) | 33.3% below entry | 6.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=C) / [Yahoo](https://finance.yahoo.com/quote/C/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.14 (target > 0.5)
- Max drawdown: -29.00% (target > -20%)
- Alpha: -7.35% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 33.3% |
| **Avg 5Y Sharpe** | 0.2 |
| **Avg 5Y Max DD** | -26.5% |
| **10Y Return (2015-2024)** | 77.4% |
| **10Y Sharpe** | 0.21 |
| **10Y Max DD** | -33.0% |
| **HODL Composite** | 0.18 |
| **Windows Tested** | 28 |
| **Consistency** | 64% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -33% drawdown to return 77% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit bank overweight when Fed signals rate cuts coming (dot plot shifts dovish). Falling rates compress bank margins.

</details>
