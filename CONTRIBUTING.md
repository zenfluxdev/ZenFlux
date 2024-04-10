# Contributing to ZenFlux

## Setup

```bash
git clone https://github.com/zenfluxdev/ZenFlux
cd ZenFlux
pip install -e ".[dev]"
pytest tests/ -v
```

## Adding a Signal

1. Create `zenflux/signals/your_signal.py` with a `compute(snap: MarketSnapshot) -> SignalResult` method
2. Register in `zenflux/signals/__init__.py` and add to `ALL_SIGNALS`
3. Add weight in `zenflux/engine.py` — weights must sum to 1.0
4. Write tests in `tests/test_signals_your_signal.py`

## Signal Conventions

- Score: 0–100 (50 = neutral, >55 = calm, <45 = stress)
- High score = calm/zen, Low score = stress/chaotic
- Strength: `abs(score - 50) / 50`

## Pull Requests

- Branch: `feature/signal-name` or `fix/issue`
- All tests must pass before merge