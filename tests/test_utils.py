"""Tests for ZenFlux utility modules."""

import time
import pytest
from zenflux.utils.normalizer import (
    clamp, weighted_average, signal_alignment, stress_level, regime_change_risk,
)
from zenflux.utils.cache import MarketSnapshotCache
from tests.conftest import make_snap


class TestClamp:
    def test_in_range(self):      assert clamp(50.0) == 50.0
    def test_above_max(self):     assert clamp(150.0) == 100.0
    def test_below_min(self):     assert clamp(-10.0) == 0.0
    def test_boundaries(self):    assert clamp(0.0) == 0.0; assert clamp(100.0) == 100.0
    def test_custom_bounds(self):
        assert clamp(5.0, 10.0, 20.0) == 10.0
        assert clamp(25.0, 10.0, 20.0) == 20.0
        assert clamp(15.0, 10.0, 20.0) == 15.0


class TestWeightedAverage:
    def test_equal_weights(self):
        assert abs(weighted_average({"a": 60.0, "b": 40.0}, {"a": 0.5, "b": 0.5}) - 50.0) < 0.001

    def test_missing_signal_renormalizes(self):
        assert abs(weighted_average({"a": 80.0}, {"a": 0.5, "b": 0.5}) - 80.0) < 0.001

    def test_empty_returns_50(self):
        assert weighted_average({}, {"a": 1.0}) == 50.0

    def test_all_neutral_returns_50(self):
        from zenflux.engine import WEIGHTS
        assert abs(weighted_average({k: 50.0 for k in WEIGHTS}, WEIGHTS) - 50.0) < 0.001

    def test_clamped(self):
        assert weighted_average({"a": 200.0}, {"a": 1.0}) <= 100.0


class TestSignalAlignment:
    def test_all_calm_is_one(self):
        assert signal_alignment({"a": 70.0, "b": 75.0, "c": 65.0}) == 1.0

    def test_all_stress_is_one(self):
        assert signal_alignment({"a": 20.0, "b": 25.0, "c": 15.0}) == 1.0

    def test_split_is_half(self):
        assert signal_alignment({"a": 70.0, "b": 70.0, "c": 25.0, "d": 25.0}) == 0.5

    def test_all_neutral_is_zero(self):
        assert signal_alignment({"a": 50.0, "b": 50.0}) == 0.0

    def test_empty_returns_zero(self):
        assert signal_alignment({}) == 0.0


class TestStressLevel:
    def test_zen_100_stress_0(self):
        assert stress_level(100.0) == 0.0

    def test_zen_0_stress_1(self):
        assert stress_level(0.0) == 1.0

    def test_zen_50_stress_half(self):
        assert abs(stress_level(50.0) - 0.5) < 0.001

    def test_returns_float(self):
        assert isinstance(stress_level(60.0), float)


class TestRegimeChangeRisk:
    def test_returns_float_in_range(self):
        scores = {k: 50.0 for k in ["volatility_regime", "liquidity_stress", "price_dislocation", "flow_imbalance", "correlation_break"]}
        r = regime_change_risk(scores, 50.0)
        assert 0 <= r <= 100

    def test_near_boundary_higher_risk(self):
        scores = {k: 50.0 for k in ["a", "b"]}
        near   = regime_change_risk(scores, 50.0)   # at boundary
        far    = regime_change_risk(scores, 70.0)   # away from boundary
        assert near > far

    def test_diverging_signals_higher_risk(self):
        converged = regime_change_risk({"a": 60.0, "b": 60.0}, 60.0)
        diverged  = regime_change_risk({"a": 90.0, "b": 20.0}, 60.0)
        assert diverged > converged

    def test_empty_scores_returns_50(self):
        assert regime_change_risk({}, 50.0) == 50.0


class TestMarketSnapshotCache:
    def test_set_and_get(self):
        cache = MarketSnapshotCache(ttl_seconds=60)
        snap = make_snap()
        cache.set(snap)
        assert cache.get("BTC") is snap

    def test_miss_returns_none(self):
        assert MarketSnapshotCache().get("MISSING") is None

    def test_expired_returns_none(self):
        cache = MarketSnapshotCache(ttl_seconds=0.01)
        cache.set(make_snap())
        time.sleep(0.05)
        assert cache.get("BTC") is None

    def test_invalidate(self):
        cache = MarketSnapshotCache()
        cache.set(make_snap())
        cache.invalidate("BTC")
        assert cache.get("BTC") is None

    def test_clear(self):
        cache = MarketSnapshotCache()
        cache.set(make_snap(symbol="A"))
        cache.set(make_snap(symbol="B"))
        cache.clear()
        assert cache.size() == 0

    def test_size(self):
        cache = MarketSnapshotCache()
        cache.set(make_snap(symbol="A"))
        cache.set(make_snap(symbol="B"))
        assert cache.size() == 2

    def test_valid_symbols(self):
        cache = MarketSnapshotCache(ttl_seconds=60)
        cache.set(make_snap(symbol="BTC"))
        cache.set(make_snap(symbol="ETH"))
        syms = cache.valid_symbols()
        assert "BTC" in syms and "ETH" in syms

    def test_overwrite_refreshes(self):
        cache = MarketSnapshotCache()
        cache.set(make_snap(price=40_000.0))
        cache.set(make_snap(price=50_000.0))
        assert cache.get("BTC").price == 50_000.0
