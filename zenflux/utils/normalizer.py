"""Normalizer utilities for ZenFlux."""

from typing import Dict


def clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def weighted_average(scores: Dict[str, float], weights: Dict[str, float]) -> float:
    total_w, total_s = 0.0, 0.0
    for name, score in scores.items():
        w = weights.get(name, 0.0)
        if w > 0:
            total_s += score * w
            total_w += w
    return clamp(total_s / total_w) if total_w > 0 else 50.0


def signal_alignment(scores: Dict[str, float], threshold: float = 5.0) -> float:
    if not scores:
        return 0.0
    calm   = sum(1 for s in scores.values() if s > 50 + threshold)
    stress = sum(1 for s in scores.values() if s < 50 - threshold)
    return round(max(calm, stress) / len(scores), 3)


def stress_level(zen_index: float) -> float:
    """Convert zen_index (0-100) to stress level (0-1). High zen = low stress."""
    return round((100 - zen_index) / 100, 3)


def regime_change_risk(scores: Dict[str, float], zen_index: float) -> float:
    """
    Estimate probability of imminent regime change (0-100).
    High when: zen_index near boundaries (25, 50, 75) AND signals diverging.
    """
    if not scores:
        return 50.0

    # Distance from nearest phase boundary
    boundaries = [25.0, 50.0, 75.0]
    dist = min(abs(zen_index - b) for b in boundaries)

    # Closer to boundary = higher transition risk
    boundary_risk = max(0, 30 - dist * 2)

    # Signal divergence = higher risk
    values = list(scores.values())
    avg = sum(values) / len(values)
    variance = sum((v - avg) ** 2 for v in values) / len(values)
    divergence_risk = min(40, variance ** 0.5 * 2)

    return round(clamp(boundary_risk + divergence_risk), 2)
