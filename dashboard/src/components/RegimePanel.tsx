import React from 'react';
import type { ZenState } from '../types';

const STATES: { key: ZenState; label: string; color: string }[] = [
  { key: 'chaotic',   label: 'Chaotic',   color: '#ef4444' },
  { key: 'turbulent', label: 'Turbulent', color: '#f97316' },
  { key: 'flux',      label: 'Flux',      color: '#eab308' },
  { key: 'calm',      label: 'Calm',      color: '#22c55e' },
  { key: 'serene',    label: 'Serene',    color: '#06b6d4' },
];

interface Props {
  current: ZenState; regimeRisk: number; alignment: number;
  calmSignals: string[]; stressSignals: string[]; alertFlags: string[];
}

export const RegimePanel: React.FC<Props> = ({ current, regimeRisk, alignment, calmSignals, stressSignals, alertFlags }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
    <div style={{ background: '#111827', borderRadius: 10, border: '1px solid #1f2937', padding: '14px 16px' }}>
      <div style={{ fontSize: 11, color: '#6b7280', marginBottom: 10, textTransform: 'uppercase' }}>Regime Arc</div>
      <div style={{ display: 'flex', gap: 3 }}>
        {STATES.map(s => (
          <div key={s.key} style={{ flex: 1, height: 6, borderRadius: 99, background: s.key === current ? s.color : '#1f2937' }} />
        ))}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 6 }}>
        {STATES.map(s => (
          <div key={s.key} style={{ fontSize: 9, color: s.key === current ? s.color : '#374151', textAlign: 'center', flex: 1 }}>{s.label}</div>
        ))}
      </div>
      <div style={{ marginTop: 12, display: 'flex', justifyContent: 'space-between' }}>
        <span style={{ fontSize: 11, color: '#6b7280' }}>Regime Change Risk</span>
        <span style={{ fontSize: 12, color: regimeRisk > 50 ? '#f97316' : '#6b7280' }}>{regimeRisk.toFixed(0)}%</span>
      </div>
    </div>

    <div style={{ background: '#111827', borderRadius: 10, border: '1px solid #1f2937', padding: '14px 16px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
        <span style={{ fontSize: 11, color: '#6b7280', textTransform: 'uppercase' }}>Signal Alignment</span>
        <span style={{ fontSize: 12, color: '#22c55e' }}>{(alignment * 100).toFixed(0)}%</span>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
        <div>
          <div style={{ fontSize: 10, color: '#22c55e', marginBottom: 4 }}>CALM</div>
          {calmSignals.map(s => <div key={s} style={{ fontSize: 11, color: '#9ca3af' }}>• {s.replace(/_/g, ' ')}</div>)}
        </div>
        <div>
          <div style={{ fontSize: 10, color: '#ef4444', marginBottom: 4 }}>STRESS</div>
          {stressSignals.length === 0
            ? <div style={{ fontSize: 11, color: '#374151' }}>none</div>
            : stressSignals.map(s => <div key={s} style={{ fontSize: 11, color: '#9ca3af' }}>• {s.replace(/_/g, ' ')}</div>)}
        </div>
      </div>
    </div>

    {alertFlags.length > 0 && (
      <div style={{ background: '#111827', borderRadius: 10, border: '1px solid #1f2937', padding: '14px 16px' }}>
        <div style={{ fontSize: 11, color: '#ef4444', marginBottom: 6, textTransform: 'uppercase' }}>Alerts</div>
        {alertFlags.map(f => <div key={f} style={{ fontSize: 11, color: '#9ca3af' }}>⚠ {f.replace(/_/g, ' ')}</div>)}
      </div>
    )}
  </div>
);