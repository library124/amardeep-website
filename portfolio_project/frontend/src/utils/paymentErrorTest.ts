// Payment Error Handling Test Utility
// This file contains test functions to verify error handling works correctly

import { ErrorUtils } from '../services/ErrorHandlingService';
import { ValidationUtils } from '../services/PaymentValidationService';

// Test data for various error scenarios
export const testErrorScenarios = {
  // Null/undefined errors
  nullError: null,
  undefinedError: undefined,
  
  // Empty object error
  emptyObjectError: {},
  
  // Payment-specific errors
  razorpayError: {
    code: 'PAYMENT_FAILED',
    description: 'Payment was declined by the bank',
    source: 'razorpay',
    step: 'payment_capture',
    reason: 'insufficient_funds',
    metadata: {
      order_id: 'order_test_123',
      payment_id: 'pay_test_456'
    }
  },
  
  // Network errors
  networkError: {
    message: 'Network Error',
    response: {
      status: 500,
      statusText: 'Internal Server Error',
      data: {
        error: 'Server temporarily unavailable'
      }
    }
  },
  
  // Standard JavaScript errors
  standardError: new Error('Something went wrong'),
  typeError: new TypeError('Cannot read property of undefined'),
  
  // API response errors
  apiError: {
    response: {
      status: 400,
      data: {
        error: 'Invalid payment data provided'
      }
    },
    message: 'Request failed with status code 400'
  },
  
  // Timeout errors
  timeoutError: {
    message: 'timeout of 30000ms exceeded',
    code: 'ECONNABORTED'
  },
  
  // String errors
  stringError: 'Payment processing failed',
  
  // Complex nested error
  complexError: {
    error: {
      details: {
        payment: {
          status: 'failed',
          reason: 'card_declined',
          message: 'Your card was declined'
        }
      }
    },
    originalError: new Error('Card processing failed')
  }
};

// Test validation scenarios
export const testValidationScenarios = {
  validPaymentContext: {
    item: {
      id: 1,
      title: 'Test Course',
      price: 1000,
      price_display: '₹1,000',
      currency: 'INR'
    },
    itemType: 'course' as const,
    formData: {
      email: 'test@example.com',
      user_name: 'John Doe',
      user_phone: '+91 9876543210'
    },
    user: { id: 1, email: 'test@example.com' }
  },
  
  invalidEmailContext: {
    item: {
      id: 1,
      title: 'Test Course',
      price: 1000,
      price_display: '₹1,000',
      currency: 'INR'
    },
    itemType: 'course' as const,
    formData: {
      email: 'invalid-email',
      user_name: 'John Doe',
      user_phone: '+91 9876543210'
    },
    user: { id: 1, email: 'test@example.com' }
  },
  
  missingNameContext: {
    item: {
      id: 1,
      title: 'Test Workshop',
      price: 2000,
      price_display: '₹2,000',
      currency: 'INR'
    },
    itemType: 'workshop' as const,
    formData: {
      email: 'test@example.com',
      user_name: '',
      user_phone: '+91 9876543210',
      experience_level: 'beginner'
    },
    user: { id: 1, email: 'test@example.com' }
  }
};

// Test functions
export class PaymentErrorTestSuite {
  // Test error handling for all scenarios
  static testAllErrorScenarios(): void {
    console.log('🧪 Testing Payment Error Handling...\n');
    
    Object.entries(testErrorScenarios).forEach(([scenarioName, error]) => {
      console.log(`Testing scenario: ${scenarioName}`);
      
      try {
        const processed = ErrorUtils.handlePaymentError(error, `Test: ${scenarioName}`);
        
        console.log(`✅ Processed successfully:`);
        console.log(`   User Message: ${processed.userMessage}`);
        console.log(`   Code: ${processed.code}`);
        console.log(`   Severity: ${processed.severity}`);
        console.log('');
        
      } catch (testError) {
        console.error(`❌ Error processing scenario ${scenarioName}:`, testError);
        console.log('');
      }
    });
  }
  
  // Test validation scenarios
  static testValidationScenarios(): void {
    console.log('🧪 Testing Payment Validation...\n');
    
    Object.entries(testValidationScenarios).forEach(([scenarioName, context]) => {
      console.log(`Testing validation scenario: ${scenarioName}`);
      
      try {
        const validation = ValidationUtils.validatePaymentContext(context);
        
        console.log(`${validation.isValid ? '✅' : '❌'} Validation result:`);
        console.log(`   Valid: ${validation.isValid}`);
        if (!validation.isValid) {
          console.log(`   Message: ${validation.message}`);
          console.log(`   Code: ${validation.code}`);
        }
        console.log('');
        
      } catch (testError) {
        console.error(`❌ Error in validation scenario ${scenarioName}:`, testError);
        console.log('');
      }
    });
  }
  
  // Test specific error types
  static testSpecificErrorType(errorType: keyof typeof testErrorScenarios): void {
    const error = testErrorScenarios[errorType];
    console.log(`🧪 Testing specific error type: ${errorType}`);
    
    try {
      const processed = ErrorUtils.handlePaymentError(error, `Specific Test: ${errorType}`);
      console.log('✅ Result:', processed);
    } catch (testError) {
      console.error('❌ Test failed:', testError);
    }
  }
  
  // Test error boundary simulation
  static simulateErrorBoundaryScenario(): void {
    console.log('🧪 Simulating Error Boundary Scenario...\n');
    
    try {
      // Simulate a React component error
      throw new Error('Component rendering failed');
    } catch (error) {
      const processed = ErrorUtils.handlePaymentError(error, 'React Error Boundary');
      console.log('✅ Error Boundary handled error:', processed);
    }
  }
  
  // Run comprehensive test suite
  static runComprehensiveTests(): void {
    console.log('🚀 Running Comprehensive Payment Error Handling Tests\n');
    console.log('=' .repeat(60));
    
    this.testAllErrorScenarios();
    console.log('=' .repeat(60));
    
    this.testValidationScenarios();
    console.log('=' .repeat(60));
    
    this.simulateErrorBoundaryScenario();
    console.log('=' .repeat(60));
    
    console.log('✅ All tests completed!');
  }
}

// Utility function to run tests in development
export const runPaymentErrorTests = () => {
  if (process.env.NODE_ENV === 'development') {
    PaymentErrorTestSuite.runComprehensiveTests();
  }
};

// Export for manual testing
export default PaymentErrorTestSuite;