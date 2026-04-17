# WINNING Strategy: bonds_down_banks_up

> **What it does:** Rising rates crush bonds but boost banks (wider NIM) + insurance (float income). TLT↓ = XLF↑.
>
> **Hypothesis:** Bonds Down → Banks Up (Rate Rotation)

**Generated:** 2026-04-12T19:02:23.526144
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 33.99%
- **sharpe_ratio:** 0.51
- **max_drawdown:** -20.35%
- **win_rate:** 54.46%
- **alpha:** -12.85%

## Risk Parameters
- **max_portfolio_allocation:** 8.5%
- **stop_loss:** 15.0%
- **take_profit_target:** 8.0%
- **max_drawdown_tolerance:** 20.3%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** market
- **limit_offset:** market: Enter immediately when trigger fires. Speed matters more than price.
- **timing:** SAFE TO BUY. Even better: add more when interest rates are rising — banks earn wider margins on loans.
- **scaling:** Full position at trigger. No scaling — the signal is binary.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **JPM** | BUY | 25% | Limit 0.5% below market | 16.0% below entry | 8.6% above entry | 7.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **GS** | BUY | 31% | Market order (volatile) | 19.7% below entry | 10.5% above entry | 6.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GS) / [Yahoo](https://finance.yahoo.com/quote/GS/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 7.9% below entry | 4.2% above entry | 16.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 33.3% |
| **Avg 5Y Sharpe** | 0.2 |
| **10Y Return** | 77.4% |
| **10Y Sharpe** | 0.21 |
| **HODL Composite** | 0.21 |
| **Consistency** | 64% |
| **Suitable for passive** | No |

This strategy has **moderate long-term potential** but requires monitoring.

- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -33% drawdown to return 77% long-term.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>
