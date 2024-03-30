import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, Cell, ResponsiveContainer } from 'recharts';

const LABELS: Record<string, string> = {
  volatility_regime: 'Volatility', liquidity_stress: 'Liquidity',
  price_dislocation: 'Dislocation', flow_imbalance: 'Flow', correlation_break: 'Correlation',
};

const getColor = (s: number) => s > 65 ? '#22c55e' : s > 55 ? '#86efac' : s < 35 ? '#ef4444' : s < 45 ? '#fca5a5' : '#6b7280';

export const StressChart: React.FC<{ scores: { name: string; score: number }[] }> = ({ scores }) => {
  const data = scores.map(s => ({ name: LABELS[s.name] ?? s.name, score: s.score }));
  return (
    <div style={{ padding: '16px 0' }}>
      <h3 style={{ fontSize: 12, color: '#6b7280', marginBottom: 12, textTransform: 'uppercase', letterSpacing: '0.06em' }}>Stress Signals</h3>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data} layout="vertical" margin={{ left: 12, right: 24, top: 4, bottom: 4 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" horizontal={false} />
          <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 11, fill: '#6b7280' }} />
          <YAxis type="category" dataKey="name" tick={{ fontSize: 11, fill: '#9ca3af' }} width={78} />
          <Tooltip contentStyle={{ background: '#111827', border: '1px solid #1f2937', borderRadius: 6, fontSize: 12 }} formatter={(v: number) => [`${v.toFixed(1)}/100`, 'Score']} />
          <ReferenceLine x={50} stroke="#374151" strokeDasharray="4 4" />
          <Bar dataKey="score" radius={[0, 3, 3, 0]}>
            {data.map((e, i) => <Cell key={i} fill={getColor(e.score)} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};