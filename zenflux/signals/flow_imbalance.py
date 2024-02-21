"""Signal 4: Flow Imbalance — buy/sell pressure asymmetry as stress indicator."""

from ..models import MarketSnapshot, SignalResult, SignalBias


class FlowImbalanceSignal:
    """
    Extreme buy/sell imbalance = aggressive directional pressure = stress.
    Balanced flow = healthy two-sided market = calm.
    """

    name = "flow_imbalance"

    def compute(self, snap: MarketSnapshot) -> SignalResult:
        buy_1h  = snap.buy_volume_1h
        sell_1h = snap.sell_volume_1h
        buy_24h = snap.buy_volume_24h
        sell_24h = snap.sell_volume_24h

        score = 50.0

        # 1h imbalance
        total_1h = buy_1h + sell_1h
        if total_1h > 0:
            imbalance_1h = abs(buy_1h - sell_1h) / total_1h  # 0-1
            if imbalance_1h < 0.05:
                score += 15   # Very balanced
            elif imbalance_1h < 0.10:
                score += 8
            elif imbalance_1h < 0.20:
                score += 2
            elif imbalance_1h < 0.35:
                score -= 8
            elif imbalance_1h < 0.55:
                score -= 18
            else:
                score -= 28   # Extreme one-sided flow

        # 24h imbalance (persistent pressure = more stress)
        total_24h = buy_24h + sell_24h
        if total_24h > 0:
            imbalance_24h = abs(buy_24h - sell_24h) / total_24h
            if imbalance_24h < 0.05:
                score += 10
            elif imbalance_24h < 0.15:
                score += 4
            elif imbalance_24h > 0.40:
                score -= 12
            elif imbalance_24h > 0.25:
                score -= 6

        # 1h vs 24h divergence (sudden shift = stress)
        if total_1h > 0 and total_24h > 0:
            ratio_1h  = buy_1h / total_1h
            ratio_24h = buy_24h / total_24h
            shift = abs(ratio_1h - ratio_24h)
            if shift > 0.25:
                score -= 10   # Sudden flow reversal = uncertainty
            elif shift > 0.15:
                score -= 5

        score = max(0.0, min(100.0, score))
        bias = SignalBias.CALM if score > 55 else SignalBias.STRESS if score < 45 else SignalBias.NEUTRAL
        strength = round(abs(score - 50) / 50, 3)

        imb_1h_disp = abs(buy_1h - sell_1h) / (buy_1h + sell_1h) * 100 if (buy_1h + sell_1h) > 0 else 0
        detail = (
            f"1h imbalance: {imb_1h_disp:.1f}%, "
            f"Buy: ${buy_1h/1e6:.1f}M / Sell: ${sell_1h/1e6:.1f}M"
        )

        return SignalResult(
            signal_name=self.name,
            score=round(score, 2),
            bias=bias,
            strength=strength,
            detail=detail,
        )
