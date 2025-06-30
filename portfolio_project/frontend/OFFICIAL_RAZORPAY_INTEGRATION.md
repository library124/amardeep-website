# Official Razorpay Frontend Integration

This document details the implementation of the official Razorpay frontend integration following SOLID principles and best practices.

## Overview

The implementation uses the official Razorpay Checkout script and follows Razorpay's recommended frontend integration patterns. This ensures compatibility, security, and access to all Razorpay features.

## Architecture

### Core Components

#### 1. RazorpayConfigManager (`src/lib/razorpayConfig.ts`)
- **Purpose**: Manages Razorpay configuration and creates checkout options
- **Pattern**: Singleton Pattern
- **Features**:
  - Official Razorpay checkout options interface
  - Environment-based configuration
  - Comprehensive checkout customization
  - TypeScript interfaces for type safety

#### 2. RazorpayService (`src/lib/razorpayService.ts`)
- **Purpose**: Handles official Razorpay script loading and checkout
- **Pattern**: Singleton + Factory Pattern
- **Features**:
  - Dynamic script loading from official CDN
  - Official Razorpay checkout integration
  - Event handling and error management
  - Payment response validation

#### 3. PaymentService (`src/lib/paymentService.ts`)
- **Purpose**: Unified payment orchestration
- **Pattern**: Singleton Pattern
- **Features**:
  - Integration with official Razorpay service
  - Mock payment for development
  - Order creation and success handling
  - Multi-item type support

## Official Razorpay Features Implemented

### 1. Checkout Options
```typescript
interface RazorpayCheckoutOptions {
  key: string;                    // Razorpay Key ID
  amount: number;                 // Amount in paise
  currency: string;               // Currency code
  name: string;                   // Company name
  description: string;            // Payment description
  image?: string;                 // Company logo
  order_id: string;              // Order ID from backend
  handler: (response) => void;    // Success callback
  prefill: {                     // Pre-filled customer data
    name: string;
    email: string;
    contact: string;
  };
  notes?: object;                // Custom notes
  theme: {                       // UI customization
    color: string;
  };
  modal: {                       // Modal behavior
    ondismiss: () => void;
    confirm_close?: boolean;
    animation?: boolean;
  };
  retry?: {                      // Retry configuration
    enabled: boolean;
    max_count?: number;
  };
  send_sms_hash?: boolean;       // SMS hash for OTP
  allow_rotation?: boolean;      // Screen rotation
  remember_customer?: boolean;   // Remember customer
  timeout?: number;              // Payment timeout
  readonly?: {                   // Read-only fields
    email?: boolean;
    contact?: boolean;
    name?: boolean;
  };
}
```

### 2. Payment Response
```typescript
interface RazorpayPaymentResponse {
  razorpay_payment_id: string;   // Payment ID
  razorpay_order_id: string;     // Order ID
  razorpay_signature: string;    // Payment signature
}
```

### 3. Error Handling
```typescript
interface RazorpayError {
  code: string;                  // Error code
  description: string;           // Error description
  source: string;                // Error source
  step: string;                  // Payment step
  reason: string;                // Failure reason
  metadata: {                    // Additional data
    order_id: string;
    payment_id: string;
  };
}
```

## Implementation Details

### 1. Script Loading
```typescript
public loadScript(): Promise<boolean> {
  return new Promise((resolve, reject) => {
    // Check if already loaded
    if (this.isAvailable()) {
      resolve(true);
      return;
    }

    // Load official script
    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.async = true;
    script.crossOrigin = 'anonymous';
    
    script.onload = () => resolve(true);
    script.onerror = () => reject(new Error('Failed to load'));
    
    document.head.appendChild(script);
  });
}
```

### 2. Checkout Integration
```typescript
public async openCheckout(
  order: PaymentOrder,
  userInfo: PaymentUserInfo,
  callbacks: PaymentCallbacks
): Promise<void> {
  // Load script
  await this.loadScript();
  
  // Create options
  const options = razorpayConfig.createCheckoutOptions(
    order, userInfo, callbacks.onSuccess, callbacks.onError
  );
  
  // Create instance
  const razorpay = new window.Razorpay(options);
  
  // Add event listeners
  razorpay.on('payment.failed', callbacks.onError);
  
  // Open checkout
  razorpay.open();
}
```

### 3. Amount Formatting
```typescript
public formatAmountForRazorpay(amount: number, currency: string = 'INR'): number {
  // Razorpay expects amount in smallest currency unit
  if (currency === 'INR') {
    return Math.round(amount * 100); // Convert to paise
  }
  return amount;
}
```

## Configuration

