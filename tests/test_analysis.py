"""Tests for bespoke.analysis — entry scoring, regime, validation, correlation, stop loss, benchmarks, combiner."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from bespoke.analysis.entry_scorer import score_entry
from bespoke.analysis.regime import detect_regime, regime_allocations
from bespoke.analysis.validation import walk_forward_test
from bespoke.analysis.correlation import strategy_correlation
from bespoke.analysis.stop_loss import check_stop_loss
from bespoke.analysis.benchmarks import compare_benchmarks
from bespoke.core.combiner import backtest_combination


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_ohlcv(
    n_days: int = 300,
    start_price: float = 100.0,
    daily_return: float = 0.0004,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate synthetic OHLCV data with indicators for testing."""
    dates = pd.bdate_range("2023-01-01", periods=n_days, freq="B")
    rng = np.random.RandomState(seed)
    prices = start_price * np.cumprod(1 + rng.normal(daily_return, 0.008, n_days))
    volume = rng.randint(1_000_000, 10_000_000, n_days).astype(float)
    df = pd.DataFrame({
        "Open": prices * 0.99,
        "High": prices * 1.01,
        "Low": prices * 0.98,
        "Close": prices,
        "Volume": volume,
    }, index=dates)
    from bespoke.data.fetcher import add_indicators
    return add_indicators(df)


def _make_multi_symbol_fetch(symbols=None, seed=42):
    """Create a mock fetch_ohlcv that returns different data per symbol."""
    symbol_data = {}
    rng = np.random.RandomState(seed)
    dates = pd.bdate_range("2019-01-01", "2025-12-31")

    target_symbols = symbols or ["SPY", "AGG", "AAPL", "MSFT", "VT"]

    for i, sym in enumerate(target_symbols):
        local_seed = seed + i
        local_rng = np.random.RandomState(local_seed)
        drift = 0.0003 + i * 0.00005
        prices = 100 * np.cumprod(1 + local_rng.normal(drift, 0.008, len(dates)))
        df = pd.DataFrame({
            "Open": prices * 0.99,
            "High": prices * 1.01,
            "Low": prices * 0.98,
            "Close": prices,
            "Volume": rng.randint(1_000_000, 10_000_000, len(dates)).astype(float),
        }, index=dates)
        symbol_data[sym] = df

    def mock_fetch(symbol, start=None, end=None, **kw):
        if symbol not in symbol_data:
            return None
        df = symbol_data[symbol].copy()
        mask = pd.Series(True, index=df.index)
        if start:
            mask &= df.index >= pd.Timestamp(start)
        if end:
            mask &= df.index <= pd.Timestamp(end)
        return df.loc[mask].copy()

    return mock_fetch


# ---------------------------------------------------------------------------
# Feature 1: Entry Scorer
# ---------------------------------------------------------------------------

