"use client";

import React, { useEffect, useState } from 'react';
import StatTile from '@/components/ui/StatTile';
import Card from '@/components/ui/Card';
import { getDashboardSnapshot, getShipmentDelays } from '@/lib/api';

export default function Dashboard() {
  const [snapshot, setSnapshot] = useState<any>(null);
  const [delays, setDelays] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [snapRes, delaysRes] = await Promise.all([
          getDashboardSnapshot(),
          getShipmentDelays()
        ]);
        setSnapshot(snapRes);
        setDelays(delaysRes);
      } catch (err) {
        console.error("Failed to load dashboard data", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-xl)' }}>
      
      {/* Drifting gradient hero */}
      <section 
        className="duotone-bg" 
        style={{ 
          padding: 'var(--spacing-xl)', 
          borderRadius: 'var(--radius-lg)',
          border: 'var(--border-hairline)',
          display: 'flex',
          flexDirection: 'column',
          gap: 'var(--spacing-md)'
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <h1 style={{ marginBottom: '8px' }}>Global Control Tower</h1>
            <p style={{ color: 'var(--text-muted)', maxWidth: '600px', fontSize: '1.1rem' }}>
              Predicting supply chain state for the upcoming week based on live telemetry from 142 global nodes.
            </p>
          </div>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', border: 'var(--border-hairline)', padding: '6px 12px', borderRadius: 'var(--radius-pill)', background: 'var(--bg-cream)' }}>
            Data updated: {loading ? 'Updating...' : new Date().toLocaleTimeString()}
          </div>
        </div>
      </section>

      {/* Bento Grid layout */}
      <section style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: 'var(--spacing-lg)',
        gridAutoRows: 'minmax(120px, auto)'
      }}>
        {/* Stat Tiles */}
        <div style={{ gridColumn: 'span 1' }}>
          <StatTile 
            title="Global Inventory Value" 
            value={14.2} 
            prefix="₹" 
            suffix="B"
            trend={2.4} 
            trendLabel="vs last week" 
          />
        </div>
        <div style={{ gridColumn: 'span 1' }}>
          <StatTile 
            title="SKUs At Risk (7D)" 
            value={snapshot?.metrics?.shortage_forecasts || 124} 
            trend={-12} 
            trendLabel="improvement" 
          />
        </div>
        <div style={{ gridColumn: 'span 1' }}>
          <StatTile 
            title="Delayed Freight Routes" 
            value={snapshot?.metrics?.delayed_shipments || 32} 
            trend={5} 
            trendLabel="increase" 
          />
        </div>
        <div style={{ gridColumn: 'span 1' }}>
          <StatTile 
            title="Network Resilience" 
            value={87} 
            suffix="/100" 
            trend={1.2} 
            trendLabel="stable" 
          />
        </div>

        {/* Dense Dashboard grid tiles */}
        <Card variant="outlined" className="animate-enter" style={{ gridColumn: 'span 2', gridRow: 'span 2', animationDelay: '100ms' }}>
          <h2 style={{ fontSize: '1.25rem' }}>Predicted Shortages</h2>
          <div style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
            [ Chart Placeholder: Inventory vs Forecast ]
          </div>
        </Card>

        <Card variant="elevated" className="animate-enter" style={{ gridColumn: 'span 2', gridRow: 'span 2', animationDelay: '200ms', overflowY: 'auto', maxHeight: '400px' }}>
          <h2 style={{ fontSize: '1.25rem', marginBottom: 'var(--spacing-md)' }}>Active Disruptions</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-md)' }}>
            {loading ? (
              <div style={{ padding: 'var(--spacing-md)', color: 'var(--text-muted)' }}>Loading live disruptions...</div>
            ) : delays?.shipments?.filter((s:any) => s.status === 'DELAYED').length > 0 ? (
              delays.shipments.filter((s:any) => s.status === 'DELAYED').map((shipment: any) => (
                <div key={shipment.shipment_id} style={{ padding: 'var(--spacing-md)', background: 'rgba(217, 56, 30, 0.05)', borderLeft: '4px solid var(--accent-red)', borderRadius: '0 var(--radius-lg) var(--radius-lg) 0' }}>
                  <div style={{ fontWeight: 600, color: 'var(--text-ink)' }}>Shipment {shipment.shipment_id} Delayed ({shipment.delay_days} days)</div>
                  <div style={{ fontSize: '14px', color: 'var(--text-muted)', marginTop: '4px' }}>
                    Supplier: {shipment.supplier_name}. Impact: {shipment.reasoning}
                  </div>
                </div>
              ))
            ) : (
              <div style={{ padding: 'var(--spacing-md)', color: 'var(--text-muted)' }}>No active disruptions detected.</div>
            )}
          </div>
        </Card>

      </section>
    </div>
  );
}
