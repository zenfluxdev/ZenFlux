"""Tests for PriceDislocationSignal."""

from zenflux.signals.price_dislocation import PriceDislocationSignal
from zenflux.models import SignalBias
from tests.conftest import make_snap

sig = PriceDislocationSignal()


class TestPriceDislocationBasics:
    def test_name(self):
        assert sig.name == "price_dislocation"

    def test_score_clamped(self):
        snap = make_snap(price=100_000.0, ma_7d=40_000.0)
        r = sig.compute(snap)
        assert 0 <= r.score <= 100

    def test_detail_contains_price(self):
        r = sig.compute(make_snap())
        assert "$" in r.detail or "%" in r.detail


class TestPriceDislocationLogic:
    def test_price_near_ma_calm(self):
        snap = make_snap(price=42_000.0, ma_7d=42_100.0, ma_30d=41_800.0)
        r = sig.compute(snap)
        assert r.bias == SignalBias.CALM
        assert r.score > 55

    def test_price_far_from_ma_stress(self):
        snap = make_snap(price=50_000.0, ma_7d=42_000.0, ma_30d=40_000.0)
        r = sig.compute(snap)
        assert r.bias == SignalBias.STRESS
        assert r.score < 45

    def test_mid_range_position_bonus(self):
        mid  = sig.compute(make_snap(price=42_000.0, price_high_30d=48_000.0, price_low_30d=36_000.0))
        extreme = sig.compute(make_snap(price=47_500.0, price_high_30d=48_000.0, price_low_30d=36_000.0))
        assert mid.score > extreme.score

    def test_price_at_30d_high_stress(self):
        snap = make_snap(
            price=47_800.0, ma_7d=44_000.0,
            price_high_30d=48_000.0, price_low_30d=36_000.0,
        )
        r = sig.compute(snap)
        assert r.score < 50

    def test_price_at_30d_low_stress(self):
        snap = make_snap(
            price=36_300.0, ma_7d=44_000.0,
            price_high_30d=48_000.0, price_low_30d=36_000.0,
        )
        r = sig.compute(snap)
        assert r.score < 40

    def test_zero_ma_no_crash(self):
        snap = make_snap(ma_7d=0.0, ma_30d=0.0)
        r = sig.compute(snap)
        assert 0 <= r.score <= 100

    def test_flat_range_no_crash(self):
        snap = make_snap(price_high_30d=42_000.0, price_low_30d=42_000.0)
        r = sig.compute(snap)
        assert 0 <= r.score <= 100

    def test_deviation_increases_stress(self):
        close = sig.compute(make_snap(price=42_100.0, ma_7d=42_000.0))
        far   = sig.compute(make_snap(price=47_000.0, ma_7d=42_000.0))
        assert close.score > far.score
