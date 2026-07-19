"use client";

import React, { useEffect, useState } from 'react';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import { ArrowDown } from 'lucide-react';
import { getShipmentDelays, fetchAPI, triggerDemoDelay } from '@/lib/api';

export default function ShipmentsScreen() {
  const [delays, setDelays] = useState<any>(null);
  const [impacts, setImpacts] = useState<any>({});
  const [loading, setLoading] = useState(true);

  async function loadData() {
    setLoading(true);
    try {
      const delaysData = await getShipmentDelays();
      setDelays(delaysData);
      
      const delayedShipments = delaysData.shipments.filter((s:any) => s.status === 'DELAYED');
      const impactPromises = delayedShipments.map((s:any) => fetchAPI(`/shipments/${s.shipment_id}/impact`));
      const impactResults = await Promise.all(impactPromises);
      
      const impactMap:any = {};
      delayedShipments.forEach((s:any, idx:number) => {
        impactMap[s.shipment_id] = impactResults[idx];
      });
      setImpacts(impactMap);
    } catch (err) {
      console.error("Failed to load shipment data", err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  const handleTrigger = async () => {
    await triggerDemoDelay();
    await loadData();
  };

  const delayedList = delays?.shipments?.filter((s:any) => s.status === 'DELAYED') || [];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-xl)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1 style={{ marginBottom: '8px' }}>Shipment Disruptions</h1>
          <p style={{ color: 'var(--text-muted)' }}>Tracking delays and calculating downstream impact on customer orders.</p>
        </div>
        <Button variant="accent" onClick={handleTrigger}>Trigger Disruption</Button>
      </div>

      {loading ? (
        <div style={{ padding: 'var(--spacing-xl)', color: 'var(--text-muted)' }}>Calculating disruption cascades...</div>
      ) : delayedList.length > 0 ? (
        delayedList.map((shipment: any, idx: number) => {
          const impact = impacts[shipment.shipment_id]?.cascade_analysis;
          
          return (
            <Card key={shipment.shipment_id} variant="elevated" className="animate-enter" style={{ animationDelay: `${idx * 100}ms` }}>
              <h2 style={{ fontSize: '1.25rem', marginBottom: 'var(--spacing-lg)' }}>Disruption Cascade Simulator</h2>
              
              <div style={{ 
                display: 'flex', 
                flexDirection: 'column', 
                alignItems: 'center', 
                padding: 'var(--spacing-xl)',
                background: 'var(--bg-cream)',
                borderRadius: 'var(--radius-lg)',
                border: 'var(--border-hairline)'
              }}>
                {/* Level 1: Shipment */}
                <div style={{ padding: 'var(--spacing-md) var(--spacing-xl)', border: '1px solid var(--accent-red)', borderRadius: 'var(--radius-lg)', background: 'rgba(217, 56, 30, 0.05)', color: 'var(--accent-red)', fontWeight: 600 }}>
                  Delay: Shipment {shipment.shipment_id} ({shipment.delay_days} Days Late)
                  <div style={{ fontSize: '12px', fontWeight: 400, marginTop: '4px', textAlign: 'center' }}>{shipment.reasoning}</div>
                </div>
                
                <ArrowDown size={24} style={{ color: 'var(--text-muted)', margin: 'var(--spacing-md) 0' }} />
                
                {/* Level 2: Product */}
                <div style={{ padding: 'var(--spacing-md) var(--spacing-xl)', border: 'var(--border-hairline)', borderRadius: 'var(--radius-lg)', background: 'var(--surface-color)', fontWeight: 600 }}>
                  Impacts: {impacts[shipment.shipment_id]?.product_name || shipment.product_id} Stock
                </div>

                <ArrowDown size={24} style={{ color: 'var(--text-muted)', margin: 'var(--spacing-md) 0' }} />
                
                {/* Level 3: Orders */}
                <div style={{ display: 'flex', gap: 'var(--spacing-lg)' }}>
                  <div style={{ padding: 'var(--spacing-md)', border: 'var(--border-hairline)', borderRadius: 'var(--radius-lg)', background: 'var(--surface-color)', textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', fontFamily: 'var(--font-serif)', color: 'var(--text-ink)' }}>
                      {impact?.affected_customer_orders || 0}
                    </div>
                    <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Customer Orders at Risk</div>
                  </div>
                  <div style={{ padding: 'var(--spacing-md)', border: '1px solid var(--accent-red)', borderRadius: 'var(--radius-lg)', background: 'rgba(217, 56, 30, 0.05)', textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', fontFamily: 'var(--font-serif)', color: 'var(--accent-red)' }}>
                      ₹{(impact?.business_impact?.revenue_at_risk || 0).toLocaleString()}
                    </div>
                    <div style={{ fontSize: '12px', color: 'var(--accent-red)' }}>Revenue at Risk</div>
                  </div>
                </div>
              </div>
            </Card>
          );
        })
      ) : (
        <Card variant="outlined">
          <div style={{ padding: 'var(--spacing-xl)', textAlign: 'center', color: 'var(--text-muted)' }}>
            No delayed shipments detected. All logistics are operating normally.
          </div>
        </Card>
      )}
    </div>
  );
}
