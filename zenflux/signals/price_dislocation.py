"""Signal 3: Price Dislocation — deviation from moving averages and 30d range."""

from ..models import MarketSnapshot, SignalResult, SignalBias


class PriceDislocationSignal:
    """
    Price far from moving averages = dislocated = stressed regime.
    Price near fair value (MAs) = calm, mean-reverting regime.
    Extreme range position (near 30d high/low) = stress.
    """

    name = "price_dislocation"

    def compute(self, snap: MarketSnapshot) -> SignalResult:
        price    = snap.price
        ma_7d    = snap.ma_7d
        ma_30d   = snap.ma_30d
        high_30d = snap.price_high_30d
        low_30d  = snap.price_low_30d

        score = 50.0

        # Deviation from 7d MA
        if ma_7d > 0:
            dev_7d = abs(price - ma_7d) / ma_7d * 100
            if dev_7d < 1.0:
                score += 20   # Very close to MA = calm
            elif dev_7d < 3.0:
                score += 10
            elif dev_7d < 6.0:
                score -= 5
            elif dev_7d < 12.0:
                score -= 15
            else:
                score -= 25   # Far from MA = dislocated

        # Deviation from 30d MA (longer-term displacement)
        if ma_30d > 0:
            dev_30d = abs(price - ma_30d) / ma_30d * 100
            if dev_30d < 3.0:
                score += 8
            elif dev_30d < 8.0:
                score += 2
            elif dev_30d > 20.0:
                score -= 12
            elif dev_30d > 12.0:
                score -= 6

        # 30d range position (0=low, 1=high)
        rng = high_30d - low_30d
        if rng > 0:
            position = (price - low_30d) / rng
            # Extreme positions = stressed (near high or low)
            if position > 0.90 or position < 0.10:
                score -= 15   # At extreme of range
            elif position > 0.80 or position < 0.20:
                score -= 7
            elif 0.40 <= position <= 0.60:
                score += 8    # Mid-range = stable

        score = max(0.0, min(100.0, score))
        bias = SignalBias.CALM if score > 55 else SignalBias.STRESS if score < 45 else SignalBias.NEUTRAL
        strength = round(abs(score - 50) / 50, 3)

        dev_7d_disp = abs(price - ma_7d) / ma_7d * 100 if ma_7d > 0 else 0
        detail = (
            f"Price: ${price:.2f}, "
            f"Dev 7d MA: {dev_7d_disp:+.1f}%, "
            f"30d range pos: {((price - low_30d) / (high_30d - low_30d) * 100):.0f}%"
            if (high_30d - low_30d) > 0
            else f"Price: ${price:.2f}, dev 7d MA: {dev_7d_disp:+.1f}%"
        )

        return SignalResult(
            signal_name=self.name,
            score=round(score, 2),
            bias=bias,
            strength=strength,
            detail=detail,
        )
