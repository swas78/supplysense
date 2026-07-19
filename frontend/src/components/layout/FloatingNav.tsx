"use client";

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, AlertTriangle, ShieldAlert } from 'lucide-react';
import styles from './FloatingNav.module.css';

export default function FloatingNav() {
  const [isVisible, setIsVisible] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const handleScroll = () => {
      // Show when scrolled down a bit
      if (window.scrollY > 100) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const quickLinks = [
    { name: 'Dashboard', path: '/', icon: <LayoutDashboard size={16} /> },
    { name: 'Disruptions', path: '/shipments', icon: <AlertTriangle size={16} /> },
    { name: 'Suppliers', path: '/suppliers', icon: <ShieldAlert size={16} /> }
  ];

  return (
    <div className={`${styles.floatingNav} ${!isVisible ? styles.hidden : ''}`}>
      {quickLinks.map(link => (
        <Link 
          key={link.path} 
          href={link.path}
          className={`${styles.pillLink} ${pathname === link.path ? styles.active : ''}`}
        >
          {link.icon}
          {link.name}
        </Link>
      ))}
    </div>
  );
}