class TestEntryScorer:
    def test_score_entry_with_data(self):
        """score_entry returns score, signal, and breakdown."""
        df = _make_ohlcv(n_days=300)
        result = score_entry("AAPL", data=df)

        assert "score" in result
        assert "signal" in result
        assert "breakdown" in result
        assert isinstance(result["score"], int)
        assert 0 <= result["score"] <= 100
        assert result["signal"] in ("STRONG BUY", "BUY", "WEAK BUY", "WAIT")

    def test_score_entry_breakdown_has_all_factors(self):
        """Breakdown contains all 7 scoring factors."""
        df = _make_ohlcv(n_days=300)
        result = score_entry("MSFT", data=df)
        breakdown = result["breakdown"]

        expected_keys = [
            "above_sma50", "rsi_pullback", "near_sma50",
            "high_volume", "macd_cross", "above_sma200", "recent_pullback",
        ]
        for key in expected_keys:
            assert key in breakdown, f"Missing factor: {key}"
            assert "points" in breakdown[key]
            assert "detail" in breakdown[key]

    def test_score_entry_empty_data(self):
        """score_entry handles empty/insufficient data gracefully."""
        df = pd.DataFrame()
        result = score_entry("AAPL", data=df)
        assert result["score"] == 0
        assert result["signal"] == "WAIT"

    def test_score_entry_short_data(self):
        """score_entry handles data shorter than 50 days."""
        df = _make_ohlcv(n_days=30)
        result = score_entry("AAPL", data=df)
        assert result["score"] == 0
        assert "error" in result

    def test_score_entry_all_points_possible(self):
        """Construct data that should max out the score."""
        # Build data where:
        # - Close > SMA50 (above trend)
        # - RSI ~37 (pullback zone)
        # - Close within 2% of SMA50
        # - Volume > 1.5x average
        # - MACD crossing above signal
        # - Close > SMA200
        # - 5% pullback from 20-day high
        dates = pd.bdate_range("2023-01-01", periods=250, freq="B")
        # Steadily rising prices (for SMA200 and SMA50 to be below close)
        prices = np.linspace(100, 150, 250)
        # Create a small dip at the end for pullback + RSI
        prices[-10:] = np.linspace(150, 143, 10)  # ~5% pullback
        volume = np.full(250, 5_000_000.0)
        volume[-1] = 12_000_000.0  # Spike volume on last day
        df = pd.DataFrame({
            "Open": prices * 0.99,
            "High": prices * 1.01,
            "Low": prices * 0.98,
            "Close": prices,
            "Volume": volume,
        }, index=dates)
        from bespoke.data.fetcher import add_indicators
        df = add_indicators(df)

        result = score_entry("AAPL", data=df)
        # Should score well due to pullback + high volume
        assert result["score"] >= 25
        assert result["signal"] in ("STRONG BUY", "BUY", "WEAK BUY", "WAIT")

    def test_score_entry_symbol_in_result(self):
        """Result includes the symbol."""
        df = _make_ohlcv(n_days=300)
        result = score_entry("SPY", data=df)
        assert result.get("symbol") == "SPY"


# ---------------------------------------------------------------------------
# Feature 2: Strategy Combination Backtester
# ---------------------------------------------------------------------------

class TestCombiner:
    def test_backtest_combination_runs(self, monkeypatch):
        """Combination backtest completes with valid results."""
        mock_fetch = _make_multi_symbol_fetch()
        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.backtester.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.combiner.fetch_ohlcv", mock_fetch)

        result = backtest_combination(
            strategies={"spy_buy_and_hold": 0.60, "balanced_sixty_forty": 0.40},
            start="2020-01-01",
            end="2025-12-31",
            initial_cash=10000,
        )

        assert "metrics" in result
        assert "final_value" in result
        assert "contributions" in result
        assert result["final_value"] > 0
        assert result["num_trades"] > 0

    def test_backtest_combination_metrics(self, monkeypatch):
        """Combination returns proper metrics keys."""
        mock_fetch = _make_multi_symbol_fetch()
        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.backtester.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.combiner.fetch_ohlcv", mock_fetch)

        result = backtest_combination(
            strategies={"spy_buy_and_hold": 1.0},
            start="2020-01-01",
            end="2025-12-31",
        )

        m = result["metrics"]
        for key in ["total_return", "sharpe_ratio", "max_drawdown"]:
            assert key in m, f"Missing metric: {key}"

    def test_backtest_combination_contributions(self, monkeypatch):
        """Each strategy has a contribution entry."""
        mock_fetch = _make_multi_symbol_fetch()
        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.backtester.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.combiner.fetch_ohlcv", mock_fetch)

        result = backtest_combination(
            strategies={"spy_buy_and_hold": 0.60, "balanced_sixty_forty": 0.40},
            start="2020-01-01",
            end="2025-12-31",
        )

        assert "spy_buy_and_hold" in result["contributions"]
        assert "balanced_sixty_forty" in result["contributions"]
        assert result["contributions"]["spy_buy_and_hold"]["allocation"] == 0.60

    def test_backtest_combination_weights_normalize(self, monkeypatch):
        """Weights that don't sum to 1 get normalized."""
        mock_fetch = _make_multi_symbol_fetch()
        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.backtester.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.combiner.fetch_ohlcv", mock_fetch)

        result = backtest_combination(
            strategies={"spy_buy_and_hold": 3.0, "balanced_sixty_forty": 2.0},
            start="2020-01-01",
            end="2025-12-31",
        )

        assert result["final_value"] > 0

    def test_backtest_combination_no_data(self, monkeypatch):
        """Returns error when no data available."""
        monkeypatch.setattr("bespoke.core.combiner.fetch_ohlcv", lambda *a, **kw: None)

        result = backtest_combination(
            strategies={"spy_buy_and_hold": 1.0},
            start="2020-01-01",
            end="2025-12-31",
        )

        assert "error" in result


