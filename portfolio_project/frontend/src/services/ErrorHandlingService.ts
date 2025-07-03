// Error Handling Service following SOLID principles
// Single Responsibility: Handles all error processing and logging
// Open/Closed: Extensible for new error types without modification
// Interface Segregation: Separate interfaces for different error concerns
// Dependency Inversion: Depends on abstractions, not concrete implementations

export interface ErrorLogger {
  log(error: any, context?: string): void;
  logWithDetails(error: any, details: any, context?: string): void;
}

export interface ErrorProcessor {
  processError(error: any): ProcessedError;
  extractUserMessage(error: any): string;
}

export interface ProcessedError {
  message: string;
  userMessage: string;
  code: string;
  source: string;
  timestamp: string;
  details: any;
  severity: 'low' | 'medium' | 'high' | 'critical';
}

// Payment-specific error types
export interface PaymentError {
  code?: string;
  description?: string;
  source?: string;
  step?: string;
  reason?: string;
  metadata?: any;
  message?: string;
  originalError?: any;
}

export interface NetworkError {
  response?: {
    status?: number;
    statusText?: string;
    data?: any;
  };
  message?: string;
  stack?: string;
}

// Concrete implementation of error logger
export class ConsoleErrorLogger implements ErrorLogger {
  log(error: any, context: string = 'General'): void {
    console.error(`[${context}] Error:`, error);
  }

  logWithDetails(error: any, details: any, context: string = 'General'): void {
    // Prevent logging empty objects or null/undefined details
    const hasValidDetails = details && 
      typeof details === 'object' && 
      Object.keys(details).length > 0;

    if (hasValidDetails) {
      console.error(`[${context}] Error with details:`, {
        error: this.safeStringify(error),
        details: this.safeStringify(details),
        timestamp: new Date().toISOString()
      });
    } else {
      // Just log the error without empty details
      console.error(`[${context}] Error:`, this.safeStringify(error));
    }
  }

  private safeStringify(obj: any): any {
    try {
      // Handle null/undefined
      if (obj === null || obj === undefined) {
        return obj;
      }

      // Handle primitives
      if (typeof obj !== 'object') {
        return obj;
      }

      // Handle arrays
      if (Array.isArray(obj)) {
        return obj.map(item => this.safeStringify(item));
      }

      // Handle objects
      const result: any = {};
      for (const key in obj) {
        try {
          if (obj.hasOwnProperty(key)) {
            const value = obj[key];
            
            // Skip functions and undefined values
            if (typeof value === 'function' || value === undefined) {
              continue;
            }

            // Handle circular references and complex objects
            if (typeof value === 'object' && value !== null) {
              if (value === obj) {
                result[key] = '[Circular Reference]';
              } else {
                try {
                  result[key] = this.safeStringify(value);
                } catch {
                  result[key] = '[Complex Object]';
                }
              }
            } else {
              result[key] = value;
            }
          }
        } catch {
          result[key] = '[Error accessing property]';
        }
      }
      return result;
    } catch {
      return '[Error stringifying object]';
    }
  }
}

// Concrete implementation of error processor
export class PaymentErrorProcessor implements ErrorProcessor {
  processError(error: any): ProcessedError {
    const timestamp = new Date().toISOString();
    
    // Handle null/undefined errors
    if (!error) {
      return {
        message: 'Unknown error occurred',
        userMessage: 'An unexpected error occurred. Please try again.',
        code: 'UNKNOWN_ERROR',
        source: 'unknown',
        timestamp,
        details: { originalError: error },
        severity: 'medium'
      };
    }

    // Handle payment-specific errors
    if (this.isPaymentError(error)) {
      return this.processPaymentError(error, timestamp);
    }

    // Handle network errors
    if (this.isNetworkError(error)) {
      return this.processNetworkError(error, timestamp);
    }

    // Handle standard JavaScript errors
    if (error instanceof Error) {
      return this.processStandardError(error, timestamp);
    }

    // Handle unknown error types
    return this.processUnknownError(error, timestamp);
  }

  extractUserMessage(error: any): string {
    const processed = this.processError(error);
    return processed.userMessage;
  }

  private isPaymentError(error: any): error is PaymentError {
    return error && (
      typeof error.code === 'string' ||
      typeof error.description === 'string' ||
      typeof error.source === 'string' ||
      typeof error.step === 'string' ||
      typeof error.reason === 'string'
    );
  }

  private isNetworkError(error: any): error is NetworkError {
    return error && (
      error.response ||
      (error.message && (
        error.message.includes('Network Error') ||
        error.message.includes('fetch') ||
        error.message.includes('timeout')
      ))
    );
  }

  private processPaymentError(error: PaymentError, timestamp: string): ProcessedError {
    const code = error.code || 'PAYMENT_ERROR';
    const description = error.description || error.message || 'Payment failed';
    
    let userMessage = 'Payment failed. Please try again.';
    let severity: ProcessedError['severity'] = 'medium';

    // Customize user message based on error type
    if (description.includes('cancelled') || code.includes('CANCELLED')) {
      userMessage = 'Payment was cancelled. You can try again.';
      severity = 'low';
    } else if (description.includes('network') || description.includes('connection')) {
      userMessage = 'Network error. Please check your connection and try again.';
      severity = 'medium';
    } else if (description.includes('timeout')) {
      userMessage = 'Payment timed out. Please try again.';
      severity = 'medium';
    } else if (description.includes('insufficient') || description.includes('declined')) {
      userMessage = 'Payment was declined. Please check your payment method and try again.';
      severity = 'medium';
    } else if (code.includes('INVALID') || description.includes('invalid')) {
      userMessage = 'Invalid payment details. Please check and try again.';
      severity = 'medium';
    } else {
      userMessage = `Payment failed: ${description}`;
      severity = 'high';
    }

    return {
      message: description,
      userMessage,
      code,
      source: error.source || 'payment',
      timestamp,
      details: {
        step: error.step,
        reason: error.reason,
        metadata: error.metadata,
        originalError: error.originalError
      },
      severity
    };
  }

