
import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export const Card: React.FC<CardProps> = ({ children, className }) => {
  return (
    <div className={`bg-slate-800 border border-slate-700 rounded-2xl shadow-xl ${className}`}>
      {children}
    </div>
  );
};

interface CardContentProps {
  children: React.ReactNode;
  className?: string;
}
export const CardContent: React.FC<CardContentProps> = ({ children, className }) => {
    return (
        <div className={`p-2 ${className}`}>
            {children}
        </div>
    );
};