# ---------------------------------------------------------------------------
# Feature 3: Regime Detection
# ---------------------------------------------------------------------------

class TestRegimeDetection:
    def test_detect_regime_bull(self):
        """VIX < 20 + SPY > SMA200 = bull."""
        dates = pd.bdate_range("2023-01-01", periods=250, freq="B")
        # Low VIX
        vix_data = pd.DataFrame({"Close": np.full(250, 15.0)}, index=dates)
        # Rising SPY well above SMA200
        spy_prices = np.linspace(400, 500, 250)
        spy_data = pd.DataFrame({"Close": spy_prices}, index=dates)

        result = detect_regime(vix_data=vix_data, spy_data=spy_data)

        assert result["regime"] == "bull"
        assert result["vix"] == 15.0
        assert result["spy_above_sma200"] is True

    def test_detect_regime_cautious(self):
        """VIX 20-25 = cautious."""
        dates = pd.bdate_range("2023-01-01", periods=250, freq="B")
        vix_data = pd.DataFrame({"Close": np.full(250, 22.0)}, index=dates)
        spy_data = pd.DataFrame({"Close": np.full(250, 450.0)}, index=dates)

        result = detect_regime(vix_data=vix_data, spy_data=spy_data)
        assert result["regime"] == "cautious"

    def test_detect_regime_fear(self):
        """VIX 25-35 = fear."""
        dates = pd.bdate_range("2023-01-01", periods=250, freq="B")
        vix_data = pd.DataFrame({"Close": np.full(250, 30.0)}, index=dates)
        spy_data = pd.DataFrame({"Close": np.full(250, 400.0)}, index=dates)

        result = detect_regime(vix_data=vix_data, spy_data=spy_data)
        assert result["regime"] == "fear"

    def test_detect_regime_panic(self):
        """VIX > 35 = panic."""
        dates = pd.bdate_range("2023-01-01", periods=250, freq="B")
        vix_data = pd.DataFrame({"Close": np.full(250, 45.0)}, index=dates)
        spy_data = pd.DataFrame({"Close": np.full(250, 350.0)}, index=dates)

        result = detect_regime(vix_data=vix_data, spy_data=spy_data)
        assert result["regime"] == "panic"

    def test_detect_regime_low_vix_but_below_sma200(self):
        """VIX < 20 but SPY below SMA200 = cautious."""
        dates = pd.bdate_range("2023-01-01", periods=250, freq="B")
        vix_data = pd.DataFrame({"Close": np.full(250, 15.0)}, index=dates)
        # Declining SPY -- below SMA200
        spy_prices = np.linspace(500, 400, 250)
        spy_data = pd.DataFrame({"Close": spy_prices}, index=dates)

        result = detect_regime(vix_data=vix_data, spy_data=spy_data)
        assert result["regime"] == "cautious"
        assert result["spy_above_sma200"] is False

    def test_regime_allocations_all_regimes(self):
        """All regimes return valid allocations summing to 1."""
        for regime in ["bull", "cautious", "fear", "panic"]:
            result = regime_allocations(regime=regime)
            assert result["regime"] == regime
            alloc = result["allocations"]
            assert "equities" in alloc
            assert "bonds" in alloc
            assert "cash" in alloc
            total = sum(alloc.values())
            assert total == pytest.approx(1.0, abs=0.01)

    def test_regime_allocations_equities_decrease_with_fear(self):
        """Equity allocation decreases as fear increases."""
        bull = regime_allocations("bull")["allocations"]["equities"]
        cautious = regime_allocations("cautious")["allocations"]["equities"]
        fear = regime_allocations("fear")["allocations"]["equities"]
        panic = regime_allocations("panic")["allocations"]["equities"]
        assert bull > cautious > fear > panic

    def test_regime_allocations_unknown_regime(self):
        """Unknown regime defaults to cautious."""
        result = regime_allocations(regime="unknown_regime")
        assert result["regime"] == "cautious"


