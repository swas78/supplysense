"use client";

import React, { useEffect, useState } from 'react';
import Card from '@/components/ui/Card';
import StatTile from '@/components/ui/StatTile';
import { ShieldCheck, ShieldAlert, AlertTriangle } from 'lucide-react';
import { getSupplierScores } from '@/lib/api';

export default function SuppliersScreen() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const scores = await getSupplierScores();
        setData(scores);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const suppliers = data?.suppliers || [];
  const highRisk = suppliers.filter((s:any) => s.risk_level === 'HIGH_RISK').length;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-xl)' }}>
      <div>
        <h1 style={{ marginBottom: '8px' }}>Supplier Risk & Resilience</h1>
        <p style={{ color: 'var(--text-muted)' }}>Evaluating vendor performance and recovery capabilities.</p>
      </div>

      <section style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: 'var(--spacing-lg)'
      }}>
        <StatTile title="Total Suppliers" value={loading ? '...' : suppliers.length} />
        <StatTile title="Critical Risk Vendors" value={loading ? '...' : highRisk} trend={-1} trendLabel="improvement" />
        <StatTile title="Network Resilience" value={loading ? '...' : 82} suffix="/100" />
      </section>

      <Card variant="outlined" className="animate-enter">
        <h2 style={{ fontSize: '1.25rem' }}>Supplier Scorecard</h2>
        
        {loading ? (
          <div style={{ padding: 'var(--spacing-xl)', textAlign: 'center', color: 'var(--text-muted)' }}>Loading vendor performance telemetry...</div>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: 'var(--spacing-md)' }}>
            <thead>
              <tr style={{ borderBottom: 'var(--border-hairline)', textAlign: 'left' }}>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Supplier Name</th>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>On-Time Rate</th>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Quality Rate</th>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Reliability Score</th>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {suppliers.map((s: any) => (
                <tr key={s.supplier_id} style={{ borderBottom: 'var(--border-hairline)' }}>
                  <td style={{ padding: 'var(--spacing-md) 0', fontWeight: 500 }}>
                    {s.supplier_name}
                    <div style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 400 }}>{s.reasoning}</div>
                  </td>
                  <td style={{ padding: 'var(--spacing-md) 0' }}>{(s.on_time_rate * 100).toFixed(0)}%</td>
                  <td style={{ padding: 'var(--spacing-md) 0' }}>{(s.quality_rate * 100).toFixed(0)}%</td>
                  <td style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: s.risk_level === 'HIGH_RISK' ? 'var(--accent-red)' : 'inherit' }}>
                    {Math.round(s.reliability_score * 100)}/100
                  </td>
                  <td style={{ padding: 'var(--spacing-md) 0', color: s.risk_level === 'LOW_RISK' ? '#2e7d32' : s.risk_level === 'HIGH_RISK' ? 'var(--accent-red)' : '#f57c00' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                      {s.risk_level === 'LOW_RISK' ? <ShieldCheck size={16} /> : s.risk_level === 'HIGH_RISK' ? <ShieldAlert size={16} /> : <AlertTriangle size={16} />} 
                      {s.risk_level.replace('_', ' ')}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </Card>
    </div>
  );
}
