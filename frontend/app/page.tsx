'use client';
import { useEffect, useMemo, useRef, useState } from 'react';
import Controls, { ControlsState } from './components/Controls';
import ChainTable from './components/ChainTable';
import { fetchChain } from '../lib/api';

export default function Page() {
  const [ctrls, setCtrls] = useState<ControlsState>({ symbol: 'NIFTY', instrument: 'INDEX', optionType: 'ALL', refresh: 15 });
  const [data, setData] = useState<any>(null);
  const timer = useRef<any>(null);

  async function load() {
    try {
      const q: any = { symbol: ctrls.symbol, instrument: ctrls.instrument, optionType: ctrls.optionType };
      if (ctrls.expiry) q.expiry = ctrls.expiry;
      const res = await fetchChain(q);
      setData(res);
    } catch (e) {
      console.error(e);
    }
  }

  useEffect(() => {
    load();
    if (timer.current) clearInterval(timer.current);
    timer.current = setInterval(load, Math.max(5, ctrls.refresh) * 1000);
    return () => clearInterval(timer.current);
  }, [ctrls.symbol, ctrls.instrument, ctrls.optionType, ctrls.expiry, ctrls.refresh]);

  return (
    <div style={{ display: 'grid', gap: 16 }}>
      <Controls onChange={setCtrls} />
      <div style={{ opacity: data ? 1 : 0.6 }}>{data ? <ChainTable data={data} /> : <div>Loading…</div>}</div>
      <div style={{ fontSize: 12, opacity: 0.7 }}>Tip: Use expiry like <code>28-Aug-2025</code>. Keep refresh ≥ 10s to avoid NSE throttling.</div>
    </div>
  );
}