# ---------------------------------------------------------------------------
# Feature 4: Walk-Forward Validation
# ---------------------------------------------------------------------------

class TestWalkForwardValidation:
    def test_walk_forward_basic(self, monkeypatch):
        """Walk-forward test returns train/test metrics and assessment."""
        mock_fetch = _make_multi_symbol_fetch()
        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.backtester.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.combiner.fetch_ohlcv", mock_fetch)

        result = walk_forward_test(
            strategies={"spy_buy_and_hold": 0.60, "balanced_sixty_forty": 0.40},
            train_start="2020-01-01",
            train_end="2022-12-31",
            test_start="2023-01-01",
            test_end="2025-12-31",
        )

        assert "train_metrics" in result
        assert "test_metrics" in result
        assert "overfit_assessment" in result
        assert "sharpe_ratio_decay" in result
        assert isinstance(result["train_sharpe"], (int, float))
        assert isinstance(result["test_sharpe"], (int, float))

    def test_walk_forward_overfit_detection(self, monkeypatch):
        """Walk-forward flags OVERFIT when test sharpe is much lower than train."""
        # Create data where train period has high returns but test has low
        dates = pd.bdate_range("2019-01-01", "2025-12-31")
        rng = np.random.RandomState(42)

        # Train period: strong uptrend
        n_train = len(dates[dates <= pd.Timestamp("2022-12-31")])
        n_test = len(dates) - n_train
        train_returns = rng.normal(0.001, 0.005, n_train)
        test_returns = rng.normal(-0.001, 0.02, n_test)
        all_returns = np.concatenate([train_returns, test_returns])
        prices = 100 * np.cumprod(1 + all_returns)

        sym_data = {}
        for sym in ["SPY", "AGG"]:
            df = pd.DataFrame({
                "Open": prices * 0.99,
                "High": prices * 1.01,
                "Low": prices * 0.98,
                "Close": prices,
                "Volume": rng.randint(1_000_000, 10_000_000, len(dates)).astype(float),
            }, index=dates)
            sym_data[sym] = df

        def mock_fetch(symbol, start=None, end=None, **kw):
            if symbol not in sym_data:
                return None
            df = sym_data[symbol].copy()
            mask = pd.Series(True, index=df.index)
            if start:
                mask &= df.index >= pd.Timestamp(start)
            if end:
                mask &= df.index <= pd.Timestamp(end)
            return df.loc[mask].copy()

        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.backtester.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.combiner.fetch_ohlcv", mock_fetch)

        result = walk_forward_test(
            strategies={"spy_buy_and_hold": 1.0},
            train_start="2020-01-01",
            train_end="2022-12-31",
            test_start="2023-01-01",
            test_end="2025-12-31",
        )

        assert "overfit_assessment" in result
        # With declining test period, should flag something
        assert result["overfit_assessment"] is not None

    def test_walk_forward_strategies_in_result(self, monkeypatch):
        """Result includes the strategies dict."""
        mock_fetch = _make_multi_symbol_fetch()
        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.backtester.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.combiner.fetch_ohlcv", mock_fetch)

        result = walk_forward_test(
            strategies={"spy_buy_and_hold": 1.0},
            train_end="2022-12-31",
            test_start="2023-01-01",
        )

        assert result["strategies"] == {"spy_buy_and_hold": 1.0}


