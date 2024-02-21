"""Signal 1: Volatility Regime — realized vol trend as stress indicator."""

from ..models import MarketSnapshot, SignalResult, SignalBias


class VolatilityRegimeSignal:
    """
    High score = low/stable volatility = calm regime.
    Low score = elevated/rising volatility = stressed regime.

    Uses realized vol vs 30d baseline and vol-of-vol (vol trend).
    """

    name = "volatility_regime"

    def compute(self, snap: MarketSnapshot) -> SignalResult:
        vol_1d  = snap.realized_vol_1d
        vol_7d  = snap.realized_vol_7d
        vol_30d = snap.realized_vol_30d   # baseline

        score = 50.0

        # Current vol vs 30d baseline
        if vol_30d > 0:
            ratio_1d = vol_1d / vol_30d
            if ratio_1d < 0.5:
                score += 25    # Very calm vs baseline
            elif ratio_1d < 0.8:
                score += 15
            elif ratio_1d < 1.1:
                score += 5
            elif ratio_1d < 1.5:
                score -= 10
            elif ratio_1d < 2.5:
                score -= 20
            else:
                score -= 30    # Extreme vol spike

        # Vol trend: is vol rising or falling?
        if vol_7d > 0 and vol_30d > 0:
            vol_trend = (vol_1d - vol_7d) / vol_7d
            if vol_trend < -0.20:
                score += 10   # Vol collapsing = regime calming
            elif vol_trend < -0.05:
                score += 5
            elif vol_trend > 0.30:
                score -= 10   # Vol surging = stress building
            elif vol_trend > 0.10:
                score -= 5

        # Absolute vol level penalty
        if vol_1d > 150:
            score -= 15
        elif vol_1d > 100:
            score -= 8
        elif vol_1d < 30:
            score += 8
        elif vol_1d < 50:
            score += 4

        score = max(0.0, min(100.0, score))
        bias = SignalBias.CALM if score > 55 else SignalBias.STRESS if score < 45 else SignalBias.NEUTRAL
        strength = round(abs(score - 50) / 50, 3)

        ratio_display = f"{vol_1d / vol_30d:.2f}x" if vol_30d > 0 else "N/A"
        detail = (
            f"Vol 1d: {vol_1d:.1f}% ann, "
            f"7d: {vol_7d:.1f}%, 30d: {vol_30d:.1f}% "
            f"(ratio {ratio_display})"
        )

        return SignalResult(
            signal_name=self.name,
            score=round(score, 2),
            bias=bias,
            strength=strength,
            detail=detail,
        )
