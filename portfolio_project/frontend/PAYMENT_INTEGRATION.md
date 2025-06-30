# Payment Integration Guide

This document explains the Razorpay payment integration implemented in the portfolio project, following SOLID principles.

## Architecture Overview

The payment system is built with a modular, extensible architecture:

### Core Components

1. **RazorpayConfigManager** (`src/lib/razorpayConfig.ts`)
   - Singleton pattern for configuration management
   - Handles Razorpay options creation
   - Environment variable validation

2. **RazorpayService** (`src/lib/razorpayService.ts`)
   - Handles Razorpay SDK loading and integration
   - Implements PaymentProvider interface
   - Manages checkout process

3. **PaymentService** (`src/lib/paymentService.ts`)
   - Unified service for all payment types (courses, workshops, services)
   - Handles order creation and payment success
   - Supports both mock and real payments

4. **PaymentButton** (`src/components/PaymentButton.tsx`)
   - Reusable payment button component
   - Supports different variants and sizes
   - Integrates with UnifiedPaymentModal

5. **UnifiedPaymentModal** (`src/components/UnifiedPaymentModal.tsx`)
   - Modal for payment processing
   - Handles different item types with specific forms
   - Integrates with payment services

## SOLID Principles Implementation

### Single Responsibility Principle (SRP)
- Each class has one reason to change
- `RazorpayConfigManager`: Only manages configuration
- `RazorpayService`: Only handles Razorpay integration
- `PaymentService`: Only manages payment flow

### Open/Closed Principle (OCP)
- Easy to extend for new payment providers
- PaymentButton supports new variants without modification
- Payment types can be extended without changing core logic

### Liskov Substitution Principle (LSP)
- PaymentProvider interface can be implemented by different providers
- All payment handlers follow the same contract

### Interface Segregation Principle (ISP)
- Separate interfaces for different concerns
- PaymentProvider, PaymentHandler interfaces are focused
- No client depends on methods it doesn't use

### Dependency Inversion Principle (DIP)
- High-level modules don't depend on low-level modules
- PaymentService depends on abstractions, not concrete implementations
- Easy to mock for testing

## Setup Instructions

### 1. Environment Configuration

Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_RAZORPAY_KEY_ID=your_razorpay_key_id_here
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
```

### 2. Razorpay Account Setup

1. Create a Razorpay account at https://dashboard.razorpay.com/
2. Get your Key ID from the API Keys section
3. Add the Key ID to your environment variables

### 3. Backend Integration

Ensure your Django backend has the corresponding endpoints:
- `/api/create-order/` - For course orders
- `/api/workshop-order/` - For workshop orders  
- `/api/service-order/` - For service orders
- `/api/payment-success/` - For payment verification

## Usage Examples

### Basic Payment Button

```tsx
import PaymentButton from '../components/PaymentButton';

<PaymentButton
  item={course}
  itemType="course"
  onPaymentSuccess={(result) => console.log('Success:', result)}
  onPaymentError={(error) => console.log('Error:', error)}
/>
```

### Custom Payment Button

```tsx
<PaymentButton
  item={workshop}
  itemType="workshop"
  variant="outline"
  size="lg"
  className="custom-class"
  onPaymentSuccess={handleSuccess}
  onPaymentError={handleError}
>
  Join Workshop Now
</PaymentButton>
```

### Direct Payment Service Usage

```tsx
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
      (response) => console.log('Payment successful:', response),
      (error) => console.log('Payment failed:', error),
      { name: user.name, email: user.email }
    );
  } catch (error) {
    console.error('Payment initiation failed:', error);
  }
};
```

## Development vs Production

### Development Mode
- When `NEXT_PUBLIC_RAZORPAY_KEY_ID` is not set, the system uses mock payments
- Mock payments show a confirmation dialog instead of real payment
- Useful for testing without actual transactions

### Production Mode
- Requires valid Razorpay Key ID
- Uses real Razorpay checkout
- Handles actual payment processing

## Error Handling

The system includes comprehensive error handling:

1. **Configuration Errors**: Missing Razorpay key ID
2. **Network Errors**: API failures, timeout issues
3. **Payment Errors**: User cancellation, payment failures
4. **Validation Errors**: Invalid form data

## Security Considerations

1. **Environment Variables**: Sensitive data stored in environment variables
2. **Payment Verification**: Server-side payment verification required
3. **User Authentication**: Payment requires authenticated users
4. **Data Validation**: Client and server-side validation

## Testing

### Mock Payment Testing
```bash
# Set environment for mock payments
NODE_ENV=development
# Don't set NEXT_PUBLIC_RAZORPAY_KEY_ID

# Run the application
npm run dev
```

### Real Payment Testing
```bash
# Set environment for real payments
NODE_ENV=development
NEXT_PUBLIC_RAZORPAY_KEY_ID=your_test_key_id

# Run the application
npm run dev
```

## Troubleshooting

### Common Issues

1. **Payment Modal Not Opening**
   - Check if Razorpay script is loaded
   - Verify environment variables
   - Check browser console for errors

2. **Mock Payments Not Working**
   - Ensure `NEXT_PUBLIC_RAZORPAY_KEY_ID` is not set in development
   - Check browser console for configuration messages

3. **Real Payments Failing**
   - Verify Razorpay Key ID is correct
   - Check network connectivity
   - Ensure backend endpoints are working

### Debug Mode

Enable debug logging by setting:
```env
NODE_ENV=development
```

This will show additional console logs for payment flow debugging.

## Future Enhancements

1. **Multiple Payment Providers**: Easy to add PayPal, Stripe, etc.
2. **Payment Analytics**: Track payment success rates
3. **Subscription Payments**: Recurring payment support
4. **Mobile Optimization**: Enhanced mobile payment experience
5. **Offline Payment**: Support for offline payment methods