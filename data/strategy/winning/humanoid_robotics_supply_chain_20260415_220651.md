# WINNING Strategy: humanoid_robotics_supply_chain

> **What it does:** Brain + body + integrator robotics stack (KraneShares KOID thesis)
>
> **Hypothesis:** Humanoid robotics value chain: brain + body + integrator stack.

**Generated:** 2026-04-15T22:06:50.111021
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 104.57%
- **sharpe_ratio:** 0.99
- **max_drawdown:** -26.52%
- **win_rate:** 53.26%
- **alpha:** -39.32%

## Risk Parameters
- **max_portfolio_allocation:** 9.8%
- **stop_loss:** 25.0%
- **take_profit_target:** 13.5%
- **max_drawdown_tolerance:** 26.5%
- **rebalance_frequency:** monthly

## Execution Guidance
- **order_type:** market
- **limit_offset:** market: Use market orders for volatile names.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter in 3 tranches over 1-2 weeks.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **ADI** | BUY | 36% | Market order (volatile) | 38.1% below entry | 20.6% above entry | 6.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ADI) / [Yahoo](https://finance.yahoo.com/quote/ADI/) |
| **ROK** | BUY | 32% | Market order (volatile) | 34.0% below entry | 18.4% above entry | 7.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ROK) / [Yahoo](https://finance.yahoo.com/quote/ROK/) |
| **BOTZ** | BUY | 26% | Limit 0.5% below market | 27.4% below entry | 14.8% above entry | 8.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BOTZ) / [Yahoo](https://finance.yahoo.com/quote/BOTZ/) |
| **MBLY** | BUY | 65% | Market order (volatile) | 40.0% below entry | 36.8% above entry | 3.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MBLY) / [Yahoo](https://finance.yahoo.com/quote/MBLY/) |
| **APH** | BUY | 39% | Market order (volatile) | 40.0% below entry | 22.0% above entry | 6.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=APH) / [Yahoo](https://finance.yahoo.com/quote/APH/) |
| **RRX** | BUY | 45% | Market order (volatile) | 40.0% below entry | 25.8% above entry | 5.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=RRX) / [Yahoo](https://finance.yahoo.com/quote/RRX/) |
| **JBL** | BUY | 40% | Market order (volatile) | 40.0% below entry | 23.0% above entry | 5.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JBL) / [Yahoo](https://finance.yahoo.com/quote/JBL/) |
| **TER** | BUY | 58% | Market order (volatile) | 40.0% below entry | 32.7% above entry | 4.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TER) / [Yahoo](https://finance.yahoo.com/quote/TER/) |
| **ISRG** | BUY | 32% | Market order (volatile) | 33.6% below entry | 18.2% above entry | 7.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ISRG) / [Yahoo](https://finance.yahoo.com/quote/ISRG/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 40.0% below entry | 27.6% above entry | 4.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **TEL** | BUY | 30% | Limit 0.5% below market | 31.3% below entry | 16.9% above entry | 7.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TEL) / [Yahoo](https://finance.yahoo.com/quote/TEL/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Research Source

Based on KraneShares KOID ETF thesis from [CICC/KraneShares/ARK Research](../../knowledge/cicc_kranos_ark_research.md). Humanoid robots require three layers: Brain (AI compute, sensors), Body (actuators, connectors, motors), and Integrators (companies assembling complete systems). Brain tier gets 1.5x weight since AI compute is the bottleneck.


<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 159.8% |
| **Avg 5Y Sharpe** | 0.77 |
| **Avg 5Y Max DD** | -32.8% |
| **10Y Return (2015-2024)** | 476.4% |
| **10Y Sharpe** | 0.74 |
| **10Y Max DD** | -36.4% |
| **HODL Composite** | 1.21 |
| **Windows Tested** | 28 |
| **Consistency** | 93% |

### How to Use This Strategy Passively

This strategy has strong long-term performance with good consistency (93% of windows positive Sharpe). **Consider allocating 5-10% of portfolio.** Rebalance quarterly.

**Simplest passive approach:** Equal-weight NVDA, ISRG, APH, ROK, ADI. These five span AI compute (NVDA), surgical precision integration (ISRG), connectivity backbone (APH), industrial automation (ROK), and analog sensing (ADI). Or buy BOTZ for managed robotics exposure.

**Note:** MBLY (Mobileye) only IPO'd in late 2022, so it contributes only in recent windows. ABB has data issues on some providers. The strategy gracefully handles missing tickers by redistributing weight.

</details>
