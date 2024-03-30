import React from 'react';
import type { ZenState } from '../types';

const STATE_COLORS: Record<ZenState, string> = {
  chaotic: '#ef4444', turbulent: '#f97316', flux: '#eab308', calm: '#22c55e', serene: '#06b6d4',
};
const STATE_LABELS: Record<ZenState, string> = {
  chaotic: 'CHAOTIC', turbulent: 'TURBULENT', flux: 'FLUX', calm: 'CALM', serene: 'SERENE',
};

interface Props { index: number; state: ZenState; stressLevel: number; conviction: number; }

export const ZenGauge: React.FC<Props> = ({ index, state, stressLevel, conviction }) => {
  const color = STATE_COLORS[state];
  return (
    <div style={{ textAlign: 'center', padding: '24px' }}>
      <div style={{
        width: 160, height: 160, borderRadius: '50%', border: `8px solid ${color}`,
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        margin: '0 auto 16px', background: `${color}15`,
      }}>
        <span style={{ fontSize: 36, fontWeight: 700, color }}>{index.toFixed(1)}</span>
        <span style={{ fontSize: 11, color: '#6b7280', marginTop: 2 }}>ZEN INDEX</span>
      </div>
      <div style={{ fontSize: 13, fontWeight: 600, color, letterSpacing: '0.08em' }}>{STATE_LABELS[state]}</div>
      <div style={{ fontSize: 11, color: '#6b7280', marginTop: 6 }}>
        Stress {(stressLevel * 100).toFixed(0)}% · Conviction {(conviction * 100).toFixed(0)}%
      </div>
    </div>
  );
};