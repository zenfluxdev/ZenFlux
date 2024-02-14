"""
ZenFlux — Market Stress Regime Engine.

Five microstructure signals → one zen_index → five market states.
"""

from .engine import ZenEngine, WEIGHTS
from .models import MarketSnapshot, ZenAnalysis, ZenState, SignalBias, SignalResult
from .signals import (
    VolatilityRegimeSignal, LiquidityStressSignal, PriceDislocationSignal,
    FlowImbalanceSignal, CorrelationBreakSignal, ALL_SIGNALS,
)

__version__ = "0.1.0"
__all__ = [
    "ZenEngine", "WEIGHTS",
    "MarketSnapshot", "ZenAnalysis", "ZenState", "SignalBias", "SignalResult",
    "VolatilityRegimeSignal", "LiquidityStressSignal", "PriceDislocationSignal",
    "FlowImbalanceSignal", "CorrelationBreakSignal", "ALL_SIGNALS",
]
