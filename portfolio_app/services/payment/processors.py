"""
Payment processors following SOLID principles
"""
import logging
from typing import Dict, Any
from django.utils import timezone

from .interfaces import (
    IPaymentProcessor, IPaymentGateway, IPaymentRepository, IItemRepository,
    IValidationService, IPostPaymentHandler, PaymentRequest, PaymentResponse,
    PaymentCompletionRequest, PaymentType, PaymentStatus
)
from .handlers import PaymentHandlerFactory

logger = logging.getLogger(__name__)


class PaymentProcessor(IPaymentProcessor):
    """Main payment processor implementation"""
    
    def __init__(
        self,
        gateway: IPaymentGateway,
        payment_repository: IPaymentRepository,
        item_repository: IItemRepository,
        validation_service: IValidationService
    ):
        self.gateway = gateway
        self.payment_repository = payment_repository
        self.item_repository = item_repository
        self.validation_service = validation_service
    
    def process_payment_request(self, request: PaymentRequest) -> PaymentResponse:
        """Process payment request"""
        try:
            # Validate request
            is_valid, error_message = self.validation_service.validate_payment_request(request)
            if not is_valid:
                return PaymentResponse(success=False, error_message=error_message)
            
            # Validate item availability
            is_available, availability_error = self.validation_service.validate_item_availability(
                request.item_id, request.item_type, request.customer_email
            )
            if not is_available:
                return PaymentResponse(success=False, error_message=availability_error)
            
            # Get item details
            item = self.item_repository.get_item_by_id(request.item_id, request.item_type)
            if not item:
                return PaymentResponse(success=False, error_message="Item not found")
            
            # Handle item-specific logic
            related_object = self._handle_item_specific_logic(request, item)
            
            # Create order with gateway
            order_data, gateway_error = self.gateway.create_order(request)
            
            # Create payment record
            payment = self.payment_repository.create_payment_record(
                request, order_data or {}, related_object
            )
            
            # Build response
            return PaymentResponse(
                success=True,
                order_id=order_data.get('id') if order_data else payment.razorpay_order_id,
                payment_id=payment.payment_id,
                amount=order_data.get('amount') if order_data else int(request.amount * 100),
                currency=request.currency,
                additional_data={
                    'item_title': getattr(item, 'title', getattr(item, 'name', 'Unknown')),
                    'item_price': getattr(item, 'price_display', f"{request.currency} {request.amount}"),
                    'item_type': request.item_type.value,
                    'mock': not bool(order_data),
                    'related_object_id': related_object.id if related_object else None
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing payment request: {e}")
            return PaymentResponse(success=False, error_message="Failed to process payment request")
    
    def complete_payment(self, completion_request: PaymentCompletionRequest) -> PaymentResponse:
        """Complete payment after gateway confirmation"""
        try:
            # Get payment record
            payment = self.payment_repository.get_payment_by_id(completion_request.payment_id)
            if not payment:
                return PaymentResponse(success=False, error_message="Payment not found")
            
            if payment.status == 'completed':
                return PaymentResponse(success=False, error_message="Payment already processed")
            
            # Verify payment with gateway
            if not self.gateway.verify_payment(completion_request):
                return PaymentResponse(success=False, error_message="Payment verification failed")
            
            # Update payment status
            gateway_data = {
                'razorpay_payment_id': completion_request.gateway_payment_id,
                'razorpay_order_id': completion_request.gateway_order_id,
                'razorpay_signature': completion_request.gateway_signature,
                'user_id': completion_request.user_id,
                'timestamp': timezone.now().isoformat(),
                'payment_method': 'razorpay'
            }
            
            success = self.payment_repository.update_payment_status(
                completion_request.payment_id, PaymentStatus.COMPLETED, gateway_data
            )
            
            if not success:
                return PaymentResponse(success=False, error_message="Failed to update payment status")
            
            # Handle post-payment actions
            self._handle_post_payment_actions(payment)
            
            # Build success response
            return self._build_completion_response(payment)
            
        except Exception as e:
            logger.error(f"Error completing payment: {e}")
            return PaymentResponse(success=False, error_message="Failed to complete payment")
    
    def _handle_item_specific_logic(self, request: PaymentRequest, item: Any) -> Any:
        """Handle item-specific logic before payment"""
        if request.item_type == PaymentType.WORKSHOP:
            # Create workshop application
            application_data = {
                'name': request.customer_name,
                'email': request.customer_email,
                'phone': request.customer_phone,
                'experience_level': request.additional_data.get('experience_level', 'beginner'),
                'motivation': request.additional_data.get('motivation', '')
            }
            return self.item_repository.create_workshop_application(request.item_id, application_data)
        
        elif request.item_type == PaymentType.SERVICE:
            # Create service booking
            booking_data = {
                'name': request.customer_name,
                'email': request.customer_email,
                'phone': request.customer_phone,
                'message': request.additional_data.get('message', ''),
                'preferred_contact_method': request.additional_data.get('preferred_contact_method', 'whatsapp'),
                'preferred_time': request.additional_data.get('preferred_time', '')
            }
            return self.item_repository.create_service_booking(request.item_id, booking_data)
        
        return None
    
    def _handle_post_payment_actions(self, payment: Any) -> None:
        """Handle post-payment actions"""
        try:
            # Determine payment type
            payment_type = PaymentType(payment.payment_type)
            
            # Get appropriate item
            item = None
            if payment_type == PaymentType.COURSE and payment.course:
                item = payment.course
            elif payment_type == PaymentType.WORKSHOP and payment.workshop_application:
                item = payment.workshop_application.workshop
            elif payment_type == PaymentType.SERVICE and payment.trading_service:
                item = payment.trading_service
            
            if item:
                # Get appropriate handler and execute
                handler = PaymentHandlerFactory.create_handler(payment_type)
                handler.handle_successful_payment(payment, item, payment_type)
            
        except Exception as e:
            logger.error(f"Error in post-payment actions: {e}")
    
    def _build_completion_response(self, payment: Any) -> PaymentResponse:
        """Build payment completion response"""
        additional_data = {
            'message': 'Payment successful!',
            'amount_paid': float(payment.amount),
            'currency': payment.currency,
        }
        
        # Add item-specific data
        payment_type = PaymentType(payment.payment_type)
        
        if payment_type == PaymentType.COURSE and payment.course:
            additional_data.update({
                'item_title': payment.course.title,
                'access_instructions': 'You can now access the course from your dashboard.',
            })
        elif payment_type == PaymentType.WORKSHOP and payment.workshop_application:
            additional_data.update({
                'item_title': payment.workshop_application.workshop.title,
                'access_instructions': 'Workshop details will be sent to your email.',
                'application_id': payment.workshop_application.id
            })
        elif payment_type == PaymentType.SERVICE and payment.trading_service:
            additional_data.update({
                'item_title': payment.trading_service.name,
                'access_instructions': 'We will contact you soon to discuss the service details.',
            })
        
        return PaymentResponse(
            success=True,
            payment_id=payment.payment_id,
            additional_data=additional_data
        )