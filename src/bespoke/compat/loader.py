"""Load agents-assemble strategies into bespoke's registry.

This bridge allows bespoke to use ALL 251+ strategies from agents-assemble
without copying or rewriting them. It wraps BasePersona classes as
bespoke BaseStrategy instances.

Usage:
    from bespoke.compat import load_agents_assemble
    load_agents_assemble("/path/to/agents-assemble")
    # Now all strategies are available via get_strategy()
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from bespoke.strategies.base import BaseStrategy, StrategyConfig
from bespoke.strategies.registry import register_strategy


# Map agents-assemble module names → registry dict names → category
MODULES = [
    ("personas", "ALL_PERSONAS", "generic"),
    ("famous_investors", "FAMOUS_INVESTORS", "famous"),
    ("theme_strategies", "THEME_STRATEGIES", "themes"),
    ("portfolio_strategies", "PORTFOLIO_STRATEGIES", "portfolio"),
    ("recession_strategies", "RECESSION_STRATEGIES", "recession"),
    ("unconventional_strategies", "UNCONVENTIONAL_STRATEGIES", "unconventional"),
    ("research_strategies", "RESEARCH_STRATEGIES", "research"),
    ("math_strategies", "MATH_STRATEGIES", "math"),
    ("hedge_fund_strategies", "HEDGE_FUND_STRATEGIES", "hedge_fund"),
    ("crisis_commodity_strategies", "CRISIS_COMMODITY_STRATEGIES", "crisis"),
    ("williams_seasonal_strategies", "WILLIAMS_SEASONAL_STRATEGIES", "seasonal"),
    ("news_event_strategies", "NEWS_EVENT_STRATEGIES", "news_event"),
    ("political_strategies", "POLITICAL_STRATEGIES", "political"),
    ("strategy_orchestrator", "ORCHESTRATOR_STRATEGIES", "orchestrator"),
    ("gap_strategies", "GAP_STRATEGIES", "generic"),
]


class PersonaAdapter(BaseStrategy):
    """Wraps an agents-assemble BasePersona as a bespoke BaseStrategy.

    This adapter makes any persona callable with bespoke's interface while
    preserving the original generate_signals() behavior.
    """

    def __init__(self, persona_instance, category: str = "generic"):
        # Extract config from persona
        if hasattr(persona_instance, "config"):
            pc = persona_instance.config
            config = StrategyConfig(
                name=getattr(pc, "name", persona_instance.__class__.__name__),
                description=getattr(pc, "description", ""),
                universe=list(getattr(pc, "universe", [])),
                benchmark=getattr(pc, "benchmark", "SPY"),
                rebalance_frequency=_fix_rebalance(getattr(pc, "rebalance_frequency", "monthly")),
                max_positions=getattr(pc, "max_positions", 20),
                max_position_size=getattr(pc, "max_position_size", 0.20),
                category=category,
            )
        else:
            config = StrategyConfig(
                name=persona_instance.__class__.__name__.lower(),
                universe=list(getattr(persona_instance, "universe", [])),
                category=category,
            )

        super().__init__(config)
        self._persona = persona_instance

    def generate_signals(self, date, prices, portfolio, data):
        """Delegate to the wrapped persona's generate_signals."""
        return self._persona.generate_signals(date, prices, portfolio, data)

    def __repr__(self):
        return f"PersonaAdapter({self.name!r}, category={self.config.category!r}, universe={len(self.universe)} tickers)"


def load_agents_assemble(
    path: str = "/Users/alvas/jean-claude/agents-assemble",
    verbose: bool = False,
) -> Dict[str, BaseStrategy]:
    """Load ALL strategies from agents-assemble into bespoke's registry.

    Args:
        path: Path to agents-assemble repo root
        verbose: Print loading progress

    Returns:
        Dict of {name: PersonaAdapter} for all loaded strategies
    """
    repo = Path(path)
    if not repo.exists():
        raise FileNotFoundError(f"agents-assemble not found at {path}")

    # Add repo root to sys.path so we can import the flat files
    repo_str = str(repo)
    if repo_str not in sys.path:
        sys.path.insert(0, repo_str)

    loaded = {}
    errors = []

    for mod_name, dict_name, category in MODULES:
        try:
            # Import the module
            if mod_name in sys.modules:
                mod = importlib.reload(sys.modules[mod_name])
            else:
                mod = importlib.import_module(mod_name)

            # Get the registry dict
            registry = getattr(mod, dict_name, {})

            for key, cls in registry.items():
                try:
                    persona = cls()
                    adapter = PersonaAdapter(persona, category=category)
                    register_strategy(key, type(adapter))
                    # Store factory so get_strategy() can create fresh instances
                    _PERSONA_FACTORIES[key] = (cls, category)
                    loaded[key] = adapter

                    if verbose:
                        print(f"  {key:40s} [{category}] ({len(adapter.universe)} tickers)")
                except Exception as e:
                    errors.append((key, str(e)))

        except Exception as e:
            if verbose:
                print(f"  SKIP module {mod_name}: {e}")

    if verbose:
        print(f"\nLoaded: {len(loaded)}, Errors: {len(errors)}")
        if errors:
            for name, err in errors[:5]:
                print(f"  ERROR {name}: {err}")

    return loaded


# Factory storage for creating fresh persona instances
_PERSONA_FACTORIES: Dict[str, tuple] = {}


def _make_persona_adapter_class(key: str, cls: type, category: str) -> Type[BaseStrategy]:
    """Create a PersonaAdapter subclass for registry storage."""

    class _Adapter(PersonaAdapter):
        def __init__(self):
            persona = cls()
            super().__init__(persona, category=category)

    _Adapter.__name__ = f"Adapted_{key}"
    _Adapter.__qualname__ = f"Adapted_{key}"
    return _Adapter


def load_agents_assemble_v2(
    path: str = "/Users/alvas/jean-claude/agents-assemble",
    verbose: bool = False,
) -> int:
    """Load ALL strategies from agents-assemble (v2 — proper registry).

    This version registers adapter CLASSES (not instances) so get_strategy()
    creates fresh instances each time.

    Returns:
        Number of strategies loaded
    """
    repo = Path(path)
    if not repo.exists():
        raise FileNotFoundError(f"agents-assemble not found at {path}")

    repo_str = str(repo)
    if repo_str not in sys.path:
        sys.path.insert(0, repo_str)

    count = 0
    for mod_name, dict_name, category in MODULES:
        try:
            if mod_name in sys.modules:
                mod = importlib.reload(sys.modules[mod_name])
            else:
                mod = importlib.import_module(mod_name)

            registry = getattr(mod, dict_name, {})
            for key, cls in registry.items():
                try:
                    adapter_cls = _make_persona_adapter_class(key, cls, category)
                    register_strategy(key, adapter_cls)
                    count += 1
                    if verbose:
                        print(f"  {key:40s} [{category}]")
                except Exception:
                    pass
        except Exception:
            pass

    if verbose:
        print(f"\nTotal: {count} strategies loaded")
    return count


def _fix_rebalance(freq: str) -> str:
    """Fix non-standard rebalance frequencies."""
    valid = {"daily", "weekly", "monthly"}
    if freq in valid:
        return freq
    if freq == "quarterly":
        return "monthly"
    return "monthly"
