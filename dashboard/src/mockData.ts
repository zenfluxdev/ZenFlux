import type { ZenAnalysis } from './types';

export const mockAnalysis: ZenAnalysis = {
  symbol: 'BTC',
  volatility_regime_score: 72.0,
  liquidity_stress_score: 68.0,
  price_dislocation_score: 65.0,
  flow_imbalance_score: 62.0,
  correlation_break_score: 74.0,
  zen_index: 68.85,
  zen_state: 'calm',
  stress_level: 0.311,
  regime_change_risk: 18.4,
  dominant_signal: 'correlation_break',
  calm_signals: ['volatility_regime', 'liquidity_stress', 'price_dislocation', 'flow_imbalance', 'correlation_break'],
  stress_signals: [],
  alert_flags: [],
  bias: 'calm',
  conviction: 0.377,
  signal_alignment: 1.0,
  reasoning: 'Zen index 68.9/100 → calm. Regime: 5 calm, 0 stress signals. Volatility compressed — low-stress regime confirmed. Liquidity deep and spreads tight — healthy market microstructure. Stress level: 31.1%.',
};