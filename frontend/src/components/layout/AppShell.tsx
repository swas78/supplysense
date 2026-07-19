"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, 
  Package, 
  AlertTriangle, 
  Truck, 
  MessageSquare,
  ShieldAlert,
  ListOrdered,
  ShoppingCart,
  TrendingUp
} from 'lucide-react';
import styles from './AppShell.module.css';

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  const swastikRoutes = [
    { name: 'Dashboard', path: '/', icon: <LayoutDashboard size={20} /> },
    { name: 'Inventory', path: '/inventory', icon: <Package size={20} /> },
    { name: 'Anomalies', path: '/anomalies', icon: <AlertTriangle size={20} /> },
    { name: 'Shipments', path: '/shipments', icon: <Truck size={20} /> },
  ];

  const tanishkaRoutes = [
    { name: 'Exec Summary', path: '/executive', icon: <TrendingUp size={20} /> },
    { name: 'Suppliers', path: '/suppliers', icon: <ShieldAlert size={20} /> },
    { name: 'Allocation', path: '/allocation', icon: <ListOrdered size={20} /> },
    { name: 'Procurement', path: '/procurement', icon: <ShoppingCart size={20} /> },
  ];

  const [activeAlerts, setActiveAlerts] = useState(0);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const { getShipmentDelays } = await import('@/lib/api');
        const delays = await getShipmentDelays();
        const delayedCount = delays?.shipments?.filter((s:any) => s.status === 'delayed' || s.status === 'DELAYED').length || 0;
        setActiveAlerts(delayedCount);
      } catch (err) {
        console.error("Failed to fetch background alerts", err);
      }
    };
    
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 60000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className={styles.layout}>
      <aside className={styles.sidebar}>
        <div className={styles.brand}>
          <div className={styles.brandName}>
            Supply<span className={styles.brandAccent}>Sense</span>
          </div>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px', fontWeight: 500 }}>
            Acme Corp • Global Network
          </div>
        </div>

        <nav className={styles.nav}>
          <div style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.05em', margin: '16px 8px 8px', color: 'var(--text-muted)' }}>Command Center</div>
          {swastikRoutes.map(route => (
            <Link 
              key={route.path} 
              href={route.path}
              className={`${styles.navLink} ${pathname === route.path ? styles.active : ''}`}
            >
              {route.icon}
              {route.name}
            </Link>
          ))}
          
          <div style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.05em', margin: '24px 8px 8px', color: 'var(--text-muted)' }}>Strategic Operations</div>
          {tanishkaRoutes.map(route => (
            <Link 
              key={route.path} 
              href={route.path}
              className={`${styles.navLink} ${pathname === route.path ? styles.active : ''}`}
            >
              {route.icon}
              {route.name}
            </Link>
          ))}
        </nav>
      </aside>

      <main className={styles.main}>
        <header className={styles.topbar}>
          <div style={{ fontSize: '13px', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#2e7d32', boxShadow: '0 0 8px #2e7d32' }}></div>
            Live Sync Active <span style={{ margin: '0 8px', color: 'var(--border-hairline)' }}>|</span> 
            {activeAlerts > 0 ? (
              <span style={{ color: 'var(--accent-red)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span className="pulse-alert" style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--accent-red)' }}></span>
                {activeAlerts} Critical Disruptions
              </span>
            ) : (
              <span style={{ color: '#2e7d32', fontWeight: 600 }}>0 Active Alerts</span>
            )}
          </div>
          <div>
            <button 
              className="ghost-btn" 
              style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
              onClick={async () => {
                const { triggerDemoDelay } = await import('@/lib/api');
                await triggerDemoDelay();
                window.location.reload();
              }}
            >
              <AlertTriangle size={16} /> Trigger Disruption
            </button>
          </div>
        </header>
        <div className={`${styles.content} animate-enter`}>
          {children}
        </div>
      </main>
    </div>
  );
}
