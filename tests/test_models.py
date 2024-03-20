"""Tests for ZenFlux core models."""

from zenflux.models import MarketSnapshot, ZenAnalysis, ZenState, SignalBias, SignalResult
from tests.conftest import make_snap


class TestZenState:
    def test_five_states(self):
        assert len(list(ZenState)) == 5

    def test_state_values(self):
        assert ZenState.CHAOTIC   == "chaotic"
        assert ZenState.TURBULENT == "turbulent"
        assert ZenState.FLUX      == "flux"
        assert ZenState.CALM      == "calm"
        assert ZenState.SERENE    == "serene"

    def test_is_string_enum(self):
        assert isinstance(ZenState.CALM, str)


class TestSignalBias:
    def test_three_biases(self):
        assert len(list(SignalBias)) == 3

    def test_values(self):
        assert SignalBias.CALM   == "calm"
        assert SignalBias.STRESS == "stress"
        assert SignalBias.NEUTRAL == "neutral"


class TestMarketSnapshot:
    def test_create_basic(self):
        snap = make_snap()
        assert snap.symbol == "BTC"
        assert snap.price == 42_000.0

    def test_default_metadata_empty(self):
        assert make_snap().metadata == {}

    def test_all_fields_present(self):
        snap = make_snap()
        for field in ["realized_vol_1d", "bid_ask_spread_pct", "orderbook_depth_usd",
                      "price", "ma_7d", "ma_30d", "buy_volume_1h", "sell_volume_1h",
                      "correlation_7d", "correlation_30d"]:
            assert hasattr(snap, field)

    def test_metadata_mutable(self):
        snap = make_snap()
        snap.metadata["exchange"] = "binance"
        assert snap.metadata["exchange"] == "binance"

    def test_zero_vol_allowed(self):
        snap = make_snap(realized_vol_1d=0.0)
        assert snap.realized_vol_1d == 0.0


class TestSignalResult:
    def test_create(self):
        r = SignalResult("volatility_regime", 72.0, SignalBias.CALM, 0.44, "test")
        assert r.signal_name == "volatility_regime"
        assert r.score == 72.0
