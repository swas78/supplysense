import React from 'react';
import styles from './Button.module.css';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'ghost' | 'primary' | 'accent';
  children: React.ReactNode;
}

export default function Button({ variant = 'ghost', children, className = '', ...props }: ButtonProps) {
  return (
    <button 
      className={`${styles.btn} ${styles[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
