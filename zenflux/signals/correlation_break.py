"""Signal 5: Correlation Break — cross-asset correlation shift as regime change detector."""

from ..models import MarketSnapshot, SignalResult, SignalBias


class CorrelationBreakSignal:
    """
    Stable correlation to BTC = predictable regime = calm.
    Sudden correlation breakdown = regime flux = stress.
    De-correlation during market stress = contagion risk.
    """

    name = "correlation_break"

    def compute(self, snap: MarketSnapshot) -> SignalResult:
        corr_7d  = snap.correlation_7d   # recent
        corr_30d = snap.correlation_30d  # baseline

        score = 50.0

        # Absolute correlation level — high correlation = predictable = calmer
        if abs(corr_7d) > 0.85:
            score += 12   # Strongly correlated = regime stable
        elif abs(corr_7d) > 0.70:
            score += 6
        elif abs(corr_7d) > 0.50:
            score += 2
        elif abs(corr_7d) < 0.20:
            score -= 10   # Near-zero correlation = isolated/unstable
        elif abs(corr_7d) < 0.35:
            score -= 5

        # Correlation shift vs 30d baseline
        corr_shift = abs(corr_7d - corr_30d)
        if corr_shift < 0.05:
            score += 12   # Stable correlation = calm regime
        elif corr_shift < 0.10:
            score += 6
        elif corr_shift < 0.20:
            score -= 5
        elif corr_shift < 0.35:
            score -= 15
        else:
            score -= 25   # Large correlation break = regime change

        # Sign flip (positive → negative or vice versa) = extreme regime break
        if corr_7d * corr_30d < 0 and abs(corr_30d) > 0.3:
            score -= 15

        score = max(0.0, min(100.0, score))
        bias = SignalBias.CALM if score > 55 else SignalBias.STRESS if score < 45 else SignalBias.NEUTRAL
        strength = round(abs(score - 50) / 50, 3)

        detail = (
            f"Corr 7d: {corr_7d:+.2f}, "
            f"30d: {corr_30d:+.2f}, "
            f"shift: {corr_shift:+.2f} "
            f"({'stable' if corr_shift < 0.10 else 'breaking'})"
        )

        return SignalResult(
            signal_name=self.name,
            score=round(score, 2),
            bias=bias,
            strength=strength,
            detail=detail,
        )
