# bespoke

A Python library for backtesting, comparing, and building trading strategies. Bespoke provides a clean API for defining strategy logic, running historical simulations with realistic slippage modeling, and evaluating performance through standard financial metrics like Sharpe ratio, CAGR, max drawdown, and rolling-window composite scores.

## Install

```bash
pip install bespoke
```

## Quick Start

```python
from bespoke import Backtester
from bespoke.strategies import get_strategy

strategy = get_strategy("spy_buy_and_hold")
bt = Backtester(strategy, start="2020-01-01", end="2025-12-31")
result = bt.run()
print(f"Return: {result['metrics']['total_return']:.2%}")
print(f"Sharpe: {result['metrics']['sharpe_ratio']:.2f}")
```

## CLI

Bespoke includes a command-line interface for quick analysis.

```bash
# List all available strategies
bespoke list

# Show details for a strategy
bespoke info spy_buy_and_hold

# Run a backtest
bespoke backtest spy_buy_and_hold --start 2020-01-01 --end 2025-12-31

# Run on all 28 rolling windows (1Y-15Y x 4 end years)
bespoke backtest spy_buy_and_hold --windows

# Compare two strategies side by side
bespoke compare spy_buy_and_hold balanced_sixty_forty

# Save results to JSON
bespoke save spy_buy_and_hold --output results.json
```

## Creating a Custom Strategy

Subclass `BaseStrategy` and implement `generate_signals`:

```python
from bespoke.strategies.base import BaseStrategy, StrategyConfig

class MomentumStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(StrategyConfig(
            name="momentum",
            description="Buy assets with positive 50-day momentum",
            universe=["SPY", "QQQ", "IWM"],
            rebalance_frequency="monthly",
            max_position_size=0.50,
        ))

    def generate_signals(self, date, prices, portfolio, data):
        signals = {}
        for sym in self.universe:
            if sym in data and date in data[sym].index:
                sma50 = data[sym].loc[:date, "SMA_50"].iloc[-1]
                if prices.get(sym, 0) > sma50:
                    signals[sym] = 1.0
        return signals
```

Then backtest it:

```python
from bespoke import Backtester

bt = Backtester(MomentumStrategy(), start="2020-01-01")
result = bt.run()
```

## Architecture

```
bespoke/
  core/
    backtester.py    Event-driven backtester with slippage + rebalancing
    portfolio.py     Position tracking, cash management, trade history
    metrics.py       Sharpe, Sortino, CAGR, drawdown, alpha/beta, composite
  data/
    fetcher.py       OHLCV via yfinance with parquet caching + indicators
  strategies/
    base.py          BaseStrategy + StrategyConfig dataclass
    registry.py      Auto-discovery and name-based lookup
    generic/         Baseline strategies (SPY, 60/40, three-fund)
  compat/
    loader.py        Bridge to load external strategy collections
  cli/
    main.py          Command-line interface (argparse)
```

**Data flow:**
1. `Backtester` loads OHLCV data via `fetch_ohlcv` (cached locally)
2. Technical indicators are added (SMA, RSI, MACD, Bollinger, ATR)
3. On each trading day, `Strategy.generate_signals()` returns target weights
4. `Portfolio` executes rebalancing trades with slippage
5. `compute_metrics()` evaluates the resulting equity curve

## Available Strategies

Three baseline strategies are included out of the box:

| Name | Description | Universe |
|------|-------------|----------|
| `spy_buy_and_hold` | 100% S&P 500, never trade | SPY |
| `balanced_sixty_forty` | 60% stocks / 40% bonds, monthly rebalance | SPY, AGG |
| `three_fund_passive` | 50% SPY + 30% QQQ + 20% GLD | SPY, QQQ, GLD |

These baselines serve as the performance bar that any custom strategy must clear to justify its complexity.

The `bespoke.compat` module provides a bridge to load additional strategy collections. See `bespoke/compat/loader.py` for details.

## Metrics

Every backtest produces:

- **Total Return** and **CAGR** -- absolute and annualized performance
- **Sharpe Ratio** -- risk-adjusted return (excess over risk-free rate)
- **Sortino Ratio** -- penalizes only downside volatility
- **Max Drawdown** -- worst peak-to-trough decline
- **Calmar Ratio** -- CAGR / max drawdown
- **Win Rate** -- fraction of positive trading days
- **Alpha / Beta** -- vs benchmark (when benchmark data available)
- **Composite Score** -- rolling-window consistency metric

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-strategy`)
3. Add your strategy in `src/bespoke/strategies/`
4. Write tests in `tests/`
5. Run `pytest` to verify
6. Submit a pull request

## License

MIT License. See [LICENSE](LICENSE) for details.
