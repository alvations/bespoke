# LOSING Strategy: bond_fixed_income

> **What it does:** Diversified bonds: duration ladder + credit spectrum + EM, 3-5% yield target
>
> **Hypothesis:** Bond & Fixed Income Portfolio 4Y (2022-2025)

**Generated:** 2026-04-08T23:04:17.138386
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -0.47%
- **sharpe_ratio:** -0.51
- **max_drawdown:** -19.46%
- **win_rate:** 51.00%
- **alpha:** -10.98%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 23.3%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 19.5%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: Always hold for income (DCA on rebalance). STRONG BUY: On price dip to SMA200 — yield expands, lock in higher income rate.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **TLT** | BUY | 13% | Limit 0.5% below market | 12.3% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **LQD** | BUY | 7% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LQD) / [Yahoo](https://finance.yahoo.com/quote/LQD/) |
| **HYG** | BUY | 5% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=HYG) / [Yahoo](https://finance.yahoo.com/quote/HYG/) |
| **VWOB** | BUY | 6% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VWOB) / [Yahoo](https://finance.yahoo.com/quote/VWOB/) |
| **SCHI** | BUY | 5% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SCHI) / [Yahoo](https://finance.yahoo.com/quote/SCHI/) |
| **VTEB** | BUY | 4% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VTEB) / [Yahoo](https://finance.yahoo.com/quote/VTEB/) |
| **AGG** | BUY | 5% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AGG) / [Yahoo](https://finance.yahoo.com/quote/AGG/) |
| **BND** | BUY | 5% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BND) / [Yahoo](https://finance.yahoo.com/quote/BND/) |
| **FBND** | BUY | 5% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=FBND) / [Yahoo](https://finance.yahoo.com/quote/FBND/) |
| **SPBO** | BUY | 5% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPBO) / [Yahoo](https://finance.yahoo.com/quote/SPBO/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.51 (target > 0.5)
- Max drawdown: -19.46% (target > -20%)
- Alpha: -10.98% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 11.8% |
| **Avg 5Y Sharpe** | -0.2 |
| **Avg 5Y Max DD** | -17.4% |
| **10Y Return (2015-2024)** | 19.2% |
| **10Y Sharpe** | -0.31 |
| **10Y Max DD** | -21.1% |
| **HODL Composite** | 0.04 |
| **Windows Tested** | 28 |
| **Consistency** | 42% |

### How to Use This Strategy Passively

This strategy is **NOT recommended for passive investing**. It has low consistency across time periods or negative long-term returns.

**If you still want exposure:** Limit to 5% of your portfolio maximum. Use the strategy orchestrator (conservative_regime) instead for passive allocation.

</details>