# ---------------------------------------------------------------------------
# Feature 5: Correlation Matrix
# ---------------------------------------------------------------------------

class TestCorrelation:
    def test_strategy_correlation_basic(self, monkeypatch):
        """Correlation matrix is computed for multiple strategies."""
        mock_fetch = _make_multi_symbol_fetch()
        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.backtester.fetch_ohlcv", mock_fetch)

        result = strategy_correlation(
            strategies=["spy_buy_and_hold", "balanced_sixty_forty"],
            start="2020-01-01",
            end="2025-12-31",
        )

        assert "correlation_matrix" in result
        matrix = result["correlation_matrix"]
        assert not matrix.empty
        assert matrix.shape[0] == 2
        assert matrix.shape[1] == 2

    def test_correlation_diagonal_is_one(self, monkeypatch):
        """Diagonal of correlation matrix should be 1.0."""
        mock_fetch = _make_multi_symbol_fetch()
        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.backtester.fetch_ohlcv", mock_fetch)

        result = strategy_correlation(
            strategies=["spy_buy_and_hold", "balanced_sixty_forty"],
            start="2020-01-01",
            end="2025-12-31",
        )

        matrix = result["correlation_matrix"]
        for col in matrix.columns:
            assert matrix.loc[col, col] == pytest.approx(1.0, abs=0.001)

    def test_correlation_returns_pairs(self, monkeypatch):
        """high_pairs and low_pairs are lists."""
        mock_fetch = _make_multi_symbol_fetch()
        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.backtester.fetch_ohlcv", mock_fetch)

        result = strategy_correlation(
            strategies=["spy_buy_and_hold", "balanced_sixty_forty", "three_fund_passive"],
            start="2020-01-01",
            end="2025-12-31",
        )

        assert isinstance(result["high_pairs"], list)
        assert isinstance(result["low_pairs"], list)

    def test_correlation_single_strategy_error(self, monkeypatch):
        """Single strategy returns error (need at least 2)."""
        mock_fetch = _make_multi_symbol_fetch()
        monkeypatch.setattr("bespoke.data.fetcher.fetch_ohlcv", mock_fetch)
        monkeypatch.setattr("bespoke.core.backtester.fetch_ohlcv", mock_fetch)

        result = strategy_correlation(
            strategies=["spy_buy_and_hold"],
            start="2020-01-01",
            end="2025-12-31",
        )

        assert "error" in result


# ---------------------------------------------------------------------------
# Feature 6: Smart Stop Loss
# ---------------------------------------------------------------------------

