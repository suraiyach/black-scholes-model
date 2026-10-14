'use client';
import { useMemo, useState } from 'react';

function num(n: any) { return typeof n === 'number' ? n : Number(n ?? 0); }

export default function ChainTable({ data }: { data: any }) {
  const [sortKey, setSortKey] = useState<string>('strikePrice');
  const [asc, setAsc] = useState<boolean>(true);

  const rows = useMemo(() => {
    if (!data?.rows) return [];
    const sorted = [...data.rows].sort((a: any, b: any) => {
      const A = num(a[sortKey]);
      const B = num(b[sortKey]);
      return asc ? A - B : B - A;
    });
    return sorted;
  }, [data, sortKey, asc]);

  function clickSort(key: string) {
    if (sortKey === key) setAsc(!asc); else { setSortKey(key); setAsc(true); }
  }

  const headers = ['strikePrice','optionType','impliedVolatility','lastPrice','totalTradedVolume','bsPrice','delta_call','delta_put','gamma','vega','theta_call','theta_put','rho_call','rho_put'];

  return (
    <div style={{ marginTop: 16 }}>
      <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
        <div>Spot: <b>{data?.spot?.toFixed?.(2)}</b></div>
        <div>Expiry: <b>{data?.expiry}</b></div>
        <div>Risk-free: <b>{(data?.riskFree * 100).toFixed(2)}%</b></div>
        <div>Rows: <b>{data?.rows?.length ?? 0}</b></div>
      </div>

      <div style={{ overflow: 'auto', marginTop: 12 }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              {headers.map(k => (
                <th key={k} onClick={() => clickSort(k)} style={{ cursor: 'pointer', textAlign: 'right', padding: 8, borderBottom: '1px solid #1f2937', position: 'sticky', top: 0, background: '#0b1220' }}>
                  {k}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r: any, i: number) => (
              <tr key={i} style={{ borderBottom: '1px solid #111827' }}>
                <td style={{ textAlign: 'right', padding: 6 }}>{r.strikePrice}</td>
                <td style={{ textAlign: 'right', padding: 6 }}>{r.optionType}</td>
                <td style={{ textAlign: 'right', padding: 6 }}>{(r.impliedVolatility*100).toFixed(2)}%</td>
                <td style={{ textAlign: 'right', padding: 6 }}>{r.lastPrice?.toFixed?.(2)}</td>
                <td style={{ textAlign: 'right', padding: 6 }}>{r.totalTradedVolume}</td>
                <td style={{ textAlign: 'right', padding: 6 }}>{r.bsPrice?.toFixed?.(2)}</td>
                <td style={{ textAlign: 'right', padding: 6 }}>{r.delta_call}</td>
                <td style={{ textAlign: 'right', padding: 6 }}>{r.delta_put}</td>
                <td style={{ textAlign: 'right', padding: 6 }}>{r.gamma}</td>
                <td style={{ textAlign: 'right', padding: 6 }}>{r.vega}</td>
                <td style={{ textAlign: 'right', padding: 6 }}>{r.theta_call}</td>
                <td style={{ textAlign: 'right', padding: 6 }}>{r.theta_put}</td>
                <td style={{ textAlign: 'right', padding: 6 }}>{r.rho_call}</td>
                <td style={{ textAlign: 'right', padding: 6 }}>{r.rho_put}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
