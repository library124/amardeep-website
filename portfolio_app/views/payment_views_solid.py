"""
SOLID-compliant payment views using service layer architecture
"""
import logging
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services.payment.service import PaymentService

logger = logging.getLogger(__name__)


class BasePaymentView(APIView):
    """Base payment view with common functionality"""
    permission_classes = (permissions.AllowAny,)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payment_service = PaymentService()
    
    def handle_payment_response(self, payment_response) -> Response:
        """Convert PaymentResponse to DRF Response"""
        if payment_response.success:
            response_data = {
                'order_id': payment_response.order_id,
                'payment_id': payment_response.payment_id,
                'amount': payment_response.amount,
                'currency': payment_response.currency,
            }
            
            if payment_response.additional_data:
                response_data.update(payment_response.additional_data)
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': payment_response.error_message}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class CreateCourseOrderView(BasePaymentView):
    """Create order for course payment"""
    
    def post(self, request):
        """Handle course order creation"""
        try:
            course_id = request.data.get('course_id')
            user = request.user if request.user.is_authenticated else None
            email = request.data.get('email', 'guest@example.com')
            
            if not course_id:
                return Response(
                    {'error': 'Course ID is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Use service to create order
            payment_response = self.payment_service.create_course_order(course_id, user, email)
            return self.handle_payment_response(payment_response)
            
        except Exception as e:
            logger.error(f"Error creating course order: {e}")
            return Response(
                {'error': 'Failed to create course order'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateWorkshopOrderView(BasePaymentView):
    """Create order for workshop payment"""
    
    def post(self, request):
        """Handle workshop order creation"""
        try:
            workshop_id = request.data.get('workshop_id')
            
            if not workshop_id:
                return Response(
                    {'error': 'Workshop ID is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Prepare application data
            application_data = {
                'user_name': request.data.get('user_name', 'Guest User'),
                'email': request.data.get('email', 'guest@example.com'),
                'user_phone': request.data.get('user_phone', ''),
                'experience_level': request.data.get('experience_level', 'beginner'),
                'motivation': request.data.get('motivation', '')
            }
            
            # Use service to create order
            payment_response = self.payment_service.create_workshop_order(workshop_id, application_data)
            return self.handle_payment_response(payment_response)
            
        except Exception as e:
            logger.error(f"Error creating workshop order: {e}")
            return Response(
                {'error': 'Failed to create workshop order'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateServiceOrderView(BasePaymentView):
    """Create order for service payment"""
    
    def post(self, request):
        """Handle service order creation"""
        try:
            service_id = request.data.get('service_id')
            
            if not service_id:
                return Response(
                    {'error': 'Service ID is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Prepare booking data
            booking_data = {
                'user_name': request.data.get('user_name', 'Guest User'),
                'email': request.data.get('email', 'guest@example.com'),
                'user_phone': request.data.get('user_phone', ''),
                'message': request.data.get('message', ''),
                'preferred_contact_method': request.data.get('preferred_contact_method', 'whatsapp'),
                'preferred_time': request.data.get('preferred_time', '')
            }
            
            # Use service to create order
            payment_response = self.payment_service.create_service_order(service_id, booking_data)
            return self.handle_payment_response(payment_response)
            
        except Exception as e:
            logger.error(f"Error creating service order: {e}")
            return Response(
                {'error': 'Failed to create service order'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentSuccessView(BasePaymentView):
    """Handle payment success for all payment types"""
    
    def post(self, request):
        """Handle payment completion"""
        try:
            payment_id = request.data.get('payment_id')
            
            if not payment_id:
                return Response(
                    {'error': 'Payment ID is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Prepare completion data
            completion_data = {
                'payment_id': payment_id,
                'razorpay_payment_id': request.data.get('razorpay_payment_id', f"pay_mock_{payment_id}"),
                'razorpay_order_id': request.data.get('razorpay_order_id'),
                'razorpay_signature': request.data.get('razorpay_signature', 'mock_signature'),
                'user_id': request.user.id if request.user.is_authenticated else None
            }
            
            # Use service to complete payment
            payment_response = self.payment_service.complete_payment(completion_data)
            return self.handle_payment_response(payment_response)
            
        except Exception as e:
            logger.error(f"Error processing payment success: {e}")
            return Response(
                {'error': 'Failed to process payment'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Legacy view names for backward compatibility
CreateOrderView = CreateCourseOrderView
PaymentSuccessView = PaymentSuccessView
WorkshopOrderView = CreateWorkshopOrderView
ServiceOrderView = CreateServiceOrderView
EnhancedPaymentSuccessView = PaymentSuccessView