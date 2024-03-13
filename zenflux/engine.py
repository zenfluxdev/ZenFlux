"""ZenEngine — orchestrates 5 market stress signals into a composite regime analysis."""

from typing import Dict, List, Optional

from .models import MarketSnapshot, ZenAnalysis, ZenState, SignalBias, SignalResult
from .signals import ALL_SIGNALS
from .utils.normalizer import (
    weighted_average,
    signal_alignment as compute_alignment,
    stress_level as compute_stress,
    regime_change_risk as compute_regime_risk,
)

WEIGHTS: Dict[str, float] = {
    "volatility_regime": 0.30,
    "liquidity_stress":  0.25,
    "price_dislocation": 0.20,
    "flow_imbalance":    0.15,
    "correlation_break": 0.10,
}
# Total = 1.00 ✓


def _state_from_index(idx: float) -> ZenState:
    if idx >= 80:
        return ZenState.SERENE
    elif idx >= 60:
        return ZenState.CALM
    elif idx >= 40:
        return ZenState.FLUX
    elif idx >= 20:
        return ZenState.TURBULENT
    else:
        return ZenState.CHAOTIC


def _bias_from_index(idx: float) -> SignalBias:
    if idx > 55:
        return SignalBias.CALM
    elif idx < 45:
        return SignalBias.STRESS
    return SignalBias.NEUTRAL


def _conviction(idx: float) -> float:
    return round(abs(idx - 50) / 50, 3)


def _dominant_signal(results: List[SignalResult]) -> str:
    if not results:
        return "none"
    return max(results, key=lambda r: abs(r.score - 50)).signal_name


def _categorize(results: List[SignalResult]):
    calm   = [r.signal_name for r in results if r.bias == SignalBias.CALM]
    stress = [r.signal_name for r in results if r.bias == SignalBias.STRESS]
    return calm, stress


def _alert_flags(scores: Dict[str, float], alignment: float, zen_index: float) -> List[str]:
    flags = []
    if alignment < 0.5:
        flags.append("low_signal_alignment")
    if scores.get("volatility_regime", 50) < 30:
        flags.append("extreme_volatility_spike")
    if scores.get("liquidity_stress", 50) < 25:
        flags.append("liquidity_crisis_risk")
    if scores.get("correlation_break", 50) < 30:
        flags.append("correlation_breakdown")
    if zen_index < 20:
        flags.append("regime_chaotic_avoid")
    if scores.get("flow_imbalance", 50) < 25:
        flags.append("extreme_flow_asymmetry")
    return flags


def _build_reasoning(
    scores: Dict[str, float],
    zen_index: float,
    state: ZenState,
    calm_sigs: List[str],
    stress_sigs: List[str],
    stress: float,
) -> str:
    vol   = scores.get("volatility_regime", 50)
    liq   = scores.get("liquidity_stress", 50)
    flow  = scores.get("flow_imbalance", 50)
    corr  = scores.get("correlation_break", 50)

    parts = [
        f"Zen index {zen_index:.1f}/100 → {state.value}.",
        f"Regime: {len(calm_sigs)} calm, {len(stress_sigs)} stress signals.",
    ]

    if vol > 65:
        parts.append("Volatility compressed — low-stress regime confirmed.")
    elif vol < 35:
        parts.append("Volatility spiking — regime under significant stress.")

    if liq > 65:
        parts.append("Liquidity deep and spreads tight — healthy market microstructure.")
    elif liq < 35:
        parts.append("Spread widening and book thinning — liquidity stress elevated.")

    if flow > 65:
        parts.append("Balanced buy/sell flow — two-sided market active.")
    elif flow < 35:
        parts.append("Extreme flow imbalance — one-sided pressure detected.")

    if corr < 35:
        parts.append("Correlation breakdown — regime transition risk elevated.")

    parts.append(f"Stress level: {stress:.1%}.")

    return " ".join(parts)


class ZenEngine:
    """
    Orchestrates 5 market stress signals into a composite ZenAnalysis.

    Usage:
        engine = ZenEngine()
        analysis = engine.analyze(snap)
    """

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or WEIGHTS
        self.signals = ALL_SIGNALS

    def analyze(self, snap: MarketSnapshot) -> ZenAnalysis:
        results: List[SignalResult] = [sig.compute(snap) for sig in self.signals]
        scores: Dict[str, float]   = {r.signal_name: r.score for r in results}

        zen_index  = weighted_average(scores, self.weights)
        state      = _state_from_index(zen_index)
        bias       = _bias_from_index(zen_index)
        conviction = _conviction(zen_index)
        alignment  = compute_alignment(scores)
        stress     = compute_stress(zen_index)
        regime_risk = compute_regime_risk(scores, zen_index)

        dominant         = _dominant_signal(results)
        calm_sigs, stress_sigs = _categorize(results)
        flags            = _alert_flags(scores, alignment, zen_index)
        reasoning        = _build_reasoning(scores, zen_index, state, calm_sigs, stress_sigs, stress)

        return ZenAnalysis(
            symbol                   = snap.symbol,
            volatility_regime_score  = scores.get("volatility_regime", 50),
            liquidity_stress_score   = scores.get("liquidity_stress", 50),
            price_dislocation_score  = scores.get("price_dislocation", 50),
            flow_imbalance_score     = scores.get("flow_imbalance", 50),
            correlation_break_score  = scores.get("correlation_break", 50),
            zen_index                = round(zen_index, 2),
            zen_state                = state,
            stress_level             = stress,
            regime_change_risk       = regime_risk,
            dominant_signal          = dominant,
            calm_signals             = calm_sigs,
            stress_signals           = stress_sigs,
            alert_flags              = flags,
            bias                     = bias,
            conviction               = conviction,
            signal_alignment         = alignment,
            reasoning                = reasoning,
        )
