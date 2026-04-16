"""Tests for bespoke.cli — command-line interface."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from bespoke.cli.main import main, _build_parser


def _mock_fetch_factory():
    """Create a mock fetch function returning synthetic data."""
    dates = pd.bdate_range("2019-01-01", "2025-12-31")
    rng = np.random.RandomState(42)
    prices = 100 * np.cumprod(1 + rng.normal(0.0003, 0.01, len(dates)))
    fake_df = pd.DataFrame({
        "Open": prices * 0.99,
        "High": prices * 1.01,
        "Low": prices * 0.98,
        "Close": prices,
        "Volume": rng.randint(1_000_000, 10_000_000, len(dates)),
    }, index=dates)

    def mock_fetch(symbol, start=None, end=None, **kw):
        mask = pd.Series(True, index=fake_df.index)
        if start:
            mask &= fake_df.index >= pd.Timestamp(start)
        if end:
            mask &= fake_df.index <= pd.Timestamp(end)
        return fake_df.loc[mask].copy()

    return mock_fetch


class TestListCommand:
    def test_list_command(self, capsys):
        """bespoke list shows strategies."""
        rc = main(["list"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "spy_buy_and_hold" in out
        assert "balanced_sixty_forty" in out

    def test_list_with_category(self, capsys):
        """bespoke list --category generic filters by category."""
        rc = main(["list", "--category", "generic"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "spy_buy_and_hold" in out


class TestInfoCommand:
    def test_info_command(self, capsys):
        """bespoke info shows strategy details."""
        rc = main(["info", "spy_buy_and_hold"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "spy_buy_and_hold" in out
        assert "SPY" in out

    def test_info_missing_strategy(self, capsys):
        """bespoke info with unknown strategy returns error."""
        rc = main(["info", "nonexistent_xyz_99"])
        assert rc == 1


class TestBacktestCommand:
    def test_backtest_command(self, capsys, monkeypatch):
        """bespoke backtest runs and prints results."""
        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", _mock_fetch_factory())

        rc = main(["backtest", "spy_buy_and_hold", "--start", "2023-01-01", "--end", "2024-12-31"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "Total Return" in out
        assert "Sharpe Ratio" in out

    def test_backtest_missing_strategy(self, capsys):
        """bespoke backtest with unknown strategy returns error."""
        rc = main(["backtest", "nonexistent_xyz_99"])
        assert rc == 1


class TestSaveCommand:
    def test_save_command(self, capsys, monkeypatch, tmp_path):
        """bespoke save produces a valid JSON file."""
        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", _mock_fetch_factory())

        out_file = tmp_path / "result.json"
        rc = main([
            "save", "spy_buy_and_hold",
            "--output", str(out_file),
            "--start", "2023-01-01",
            "--end", "2024-12-31",
        ])
        assert rc == 0
        assert out_file.exists()

        data = json.loads(out_file.read_text())
        assert data["strategy"] == "spy_buy_and_hold"
        assert "metrics" in data


class TestNoCommand:
    def test_no_command_shows_help(self, capsys):
        """Running bespoke with no args shows help."""
        rc = main([])
        assert rc == 0

    def test_parser_builds(self):
        """Parser builds without error."""
        parser = _build_parser()
        assert parser is not None
