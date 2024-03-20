"""Tests for CorrelationBreakSignal."""

from zenflux.signals.correlation_break import CorrelationBreakSignal
from zenflux.models import SignalBias
from tests.conftest import make_snap

sig = CorrelationBreakSignal()


class TestCorrelationBreakBasics:
    def test_name(self):
        assert sig.name == "correlation_break"

    def test_score_clamped(self):
        r = sig.compute(make_snap(correlation_7d=-1.0, correlation_30d=1.0))
        assert 0 <= r.score <= 100

    def test_detail_contains_corr(self):
        r = sig.compute(make_snap())
        assert "Corr" in r.detail or "corr" in r.detail.lower()


class TestCorrelationBreakLogic:
    def test_stable_high_correlation_calm(self):
        snap = make_snap(correlation_7d=0.88, correlation_30d=0.86)
        r = sig.compute(snap)
        assert r.bias == SignalBias.CALM
        assert r.score > 60

    def test_large_corr_break_stress(self):
        snap = make_snap(correlation_7d=0.15, correlation_30d=0.82)
        r = sig.compute(snap)
        assert r.bias == SignalBias.STRESS
        assert r.score < 40

    def test_sign_flip_extreme_stress(self):
        """Correlation flipping sign = regime breakdown."""
        snap = make_snap(correlation_7d=-0.40, correlation_30d=0.80)
        r = sig.compute(snap)
        assert r.score < 30

    def test_stable_corr_bonus(self):
        stable   = sig.compute(make_snap(correlation_7d=0.80, correlation_30d=0.80))
        shifting = sig.compute(make_snap(correlation_7d=0.50, correlation_30d=0.80))
        assert stable.score > shifting.score

    def test_near_zero_corr_penalty(self):
        zero_corr = sig.compute(make_snap(correlation_7d=0.05, correlation_30d=0.75))
        high_corr = sig.compute(make_snap(correlation_7d=0.85, correlation_30d=0.80))
        assert high_corr.score > zero_corr.score

    def test_detail_shows_stable_or_breaking(self):
        stable  = sig.compute(make_snap(correlation_7d=0.82, correlation_30d=0.80))
        breaking = sig.compute(make_snap(correlation_7d=0.20, correlation_30d=0.80))
        assert "stable" in stable.detail
        assert "breaking" in breaking.detail

    def test_negative_corr_but_stable_is_calm(self):
        """Stable negative correlation is predictable = calm."""
        snap = make_snap(correlation_7d=-0.80, correlation_30d=-0.78)
        r = sig.compute(snap)
        assert r.score > 55
