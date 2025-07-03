'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ApiUtils } from '../utils/api';

// Interface for API status following Interface Segregation Principle
interface ApiStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  message: string;
  isHealthy: boolean;
  lastChecked?: string;
}

// Props interface following Single Responsibility Principle
interface ApiStatusIndicatorProps {
  showDetails?: boolean;
  autoRefresh?: boolean;
  refreshInterval?: number;
  className?: string;
}

// API Status Indicator Component following SOLID principles
const ApiStatusIndicator: React.FC<ApiStatusIndicatorProps> = ({
  showDetails = false,
  autoRefresh = true,
  refreshInterval = 30000, // 30 seconds
  className = ''
}) => {
  const [apiStatus, setApiStatus] = useState<ApiStatus>({
    status: 'healthy',
    message: 'Checking API status...',
    isHealthy: true
  });
  const [isLoading, setIsLoading] = useState(true);
  const [showTooltip, setShowTooltip] = useState(false);

  // Check API status
  const checkApiStatus = async () => {
    try {
      setIsLoading(true);
      const status = await ApiUtils.getStatus();
      setApiStatus({
        ...status,
        lastChecked: new Date().toLocaleTimeString()
      });
    } catch (error) {
      setApiStatus({
        status: 'unhealthy',
        message: 'Unable to connect to API',
        isHealthy: false,
        lastChecked: new Date().toLocaleTimeString()
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Effect for initial load and auto-refresh
  useEffect(() => {
    checkApiStatus();

    if (autoRefresh) {
      const interval = setInterval(checkApiStatus, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [autoRefresh, refreshInterval]);

  // Get status color based on API health
  const getStatusColor = () => {
    switch (apiStatus.status) {
      case 'healthy':
        return 'text-green-600 bg-green-100';
      case 'degraded':
        return 'text-yellow-600 bg-yellow-100';
      case 'unhealthy':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  // Get status icon
  const getStatusIcon = () => {
    if (isLoading) {
      return (
        <svg className="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      );
    }

    switch (apiStatus.status) {
      case 'healthy':
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
        );
      case 'degraded':
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        );
      case 'unhealthy':
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
        );
      default:
        return null;
    }
  };

  // Compact indicator (default)
  if (!showDetails) {
    return (
      <div 
        className={`relative inline-flex items-center ${className}`}
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
      >
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium ${getStatusColor()}`}
        >
          {getStatusIcon()}
          <span className="hidden sm:inline">API</span>
        </motion.div>

        {/* Tooltip */}
        <AnimatePresence>
          {showTooltip && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg shadow-lg whitespace-nowrap z-50"
            >
              <div className="font-medium">{apiStatus.status.toUpperCase()}</div>
              <div>{apiStatus.message}</div>
              {apiStatus.lastChecked && (
                <div className="text-gray-300">Last checked: {apiStatus.lastChecked}</div>
              )}
              <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    );
  }

  // Detailed indicator
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-white rounded-lg shadow-lg border border-gray-200 p-4 ${className}`}
    >
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-gray-900">API Status</h3>
        <button
          onClick={checkApiStatus}
          disabled={isLoading}
          className="text-gray-500 hover:text-gray-700 transition-colors disabled:opacity-50"
        >
          <svg className={`w-5 h-5 ${isLoading ? 'animate-spin' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>

      <div className="space-y-3">
        {/* Status Badge */}
        <div className={`inline-flex items-center space-x-2 px-3 py-2 rounded-full text-sm font-medium ${getStatusColor()}`}>
          {getStatusIcon()}
          <span>{apiStatus.status.toUpperCase()}</span>
        </div>

        {/* Status Message */}
        <p className="text-gray-600">{apiStatus.message}</p>

        {/* Last Checked */}
        {apiStatus.lastChecked && (
          <p className="text-xs text-gray-500">
            Last checked: {apiStatus.lastChecked}
          </p>
        )}

        {/* Actions */}
        {!apiStatus.isHealthy && (
          <div className="pt-3 border-t border-gray-200">
            <p className="text-sm text-gray-600 mb-2">
              The API is currently unavailable. The application will use cached data when possible.
            </p>
            <button
              onClick={checkApiStatus}
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              Retry Connection
            </button>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default ApiStatusIndicator;