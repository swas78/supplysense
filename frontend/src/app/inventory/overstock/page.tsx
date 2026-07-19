"use client";

import React from 'react';
import Card from '@/components/ui/Card';
import StatTile from '@/components/ui/StatTile';
import Link from 'next/link';
import { ArrowLeft, TrendingDown } from 'lucide-react';

export default function OverstockScreen() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-xl)' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
        <div>
          <Link href="/inventory" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', fontSize: '13px', color: 'var(--text-muted)', marginBottom: '8px', fontWeight: 500 }}>
            <ArrowLeft size={14} /> Back to Inventory
          </Link>
          <h1 style={{ marginBottom: '8px' }}>Overstock Analysis</h1>
          <p style={{ color: 'var(--text-muted)' }}>Identifying excess inventory and tied-up capital.</p>
        </div>
      </div>

      <section style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: 'var(--spacing-lg)'
      }}>
        <StatTile title="Total Excess Units" value={45200} />
        <StatTile title="Wasted Capital (₹)" value={2840000} prefix="₹" trend={5.2} trendLabel="vs last month" />
      </section>

      <Card variant="outlined" className="animate-enter">
        <h2 style={{ fontSize: '1.25rem' }}>Top Overstocked SKUs</h2>
        
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: 'var(--spacing-md)' }}>
          <thead>
            <tr style={{ borderBottom: 'var(--border-hairline)', textAlign: 'left' }}>
              <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>SKU</th>
              <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Warehouse</th>
              <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Current Stock</th>
              <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Excess Units</th>
              <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>₹ Impact</th>
            </tr>
          </thead>
          <tbody>
            <tr style={{ borderBottom: 'var(--border-hairline)' }}>
              <td style={{ padding: 'var(--spacing-md) 0', fontWeight: 500 }}>PROD-089</td>
              <td style={{ padding: 'var(--spacing-md) 0', color: 'var(--text-muted)' }}>Bangalore Hub</td>
              <td style={{ padding: 'var(--spacing-md) 0' }}>8,500 units</td>
              <td style={{ padding: 'var(--spacing-md) 0', color: 'var(--accent-red)', fontWeight: 500 }}>
                +3,200 units
              </td>
              <td style={{ padding: 'var(--spacing-md) 0', fontWeight: 600 }}>₹480,000</td>
            </tr>
          </tbody>
        </table>
      </Card>

    </div>
  );
}
