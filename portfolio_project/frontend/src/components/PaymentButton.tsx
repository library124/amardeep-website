'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import UnifiedPaymentModal from './UnifiedPaymentModal';

// Interface Segregation Principle - separate interfaces for different item types
interface BasePaymentItem {
  id: number;
  price: number;
  price_display: string;
  currency?: string;
}

interface CoursePaymentItem extends BasePaymentItem {
  title: string;
  slug: string;
  is_full?: boolean;
}

interface WorkshopPaymentItem extends BasePaymentItem {
  name: string;
  is_full?: boolean;
  spots_remaining?: number;
}

interface ServicePaymentItem extends BasePaymentItem {
  name: string;
  description?: string;
}

type PaymentItem = CoursePaymentItem | WorkshopPaymentItem | ServicePaymentItem;

interface PaymentButtonProps {
  item: PaymentItem;
  itemType: 'course' | 'workshop' | 'service';
  onPaymentSuccess?: (result: any) => void;
  onPaymentError?: (error: any) => void;
  disabled?: boolean;
  className?: string;
  children?: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
}

// Single Responsibility Principle - handles only payment button logic
const PaymentButton: React.FC<PaymentButtonProps> = ({
  item,
  itemType,
  onPaymentSuccess,
  onPaymentError,
  disabled = false,
  className = '',
  children,
  variant = 'primary',
  size = 'md'
}) => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Open Closed Principle - easy to extend button variants
  const getButtonClasses = () => {
    const baseClasses = 'font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2';
    
    const sizeClasses = {
      sm: 'px-3 py-2 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg'
    };

    const variantClasses = {
      primary: 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 focus:ring-blue-500',
      secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500',
      outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white focus:ring-blue-500'
    };

    const disabledClasses = 'opacity-50 cursor-not-allowed';

    return `${baseClasses} ${sizeClasses[size]} ${variantClasses[variant]} ${disabled ? disabledClasses : ''} ${className}`;
  };

  const handleClick = () => {
    if (disabled) return;
    setIsModalOpen(true);
  };

  const handlePaymentSuccess = (result: any) => {
    setIsModalOpen(false);
    onPaymentSuccess?.(result);
  };

  const handlePaymentError = (error: any) => {
    onPaymentError?.(error);
  };

  const getButtonText = () => {
    if (children) return children;

    // Check if item is full (for courses and workshops)
    const isFull = 'is_full' in item && item.is_full;
    
    if (isFull) {
      return itemType === 'course' ? 'Course Full' : 'Workshop Full';
    }

    switch (itemType) {
      case 'course':
        return `Enroll Now - ${item.price_display}`;
      case 'workshop':
        return `Join Workshop - ${item.price_display}`;
      case 'service':
        return `Book Service - ${item.price_display}`;
      default:
        return `Pay ${item.price_display}`;
    }
  };

  const isItemFull = 'is_full' in item && item.is_full;
  const isDisabled = disabled || isItemFull;

  return (
    <>
      <motion.button
        onClick={handleClick}
        disabled={isDisabled}
        className={getButtonClasses()}
        whileHover={!isDisabled ? { scale: 1.02 } : {}}
        whileTap={!isDisabled ? { scale: 0.98 } : {}}
        transition={{ type: "spring", stiffness: 400, damping: 17 }}
      >
        {getButtonText()}
      </motion.button>

      {isModalOpen && (
        <UnifiedPaymentModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          onSuccess={handlePaymentSuccess}
          item={item}
          itemType={itemType}
          onError={handlePaymentError}
        />
      )}
    </>
  );
};

export default PaymentButton;