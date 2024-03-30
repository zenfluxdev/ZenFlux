import React, { useState } from 'react';
import type { ZenAnalysis } from './types';
import { ZenGauge } from './components/ZenGauge';
import { StressChart } from './components/StressChart';
import { RegimePanel } from './components/RegimePanel';
import { mockAnalysis } from './mockData';

const SIGNAL_KEYS = [
  'volatility_regime_score', 'liquidity_stress_score', 'price_dislocation_score',
  'flow_imbalance_score', 'correlation_break_score',
] as const;

const SIGNAL_NAMES: Record<string, string> = {
  volatility_regime_score: 'volatility_regime', liquidity_stress_score: 'liquidity_stress',
  price_dislocation_score: 'price_dislocation', flow_imbalance_score: 'flow_imbalance',
  correlation_break_score: 'correlation_break',
};

const BIAS_COLOR = { calm: '#22c55e', stress: '#ef4444', neutral: '#6b7280' } as const;

export default function App() {
  const [a] = useState<ZenAnalysis>(mockAnalysis);
  const scores = SIGNAL_KEYS.map(k => ({ name: SIGNAL_NAMES[k], score: a[k] }));

  return (
    <div style={{ minHeight: '100vh', background: '#030712', color: '#e5e7eb', fontFamily: 'monospace' }}>
      <div style={{ borderBottom: '1px solid #1f2937', padding: '14px 28px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <span style={{ fontSize: 17, fontWeight: 700, color: '#f9fafb', letterSpacing: '0.04em' }}>☯ ZENFLUX</span>
          <span style={{ fontSize: 11, color: '#4b5563', marginLeft: 10 }}>market stress regime engine</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <span style={{ fontSize: 13, color: '#4b5563' }}>{a.symbol}</span>
          <span style={{ fontSize: 11, fontWeight: 600, padding: '3px 10px', borderRadius: 99, border: `1px solid ${BIAS_COLOR[a.bias]}`, color: BIAS_COLOR[a.bias], textTransform: 'uppercase' }}>{a.bias}</span>
        </div>
      </div>
      <div style={{ maxWidth: 1080, margin: '0 auto', padding: '28px 20px', display: 'grid', gridTemplateColumns: '200px 1fr 280px', gap: 20 }}>
        <div style={{ background: '#111827', borderRadius: 12, border: '1px solid #1f2937' }}>
          <ZenGauge index={a.zen_index} state={a.zen_state} stressLevel={a.stress_level} conviction={a.conviction} />
          <div style={{ padding: '0 20px 18px', borderTop: '1px solid #1f2937' }}>
            <div style={{ fontSize: 10, color: '#6b7280', marginTop: 12, marginBottom: 4, textTransform: 'uppercase' }}>Dominant</div>
            <div style={{ fontSize: 12, color: '#e5e7eb' }}>{a.dominant_signal.replace(/_/g, ' ')}</div>
          </div>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div style={{ background: '#111827', borderRadius: 12, border: '1px solid #1f2937', padding: '16px 18px' }}>
            <StressChart scores={scores} />
          </div>
          <div style={{ background: '#111827', borderRadius: 12, border: '1px solid #1f2937', padding: '16px 18px' }}>
            <div style={{ fontSize: 11, color: '#6b7280', marginBottom: 8, textTransform: 'uppercase' }}>Analysis</div>
            <p style={{ fontSize: 12, color: '#9ca3af', lineHeight: 1.65, margin: 0 }}>{a.reasoning}</p>
          </div>
        </div>
        <RegimePanel current={a.zen_state} regimeRisk={a.regime_change_risk} alignment={a.signal_alignment}
          calmSignals={a.calm_signals} stressSignals={a.stress_signals} alertFlags={a.alert_flags} />
      </div>
    </div>
  );
}