### Environment Variables
```env
# Required for production
NEXT_PUBLIC_RAZORPAY_KEY_ID=rzp_test_your_key_id

# Optional
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
```

### Razorpay Dashboard Setup
1. Create account at https://dashboard.razorpay.com/
2. Get API keys from Settings > API Keys
3. Configure webhooks for payment verification
4. Set up payment methods and currencies

## Usage Examples

### Basic Payment
```typescript
import { paymentService } from '../lib/paymentService';

const handlePayment = async () => {
  try {
    const order = await paymentService.createOrder({
      item_id: courseId,
      item_type: 'course',
      email: user.email
    });

    await paymentService.openCheckout(
      order,
      (response) => console.log('Success:', response),
      (error) => console.log('Error:', error),
      { name: user.name, email: user.email, phone: user.phone }
    );
  } catch (error) {
    console.error('Payment failed:', error);
  }
};
```

### Using PaymentButton Component
```tsx
import PaymentButton from '../components/PaymentButton';

<PaymentButton
  item={course}
  itemType="course"
  onPaymentSuccess={(result) => {
    console.log('Payment successful:', result);
  }}
  onPaymentError={(error) => {
    console.error('Payment failed:', error);
  }}
/>
```

## Security Features

### 1. Payment Verification
- Server-side signature verification required
- Payment ID validation
- Order ID matching
- Amount verification

### 2. Environment Security
- Key ID stored in environment variables
- No sensitive data in client code
- HTTPS required for production

### 3. Error Handling
- Comprehensive error catching
- User-friendly error messages
- Detailed logging for debugging

## Development vs Production

### Development Mode
- Mock payments when Razorpay key not configured
- Clear development indicators
- No real transactions
- Easy testing workflow

### Production Mode
- Official Razorpay checkout
- Real payment processing
- Complete error handling
- Production security measures

## Testing

### Test Cards (Razorpay Test Mode)
```
Success: 4111 1111 1111 1111
Failure: 4000 0000 0000 0002
CVV: Any 3 digits
Expiry: Any future date
```

### Test UPI IDs
```
Success: success@razorpay
Failure: failure@razorpay
```

### Test Wallets
- Paytm, PhonePe, Google Pay available in test mode

## Error Scenarios Handled

1. **Script Loading Failures**
   - Network issues
   - CDN unavailability
   - Browser compatibility

2. **Payment Failures**
   - Insufficient funds
   - Card declined
   - Network timeout
   - User cancellation

3. **Configuration Errors**
   - Missing API key
   - Invalid order data
   - Server communication issues

## Performance Optimizations

1. **Script Loading**
   - Async loading
   - Duplicate prevention
   - Error recovery

2. **Memory Management**
   - Singleton patterns
   - Event cleanup
   - Instance management

3. **User Experience**
   - Loading states
   - Error feedback
   - Retry mechanisms

## Compliance and Standards

### PCI DSS Compliance
- No card data stored locally
- Razorpay handles sensitive data
- Secure communication channels

### Data Privacy
- Minimal data collection
- User consent handling
- GDPR compliance ready

### Accessibility
- Keyboard navigation support
- Screen reader compatibility
- High contrast support

## Monitoring and Analytics

### Payment Tracking
```typescript
// Track payment attempts
analytics.track('payment_initiated', {
  item_type: order.item_type,
  amount: order.amount,
  currency: order.currency
});

// Track payment success
analytics.track('payment_completed', {
  payment_id: response.razorpay_payment_id,
  order_id: response.razorpay_order_id
});
```

### Error Monitoring
```typescript
// Log payment errors
logger.error('Payment failed', {
  error: error.code,
  description: error.description,
  order_id: error.metadata.order_id
});
```

## Future Enhancements

1. **Advanced Features**
   - Subscription payments
   - EMI options
   - International payments
   - Multi-currency support

2. **UI Improvements**
   - Custom checkout themes
   - Mobile optimization
   - Progressive web app support

3. **Analytics Integration**
   - Payment funnel analysis
   - Conversion tracking
   - A/B testing support

## Troubleshooting

### Common Issues

1. **Script Not Loading**
   - Check network connectivity
   - Verify CDN accessibility
   - Check browser console for errors

2. **Payment Not Opening**
   - Verify API key configuration
   - Check order data format
   - Ensure HTTPS in production

3. **Payment Failures**
   - Check test card details
   - Verify amount format (paise)
   - Check server-side order creation

### Debug Mode
```typescript
// Enable debug logging
localStorage.setItem('razorpay_debug', 'true');
```

This implementation provides a robust, secure, and feature-complete integration with the official Razorpay payment system while maintaining clean architecture and following SOLID principles.