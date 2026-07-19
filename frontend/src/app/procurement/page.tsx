"use client";

import React, { useEffect, useState } from 'react';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import { getProcurementSuggestions } from '@/lib/api';

export default function ProcurementScreen() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const res = await getProcurementSuggestions();
        setData(res);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const suggestions = data?.suggestions || [];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-xl)' }}>
      <div>
        <h1 style={{ marginBottom: '8px' }}>Autonomous Procurement</h1>
        <p style={{ color: 'var(--text-muted)' }}>AI-generated purchase orders triggered by shortage forecasts.</p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-lg)' }}>
        {loading ? (
          <div style={{ padding: 'var(--spacing-xl)', color: 'var(--text-muted)' }}>Calculating optimal replenishment strategies...</div>
        ) : suggestions.length > 0 ? (
          suggestions.map((sug: any, idx: number) => (
            <Card key={`${sug.product_id}-${idx}`} variant="outlined" className="animate-enter" style={{ animationDelay: `${idx * 100}ms` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 'var(--spacing-lg)' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '4px' }}>
                    <h2 style={{ fontSize: '1.25rem', margin: 0 }}>Draft PO: {sug.product_name}</h2>
                    <span style={{ 
                      background: sug.urgency === 'CRITICAL' ? 'rgba(217, 56, 30, 0.1)' : 'rgba(26, 26, 26, 0.1)', 
                      color: sug.urgency === 'CRITICAL' ? 'var(--accent-red)' : 'var(--text-ink)', 
                      padding: '4px 8px', borderRadius: '4px', fontSize: '12px', fontWeight: 600 
                    }}>
                      {sug.urgency}
                    </span>
                  </div>
                  <p style={{ color: 'var(--text-muted)', fontSize: '14px' }}>
                    Stockout predicted in {sug.days_to_stockout} days. Order by {sug.order_deadline} to prevent shortage.
                  </p>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <Button variant="accent">Generate PO</Button>
                  <Button variant="ghost">Ignore</Button>
                </div>
              </div>

              <div style={{ background: 'var(--bg-cream)', padding: 'var(--spacing-md)', borderRadius: 'var(--radius-md)', border: 'var(--border-hairline)', display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 'var(--spacing-md)' }}>
                <div>
                  <div style={{ fontSize: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Supplier</div>
                  <div style={{ fontWeight: 600 }}>{sug.recommended_supplier_name}</div>
                  <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>{(sug.supplier_on_time_rate * 100).toFixed(0)}% On-Time</div>
                </div>
                <div>
                  <div style={{ fontSize: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Quantity</div>
                  <div style={{ fontWeight: 600 }}>{sug.suggested_quantity} units</div>
                  <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>{sug.daily_demand} daily demand</div>
                </div>
                <div>
                  <div style={{ fontSize: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Est. Cost</div>
                  <div style={{ fontWeight: 600 }}>₹{sug.estimated_cost.toLocaleString()}</div>
                </div>
                <div>
                  <div style={{ fontSize: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Lead Time</div>
                  <div style={{ fontWeight: 600 }}>{sug.supplier_lead_time_days} days</div>
                </div>
              </div>
              
              <div style={{ marginTop: 'var(--spacing-md)', fontSize: '13px', color: 'var(--text-muted)', background: 'var(--surface-color)', padding: 'var(--spacing-sm)', borderRadius: 'var(--radius-sm)' }}>
                <strong>AI Reasoning:</strong> {sug.reasoning}
              </div>
            </Card>
          ))
        ) : (
          <div style={{ padding: 'var(--spacing-xl)', color: 'var(--text-muted)' }}>No procurement suggestions currently required.</div>
        )}
      </div>
    </div>
  );
}