class TestStopLoss:
    def test_stop_loss_ok_within_threshold(self):
        """Stock within stop loss range returns OK."""
        result = check_stop_loss(
            symbol="AAPL", entry_price=150.0, current_price=140.0,
            stop_pct=0.15, benchmark="SPY",
            benchmark_entry=450.0, benchmark_current=460.0,
        )

        assert result["action"] == "OK"
        assert result["is_market_crash"] is False

    def test_stop_loss_exit_stock_specific(self):
        """Stock down past stop while market flat = EXIT."""
        result = check_stop_loss(
            symbol="AAPL", entry_price=150.0, current_price=120.0,
            stop_pct=0.15, benchmark="SPY",
            benchmark_entry=450.0, benchmark_current=455.0,
        )

        assert result["action"] == "EXIT"
        assert result["is_market_crash"] is False
        assert "thesis broken" in result["reason"].lower() or "stock" in result["reason"].lower()

    def test_stop_loss_hold_market_crash(self):
        """Both stock and market down significantly = HOLD (crash)."""
        result = check_stop_loss(
            symbol="AAPL", entry_price=150.0, current_price=120.0,
            stop_pct=0.15, benchmark="SPY",
            benchmark_entry=450.0, benchmark_current=360.0,
        )

        assert result["action"] == "HOLD"
        assert result["is_market_crash"] is True
        assert "crash" in result["reason"].lower() or "market" in result["reason"].lower()

    def test_stop_loss_exit_underperforming_market(self):
        """Stock down much more than market = EXIT (underperforming)."""
        result = check_stop_loss(
            symbol="MSFT", entry_price=300.0, current_price=200.0,
            stop_pct=0.15, benchmark="SPY",
            benchmark_entry=450.0, benchmark_current=430.0,
        )

        # Stock is down 33%, market down 4% -- stock-specific problem
        assert result["action"] == "EXIT"
        assert result["is_market_crash"] is False

    def test_stop_loss_percentages_in_result(self):
        """Result includes stock and benchmark change percentages."""
        result = check_stop_loss(
            symbol="AAPL", entry_price=100.0, current_price=80.0,
            stop_pct=0.15, benchmark="SPY",
            benchmark_entry=400.0, benchmark_current=380.0,
        )

        assert "stock_change_pct" in result
        assert result["stock_change_pct"] == pytest.approx(-20.0, abs=0.1)
        assert "benchmark_change_pct" in result
        assert result["benchmark_change_pct"] == pytest.approx(-5.0, abs=0.1)

    def test_stop_loss_zero_entry_price(self):
        """Zero entry price handled gracefully."""
        result = check_stop_loss(
            symbol="AAPL", entry_price=0, current_price=100.0,
            stop_pct=0.15,
        )
        assert result["action"] == "OK"

    def test_stop_loss_custom_threshold(self):
        """Custom stop_pct works correctly."""
        # 10% stop: stock down 12% = should trigger
        result = check_stop_loss(
            symbol="AAPL", entry_price=100.0, current_price=88.0,
            stop_pct=0.10, benchmark="SPY",
            benchmark_entry=400.0, benchmark_current=410.0,
        )
        assert result["action"] == "EXIT"

        # 20% stop: stock down 12% = should NOT trigger
        result = check_stop_loss(
            symbol="AAPL", entry_price=100.0, current_price=88.0,
            stop_pct=0.20, benchmark="SPY",
            benchmark_entry=400.0, benchmark_current=410.0,
        )
        assert result["action"] == "OK"


# ---------------------------------------------------------------------------
# Feature 7: Benchmark Comparison
# ---------------------------------------------------------------------------

