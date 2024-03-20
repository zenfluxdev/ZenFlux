"""Tests for FlowImbalanceSignal."""

from zenflux.signals.flow_imbalance import FlowImbalanceSignal
from zenflux.models import SignalBias
from tests.conftest import make_snap

sig = FlowImbalanceSignal()


class TestFlowImbalanceBasics:
    def test_name(self):
        assert sig.name == "flow_imbalance"

    def test_score_clamped(self):
        snap = make_snap(buy_volume_1h=0.0, sell_volume_1h=100_000_000.0)
        r = sig.compute(snap)
        assert 0 <= r.score <= 100

    def test_detail_contains_imbalance(self):
        r = sig.compute(make_snap())
        assert "%" in r.detail or "M" in r.detail


class TestFlowImbalanceLogic:
    def test_balanced_flow_calm(self):
        snap = make_snap(buy_volume_1h=5_000_000.0, sell_volume_1h=5_100_000.0)
        r = sig.compute(snap)
        assert r.bias == SignalBias.CALM
        assert r.score > 55

    def test_extreme_sell_imbalance_stress(self):
        snap = make_snap(buy_volume_1h=1_000_000.0, sell_volume_1h=9_000_000.0)
        r = sig.compute(snap)
        assert r.bias == SignalBias.STRESS
        assert r.score < 45

    def test_extreme_buy_imbalance_stress(self):
        """Buy-side extreme is also stress — one-sided market."""
        snap = make_snap(buy_volume_1h=9_000_000.0, sell_volume_1h=1_000_000.0)
        r = sig.compute(snap)
        assert r.score < 45

    def test_balanced_24h_adds_calm_bonus(self):
        balanced_24h = sig.compute(make_snap(
            buy_volume_1h=5_000_000.0, sell_volume_1h=5_100_000.0,
            buy_volume_24h=120_000_000.0, sell_volume_24h=120_000_000.0,
        ))
        imbalanced_24h = sig.compute(make_snap(
            buy_volume_1h=5_000_000.0, sell_volume_1h=5_100_000.0,
            buy_volume_24h=60_000_000.0, sell_volume_24h=180_000_000.0,
        ))
        assert balanced_24h.score > imbalanced_24h.score

    def test_sudden_flow_reversal_penalty(self):
        """1h flow opposite to 24h trend = uncertainty."""
        reversal = sig.compute(make_snap(
            buy_volume_1h=1_000_000.0, sell_volume_1h=9_000_000.0,
            buy_volume_24h=150_000_000.0, sell_volume_24h=90_000_000.0,
        ))
        consistent = sig.compute(make_snap(
            buy_volume_1h=1_000_000.0, sell_volume_1h=9_000_000.0,
            buy_volume_24h=60_000_000.0, sell_volume_24h=180_000_000.0,
        ))
        # Both stressed (extreme 1h sell pressure), but reversal shifts 24h differently
        assert reversal.score < 30 and consistent.score < 30

    def test_zero_volume_no_crash(self):
        snap = make_snap(buy_volume_1h=0.0, sell_volume_1h=0.0)
        r = sig.compute(snap)
        assert 0 <= r.score <= 100

    def test_strength_proportional(self):
        balanced = sig.compute(make_snap(buy_volume_1h=5e6, sell_volume_1h=5e6))
        extreme  = sig.compute(make_snap(buy_volume_1h=1e6, sell_volume_1h=9e6))
        assert extreme.strength > balanced.strength
