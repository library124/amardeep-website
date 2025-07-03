"""
Razorpay payment views following SOLID principles
"""
import uuid
import logging
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from ..models import Workshop, WorkshopApplication, TradingService, ServiceBooking, Payment, Course, PurchasedCourse
from ..services.payment.service import PaymentService
from ..services.payment.interfaces import PaymentRequest, PaymentCompletionRequest, PaymentType
from ..services.payment.exceptions import (
    PaymentException, PaymentValidationError, PaymentGatewayError, 
    PaymentNotFoundError, PaymentAlreadyProcessedError
)

logger = logging.getLogger(__name__)


class BasePaymentView(APIView):
    """Base payment view with common functionality"""
    permission_classes = (permissions.AllowAny,)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payment_service = PaymentService(gateway_type="razorpay")
    
    def handle_payment_exception(self, e: Exception) -> Response:
        """Handle payment exceptions consistently"""
        if isinstance(e, PaymentValidationError):
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(e, PaymentGatewayError):
            return Response({'error': 'Payment gateway error. Please try again.'}, status=status.HTTP_502_BAD_GATEWAY)
        elif isinstance(e, PaymentNotFoundError):
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        elif isinstance(e, PaymentAlreadyProcessedError):
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error(f"Unexpected payment error: {e}")
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateWorkshopOrderView(BasePaymentView):
    """Create Razorpay order for workshop payment"""

    def post(self, request):
        try:
            # Extract and validate request data
            workshop_id = request.data.get('workshop_id')
            user_name = request.data.get('user_name', 'Guest User')
            user_email = request.data.get('email', 'guest@example.com')
            user_phone = request.data.get('user_phone', '')
            experience_level = request.data.get('experience_level', 'beginner')
            motivation = request.data.get('motivation', '')

            if not workshop_id:
                return Response({'error': 'Workshop ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            if not user_email or '@' not in user_email:
                return Response({'error': 'Valid email is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Get workshop
            try:
                workshop = Workshop.objects.get(id=workshop_id, is_active=True)
            except Workshop.DoesNotExist:
                return Response({'error': 'Workshop not found'}, status=status.HTTP_404_NOT_FOUND)

            if workshop.is_full:
                return Response({'error': 'Workshop is full'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user already applied
            existing_application = WorkshopApplication.objects.filter(
                workshop=workshop,
                email=user_email
            ).first()

            if existing_application:
                return Response({'error': 'You have already applied for this workshop'}, status=status.HTTP_400_BAD_REQUEST)

            # Create workshop application
            application = WorkshopApplication.objects.create(
                workshop=workshop,
                name=user_name,
                email=user_email,
                phone=user_phone,
                experience_level=experience_level,
                motivation=motivation
            )

            if workshop.is_paid:
                # Create payment order using service
                order_data = {
                    'item_id': str(workshop.id),
                    'item_type': 'workshop',
                    'amount': float(workshop.price),
                    'currency': workshop.currency,
                    'customer_name': user_name,
                    'customer_email': user_email,
                    'customer_phone': user_phone,
                    'additional_data': {
                        'experience_level': experience_level,
                        'motivation': motivation,
                        'application_id': str(application.id)
                    }
                }

                payment_response = self.payment_service.create_order(order_data)

                if not payment_response.success:
                    # Clean up application if payment creation fails
                    application.delete()
                    return Response({'error': payment_response.error_message}, status=status.HTTP_400_BAD_REQUEST)

                return Response({
                    'order_id': payment_response.order_id,
                    'amount': payment_response.amount,
                    'currency': payment_response.additional_data.get('currency', workshop.currency),
                    'payment_id': payment_response.payment_id,
                    'item_title': workshop.title,
                    'item_price': workshop.price_display,
                    'item_type': 'workshop',
                    'application_id': application.id,
                    'razorpay_key': self.payment_service.gateway.api_key
                })
            else:
                # Free workshop - auto approve
                application.status = 'approved'
                application.save()
                workshop.registered_count += 1
                workshop.save()

                return Response({
                    'message': 'Successfully registered for free workshop',
                    'application_id': application.id,
                    'requires_payment': False
                })

        except PaymentException as e:
            return self.handle_payment_exception(e)
        except Exception as e:
            logger.error(f"Error creating workshop order: {e}")
            return Response({'error': 'Failed to create workshop order'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateServiceOrderView(BasePaymentView):
    """Create Razorpay order for service payment"""

    def post(self, request):
        try:
            # Extract and validate request data
            service_id = request.data.get('service_id')
            user_name = request.data.get('user_name', 'Guest User')
            user_email = request.data.get('email', 'guest@example.com')
            user_phone = request.data.get('user_phone', '')
            message = request.data.get('message', '')
            preferred_contact_method = request.data.get('preferred_contact_method', 'whatsapp')
            preferred_time = request.data.get('preferred_time', '')

            if not service_id:
                return Response({'error': 'Service ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            if not user_email or '@' not in user_email:
                return Response({'error': 'Valid email is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Get service
            try:
                service = TradingService.objects.get(id=service_id, is_active=True)
            except TradingService.DoesNotExist:
                return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)

            # Create service booking
            booking = ServiceBooking.objects.create(
                service=service,
                name=user_name,
                email=user_email,
                phone=user_phone,
                message=message,
                preferred_contact_method=preferred_contact_method,
                preferred_time=preferred_time
            )

            # Create payment order using service
            order_data = {
                'item_id': str(service.id),
                'item_type': 'service',
                'amount': float(service.price),
                'currency': service.currency,
                'customer_name': user_name,
                'customer_email': user_email,
                'customer_phone': user_phone,
                'additional_data': {
                    'message': message,
                    'preferred_contact_method': preferred_contact_method,
                    'preferred_time': preferred_time,
                    'booking_id': str(booking.id)
                }
            }

            payment_response = self.payment_service.create_order(order_data)

            if not payment_response.success:
                # Clean up booking if payment creation fails
                booking.delete()
                return Response({'error': payment_response.error_message}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'order_id': payment_response.order_id,
                'amount': payment_response.amount,
                'currency': payment_response.additional_data.get('currency', service.currency),
                'payment_id': payment_response.payment_id,
                'item_title': service.name,
                'item_price': service.price_display,
                'item_type': 'service',
                'booking_id': booking.id,
                'razorpay_key': self.payment_service.gateway.api_key
            })

        except PaymentException as e:
            return self.handle_payment_exception(e)
        except Exception as e:
            logger.error(f"Error creating service order: {e}")
            return Response({'error': 'Failed to create service order'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateCourseOrderView(BasePaymentView):
    """Create Razorpay order for course payment"""

    def post(self, request):
        try:
            # Extract and validate request data
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

            if course.is_full:
                return Response({'error': 'Course is full'}, status=status.HTTP_400_BAD_REQUEST)

            # Create payment order using service
            order_data = {
                'item_id': str(course.id),
                'item_type': 'course',
                'amount': float(course.price),
                'currency': course.currency,
                'customer_name': user.get_full_name() if user else "Guest User",
                'customer_email': user.email if user else email,
                'user_id': user.id if user else None
            }

            payment_response = self.payment_service.create_order(order_data)

            if not payment_response.success:
                return Response({'error': payment_response.error_message}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'order_id': payment_response.order_id,
                'amount': payment_response.amount,
                'currency': payment_response.additional_data.get('currency', course.currency),
                'payment_id': payment_response.payment_id,
                'item_title': course.title,
                'item_price': course.price_display,
                'item_type': 'course',
                'razorpay_key': self.payment_service.gateway.api_key
            })

        except PaymentException as e:
            return self.handle_payment_exception(e)
        except Exception as e:
            logger.error(f"Error creating course order: {e}")
            return Response({'error': 'Failed to create course order'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentSuccessView(BasePaymentView):
    """Handle Razorpay payment success for all payment types"""

    def post(self, request):
        try:
            # Extract payment completion data
            payment_id = request.data.get('payment_id')
            razorpay_payment_id = request.data.get('razorpay_payment_id')
            razorpay_order_id = request.data.get('razorpay_order_id')
            razorpay_signature = request.data.get('razorpay_signature')
            user = request.user if request.user.is_authenticated else None

            if not payment_id:
                return Response({'error': 'Payment ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            if not razorpay_payment_id or not razorpay_order_id or not razorpay_signature:
                return Response({'error': 'Missing Razorpay payment details'}, status=status.HTTP_400_BAD_REQUEST)

            # Complete payment using service
            completion_data = {
                'payment_id': payment_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_signature': razorpay_signature,
                'user_id': user.id if user else None
            }

            payment_response = self.payment_service.complete_payment(completion_data)

            if not payment_response.success:
                return Response({'error': payment_response.error_message}, status=status.HTTP_400_BAD_REQUEST)

            return Response(payment_response.additional_data)

        except PaymentException as e:
            return self.handle_payment_exception(e)
        except Exception as e:
            logger.error(f"Error processing payment success: {e}")
            return Response({'error': 'Failed to process payment'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentWebhookView(APIView):
    """Handle Razorpay webhooks for payment status updates"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            # Verify webhook signature
            webhook_signature = request.META.get('HTTP_X_RAZORPAY_SIGNATURE')
            webhook_body = request.body

            if not webhook_signature:
                return Response({'error': 'Missing webhook signature'}, status=status.HTTP_400_BAD_REQUEST)

            # TODO: Implement webhook signature verification
            # This would involve verifying the webhook using Razorpay's webhook secret

            # Process webhook event
            event_data = request.data
            event_type = event_data.get('event')

            if event_type == 'payment.captured':
                # Handle successful payment
                payment_entity = event_data.get('payload', {}).get('payment', {}).get('entity', {})
                order_id = payment_entity.get('order_id')
                payment_id = payment_entity.get('id')

                # Find and update payment record
                try:
                    payment = Payment.objects.get(razorpay_order_id=order_id)
                    if payment.status != 'completed':
                        payment.mark_completed(
                            gateway_payment_id=payment_id,
                            payment_method='razorpay',
                            gateway_response=payment_entity
                        )
                        logger.info(f"Payment {payment.payment_id} marked as completed via webhook")
                except Payment.DoesNotExist:
                    logger.warning(f"Payment not found for order_id: {order_id}")

            elif event_type == 'payment.failed':
                # Handle failed payment
                payment_entity = event_data.get('payload', {}).get('payment', {}).get('entity', {})
                order_id = payment_entity.get('order_id')

                try:
                    payment = Payment.objects.get(razorpay_order_id=order_id)
                    payment.status = 'failed'
                    payment.gateway_response = payment_entity
                    payment.save()
                    logger.info(f"Payment {payment.payment_id} marked as failed via webhook")
                except Payment.DoesNotExist:
                    logger.warning(f"Payment not found for order_id: {order_id}")

            return Response({'status': 'ok'})

        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return Response({'error': 'Webhook processing failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)