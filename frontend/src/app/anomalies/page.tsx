"use client";

import React, { useEffect, useState } from 'react';
import Card from '@/components/ui/Card';
import { getAnomalies } from '@/lib/api';

export default function AnomaliesScreen() {
  const [anomaliesData, setAnomaliesData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getAnomalies();
        setAnomaliesData(data);
      } catch (err) {
        console.error("Failed to fetch anomalies", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-xl)' }}>
      <div>
        <h1 style={{ marginBottom: '8px' }}>Anomaly Feed</h1>
        <p style={{ color: 'var(--text-muted)' }}>Detected spikes and drops in demand, auto-tagged with probable causes.</p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-md)' }}>
        {loading ? (
          <div style={{ padding: 'var(--spacing-xl)', color: 'var(--text-muted)' }}>Analyzing telemetry streams for anomalies...</div>
        ) : anomaliesData?.anomalies?.length > 0 ? (
          anomaliesData.anomalies.map((anom: any, idx: number) => (
            <Card key={anom.anomaly_id} variant="outlined" className="animate-enter" style={{ animationDelay: `${idx * 100}ms` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                    <h3 style={{ margin: 0, fontFamily: 'var(--font-sans)', fontWeight: 600 }}>{anom.product_name} ({anom.product_id})</h3>
                    <span style={{ 
                      background: anom.anomaly_type === 'SPIKE' ? 'rgba(217, 56, 30, 0.1)' : 'rgba(26, 26, 26, 0.1)', 
                      color: anom.anomaly_type === 'SPIKE' ? 'var(--accent-red)' : 'var(--text-ink)', 
                      padding: '4px 8px', borderRadius: '4px', fontSize: '12px', fontWeight: 600 
                    }}>
                      {anom.anomaly_type} Detected
                    </span>
                  </div>
                  <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginBottom: '16px' }}>{anom.reasoning}</p>
                  <div style={{ display: 'flex', gap: '24px', fontSize: '14px' }}>
                    <div><span style={{ color: 'var(--text-muted)' }}>Normal Demand:</span> <span style={{ fontWeight: 600 }}>{anom.normal_demand}</span></div>
                    <div><span style={{ color: 'var(--text-muted)' }}>Actual Demand:</span> <span style={{ fontWeight: 600 }}>{anom.actual_demand}</span></div>
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Likely Cause</div>
                  <div style={{ fontWeight: 600 }}>{anom.attributed_cause}</div>
                  <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>Confidence: {anom.confidence_score * 100}%</div>
                </div>
              </div>
            </Card>
          ))
        ) : (
          <div style={{ padding: 'var(--spacing-xl)', color: 'var(--text-muted)' }}>No demand anomalies detected in the current window.</div>
        )}
      </div>
    </div>
  );
}
