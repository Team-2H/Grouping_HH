// src/components/ui/button.tsx
import React from "react";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "outline" | "solid";
};

export const Button: React.FC<ButtonProps> = ({
  className,
  variant = "solid",
  ...props
}) => {
  const base = "px-4 py-2 rounded text-white font-medium";
  const variants = {
    solid: "bg-blue-600 hover:bg-blue-700",
    outline: "bg-white border border-gray-400 text-black hover:bg-gray-100",
  };

  return (
    <button
      className={`${base} ${variants[variant]} ${className ?? ""}`}
      {...props}
    />
  );
};
