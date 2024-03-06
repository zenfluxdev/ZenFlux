"""In-memory snapshot cache with TTL for ZenFlux."""

import time
from typing import Dict, Optional
from ..models import MarketSnapshot


class MarketSnapshotCache:
    """TTL-based cache for MarketSnapshot objects."""

    def __init__(self, ttl_seconds: float = 30.0):
        self.ttl = ttl_seconds
        self._store: Dict[str, tuple[MarketSnapshot, float]] = {}

    def get(self, symbol: str) -> Optional[MarketSnapshot]:
        entry = self._store.get(symbol)
        if not entry:
            return None
        snap, ts = entry
        if time.time() - ts > self.ttl:
            del self._store[symbol]
            return None
        return snap

    def set(self, snap: MarketSnapshot) -> None:
        self._store[snap.symbol] = (snap, time.time())

    def invalidate(self, symbol: str) -> None:
        self._store.pop(symbol, None)

    def clear(self) -> None:
        self._store.clear()

    def size(self) -> int:
        return len(self._store)

    def valid_symbols(self) -> list[str]:
        now = time.time()
        return [s for s, (_, ts) in self._store.items() if now - ts <= self.ttl]
