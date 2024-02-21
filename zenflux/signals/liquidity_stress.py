"""Signal 2: Liquidity Stress — bid-ask spread and orderbook depth as stress proxy."""

from ..models import MarketSnapshot, SignalResult, SignalBias


class LiquidityStressSignal:
    """
    Wide spreads + thin orderbooks = stressed, illiquid market.
    Tight spreads + deep books = calm, healthy market.
    """

    name = "liquidity_stress"

    def compute(self, snap: MarketSnapshot) -> SignalResult:
        spread_now = snap.bid_ask_spread_pct
        spread_avg = snap.bid_ask_spread_7d_avg
        depth_now  = snap.orderbook_depth_usd
        depth_avg  = snap.orderbook_depth_7d_avg

        score = 50.0

        # Spread vs baseline (wider = more stress = lower score)
        if spread_avg > 0:
            spread_ratio = spread_now / spread_avg
            if spread_ratio < 0.7:
                score += 20   # Spreads tightening = calm
            elif spread_ratio < 0.9:
                score += 10
            elif spread_ratio < 1.1:
                score += 2
            elif spread_ratio < 1.5:
                score -= 12
            elif spread_ratio < 2.5:
                score -= 22
            else:
                score -= 30   # Spread blown out

        # Absolute spread level
        if spread_now < 0.05:
            score += 8    # Very tight = calm
        elif spread_now < 0.1:
            score += 4
        elif spread_now > 0.5:
            score -= 12
        elif spread_now > 0.3:
            score -= 6

        # Orderbook depth vs baseline (thinner = more stress)
        if depth_avg > 0:
            depth_ratio = depth_now / depth_avg
            if depth_ratio > 1.3:
                score += 10   # Deeper than avg = calm
            elif depth_ratio > 1.0:
                score += 4
            elif depth_ratio < 0.5:
                score -= 15   # Book drained = stress
            elif depth_ratio < 0.7:
                score -= 8
            elif depth_ratio < 0.9:
                score -= 3

        score = max(0.0, min(100.0, score))
        bias = SignalBias.CALM if score > 55 else SignalBias.STRESS if score < 45 else SignalBias.NEUTRAL
        strength = round(abs(score - 50) / 50, 3)

        spread_ratio_disp = f"{spread_now / spread_avg:.2f}x" if spread_avg > 0 else "N/A"
        detail = (
            f"Spread: {spread_now:.3f}% ({spread_ratio_disp} avg), "
            f"Depth: ${depth_now/1e6:.1f}M"
        )

        return SignalResult(
            signal_name=self.name,
            score=round(score, 2),
            bias=bias,
            strength=strength,
            detail=detail,
        )