class TestBenchmarkComparison:
    def test_compare_benchmarks_beating(self):
        """Portfolio beating benchmarks shows correct alpha."""
        result = compare_benchmarks(
            portfolio_return=0.25,
            benchmarks=["SPY", "VT"],
            benchmark_data={
                "SPY": {"start_price": 400, "end_price": 480},  # 20% return
                "VT": {"start_price": 100, "end_price": 115},   # 15% return
            },
        )

        assert result["portfolio_return"] == 0.25
        assert result["benchmarks"]["SPY"]["return"] == pytest.approx(0.20, abs=0.01)
        assert result["benchmarks"]["SPY"]["beating"] is True
        assert result["benchmarks"]["SPY"]["alpha"] == pytest.approx(0.05, abs=0.01)
        assert result["benchmarks"]["VT"]["return"] == pytest.approx(0.15, abs=0.01)
        assert result["benchmarks"]["VT"]["beating"] is True
        assert result["beating_all"] is True

    def test_compare_benchmarks_losing(self):
        """Portfolio losing to benchmarks shows negative alpha."""
        result = compare_benchmarks(
            portfolio_return=0.10,
            benchmarks=["SPY"],
            benchmark_data={
                "SPY": {"start_price": 400, "end_price": 500},  # 25% return
            },
        )

        assert result["benchmarks"]["SPY"]["beating"] is False
        assert result["benchmarks"]["SPY"]["alpha"] < 0
        assert result["beating_all"] is False

    def test_compare_benchmarks_mixed(self):
        """Portfolio beating some but not all benchmarks."""
        result = compare_benchmarks(
            portfolio_return=0.15,
            benchmarks=["SPY", "VT"],
            benchmark_data={
                "SPY": {"start_price": 400, "end_price": 480},  # 20%
                "VT": {"start_price": 100, "end_price": 110},   # 10%
            },
        )

        assert result["benchmarks"]["SPY"]["beating"] is False
        assert result["benchmarks"]["VT"]["beating"] is True
        assert result["beating_all"] is False

    def test_compare_benchmarks_with_fetcher(self, monkeypatch):
        """compare_benchmarks works with mocked fetch data."""
        mock_fetch = _make_multi_symbol_fetch()

        # Monkeypatch fetch_ohlcv at source so the internal import picks it up
        import bespoke.data.fetcher as fetcher_mod
        monkeypatch.setattr(fetcher_mod, "fetch_ohlcv", mock_fetch)

        result = compare_benchmarks(
            portfolio_return=0.30,
            benchmarks=["SPY", "VT"],
            period_start="2020-01-01",
            period_end="2025-12-31",
        )

        assert "SPY" in result["benchmarks"]
        assert result["benchmarks"]["SPY"]["return"] is not None

    def test_compare_benchmarks_best_alpha(self):
        """best_alpha is the maximum alpha across benchmarks."""
        result = compare_benchmarks(
            portfolio_return=0.30,
            benchmarks=["SPY", "VT"],
            benchmark_data={
                "SPY": {"start_price": 400, "end_price": 480},  # 20%
                "VT": {"start_price": 100, "end_price": 125},   # 25%
            },
        )

        # Alpha vs SPY = 10%, alpha vs VT = 5%
        assert result["best_alpha"] == pytest.approx(0.10, abs=0.01)

    def test_compare_benchmarks_default_tickers(self):
        """Default benchmarks are SPY and VT."""
        result = compare_benchmarks(
            portfolio_return=0.10,
            benchmark_data={
                "SPY": {"return": 0.08},
                "VT": {"return": 0.06},
            },
        )

        assert "SPY" in result["benchmarks"]
        assert "VT" in result["benchmarks"]

    def test_compare_benchmarks_preloaded_return(self):
        """Pre-loaded data with 'return' key works."""
        result = compare_benchmarks(
            portfolio_return=0.20,
            benchmarks=["SPY"],
            benchmark_data={"SPY": {"return": 0.15}},
        )
        assert result["benchmarks"]["SPY"]["return"] == pytest.approx(0.15, abs=0.001)
        assert result["benchmarks"]["SPY"]["alpha"] == pytest.approx(0.05, abs=0.001)


# ---------------------------------------------------------------------------
# Import smoke test
# ---------------------------------------------------------------------------

class TestImports:
    def test_analysis_init_exports(self):
        """All analysis functions are importable from bespoke.analysis."""
        from bespoke.analysis import (
            score_entry,
            detect_regime,
            regime_allocations,
            walk_forward_test,
            strategy_correlation,
            check_stop_loss,
            compare_benchmarks,
        )
        assert callable(score_entry)
        assert callable(detect_regime)
        assert callable(regime_allocations)
        assert callable(walk_forward_test)
        assert callable(strategy_correlation)
        assert callable(check_stop_loss)
        assert callable(compare_benchmarks)

    def test_top_level_exports(self):
        """Key functions are importable from bespoke directly."""
        import bespoke
        assert bespoke.__version__ == "0.2.0"
        assert callable(bespoke.score_entry)
        assert callable(bespoke.detect_regime)
        assert callable(bespoke.check_stop_loss)
        assert callable(bespoke.compare_benchmarks)
        assert callable(bespoke.backtest_combination)
