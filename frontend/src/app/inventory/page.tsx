"use client";

import React, { useEffect, useState } from 'react';
import Card from '@/components/ui/Card';
import StatTile from '@/components/ui/StatTile';
import Link from 'next/link';
import { PackageOpen, AlertCircle, CheckCircle2 } from 'lucide-react';
import { getInventory } from '@/lib/api';

export default function InventoryScreen() {
  const [inventory, setInventory] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getInventory();
        setInventory(data);
      } catch (error) {
        console.error("Failed to fetch inventory", error);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  // Flatten products for the table
  const allProducts = inventory?.warehouses?.flatMap((wh: any) => 
    wh.products.map((p: any) => ({ ...p, warehouse_name: wh.warehouse_name }))
  ) || [];

  const totalSKUs = allProducts.length;
  const criticalSKUs = allProducts.filter((p: any) => p.status !== 'HEALTHY').length;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-xl)' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
        <div>
          <h1 style={{ marginBottom: '8px' }}>Inventory Monitor</h1>
          <p style={{ color: 'var(--text-muted)' }}>Live stock levels and supply status across all warehouses.</p>
        </div>
        <Link href="/inventory/overstock" className="ghost-btn" style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
          <PackageOpen size={16} /> View Overstock
        </Link>
      </div>

      <section style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: 'var(--spacing-lg)'
      }}>
        <StatTile title="Total SKUs Tracked" value={loading ? '...' : totalSKUs} />
        <StatTile title="SKUs Below Safety" value={loading ? '...' : criticalSKUs} trend={-2} trendLabel="vs yesterday" />
        <StatTile title="Predicted Stockouts (7D)" value={loading ? '...' : criticalSKUs > 0 ? 2 : 0} />
      </section>

      <Card variant="outlined" className="animate-enter">
        <h2 style={{ fontSize: '1.25rem' }}>Stock Levels by Warehouse</h2>
        
        {loading ? (
          <div style={{ padding: 'var(--spacing-xl)', color: 'var(--text-muted)', textAlign: 'center' }}>Loading inventory telemetry...</div>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: 'var(--spacing-md)' }}>
            <thead>
              <tr style={{ borderBottom: 'var(--border-hairline)', textAlign: 'left' }}>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>SKU</th>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Warehouse</th>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Current Stock</th>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Safety Stock</th>
                <th style={{ padding: 'var(--spacing-md) 0', fontWeight: 600, color: 'var(--text-muted)' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {allProducts.map((p: any) => (
                <tr key={`${p.warehouse_name}-${p.product_id}`} style={{ borderBottom: 'var(--border-hairline)' }}>
                  <td style={{ padding: 'var(--spacing-md) 0', fontWeight: 500 }}>
                    {p.product_id}
                    <div style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 400 }}>{p.product_name}</div>
                  </td>
                  <td style={{ padding: 'var(--spacing-md) 0', color: 'var(--text-muted)' }}>{p.warehouse_name}</td>
                  <td style={{ padding: 'var(--spacing-md) 0' }}>{p.stock_on_hand} units</td>
                  <td style={{ padding: 'var(--spacing-md) 0', color: 'var(--text-muted)' }}>{p.safety_stock} units</td>
                  <td style={{ padding: 'var(--spacing-md) 0', color: p.status === 'HEALTHY' ? '#2e7d32' : 'var(--accent-red)', fontWeight: 500 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                      {p.status === 'HEALTHY' ? <CheckCircle2 size={14} /> : <AlertCircle size={14} />} 
                      {p.status}
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