  private processNetworkError(error: NetworkError, timestamp: string): ProcessedError {
    const status = error.response?.status;
    const statusText = error.response?.statusText;
    const message = error.message || 'Network error occurred';
    
    let userMessage = 'Network error. Please check your connection and try again.';
    let code = 'NETWORK_ERROR';
    let severity: ProcessedError['severity'] = 'medium';

    if (status) {
      if (status >= 500) {
        userMessage = 'Server error. Please try again later.';
        code = 'SERVER_ERROR';
        severity = 'high';
      } else if (status === 404) {
        userMessage = 'Service not found. Please contact support.';
        code = 'NOT_FOUND';
        severity = 'high';
      } else if (status === 401 || status === 403) {
        userMessage = 'Authentication error. Please log in again.';
        code = 'AUTH_ERROR';
        severity = 'medium';
      } else if (status >= 400) {
        userMessage = 'Request error. Please check your input and try again.';
        code = 'CLIENT_ERROR';
        severity = 'medium';
      }
    }

    if (message.includes('timeout')) {
      userMessage = 'Request timed out. Please try again.';
      code = 'TIMEOUT_ERROR';
      severity = 'medium';
    }

    return {
      message,
      userMessage,
      code,
      source: 'network',
      timestamp,
      details: {
        status,
        statusText,
        responseData: error.response?.data,
        stack: error.stack
      },
      severity
    };
  }

  private processStandardError(error: Error, timestamp: string): ProcessedError {
    const message = error.message || 'An error occurred';
    let userMessage = 'An unexpected error occurred. Please try again.';
    let code = 'STANDARD_ERROR';
    let severity: ProcessedError['severity'] = 'medium';

    // Customize based on error type
    if (error.name === 'TypeError') {
      code = 'TYPE_ERROR';
      severity = 'high';
    } else if (error.name === 'ReferenceError') {
      code = 'REFERENCE_ERROR';
      severity = 'high';
    } else if (error.name === 'SyntaxError') {
      code = 'SYNTAX_ERROR';
      severity = 'critical';
    }

    return {
      message,
      userMessage,
      code,
      source: 'application',
      timestamp,
      details: {
        name: error.name,
        stack: error.stack
      },
      severity
    };
  }

  private processUnknownError(error: any, timestamp: string): ProcessedError {
    let message = 'Unknown error occurred';
    
    try {
      if (typeof error === 'string') {
        message = error;
      } else if (error && typeof error === 'object') {
        message = error.toString() || JSON.stringify(error) || message;
      }
    } catch {
      // If we can't process the error, use default message
    }

    return {
      message,
      userMessage: 'An unexpected error occurred. Please try again.',
      code: 'UNKNOWN_ERROR',
      source: 'unknown',
      timestamp,
      details: {
        originalError: error,
        errorType: typeof error,
        errorConstructor: error?.constructor?.name
      },
      severity: 'medium'
    };
  }
}

// Main error handling service
export class ErrorHandlingService {
  private static instance: ErrorHandlingService;
  private logger: ErrorLogger;
  private processor: ErrorProcessor;

  private constructor(
    logger: ErrorLogger = new ConsoleErrorLogger(),
    processor: ErrorProcessor = new PaymentErrorProcessor()
  ) {
    this.logger = logger;
    this.processor = processor;
  }

  public static getInstance(): ErrorHandlingService {
    if (!ErrorHandlingService.instance) {
      ErrorHandlingService.instance = new ErrorHandlingService();
    }
    return ErrorHandlingService.instance;
  }

  // Main method to handle any error
  public handleError(error: any, context: string = 'General'): ProcessedError {
    const processed = this.processor.processError(error);
    
    // Log the error with context
    this.logger.logWithDetails(error, processed, context);
    
    return processed;
  }

  // Extract user-friendly message from error
  public getUserMessage(error: any): string {
    return this.processor.extractUserMessage(error);
  }

  // Log error without processing
  public logError(error: any, context: string = 'General'): void {
    this.logger.log(error, context);
  }

  // Check if error is critical
  public isCriticalError(error: any): boolean {
    const processed = this.processor.processError(error);
    return processed.severity === 'critical';
  }
}

// Export singleton instance
export const errorHandlingService = ErrorHandlingService.getInstance();

// Utility functions for common error handling patterns
export const ErrorUtils = {
  // Handle payment errors specifically
  handlePaymentError: (error: any, context: string = 'Payment') => {
    return errorHandlingService.handleError(error, context);
  },

  // Handle network errors specifically
  handleNetworkError: (error: any, context: string = 'Network') => {
    return errorHandlingService.handleError(error, context);
  },

  // Get user-friendly message
  getUserMessage: (error: any) => {
    return errorHandlingService.getUserMessage(error);
  },

  // Log error safely
  logError: (error: any, context?: string) => {
    errorHandlingService.logError(error, context);
  },

  // Check if error requires immediate attention
  isCritical: (error: any) => {
    return errorHandlingService.isCriticalError(error);
  }
};