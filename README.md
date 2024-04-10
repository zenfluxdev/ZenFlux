<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:030712,100:0891b2&height=200&section=header&text=ZenFlux&fontSize=58&fontColor=f9fafb&fontAlignY=38&desc=Market%20Stress%20Regime%20Engine&descAlignY=58&descSize=18" width="100%"/>

[![Tests](https://github.com/zenfluxdev/ZenFlux/actions/workflows/test.yml/badge.svg)](https://github.com/zenfluxdev/ZenFlux/actions)
[![Python](https://img.shields.io/badge/Python-3.10%2B-0891b2?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178c6?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-374151?style=flat-square)](LICENSE)

</div>

---

Every market has a stress regime underneath the price action. When volatility spikes, spreads widen, order books drain, and flows become one-sided — the regime is breaking. When vol compresses, spreads tighten, and flows balance — the market has found its zen.

ZenFlux measures that. Five microstructure signals → one **zen index** → five states from CHAOTIC to SERENE.

---

## The Regime Spectrum

```
0 ──────── 20 ──────── 40 ──────── 60 ──────── 80 ─── 100
  CHAOTIC    TURBULENT      FLUX        CALM      SERENE
  Avoid       Caution    Uncertain   Favorable   Optimal
```

---

## Architecture

```
MarketSnapshot (microstructure data)
        │
        ▼
  ┌──────────────────────────────────────────────┐
  │  VolatilityRegimeSignal  → vol vs baseline   │
  │  LiquidityStressSignal   → spread + depth    │
  │  PriceDislocationSignal  → deviation from MA │
  │  FlowImbalanceSignal     → buy/sell ratio     │
  │  CorrelationBreakSignal  → cross-asset shift  │
  └──────────────────────────────────────────────┘
        │  weighted composite (5 signals)
        ▼
   ZenAnalysis
    • zen_index           (0–100)
    • zen_state           (chaotic → serene)
    • stress_level        (0–1)
    • regime_change_risk  (0–100)
    • conviction + alignment
    • reasoning
```

---

## Signal Weights

| Signal | Weight | What it measures |
|--------|--------|-----------------|
| Volatility Regime | **30%** | Realized vol vs 30d baseline trend |
| Liquidity Stress | **25%** | Bid-ask spread + orderbook depth |
| Price Dislocation | **20%** | Deviation from 7d/30d moving averages |
| Flow Imbalance | **15%** | Buy vs sell volume asymmetry |
| Correlation Break | **10%** | Cross-asset correlation shift |

---

## Install

```bash
pip install zenflux
```

Or from source:

```bash
git clone https://github.com/zenfluxdev/ZenFlux
cd ZenFlux
pip install -e ".[dev]"
```

---

## Usage

```python
from zenflux import ZenEngine, MarketSnapshot

engine = ZenEngine()

snap = MarketSnapshot(
    symbol="BTC",
    timestamp=1700000000.0,
    realized_vol_1d=28.0,
    realized_vol_7d=34.0,
    realized_vol_30d=72.0,
    bid_ask_spread_pct=0.035,
    bid_ask_spread_7d_avg=0.082,
    orderbook_depth_usd=22_000_000,
    orderbook_depth_7d_avg=15_000_000,
    price=43_200.0,
    ma_7d=42_800.0,
    ma_30d=41_500.0,
    price_high_30d=48_000.0,
    price_low_30d=37_000.0,
    buy_volume_1h=5_200_000,
    sell_volume_1h=4_800_000,
    buy_volume_24h=125_000_000,
    sell_volume_24h=115_000_000,
    correlation_7d=0.87,
    correlation_30d=0.84,
)

analysis = engine.analyze(snap)

print(f"Zen Index:    {analysis.zen_index:.1f}")
print(f"State:        {analysis.zen_state.value}")
print(f"Stress Level: {analysis.stress_level:.1%}")
print(f"Regime Risk:  {analysis.regime_change_risk:.0f}%")
print(f"Reasoning:    {analysis.reasoning}")
```

---

## Dashboard

```bash
cd dashboard && npm install && npm run dev
# → http://localhost:3000
```

Zen index gauge, stress signal chart, regime arc, alert panel.

---

## Tests

```bash
pytest tests/ -v
# 124 tests covering all 5 signals, engine, and utils
```

---

## Docker

```bash
docker compose up
```

---

<details>
<summary>日本語 README</summary>

## ZenFlux — 市場ストレスレジームエンジン

価格の裏にある市場のストレス状態を測定する。ボラティリティ、スプレッド、オーダーブック深度、フロー不均衡、相関崩壊の5つのシグナルから**ゼンインデックス**（0〜100）を算出。

### レジームスペクトラム

```
0 ─── 20 ─── 40 ─── 60 ─── 80 ─── 100
 混沌   乱流    変動    穏やか   静寂
```

### シグナル

| シグナル | 重み | 測定内容 |
|---------|------|---------|
| ボラティリティレジーム | 30% | 実現ボラ vs 30日ベースライン |
| 流動性ストレス | 25% | スプレッド + オーダーブック深度 |
| 価格乖離 | 20% | 移動平均からの乖離 |
| フロー不均衡 | 15% | 売買比率 |
| 相関崩壊 | 10% | クロスアセット相関シフト |

### インストール

```bash
pip install zenflux
```

### テスト

```bash
pytest tests/ -v
# 124テスト全てパス
```

</details>

---

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0891b2,100:030712&height=100&section=footer" width="100%"/>
</div>