"use client";

import React, { useEffect, useState } from 'react';
import Card from '@/components/ui/Card';
import StatTile from '@/components/ui/StatTile';
import { getExecutiveSummary } from '@/lib/api';

export default function ExecutiveScreen() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const res = await getExecutiveSummary();
        setData(res);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const kpis = data?.kpis;
  const translator = data?.cost_of_delay_translator;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-xl)' }}>
      <div>
        <h1 style={{ marginBottom: '8px' }}>Executive Summary</h1>
        <p style={{ color: 'var(--text-muted)' }}>High-level financial impact and active risk surface.</p>
      </div>

      <Card variant="outlined">
        <h2 style={{ fontSize: '1.25rem', marginBottom: '8px' }}>Global Health Status</h2>
        <p style={{ color: 'var(--text-ink)', fontSize: '15px', lineHeight: 1.6 }}>
          {loading ? (
            <span className="shimmer-text">Analyzing global metrics and generating executive narrative...</span>
          ) : data?.summary}
        </p>
      </Card>

      <section style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: 'var(--spacing-lg)'
      }}>
        <StatTile 
          title="Revenue at Risk" 
          value={loading ? '...' : kpis?.financial_impact?.pending_orders_value || 0} 
          prefix="₹" 
        />
        <StatTile 
          title="Active Issues" 
          value={loading ? '...' : (kpis?.active_issues?.delayed_shipments || 0) + (kpis?.active_issues?.shortage_forecasts || 0)} 
          trend={-2} 
          trendLabel="improvement" 
        />
        <StatTile 
          title="Est. Recovery Time" 
          value={loading ? '...' : kpis?.timeline?.estimated_recovery_days || 0} 
          suffix=" Days" 
        />
      </section>

      <Card variant="elevated" className="animate-enter" style={{ borderLeft: '4px solid var(--accent-red)' }}>
        <h2 style={{ fontSize: '1.25rem', marginBottom: 'var(--spacing-md)' }}>Cost of Delay Translator</h2>
        
        {loading ? (
          <div style={{ color: 'var(--text-muted)' }}>Loading financial translation model...</div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-lg)' }}>
            <p style={{ fontSize: '15px', lineHeight: 1.6, color: 'var(--text-ink)' }}>
              {translator?.narrative}
            </p>
            
            <div style={{ display: 'flex', gap: 'var(--spacing-xl)' }}>
              <div>
                <div style={{ fontSize: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Hourly Bleed</div>
                <div style={{ fontSize: '24px', fontFamily: 'var(--font-serif)', color: 'var(--accent-red)', fontWeight: 600 }}>
                  ₹{(translator?.hourly_cost || 0).toLocaleString()}
                </div>
              </div>
              <div>
                <div style={{ fontSize: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Daily Bleed</div>
                <div style={{ fontSize: '24px', fontFamily: 'var(--font-serif)', color: 'var(--accent-red)', fontWeight: 600 }}>
                  ₹{(translator?.daily_cost || 0).toLocaleString()}
                </div>
              </div>
              <div>
                <div style={{ fontSize: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Weekly Projection</div>
                <div style={{ fontSize: '24px', fontFamily: 'var(--font-serif)', color: 'var(--accent-red)', fontWeight: 600 }}>
                  ₹{(translator?.weekly_cost || 0).toLocaleString()}
                </div>
              </div>
            </div>

            <div style={{ background: 'rgba(217, 56, 30, 0.05)', padding: 'var(--spacing-md)', borderRadius: 'var(--radius-md)', color: 'var(--accent-red)', fontSize: '14px', fontWeight: 500 }}>
              {translator?.recommendation_impact}
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
