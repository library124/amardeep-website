'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { paymentService, CreateOrderRequest, PaymentOrder } from '../lib/paymentService';
import { useAuth } from '../context/AuthContext';
import { ErrorUtils } from '../services/ErrorHandlingService';
import { ValidationUtils, PaymentValidationContext } from '../services/PaymentValidationService';
import ErrorBoundary from './ErrorBoundary';

interface UnifiedPaymentModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (result: any) => void;
  onError?: (error: any) => void;
  item: {
    id: number;
    title?: string;
    name?: string;
    price: number;
    price_display: string;
    currency?: string;
  };
  itemType: 'course' | 'workshop' | 'service';
  additionalData?: any;
}

const UnifiedPaymentModal: React.FC<UnifiedPaymentModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
  onError,
  item,
  itemType,
  additionalData = {}
}) => {
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    email: user?.email || '',
    user_name: user?.first_name ? `${user.first_name} ${user.last_name}` : '',
    user_phone: '',
    ...additionalData
  });
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    
    // Update form data
    setFormData({
      ...formData,
      [name]: value
    });

    // Real-time field validation
    const validationContext: PaymentValidationContext = {
      item,
      itemType,
      formData: { ...formData, [name]: value },
      user
    };

    const fieldValidation = ValidationUtils.validatePaymentContext(validationContext);
    
    // Clear field error if validation passes, or update with specific field error
    setFieldErrors(prev => {
      const newErrors = { ...prev };
      
      // For now, we'll clear the field error if the overall validation passes
      // In a more sophisticated implementation, we could validate individual fields
      if (fieldValidation.isValid) {
        delete newErrors[name];
      }
      
      return newErrors;
    });

    // Clear general error when user starts typing
    if (error) {
      setError('');
    }
  };

  const handlePayment = async () => {
    try {
      setIsProcessing(true);
      setError('');

      // Validate required fields using comprehensive validation service
      const validationContext: PaymentValidationContext = {
        item,
        itemType,
        formData,
        user
      };

      const validation = ValidationUtils.validatePaymentContext(validationContext);

      if (!validation.isValid) {
        setError(validation.message || 'Please check your input and try again.');
        return;
      }

      // Create order
      const orderData: CreateOrderRequest = {
        item_id: item.id,
        item_type: itemType,
        email: formData.email,
        user_name: formData.user_name,
        user_phone: formData.user_phone,
        additional_data: formData
      };

      const order = await paymentService.createOrder(orderData);

      // Open payment checkout
      await paymentService.openCheckout(
        order,
        async (paymentResponse: any) => {
          try {
            // Handle payment success
            const successData = await paymentService.handlePaymentSuccess({
              payment_id: order.payment_id,
              razorpay_payment_id: paymentResponse.razorpay_payment_id,
              razorpay_order_id: paymentResponse.razorpay_order_id,
              razorpay_signature: paymentResponse.razorpay_signature,
              user_id: user?.id
            });

            onSuccess(successData);
            onClose();
          } catch (err) {
            // Use centralized error handling service
            const processedError = ErrorUtils.handlePaymentError(err, 'Payment Success Processing');
            setError('Payment was successful but there was an error processing it. Please contact support.');
          }
        },
        (error: any) => {
          // Use centralized error handling service
          const processedError = ErrorUtils.handlePaymentError(error, 'Payment Checkout');
          setError(processedError.userMessage);
          onError?.(error);
        },
        {
          name: formData.user_name,
          email: formData.email,
          phone: formData.user_phone
        }
      );
    } catch (err: any) {
      // Use centralized error handling service
      const processedError = ErrorUtils.handlePaymentError(err, 'Payment Initiation');
      setError(processedError.userMessage);
      onError?.(err);
    } finally {
      setIsProcessing(false);
    }
  };

  if (!isOpen) return null;

  const itemTitle = item.title || item.name || 'Item';

  return (
    <ErrorBoundary
      fallback={
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div className="absolute inset-0 bg-black bg-opacity-50" onClick={onClose} />
          <div className="relative bg-white rounded-2xl shadow-2xl max-w-md w-full mx-4 p-6">
            <div className="text-center">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Payment Error</h2>
              <p className="text-gray-600 mb-6">
                There was an error loading the payment form. Please try again.
              </p>
              <button
                onClick={onClose}
                className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      }
    >
      <AnimatePresence>
        <div className="fixed inset-0 z-50 flex items-center justify-center">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="absolute inset-0 bg-black bg-opacity-50"
          onClick={onClose}
        />

        {/* Modal */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="relative bg-white rounded-2xl shadow-2xl max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto"
        >
          {/* Header */}
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Complete Payment</h2>
                <p className="text-gray-600 mt-1">{itemTitle}</p>
              </div>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          {/* Payment Info */}
          <div className="p-6 bg-gray-50 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <span className="text-lg font-medium text-gray-900">Total Amount:</span>
              <span className="text-2xl font-bold text-blue-600">{item.price_display}</span>
            </div>
            <div className="mt-2 text-sm text-gray-600">
              {itemType.charAt(0).toUpperCase() + itemType.slice(1)} Payment
            </div>
          </div>

          {/* Form */}
          <div className="p-6">
            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-start">
                  <svg className="w-5 h-5 text-red-600 mt-0.5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                  <p className="text-red-800 text-sm">{error}</p>
                </div>
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address *
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="your@email.com"
                  required
                />
              </div>

              {(itemType === 'workshop' || itemType === 'service') && (
                <>
                  <div>
                    <label htmlFor="user_name" className="block text-sm font-medium text-gray-700 mb-2">
                      Full Name *
                    </label>
                    <input
                      type="text"
                      id="user_name"
                      name="user_name"
                      value={formData.user_name}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="Your full name"
                      required
                    />
                  </div>

                  <div>
                    <label htmlFor="user_phone" className="block text-sm font-medium text-gray-700 mb-2">
                      Phone Number
                    </label>
                    <input
                      type="tel"
                      id="user_phone"
                      name="user_phone"
                      value={formData.user_phone}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="+91 9876543210"
                    />
                  </div>
                </>
              )}

              {/* Additional fields for workshop */}
              {itemType === 'workshop' && (
                <>
                  <div>
                    <label htmlFor="experience_level" className="block text-sm font-medium text-gray-700 mb-2">
                      Trading Experience *
                    </label>
                    <select
                      id="experience_level"
                      name="experience_level"
                      value={formData.experience_level || 'beginner'}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                    >
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                    </select>
                  </div>

                  <div>
                    <label htmlFor="motivation" className="block text-sm font-medium text-gray-700 mb-2">
                      Why do you want to join this workshop?
                    </label>
                    <textarea
                      id="motivation"
                      name="motivation"
                      rows={3}
                      value={formData.motivation || ''}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                      placeholder="Tell us about your goals..."
                    />
                  </div>
                </>
              )}

              {/* Additional fields for service */}
              {itemType === 'service' && (
                <>
                  <div>
                    <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
                      Message
                    </label>
                    <textarea
                      id="message"
                      name="message"
                      rows={3}
                      value={formData.message || ''}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                      placeholder="Tell us about your requirements..."
                    />
                  </div>

                  <div>
                    <label htmlFor="preferred_contact_method" className="block text-sm font-medium text-gray-700 mb-2">
                      Preferred Contact Method
                    </label>
                    <select
                      id="preferred_contact_method"
                      name="preferred_contact_method"
                      value={formData.preferred_contact_method || 'whatsapp'}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="whatsapp">WhatsApp</option>
                      <option value="call">Phone Call</option>
                      <option value="email">Email</option>
                    </select>
                  </div>
                </>
              )}
            </div>

            {/* Payment Button */}
            <div className="mt-8 flex gap-4">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handlePayment}
                disabled={isProcessing}
                className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isProcessing ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                  </span>
                ) : (
                  `Pay ${item.price_display}`
                )}
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
    </ErrorBoundary>
  );
};

export default UnifiedPaymentModal;