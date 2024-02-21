"""ZenFlux signal modules."""

from .volatility_regime import VolatilityRegimeSignal
from .liquidity_stress import LiquidityStressSignal
from .price_dislocation import PriceDislocationSignal
from .flow_imbalance import FlowImbalanceSignal
from .correlation_break import CorrelationBreakSignal

ALL_SIGNALS = [
    VolatilityRegimeSignal(),
    LiquidityStressSignal(),
    PriceDislocationSignal(),
    FlowImbalanceSignal(),
    CorrelationBreakSignal(),
]

__all__ = [
    "VolatilityRegimeSignal",
    "LiquidityStressSignal",
    "PriceDislocationSignal",
    "FlowImbalanceSignal",
    "CorrelationBreakSignal",
    "ALL_SIGNALS",
]
