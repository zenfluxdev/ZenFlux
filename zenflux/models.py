"""Core data models for ZenFlux."""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class ZenState(str, Enum):
    CHAOTIC   = "chaotic"    # 0-19:  Extreme stress, regime breakdown
    TURBULENT = "turbulent"  # 20-39: Elevated stress, avoid
    FLUX      = "flux"       # 40-59: Transitioning, uncertain
    CALM      = "calm"       # 60-79: Stable regime, favorable
    SERENE    = "serene"     # 80-100: Optimal, low stress


class SignalBias(str, Enum):
    CALM    = "calm"
    STRESS  = "stress"
    NEUTRAL = "neutral"


@dataclass
class MarketSnapshot:
    """Point-in-time market microstructure data."""
    symbol: str
    timestamp: float

    # Realized volatility
    realized_vol_1d: float        # 1-day realized vol (% annualized)
    realized_vol_7d: float        # 7-day realized vol
    realized_vol_30d: float       # 30-day realized vol (baseline)

    # Liquidity / spread
    bid_ask_spread_pct: float     # Current bid-ask spread %
    bid_ask_spread_7d_avg: float  # 7-day average spread %
    orderbook_depth_usd: float    # Total orderbook depth (USD)
    orderbook_depth_7d_avg: float # 7d average depth

    # Price dislocation
    price: float
    ma_7d: float                  # 7-day moving average
    ma_30d: float                 # 30-day moving average
    price_high_30d: float         # 30-day high
    price_low_30d: float          # 30-day low

    # Flow imbalance (buy vs sell pressure)
    buy_volume_1h: float
    sell_volume_1h: float
    buy_volume_24h: float
    sell_volume_24h: float

    # Cross-asset correlation (vs BTC)
    correlation_7d: float         # -1 to 1
    correlation_30d: float        # -1 to 1 (baseline)

    metadata: dict = field(default_factory=dict)


@dataclass
class SignalResult:
    """Result from a single ZenFlux signal."""
    signal_name: str
    score: float       # 0-100 (50=neutral, >55=calm, <45=stress)
    bias: SignalBias
    strength: float    # 0-1
    detail: str


@dataclass
class ZenAnalysis:
    """Full ZenFlux market regime analysis output."""
    symbol: str

    # 5 signal scores
    volatility_regime_score: float
    liquidity_stress_score: float
    price_dislocation_score: float
    flow_imbalance_score: float
    correlation_break_score: float

    # Aggregated
    zen_index: float              # 0-100 composite
    zen_state: ZenState
    stress_level: float           # 0-1 (inverse of zen_index)
    regime_change_risk: float     # 0-100: probability of imminent regime shift

    # Breakdown
    dominant_signal: str
    calm_signals: list[str]
    stress_signals: list[str]
    alert_flags: list[str]

    # Action
    bias: SignalBias
    conviction: float
    signal_alignment: float
    reasoning: str
