"""Bespoke CLI — backtest, analyze, and compare trading strategies.

Usage:
    bespoke list                           # List all registered strategies
    bespoke info <strategy>                # Show strategy details
    bespoke backtest <strategy>            # Run backtest with defaults
    bespoke backtest <strategy> --start 2020-01-01 --end 2025-12-31
    bespoke backtest <strategy> --windows  # Run on all 28 rolling windows
    bespoke compare <strat1> <strat2>      # Compare two strategies
    bespoke save <strategy> --output f.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from typing import List, Optional


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bespoke",
        description="Bespoke trading strategy library",
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # list
    p_list = sub.add_parser("list", help="List all registered strategies")
    p_list.add_argument(
        "--category", "-c", default=None,
        help="Filter by category",
    )

    # info
    p_info = sub.add_parser("info", help="Show strategy details")
    p_info.add_argument("strategy", help="Strategy name")

    # backtest
    p_bt = sub.add_parser("backtest", help="Run a backtest")
    p_bt.add_argument("strategy", help="Strategy name")
    p_bt.add_argument("--start", "-s", default="2020-01-01", help="Start date (YYYY-MM-DD)")
    p_bt.add_argument("--end", "-e", default=None, help="End date (YYYY-MM-DD)")
    p_bt.add_argument("--cash", type=float, default=100_000, help="Initial cash")
    p_bt.add_argument("--benchmark", default="SPY", help="Benchmark symbol")
    p_bt.add_argument("--windows", action="store_true", help="Run on all rolling windows")

    # compare
    p_cmp = sub.add_parser("compare", help="Compare two strategies")
    p_cmp.add_argument("strategy1", help="First strategy")
    p_cmp.add_argument("strategy2", help="Second strategy")
    p_cmp.add_argument("--start", "-s", default="2020-01-01", help="Start date")
    p_cmp.add_argument("--end", "-e", default=None, help="End date")
    p_cmp.add_argument("--cash", type=float, default=100_000, help="Initial cash")

    # save
    p_save = sub.add_parser("save", help="Run backtest and save results to JSON")
    p_save.add_argument("strategy", help="Strategy name")
    p_save.add_argument("--output", "-o", required=True, help="Output JSON path")
    p_save.add_argument("--start", "-s", default="2020-01-01", help="Start date")
    p_save.add_argument("--end", "-e", default=None, help="End date")
    p_save.add_argument("--cash", type=float, default=100_000, help="Initial cash")

    return parser


# -- Rolling windows (7 horizons x 4 end years = 28 windows) ----------------

ROLLING_WINDOWS = []
for end_year in [2025, 2024, 2023, 2022]:
    for years_back in [1, 2, 3, 5, 7, 10, 15]:
        start_year = end_year - years_back
        if start_year >= 2000:
            ROLLING_WINDOWS.append({
                "name": f"{years_back}Y_ending_{end_year}",
                "start": f"{start_year}-01-01",
                "end": f"{end_year}-12-31",
            })


# -- Command handlers --------------------------------------------------------

def cmd_list(args) -> int:
    from bespoke.strategies import list_strategies

    strategies = list_strategies()
    if args.category:
        strategies = [s for s in strategies if s.config.category == args.category]

    if not strategies:
        print("No strategies found.")
        return 0

    # Group by category
    by_cat = {}
    for s in strategies:
        cat = s.config.category
        by_cat.setdefault(cat, []).append(s)

    total = len(strategies)
    print(f"\n  {total} strategies available\n")
    print(f"  {'Name':<35s} {'Category':<15s} {'Universe':<8s} {'Rebalance':<10s}")
    print(f"  {'-'*35} {'-'*15} {'-'*8} {'-'*10}")

    for cat in sorted(by_cat):
        for s in sorted(by_cat[cat], key=lambda x: x.name):
            print(
                f"  {s.name:<35s} {s.config.category:<15s} "
                f"{len(s.universe):<8d} {s.config.rebalance_frequency:<10s}"
            )

    print()
    return 0


def cmd_info(args) -> int:
    from bespoke.strategies import get_strategy

    try:
        strat = get_strategy(args.strategy)
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(f"\n  Strategy: {strat.name}")
    print(f"  Category: {strat.config.category}")
    print(f"  Description: {strat.config.description or '(none)'}")
    print(f"  Universe: {', '.join(strat.universe) if strat.universe else '(empty)'}")
    print(f"  Benchmark: {strat.config.benchmark}")
    print(f"  Rebalance: {strat.config.rebalance_frequency}")
    print(f"  Max positions: {strat.config.max_positions}")
    print(f"  Max position size: {strat.config.max_position_size:.0%}")
    print()
    return 0


def cmd_backtest(args) -> int:
    from bespoke import Backtester
    from bespoke.strategies import get_strategy

    try:
        strat = get_strategy(args.strategy)
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.windows:
        return _run_windows(strat, args)

    print(f"\n  Backtesting {strat.name} ({args.start} to {args.end or 'now'}) ...")

    bt = Backtester(
        strat, start=args.start, end=args.end,
        initial_cash=args.cash, benchmark=args.benchmark,
    )
    result = bt.run()
    _print_result(result)
    return 0


def _run_windows(strat, args) -> int:
    from bespoke import Backtester
    from bespoke.core.metrics import compute_composite

    print(f"\n  Running {len(ROLLING_WINDOWS)} rolling windows for {strat.name} ...\n")

    window_results = {}
    for w in ROLLING_WINDOWS:
        bt = Backtester(strat, start=w["start"], end=w["end"], initial_cash=args.cash)
        result = bt.run()
        m = result.get("metrics", {})
        window_results[w["name"]] = {
            "ret": m.get("total_return", 0),
            "sh": m.get("sharpe_ratio", 0),
            "dd": m.get("max_drawdown", 0),
        }
        ret = m.get("total_return", 0)
        sh = m.get("sharpe_ratio", 0)
        dd = m.get("max_drawdown", 0)
        print(f"  {w['name']:<25s}  ret={ret:>8.2%}  sharpe={sh:>6.2f}  dd={dd:>8.2%}")

    comp = compute_composite(window_results)
    print(f"\n  Composite: {comp['composite']:.4f}  "
          f"Consistency: {comp['consistency']:.0%}  "
          f"Avg Return: {comp['avg_ret']:.2%}  "
          f"Avg DD: {comp['avg_dd']:.2%}")
    print()
    return 0


def cmd_compare(args) -> int:
    from bespoke import Backtester
    from bespoke.strategies import get_strategy

    try:
        s1 = get_strategy(args.strategy1)
        s2 = get_strategy(args.strategy2)
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(f"\n  Comparing {s1.name} vs {s2.name} ({args.start} to {args.end or 'now'}) ...\n")

    bt1 = Backtester(s1, start=args.start, end=args.end, initial_cash=args.cash)
    bt2 = Backtester(s2, start=args.start, end=args.end, initial_cash=args.cash)
    r1 = bt1.run()
    r2 = bt2.run()

    m1 = r1.get("metrics", {})
    m2 = r2.get("metrics", {})

    header = f"  {'Metric':<25s} {s1.name:>20s} {s2.name:>20s}"
    print(header)
    print(f"  {'-'*25} {'-'*20} {'-'*20}")

    keys = [
        ("total_return", "Total Return", True),
        ("cagr", "CAGR", True),
        ("sharpe_ratio", "Sharpe Ratio", False),
        ("sortino_ratio", "Sortino Ratio", False),
        ("max_drawdown", "Max Drawdown", True),
        ("annual_volatility", "Annual Volatility", True),
        ("calmar_ratio", "Calmar Ratio", False),
        ("win_rate", "Win Rate", True),
    ]

    for key, label, is_pct in keys:
        v1 = m1.get(key, 0)
        v2 = m2.get(key, 0)
        if is_pct:
            print(f"  {label:<25s} {v1:>19.2%} {v2:>19.2%}")
        else:
            print(f"  {label:<25s} {v1:>20.2f} {v2:>20.2f}")

    # Final values
    fv1 = r1.get("final_value", args.cash)
    fv2 = r2.get("final_value", args.cash)
    print(f"  {'Final Value':<25s} {'$'+f'{fv1:,.0f}':>20s} {'$'+f'{fv2:,.0f}':>20s}")
    print(f"  {'Num Trades':<25s} {r1.get('num_trades', 0):>20d} {r2.get('num_trades', 0):>20d}")
    print()
    return 0


def cmd_save(args) -> int:
    from bespoke import Backtester
    from bespoke.strategies import get_strategy

    try:
        strat = get_strategy(args.strategy)
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(f"  Backtesting {strat.name} ...")
    bt = Backtester(strat, start=args.start, end=args.end, initial_cash=args.cash)
    bt.run()
    path = bt.save(args.output)
    print(f"  Saved to {path}")
    return 0


def _print_result(result: dict):
    """Pretty-print a backtest result."""
    m = result.get("metrics", {})

    if "error" in result:
        print(f"\n  Error: {result['error']}\n")
        return

    print(f"\n  Strategy:     {result['strategy']}")
    print(f"  Period:       {result['start']} to {result['end']}")
    print(f"  Final Value:  ${result.get('final_value', 0):,.2f}")
    print(f"  Num Trades:   {result.get('num_trades', 0)}")
    print()
    print(f"  Total Return:     {m.get('total_return', 0):>10.2%}")
    print(f"  CAGR:             {m.get('cagr', 0):>10.2%}")
    print(f"  Sharpe Ratio:     {m.get('sharpe_ratio', 0):>10.2f}")
    print(f"  Sortino Ratio:    {m.get('sortino_ratio', 0):>10.2f}")
    print(f"  Max Drawdown:     {m.get('max_drawdown', 0):>10.2%}")
    print(f"  Annual Vol:       {m.get('annual_volatility', 0):>10.2%}")
    print(f"  Calmar Ratio:     {m.get('calmar_ratio', 0):>10.2f}")
    print(f"  Win Rate:         {m.get('win_rate', 0):>10.2%}")
    if "alpha" in m:
        print(f"  Alpha:            {m['alpha']:>10.4f}")
        print(f"  Beta:             {m['beta']:>10.4f}")
    print()


def main(argv: Optional[List[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    handlers = {
        "list": cmd_list,
        "info": cmd_info,
        "backtest": cmd_backtest,
        "compare": cmd_compare,
        "save": cmd_save,
    }

    handler = handlers.get(args.command)
    if handler is None:
        parser.print_help()
        return 1

    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
