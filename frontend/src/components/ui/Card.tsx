import React from 'react';
import styles from './Card.module.css';

interface CardProps {
  variant?: 'outlined' | 'elevated';
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
}

export default function Card({ variant = 'outlined', children, className = '', style }: CardProps) {
  return (
    <div className={`${styles.card} ${styles[variant]} ${className}`} style={style}>
      {children}
    </div>
  );
}
