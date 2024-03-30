export type SignalBias = 'calm' | 'stress' | 'neutral';
export type ZenState = 'chaotic' | 'turbulent' | 'flux' | 'calm' | 'serene';

export interface ZenAnalysis {
  symbol: string;
  volatility_regime_score: number;
  liquidity_stress_score: number;
  price_dislocation_score: number;
  flow_imbalance_score: number;
  correlation_break_score: number;
  zen_index: number;
  zen_state: ZenState;
  stress_level: number;
  regime_change_risk: number;
  dominant_signal: string;
  calm_signals: string[];
  stress_signals: string[];
  alert_flags: string[];
  bias: SignalBias;
  conviction: number;
  signal_alignment: number;
  reasoning: string;
}