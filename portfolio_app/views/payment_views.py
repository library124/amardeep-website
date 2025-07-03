import uuid
import requests
import logging
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from ..models import Course, Payment, PurchasedCourse

logger = logging.getLogger(__name__)


class PaymentService:
    """Service class for payment operations following SRP"""
    
    @staticmethod
    def create_beeceptor_order(course, user=None, email=None):
        """Create order using Beeceptor mock API"""
        order_payload = {
            "amount": int(course.price * 100),  # Amount in paise
            "currency": course.currency,
            "receipt": f"course_{course.id}_{uuid.uuid4().hex[:8]}",
            "notes": {
                "course_id": str(course.id),
                "course_name": course.title,
                "user_id": user.id if user else None,
                "user_email": user.email if user else email
            }
        }

        # TODO: Replace with real Razorpay endpoint and add authentication for production
        # For production:
        # - Use https://api.razorpay.com/v1/orders
        # - Add Authorization header with API key
        # - Handle real Razorpay response format
        beeceptor_url = "https://razorpay-mock-api.proxy.beeceptor.com/orders"

        try:
            response = requests.post(beeceptor_url, json=order_payload, timeout=10)
            response.raise_for_status()
            return response.json(), None
        except requests.RequestException as e:
            logger.error(f"Beeceptor request failed: {e}")
            return None, str(e)

    @staticmethod
    def create_payment_record(course, order_data, user=None, email=None, is_mock=False, error=None):
        """Create payment record in database"""
        return Payment.objects.create(
            payment_id=f"PAY_{uuid.uuid4().hex[:12].upper()}",
            razorpay_order_id=order_data.get('id') if order_data else f"order_mock_{uuid.uuid4().hex[:12]}",
            amount=course.price,
            currency=course.currency,
            payment_type='course',
            customer_name=user.get_full_name() if user else "Guest User",
            customer_email=user.email if user else email,
            course=course,
            gateway_response=order_data or {'mock': True, 'error': error}
        )


class CreateOrderView(APIView):
    """Create Razorpay order using Beeceptor mock API"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            # Get course details
            course_id = request.data.get('course_id')
            user = request.user if request.user.is_authenticated else None
            email = request.data.get('email', 'guest@example.com')

            if not course_id:
                return Response({'error': 'Course ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Get course
            try:
                course = Course.objects.get(id=course_id, is_active=True)
            except Course.DoesNotExist:
                return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

            # Check if course is full
            if course.is_full:
                return Response({'error': 'Course is full'}, status=status.HTTP_400_BAD_REQUEST)

            # Create order via service
            order_data, error = PaymentService.create_beeceptor_order(course, user, email)
            
            if order_data:
                # Create payment record
                payment = PaymentService.create_payment_record(course, order_data, user, email)

                return Response({
                    'order_id': order_data.get('id'),
                    'amount': order_data.get('amount'),
                    'currency': order_data.get('currency'),
                    'payment_id': payment.payment_id,
                    'course_title': course.title,
                    'course_price': course.price_display
                })
            else:
                # Fallback to mock response
                payment = PaymentService.create_payment_record(course, None, user, email, is_mock=True, error=error)

                return Response({
                    'order_id': payment.razorpay_order_id,
                    'amount': int(course.price * 100),
                    'currency': course.currency,
                    'payment_id': payment.payment_id,
                    'course_title': course.title,
                    'course_price': course.price_display,
                    'mock': True
                })

        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return Response({'error': 'Failed to create order'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentSuccessView(APIView):
    """Handle payment success and enroll user in course"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            payment_id = request.data.get('payment_id')
            razorpay_payment_id = request.data.get('razorpay_payment_id', f"pay_mock_{uuid.uuid4().hex[:12]}")
            razorpay_order_id = request.data.get('razorpay_order_id')
            razorpay_signature = request.data.get('razorpay_signature', 'mock_signature')
            user = request.user if request.user.is_authenticated else None

            if not payment_id:
                return Response({'error': 'Payment ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Get payment record
            try:
                payment = Payment.objects.get(payment_id=payment_id)
            except Payment.DoesNotExist:
                return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

            if payment.status == 'completed':
                return Response({'error': 'Payment already processed'}, status=status.HTTP_400_BAD_REQUEST)

            # TODO: For production, verify payment signature with Razorpay
            # import hmac
            # import hashlib
            # generated_signature = hmac.new(
            #     key=settings.RAZORPAY_KEY_SECRET.encode(),
            #     msg=f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
            #     digestmod=hashlib.sha256
            # ).hexdigest()
            # if generated_signature != razorpay_signature:
            #     return Response({'error': 'Invalid signature'}, status=400)

            # Mark payment as completed
            gateway_response = {
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_signature': razorpay_signature,
                'user_id': user.id if user else None,
                'timestamp': timezone.now().isoformat()
            }

            payment.mark_completed(
                gateway_payment_id=razorpay_payment_id,
                payment_method='razorpay',
                gateway_response=gateway_response
            )

            # Get the created purchased course
            purchased_course = PurchasedCourse.objects.filter(
                course=payment.course,
                user=user
            ).order_by('-created_at').first()

            return Response({
                'message': 'Payment successful! You are now enrolled in the course.',
                'payment_id': payment.payment_id,
                'course_title': payment.course.title if payment.course else 'Unknown Course',
                'amount_paid': payment.amount,
                'currency': payment.currency,
                'enrollment_id': purchased_course.id if purchased_course else None,
                'access_instructions': 'You can now access the course from your dashboard.'
            })

        except Exception as e:
            logger.error(f"Error processing payment success: {e}")
            return Response({'error': 'Failed to process payment'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
