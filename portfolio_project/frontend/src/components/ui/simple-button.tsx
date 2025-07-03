"use client";

import React from "react";
import { cn } from "@/lib/utils";

// Simple Button Component following SOLID principles
// Single Responsibility: Renders a clean, modern button without animations
// Open/Closed: Extensible through props and className
// Interface Segregation: Clean props interface
// Dependency Inversion: Depends on React abstractions

interface SimpleButtonProps {
  children: React.ReactNode;
  as?: React.ElementType;
  className?: string;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  [key: string]: any;
}

export const SimpleButton: React.FC<SimpleButtonProps> = ({
  children,
  as: Component = "button",
  className,
  variant = 'primary',
  size = 'md',
  ...otherProps
}) => {
  // Base styles following design system principles
  const baseStyles = "inline-flex items-center justify-center font-semibold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";
  
  // Variant styles - Open/Closed Principle
  const variantStyles = {
    primary: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500 shadow-lg hover:shadow-xl",
    secondary: "bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500 shadow-lg hover:shadow-xl",
    outline: "border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white focus:ring-blue-500"
  };
  
  // Size styles - Interface Segregation Principle
  const sizeStyles = {
    sm: "px-4 py-2 text-sm rounded-lg",
    md: "px-6 py-3 text-base rounded-xl",
    lg: "px-8 py-4 text-lg rounded-2xl"
  };
  
  return (
    <Component
      className={cn(
        baseStyles,
        variantStyles[variant],
        sizeStyles[size],
        className
      )}
      {...otherProps}
    >
      {children}
    </Component>
  );
};

export default SimpleButton;