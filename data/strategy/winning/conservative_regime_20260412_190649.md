# WINNING Strategy: conservative_regime

> **What it does:** 70% regime-adaptive + 30% permanent defense (GLD/SHY/SCHD). Lower DD, steadier returns.
>
> **Hypothesis:** Conservative Regime Orchestrator

**Generated:** 2026-04-12T19:06:48.718766
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 103.23%
- **sharpe_ratio:** 1.65
- **max_drawdown:** -13.53%
- **win_rate:** 57.52%
- **alpha:** 3.64%

## Risk Parameters
- **max_portfolio_allocation:** 16.9%
- **stop_loss:** 13.5%
- **take_profit_target:** 13.4%
- **max_drawdown_tolerance:** 13.5%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** market
- **limit_offset:** market: Auto-managed. No manual entry needed — strategy self-adjusts weekly.
- **timing:** ALWAYS ACTIVE: Auto-managed. Switches between growth and defensive weekly based on market conditions. No user timing needed.
- **scaling:** Set it and forget it. Review quarterly.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **GLD** | BUY | 23% | Limit 0.5% below market | 13.0% below entry | 12.9% above entry | 17.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SHY** | BUY | 2% | Limit 0.5% below market | 6.8% below entry | 6.7% above entry | 33.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **SCHD** | BUY | 14% | Limit 0.5% below market | 8.0% below entry | 7.9% above entry | 28.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SCHD) / [Yahoo](https://finance.yahoo.com/quote/SCHD/) |
| **MSFT** | BUY | 24% | Limit 0.5% below market | 13.8% below entry | 13.7% above entry | 16.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 27.6% below entry | 27.3% above entry | 8.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 17.0% below entry | 16.8% above entry | 13.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **EPD** | BUY | 17% | Limit 0.5% below market | 9.8% below entry | 9.7% above entry | 23.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EPD) / [Yahoo](https://finance.yahoo.com/quote/EPD/) |
| **ET** | BUY | 23% | Limit 0.5% below market | 13.0% below entry | 12.9% above entry | 17.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ET) / [Yahoo](https://finance.yahoo.com/quote/ET/) |
| **MPLX** | BUY | 18% | Limit 0.5% below market | 10.3% below entry | 10.2% above entry | 22.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MPLX) / [Yahoo](https://finance.yahoo.com/quote/MPLX/) |
| **AAPL** | BUY | 29% | Limit 0.5% below market | 16.3% below entry | 16.1% above entry | 14.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **CRM** | BUY | 33% | Market order (volatile) | 19.0% below entry | 18.8% above entry | 12.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CRM) / [Yahoo](https://finance.yahoo.com/quote/CRM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 128.0% |
| **Avg 5Y Sharpe** | 0.93 |
| **10Y Return** | 445.0% |
| **10Y Sharpe** | 1.01 |
| **HODL Composite** | 0.57 |
| **Consistency** | 89% |
| **Suitable for passive** | Yes |

This strategy is **suitable for passive investing**.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -26% drawdown to return 445% long-term.
- **Exit rule:** Never manually exit — auto-managed. Review quarterly.

</details>
