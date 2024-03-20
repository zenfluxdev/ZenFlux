"""Tests for VolatilityRegimeSignal."""

from zenflux.signals.volatility_regime import VolatilityRegimeSignal
from zenflux.models import SignalBias
from tests.conftest import make_snap

sig = VolatilityRegimeSignal()


class TestVolatilityBasics:
    def test_name(self):
        assert sig.name == "volatility_regime"

    def test_score_clamped(self):
        r = sig.compute(make_snap(realized_vol_1d=500.0))
        assert 0 <= r.score <= 100

    def test_strength_in_range(self):
        assert 0 <= sig.compute(make_snap()).strength <= 1

    def test_detail_contains_vol(self):
        r = sig.compute(make_snap())
        assert "%" in r.detail or "Vol" in r.detail


class TestVolatilityRegimeLogic:
    def test_low_vol_vs_baseline_calm(self):
        """Vol much lower than 30d baseline = calm regime."""
        snap = make_snap(realized_vol_1d=25.0, realized_vol_7d=30.0, realized_vol_30d=70.0)
        r = sig.compute(snap)
        assert r.bias == SignalBias.CALM
        assert r.score > 60

    def test_extreme_vol_spike_stress(self):
        """Vol 3x+ above baseline = stressed."""
        snap = make_snap(realized_vol_1d=210.0, realized_vol_7d=150.0, realized_vol_30d=70.0)
        r = sig.compute(snap)
        assert r.bias == SignalBias.STRESS
        assert r.score < 40

    def test_vol_in_line_with_baseline_neutral(self):
        snap = make_snap(realized_vol_1d=70.0, realized_vol_7d=68.0, realized_vol_30d=70.0)
        r = sig.compute(snap)
        assert r.bias == SignalBias.NEUTRAL

    def test_falling_vol_trend_adds_bonus(self):
        """Vol trending down = regime calming."""
        falling = sig.compute(make_snap(realized_vol_1d=40.0, realized_vol_7d=60.0, realized_vol_30d=70.0))
        rising  = sig.compute(make_snap(realized_vol_1d=90.0, realized_vol_7d=60.0, realized_vol_30d=70.0))
        assert falling.score > rising.score

    def test_absolute_low_vol_bonus(self):
        low_vol  = sig.compute(make_snap(realized_vol_1d=20.0, realized_vol_7d=22.0, realized_vol_30d=22.0))
        high_vol = sig.compute(make_snap(realized_vol_1d=80.0, realized_vol_7d=78.0, realized_vol_30d=80.0))
        assert low_vol.score > high_vol.score

    def test_extreme_vol_absolute_penalty(self):
        snap = make_snap(realized_vol_1d=200.0, realized_vol_7d=180.0, realized_vol_30d=70.0)
        r = sig.compute(snap)
        assert r.score < 30

    def test_zero_baseline_no_crash(self):
        snap = make_snap(realized_vol_30d=0.0)
        r = sig.compute(snap)
        assert 0 <= r.score <= 100
