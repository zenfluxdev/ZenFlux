"""Tests for LiquidityStressSignal."""

from zenflux.signals.liquidity_stress import LiquidityStressSignal
from zenflux.models import SignalBias
from tests.conftest import make_snap

sig = LiquidityStressSignal()


class TestLiquidityStressBasics:
    def test_name(self):
        assert sig.name == "liquidity_stress"

    def test_score_clamped(self):
        r = sig.compute(make_snap(bid_ask_spread_pct=5.0, orderbook_depth_usd=0.0))
        assert 0 <= r.score <= 100

    def test_detail_contains_spread(self):
        r = sig.compute(make_snap())
        assert "%" in r.detail or "Spread" in r.detail


class TestLiquidityStressLogic:
    def test_tight_spread_deep_book_calm(self):
        snap = make_snap(
            bid_ask_spread_pct=0.03, bid_ask_spread_7d_avg=0.08,
            orderbook_depth_usd=25_000_000.0, orderbook_depth_7d_avg=15_000_000.0,
        )
        r = sig.compute(snap)
        assert r.bias == SignalBias.CALM
        assert r.score > 60

    def test_wide_spread_thin_book_stress(self):
        snap = make_snap(
            bid_ask_spread_pct=0.50, bid_ask_spread_7d_avg=0.08,
            orderbook_depth_usd=3_000_000.0, orderbook_depth_7d_avg=15_000_000.0,
        )
        r = sig.compute(snap)
        assert r.bias == SignalBias.STRESS
        assert r.score < 40

    def test_spread_tightening_bullish(self):
        tighter = sig.compute(make_snap(bid_ask_spread_pct=0.04, bid_ask_spread_7d_avg=0.08))
        wider   = sig.compute(make_snap(bid_ask_spread_pct=0.15, bid_ask_spread_7d_avg=0.08))
        assert tighter.score > wider.score

    def test_depth_draining_stress(self):
        deep  = sig.compute(make_snap(orderbook_depth_usd=20_000_000.0, orderbook_depth_7d_avg=15_000_000.0))
        thin  = sig.compute(make_snap(orderbook_depth_usd=5_000_000.0,  orderbook_depth_7d_avg=15_000_000.0))
        assert deep.score > thin.score

    def test_zero_avg_no_crash(self):
        snap = make_snap(bid_ask_spread_7d_avg=0.0, orderbook_depth_7d_avg=0.0)
        r = sig.compute(snap)
        assert 0 <= r.score <= 100

    def test_absolute_very_tight_spread_bonus(self):
        tight  = sig.compute(make_snap(bid_ask_spread_pct=0.03))
        normal = sig.compute(make_snap(bid_ask_spread_pct=0.20))
        assert tight.score > normal.score

    def test_absolute_wide_spread_penalty(self):
        snap = make_snap(bid_ask_spread_pct=0.80, bid_ask_spread_7d_avg=0.08)
        r = sig.compute(snap)
        assert r.score < 30
