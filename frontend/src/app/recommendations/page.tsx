"use client";

import React, { useEffect, useState } from 'react';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import { getRecommendations, fetchAPI } from '@/lib/api';

export default function RecommendationsScreen() {
  const [data, setData] = useState<any>(null);
  const [messages, setMessages] = useState<any>({});
  const [loading, setLoading] = useState(true);
  const [drafting, setDrafting] = useState<any>({});

  useEffect(() => {
    async function loadData() {
      try {
        const res = await getRecommendations();
        setData(res);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleDraftMessage = async (recId: string) => {
    setDrafting((prev:any) => ({ ...prev, [recId]: true }));
    try {
      const res = await fetchAPI(`/recommendations/${recId}/message`, { method: 'POST' });
      setMessages((prev:any) => ({ ...prev, [recId]: res.message }));
    } catch (err) {
      console.error(err);
    } finally {
      setDrafting((prev:any) => ({ ...prev, [recId]: false }));
    }
  };

  const recs = data?.recommendations || [];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-xl)' }}>
      <div>
        <h1 style={{ marginBottom: '8px' }}>Action Recommendations</h1>
        <p style={{ color: 'var(--text-muted)' }}>AI-generated mitigation strategies for active disruptions.</p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-lg)' }}>
        {loading ? (
          <div style={{ padding: 'var(--spacing-xl)', color: 'var(--text-muted)' }}>Loading AI recommendations...</div>
        ) : recs.length > 0 ? (
          recs.map((rec: any, idx: number) => (
            <Card key={rec.recommendation_id} variant="elevated" className="animate-enter" style={{ animationDelay: `${idx * 100}ms` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 'var(--spacing-lg)' }}>
                <div>
                  <h2 style={{ fontSize: '1.25rem', marginBottom: '4px' }}>{rec.recommended_action}</h2>
                  <p style={{ color: 'var(--accent-red)', fontWeight: 500 }}>
                    Trigger: {rec.problem}
                  </p>
                </div>
                <div style={{ background: 'var(--text-ink)', color: 'var(--bg-cream)', padding: '4px 12px', borderRadius: 'var(--radius-pill)', fontSize: '12px', fontWeight: 600 }}>
                  {Math.round(rec.confidence_score * 100)}% Confidence
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 'var(--spacing-xl)' }}>
                <div>
                  <h3 style={{ fontSize: '14px', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: '8px' }}>
                    Agent Reasoning
                  </h3>
                  <p style={{ lineHeight: 1.6 }}>{rec.reasoning_text}</p>

                  <div style={{ marginTop: 'var(--spacing-xl)' }}>
                    <h3 style={{ fontSize: '14px', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: '8px' }}>
                      Automated Execution
                    </h3>
                    
                    {!messages[rec.recommendation_id] ? (
                      <Button variant="ghost" onClick={() => handleDraftMessage(rec.recommendation_id)} disabled={drafting[rec.recommendation_id]}>
                        {drafting[rec.recommendation_id] ? 'Drafting...' : 'Draft Supplier Update'}
                      </Button>
                    ) : (
                      <div style={{ background: 'var(--surface-color)', padding: 'var(--spacing-md)', borderRadius: 'var(--radius-md)', border: 'var(--border-hairline)' }}>
                        <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '8px' }}>Draft Email to {messages[rec.recommendation_id]?.recipient || 'Supplier'}</div>
                        <p style={{ fontSize: '14px', fontFamily: 'var(--font-serif)', fontStyle: 'italic', color: 'var(--text-ink)', whiteSpace: 'pre-wrap' }}>
                          {messages[rec.recommendation_id]}
                        </p>
                        <div style={{ marginTop: '12px', display: 'flex', gap: '8px' }}>
                          <Button variant="accent">Send Message</Button>
                          <Button variant="ghost">Edit Draft</Button>
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                <div style={{ background: 'var(--bg-cream)', padding: 'var(--spacing-lg)', borderRadius: 'var(--radius-md)', border: 'var(--border-hairline)', height: 'fit-content' }}>
                  <div style={{ fontSize: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Cost Impact</div>
                  <div style={{ fontSize: '24px', fontFamily: 'var(--font-serif)', color: 'var(--text-ink)', marginBottom: '16px' }}>
                    ₹{rec.estimated_cost_impact_inr.toLocaleString()}
                  </div>
                  
                  <div style={{ fontSize: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Current Supplier</div>
                  <div style={{ fontWeight: 600, marginBottom: '16px' }}>{rec.current_supplier}</div>

                  <div style={{ fontSize: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Target Action</div>
                  <div style={{ fontWeight: 600 }}>{rec.recommended_action}</div>
                </div>
              </div>
            </Card>
          ))
        ) : (
          <div style={{ padding: 'var(--spacing-xl)', color: 'var(--text-muted)' }}>No pending recommendations.</div>
        )}
      </div>
    </div>
  );
}
