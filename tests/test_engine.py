"""Tests for ZenEngine."""

import pytest
from zenflux.engine import ZenEngine, WEIGHTS, _state_from_index, _bias_from_index, _conviction
from zenflux.models import ZenState, SignalBias
from tests.conftest import make_snap


class TestEngineWeights:
    def test_weights_sum_to_one(self):
        assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9

    def test_five_signals_weighted(self):
        expected = {"volatility_regime", "liquidity_stress", "price_dislocation", "flow_imbalance", "correlation_break"}
        assert set(WEIGHTS.keys()) == expected

    def test_volatility_highest_weight(self):
        assert WEIGHTS["volatility_regime"] == max(WEIGHTS.values())


class TestStateMappings:
    def test_serene_at_80(self):
        assert _state_from_index(80.0) == ZenState.SERENE
        assert _state_from_index(100.0) == ZenState.SERENE

    def test_calm_band(self):
        assert _state_from_index(60.0) == ZenState.CALM
        assert _state_from_index(79.9) == ZenState.CALM

    def test_flux_band(self):
        assert _state_from_index(40.0) == ZenState.FLUX
        assert _state_from_index(59.9) == ZenState.FLUX

    def test_turbulent_band(self):
        assert _state_from_index(20.0) == ZenState.TURBULENT
        assert _state_from_index(39.9) == ZenState.TURBULENT

    def test_chaotic_band(self):
        assert _state_from_index(0.0) == ZenState.CHAOTIC
        assert _state_from_index(19.9) == ZenState.CHAOTIC


class TestBiasMapping:
    def test_above_55_is_calm(self):
        assert _bias_from_index(60.0) == SignalBias.CALM

    def test_below_45_is_stress(self):
        assert _bias_from_index(40.0) == SignalBias.STRESS

    def test_between_45_55_neutral(self):
        assert _bias_from_index(50.0) == SignalBias.NEUTRAL


class TestConviction:
    def test_zero_at_neutral(self):
        assert _conviction(50.0) == 0.0

    def test_max_at_extremes(self):
        assert _conviction(100.0) == 1.0
        assert _conviction(0.0) == 1.0

    def test_half_at_75(self):
        assert abs(_conviction(75.0) - 0.5) < 0.001


class TestZenEngineAnalyze:
    def test_returns_analysis(self):
        a = ZenEngine().analyze(make_snap())
        assert a.symbol == "BTC"

    def test_zen_index_in_range(self):
        assert 0 <= ZenEngine().analyze(make_snap()).zen_index <= 100

    def test_five_scores_populated(self):
        a = ZenEngine().analyze(make_snap())
        for score in [a.volatility_regime_score, a.liquidity_stress_score,
                      a.price_dislocation_score, a.flow_imbalance_score, a.correlation_break_score]:
            assert 0 <= score <= 100

    def test_calm_snap_calm_result(self, calm_snap):
        a = ZenEngine().analyze(calm_snap)
        assert a.zen_index > 55

    def test_stress_snap_stress_result(self, stress_snap):
        a = ZenEngine().analyze(stress_snap)
        assert a.zen_index < 50

    def test_state_matches_index(self):
        a = ZenEngine().analyze(make_snap())
        assert a.zen_state == _state_from_index(a.zen_index)

    def test_stress_level_inverse_of_index(self):
        a = ZenEngine().analyze(make_snap())
        assert abs(a.stress_level - (100 - a.zen_index) / 100) < 0.001

    def test_dominant_signal_valid(self):
        a = ZenEngine().analyze(make_snap())
        valid = {"volatility_regime", "liquidity_stress", "price_dislocation", "flow_imbalance", "correlation_break", "none"}
        assert a.dominant_signal in valid

    def test_calm_stress_lists(self):
        a = ZenEngine().analyze(make_snap())
        assert isinstance(a.calm_signals, list)
        assert isinstance(a.stress_signals, list)

    def test_conviction_in_range(self):
        assert 0 <= ZenEngine().analyze(make_snap()).conviction <= 1

    def test_alignment_in_range(self):
        assert 0 <= ZenEngine().analyze(make_snap()).signal_alignment <= 1

    def test_regime_change_risk_in_range(self):
        assert 0 <= ZenEngine().analyze(make_snap()).regime_change_risk <= 100

    def test_reasoning_non_empty(self):
        a = ZenEngine().analyze(make_snap())
        assert isinstance(a.reasoning, str) and len(a.reasoning) > 10

    def test_alert_flags_is_list(self):
        assert isinstance(ZenEngine().analyze(make_snap()).alert_flags, list)

    def test_custom_weights_accepted(self):
        w = {"volatility_regime": 0.4, "liquidity_stress": 0.2,
             "price_dislocation": 0.2, "flow_imbalance": 0.1, "correlation_break": 0.1}
        a = ZenEngine(weights=w).analyze(make_snap())
        assert 0 <= a.zen_index <= 100

    def test_extreme_stress_triggers_flags(self, stress_snap):
        a = ZenEngine().analyze(stress_snap)
        assert len(a.alert_flags) > 0
