'use client';
import { useState } from 'react';

export type ControlsState = {
  symbol: string;
  instrument: 'INDEX' | 'EQUITY';
  optionType: 'ALL' | 'CE' | 'PE';
  expiry?: string;
  refresh: number;
};

export default function Controls(props: { onChange: (s: ControlsState) => void }) {
  const [state, setState] = useState<ControlsState>({ symbol: 'NIFTY', instrument: 'INDEX', optionType: 'ALL', refresh: 15 });

  function update<K extends keyof ControlsState>(k: K, v: ControlsState[K]) {
    const next = { ...state, [k]: v };
    setState(next);
    props.onChange(next);
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, minmax(0, 1fr))', gap: 12, alignItems: 'end' }}>
      <div>
        <label>Symbol</label>
        <input defaultValue={state.symbol} onChange={e => update('symbol', e.target.value.toUpperCase())} style={{ width: '100%', padding: 8, borderRadius: 8 }} />
      </div>
      <div>
        <label>Instrument</label>
        <select defaultValue={state.instrument} onChange={e => update('instrument', e.target.value as any)} style={{ width: '100%', padding: 8, borderRadius: 8 }}>
          <option value="INDEX">INDEX</option>
          <option value="EQUITY">EQUITY</option>
        </select>
      </div>
      <div>
        <label>Type</label>
        <select defaultValue={state.optionType} onChange={e => update('optionType', e.target.value as any)} style={{ width: '100%', padding: 8, borderRadius: 8 }}>
          <option value="ALL">ALL</option>
          <option value="CE">CE</option>
          <option value="PE">PE</option>
        </select>
      </div>
      <div>
        <label>Expiry (optional)</label>
        <input placeholder="28-Aug-2025" onChange={e => update('expiry', e.target.value)} style={{ width: '100%', padding: 8, borderRadius: 8 }} />
      </div>
      <div>
        <label>Auto-refresh (s)</label>
        <input type="number" min={5} defaultValue={15} onChange={e => update('refresh', Number(e.target.value || 15))} style={{ width: '100%', padding: 8, borderRadius: 8 }} />
      </div>
    </div>
  );
}
