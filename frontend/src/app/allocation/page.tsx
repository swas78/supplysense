"use client";

import React, { useEffect, useState } from 'react';
import Card from '@/components/ui/Card';
import StatTile from '@/components/ui/StatTile';
import { getAllocationPriority } from '@/lib/api';

export default function AllocationScreen() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const res = await getAllocationPriority('p1'); // Example fixed product
        setData(res);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-xl)' }}>
      <div>
        <h1 style={{ marginBottom: '8px' }}>Inventory Allocation</h1>
        <p style={{ color: 'var(--text-muted)' }}>AI-driven priority routing when pending demand exceeds available stock.</p>
      </div>

      <section style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: 'var(--spacing-lg)'
      }}>
        <StatTile title="Available Stock" value={loading ? '...' : data?.available_stock || 0} suffix=" units" />
        <StatTile title="Pending Demand" value={loading ? '...' : data?.total_pending_demand || 0} suffix=" units" trend={loading ? 0 : data?.shortage ? -data.shortage : 0} trendLabel="shortage" />
        <StatTile title="Affected SKU" value={loading ? '...' : data?.product_id || 'N/A'} />
      </section>

      {loading ? (
        <div style={{ padding: 'var(--spacing-xl)', color: 'var(--text-muted)' }}>Calculating optimal allocation routes...</div>
      ) : (
        <Card variant="outlined" className="animate-enter">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--spacing-md)' }}>
            <h2 style={{ fontSize: '1.25rem' }}>Priority Queue: {data?.product_name || 'Unknown'}</h2>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)', background: 'var(--bg-cream)', padding: '6px 12px', borderRadius: 'var(--radius-pill)', border: 'var(--border-hairline)' }}>
              {data?.summary || 'Allocation model output'}
            </div>
          </div>
          
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: 'var(--border-hairline)', textAlign: 'left' }}>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Rank</th>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Order ID</th>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Required By</th>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Requested</th>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Allocated</th>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {data?.allocation_plan?.map((plan: any) => (
                <tr key={plan.order_id} style={{ borderBottom: 'var(--border-hairline)' }}>
                  <td style={{ padding: 'var(--spacing-md) 0', fontWeight: 600 }}>#{plan.priority_rank}</td>
                  <td style={{ padding: 'var(--spacing-md) 0', fontWeight: 500 }}>
                    {plan.order_id}
                    <div style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 400 }}>{plan.reasoning}</div>
                  </td>
                  <td style={{ padding: 'var(--spacing-md) 0', color: plan.days_until_required <= 2 ? 'var(--accent-red)' : 'var(--text-muted)' }}>
                    {plan.required_by_date}
                  </td>
                  <td style={{ padding: 'var(--spacing-md) 0' }}>{plan.requested_quantity}</td>
                  <td style={{ padding: 'var(--spacing-md) 0', fontWeight: 600 }}>{plan.allocated_quantity}</td>
                  <td style={{ padding: 'var(--spacing-md) 0' }}>
                    <span style={{ 
                      padding: '4px 8px', 
                      borderRadius: '4px', 
                      fontSize: '12px', 
                      fontWeight: 600,
                      background: plan.status === 'FULFILLED' ? '#e8f5e9' : plan.status === 'PARTIAL' ? '#fff3e0' : 'rgba(217, 56, 30, 0.1)',
                      color: plan.status === 'FULFILLED' ? '#2e7d32' : plan.status === 'PARTIAL' ? '#f57c00' : 'var(--accent-red)'
                    }}>
                      {plan.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      )}
    </div>
  );
}
