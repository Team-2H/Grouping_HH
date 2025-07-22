// src/components/ui/card.tsx
import React from "react";

type CardProps = React.HTMLAttributes<HTMLDivElement>;

export const Card: React.FC<CardProps> = ({ className, children, ...props }) => {
  return (
    <div
      className={`bg-white shadow-md rounded p-4 ${className ?? ""}`}
      {...props}
    >
      {children}
    </div>
  );
};

type CardContentProps = React.HTMLAttributes<HTMLDivElement>;

export const CardContent: React.FC<CardContentProps> = ({
  className,
  children,
  ...props
}) => {
  return (
    <div className={`p-2 ${className ?? ""}`} {...props}>
      {children}
    </div>
  );
};
