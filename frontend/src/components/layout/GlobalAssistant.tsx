"use client";

import React, { useState, useRef, useEffect } from 'react';
import Button from '@/components/ui/Button';
import { Send, Bot, User, MessageSquare, X } from 'lucide-react';
import { sendChatQuery } from '@/lib/api';

export default function GlobalAssistant() {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<any[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [conversationId] = useState(() => typeof crypto !== 'undefined' ? crypto.randomUUID() : Math.random().toString(36).substring(7));
  
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    try {
      const res = await sendChatQuery(userMessage.content, conversationId);
      const botMessage = {
        role: 'bot',
        content: res.response,
        trace: res.reasoning_trace || []
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [...prev, { role: 'bot', content: "An error occurred while connecting to the SupplySense API." }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <>
      <button 
        onClick={() => setIsOpen(true)}
        style={{
          position: 'fixed',
          bottom: 'var(--spacing-xl)',
          right: 'var(--spacing-xl)',
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          background: 'var(--text-ink)',
          color: 'var(--bg-cream)',
          border: 'none',
          boxShadow: 'var(--shadow-elevated)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          zIndex: 999,
          transition: 'transform var(--transition-fast)'
        }}
      >
        <MessageSquare size={24} />
      </button>

      <div style={{
        position: 'fixed',
        top: 0,
        right: 0,
        height: '100vh',
        width: '450px',
        background: 'rgba(249, 247, 243, 0.95)',
        backdropFilter: 'blur(24px)',
        WebkitBackdropFilter: 'blur(24px)',
        borderLeft: 'var(--border-hairline)',
        boxShadow: '-12px 0 24px rgba(0,0,0,0.1)',
        zIndex: 1000,
        transform: isOpen ? 'translateX(0)' : 'translateX(100%)',
        transition: 'transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)',
        display: 'flex',
        flexDirection: 'column'
      }}>
        <div style={{ padding: 'var(--spacing-xl)', borderBottom: 'var(--border-hairline)', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <h2 style={{ fontSize: '1.25rem', marginBottom: '4px' }}>SupplySense AI</h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '13px', margin: 0 }}>Ask anything about your global supply chain.</p>
          </div>
          <button onClick={() => setIsOpen(false)} style={{ background: 'transparent', border: 'none', cursor: 'pointer', color: 'var(--text-muted)' }}>
            <X size={24} />
          </button>
        </div>

        <div style={{ flex: 1, overflowY: 'auto', padding: 'var(--spacing-xl)', display: 'flex', flexDirection: 'column', gap: 'var(--spacing-lg)' }}>
          
          {messages.length === 0 && (
            <div style={{ textAlign: 'center', color: 'var(--text-muted)', marginTop: '20px' }}>
              <Bot size={32} style={{ margin: '0 auto 16px', opacity: 0.5 }} />
              <p>Hi! I'm your SupplySense AI.<br/>Ask me about shortages, anomalies, or supplier performance.</p>
            </div>
          )}

          {messages.map((m, idx) => (
            <div key={idx} style={{ display: 'flex', gap: '16px' }}>
              {m.role === 'user' ? (
                <>
                  <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'var(--bg-cream)', border: 'var(--border-hairline)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <User size={16} />
                  </div>
                  <div style={{ flex: 1, paddingTop: '4px' }}>
                    <div style={{ fontWeight: 600, marginBottom: '4px' }}>You</div>
                    <div style={{ fontSize: '14px', lineHeight: 1.5 }}>{m.content}</div>
                  </div>
                </>
              ) : (
                <>
                  <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'var(--accent-red)', color: 'var(--bg-cream)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Bot size={16} />
                  </div>
                  <div style={{ flex: 1, paddingTop: '4px' }}>
                    <div style={{ fontWeight: 600, marginBottom: '8px' }}>SupplySense AI</div>
                    
                    {m.trace && m.trace.length > 0 && (
                      <div style={{ padding: 'var(--spacing-md)', background: 'var(--surface-color)', border: 'var(--border-hairline)', borderRadius: 'var(--radius-lg)', marginBottom: '12px', fontSize: '13px', color: 'var(--text-muted)' }}>
                        {m.trace.map((step: string, i: number) => {
                          if (step.includes("dispatch_purchase_order")) {
                            return (
                              <div key={i} style={{ padding: '8px', background: 'rgba(46, 125, 50, 0.1)', borderLeft: '3px solid #2e7d32', marginBottom: '4px', color: '#2e7d32', fontWeight: 500 }}>
                                ✓ Tool Executed: Purchase Order Dispatched
                              </div>
                            );
                          }
                          if (step.includes("send_supplier_message")) {
                            return (
                              <div key={i} style={{ padding: '8px', background: 'rgba(0, 102, 204, 0.1)', borderLeft: '3px solid #0066cc', marginBottom: '4px', color: '#0066cc', fontWeight: 500 }}>
                                ✉ Tool Executed: Email Sent to Supplier
                              </div>
                            );
                          }
                          if (step.includes("denied") || step.toLowerCase().includes("policy")) {
                            return (
                              <div key={i} style={{ padding: '8px', background: 'rgba(217, 56, 30, 0.1)', borderLeft: '3px solid var(--accent-red)', marginBottom: '4px', color: 'var(--accent-red)', fontWeight: 500 }}>
                                ⚠ Action Blocked: Safety Policy Violated
                              </div>
                            );
                          }
                          return <div key={i} style={{ fontFamily: 'monospace', marginBottom: '2px', wordBreak: 'break-word' }}>&gt; {step}</div>;
                        })}
                      </div>
                    )}
                    
                    <div style={{ fontSize: '14px', lineHeight: 1.6 }}>{m.content}</div>
                  </div>
                </>
              )}
            </div>
          ))}

          {isTyping && (
            <div style={{ display: 'flex', gap: '16px' }}>
              <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'var(--accent-red)', color: 'var(--bg-cream)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Bot size={16} />
              </div>
              <div style={{ flex: 1, paddingTop: '4px' }}>
                <div style={{ fontWeight: 600, marginBottom: '8px' }}>SupplySense AI</div>
                <div style={{ fontSize: '14px', color: 'var(--text-muted)' }}>Analyzing telemetry data...</div>
              </div>
            </div>
          )}
          <div ref={endOfMessagesRef} />
        </div>

        <form onSubmit={handleSend} style={{ padding: 'var(--spacing-lg)', borderTop: 'var(--border-hairline)', display: 'flex', gap: 'var(--spacing-md)', background: 'var(--surface-color)' }}>
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your question..." 
            style={{ 
              flex: 1, 
              padding: '12px 16px', 
              borderRadius: 'var(--radius-pill)', 
              border: 'var(--border-hairline)', 
              background: 'var(--bg-cream)',
              fontFamily: 'var(--font-sans)',
              fontSize: '14px'
            }} 
          />
          <Button variant="accent" style={{ borderRadius: 'var(--radius-pill)', padding: '12px' }} disabled={isTyping || !input.trim()}>
            <Send size={18} />
          </Button>
        </form>
      </div>
    </>
  );
}
