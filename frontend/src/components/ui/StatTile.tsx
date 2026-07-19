"use client";

import React, { useEffect, useState, useRef } from 'react';
import Card from './Card';
import styles from './StatTile.module.css';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';

interface StatTileProps {
  title: string;
  value: number;
  prefix?: string;
  suffix?: string;
  trend?: number;
  trendLabel?: string;
}

export default function StatTile({ title, value, prefix = '', suffix = '', trend, trendLabel }: StatTileProps) {
  const [displayValue, setDisplayValue] = useState(0);
  const elementRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      const [entry] = entries;
      if (entry.isIntersecting) {
        let start = 0;
        const duration = 1500;
        const increment = value / (duration / 16);
        
        const timer = setInterval(() => {
          start += increment;
          if (start >= value) {
            setDisplayValue(value);
            clearInterval(timer);
          } else {
            setDisplayValue(Math.floor(start));
          }
        }, 16);
        
        observer.disconnect();
      }
    });
    
    if (elementRef.current) {
      observer.observe(elementRef.current);
    }
    
    return () => observer.disconnect();
  }, [value]);

  return (
    <Card variant="outlined">
      <div className={styles.tile} ref={elementRef}>
        <div className={styles.title}>{title}</div>
        <div className={styles.valueContainer}>
          <div className={styles.value}>
            {prefix}{displayValue.toLocaleString()}
          </div>
          {suffix && <div className={styles.suffix}>{suffix}</div>}
        </div>
        {trend !== undefined && (
          <div className={`${styles.trend} ${trend > 0 ? styles.positive : trend < 0 ? styles.negative : ''}`}>
            {trend > 0 ? <ArrowUpRight size={14} /> : trend < 0 ? <ArrowDownRight size={14} /> : null}
            {Math.abs(trend)}% {trendLabel}
          </div>
        )}
      </div>
    </Card>
  );
}
