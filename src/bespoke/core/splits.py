"""Train / validation / test splits of the 28 rolling windows.

Evolution loops see only TRAIN. Champion selection uses VAL. TEST is opened
once at end-of-run; if the champion disagrees there, discard it.

Window key convention: ``<horizon>_<year>`` for 1Y (e.g. ``1Y_2020``) and
``<horizon>_<start>_<end>`` for multi-year (e.g. ``3Y_2022_2024``). Horizon
prefix is parsed by splitting on the first underscore.
"""
from __future__ import annotations

from typing import Any, Dict, List


TRAIN_WINDOWS: List[str] = [
    "1Y_2015", "1Y_2016", "1Y_2017", "1Y_2019", "1Y_2021", "1Y_2023",
    "3Y_2015_2017", "3Y_2016_2018", "3Y_2017_2019", "3Y_2018_2020",
    "3Y_2019_2021", "3Y_2021_2023",
    "5Y_2015_2019", "5Y_2016_2020", "5Y_2017_2021", "5Y_2019_2023",
    "5Y_2021_2025",
    "10Y_2015_2024",
]

VAL_WINDOWS: List[str] = [
    "1Y_2018", "1Y_2024",
    "3Y_2020_2022", "3Y_2022_2024",
    "5Y_2018_2022", "5Y_2020_2024",
]

TEST_WINDOWS: List[str] = [
    "1Y_2020", "1Y_2022", "1Y_2025", "3Y_2023_2025",
]

ALL_WINDOWS: List[str] = TRAIN_WINDOWS + VAL_WINDOWS + TEST_WINDOWS

SPLITS: Dict[str, List[str]] = {
    "train": TRAIN_WINDOWS,
    "val": VAL_WINDOWS,
    "test": TEST_WINDOWS,
    "all": ALL_WINDOWS,
}


def filter_windows(windows: Dict[str, Any], split: str) -> Dict[str, Any]:
    if split not in SPLITS:
        raise ValueError(f"unknown split {split!r}; expected one of {list(SPLITS)}")
    keys = set(SPLITS[split])
    return {k: v for k, v in windows.items() if k in keys}


def horizon_of(window_key: str) -> str:
    return window_key.split("_")[0]


def group_by_horizon(windows: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    groups: Dict[str, Dict[str, Any]] = {}
    for k, v in windows.items():
        groups.setdefault(horizon_of(k), {})[k] = v
    return groups
