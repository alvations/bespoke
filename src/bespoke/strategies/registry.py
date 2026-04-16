"""Strategy registry — auto-discovers all BaseStrategy subclasses."""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List, Optional, Type

from bespoke.strategies.base import BaseStrategy

_REGISTRY: Dict[str, Type[BaseStrategy]] = {}
_DISCOVERED = False


def register_strategy(name: str, cls: Type[BaseStrategy]):
    """Register a strategy class by name."""
    _REGISTRY[name] = cls


def _discover_strategies():
    """Auto-discover all strategy modules in subpackages."""
    global _DISCOVERED
    if _DISCOVERED:
        return

    strategies_dir = Path(__file__).parent
    for subdir in strategies_dir.iterdir():
        if subdir.is_dir() and not subdir.name.startswith("_"):
            pkg_name = f"bespoke.strategies.{subdir.name}"
            try:
                pkg = importlib.import_module(pkg_name)
                # Import all modules in the subpackage
                for importer, modname, ispkg in pkgutil.iter_modules(
                    [str(subdir)]
                ):
                    if not modname.startswith("_"):
                        try:
                            importlib.import_module(f"{pkg_name}.{modname}")
                        except Exception:
                            pass
            except Exception:
                pass

    # Find all BaseStrategy subclasses that aren't registered yet
    def _find_subclasses(cls):
        for sub in cls.__subclasses__():
            if sub not in _REGISTRY.values():
                # Use the class's config name or class name
                try:
                    instance = sub()
                    key = instance.config.name
                except Exception:
                    key = sub.__name__.lower()
                _REGISTRY[key] = sub
            _find_subclasses(sub)

    _find_subclasses(BaseStrategy)
    _DISCOVERED = True


def get_strategy(name: str) -> BaseStrategy:
    """Get a strategy instance by name."""
    _discover_strategies()
    if name not in _REGISTRY:
        raise KeyError(
            f"Strategy {name!r} not found. "
            f"Available: {sorted(_REGISTRY.keys())[:20]}..."
        )
    return _REGISTRY[name]()


def list_strategies() -> List[BaseStrategy]:
    """List all registered strategies."""
    _discover_strategies()
    result = []
    for name, cls in sorted(_REGISTRY.items()):
        try:
            result.append(cls())
        except Exception:
            pass
    return result


def strategy_names() -> List[str]:
    """List all registered strategy names."""
    _discover_strategies()
    return sorted(_REGISTRY.keys())
