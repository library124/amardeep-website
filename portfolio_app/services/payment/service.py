"""
Main payment service facade following SOLID principles
"""
from typing import Dict, Any

from .interfaces import PaymentRequest, PaymentResponse, PaymentCompletionRequest, PaymentType
from .gateways import PaymentGatewayFactory
from .repositories import PaymentRepository, ItemRepository
from .validators import PaymentValidationService
from .processors import PaymentProcessor
from .notifications import NotificationServiceFactory


class PaymentService:
    """Main payment service facade"""
    
    def __init__(self, gateway_type: str = "razorpay", notification_type: str = "email"):
        # Initialize dependencies
        self.gateway = PaymentGatewayFactory.create_gateway(gateway_type)
        self.payment_repository = PaymentRepository()
        self.item_repository = ItemRepository()
        self.validation_service = PaymentValidationService(self.item_repository)
        self.notification_service = NotificationServiceFactory.create_service(notification_type)
        
        # Initialize processor
        self.processor = PaymentProcessor(
            self.gateway,
            self.payment_repository,
            self.item_repository,
            self.validation_service
        )
    
    def create_order(self, order_data: Dict[str, Any]) -> PaymentResponse:
        """Create payment order"""
        # Convert order data to PaymentRequest
        request = PaymentRequest(
            item_id=str(order_data.get('item_id', '')),
            item_type=PaymentType(order_data.get('item_type', 'course')),
            amount=float(order_data.get('amount', 0)),
            currency=order_data.get('currency', 'INR'),
            customer_name=order_data.get('customer_name', 'Guest User'),
            customer_email=order_data.get('customer_email', ''),
            customer_phone=order_data.get('customer_phone', ''),
            user_id=order_data.get('user_id'),
            additional_data=order_data.get('additional_data', {})
        )
        
        return self.processor.process_payment_request(request)
    
    def complete_payment(self, completion_data: Dict[str, Any]) -> PaymentResponse:
        """Complete payment after gateway confirmation"""
        # Convert completion data to PaymentCompletionRequest
        request = PaymentCompletionRequest(
            payment_id=completion_data.get('payment_id', ''),
            gateway_payment_id=completion_data.get('razorpay_payment_id', ''),
            gateway_order_id=completion_data.get('razorpay_order_id', ''),
            gateway_signature=completion_data.get('razorpay_signature', ''),
            user_id=completion_data.get('user_id')
        )
        
        return self.processor.complete_payment(request)
    
    def create_course_order(self, course_id: str, user=None, email: str = '') -> PaymentResponse:
        """Convenience method for course orders"""
        order_data = {
            'item_id': course_id,
            'item_type': 'course',
            'customer_name': user.get_full_name() if user else 'Guest User',
            'customer_email': user.email if user else email,
            'user_id': user.id if user else None
        }
        
        # Get course to set amount
        course = self.item_repository.get_item_by_id(course_id, PaymentType.COURSE)
        if course:
            order_data['amount'] = float(course.price)
            order_data['currency'] = course.currency
        
        return self.create_order(order_data)
    
    def create_workshop_order(self, workshop_id: str, application_data: Dict[str, Any]) -> PaymentResponse:
        """Convenience method for workshop orders"""
        workshop = self.item_repository.get_item_by_id(workshop_id, PaymentType.WORKSHOP)
        if not workshop:
            return PaymentResponse(success=False, error_message="Workshop not found")
        
        order_data = {
            'item_id': workshop_id,
            'item_type': 'workshop',
            'amount': float(workshop.price) if workshop.is_paid else 0,
            'currency': workshop.currency,
            'customer_name': application_data.get('user_name', 'Guest User'),
            'customer_email': application_data.get('email', ''),
            'customer_phone': application_data.get('user_phone', ''),
            'additional_data': {
                'experience_level': application_data.get('experience_level', 'beginner'),
                'motivation': application_data.get('motivation', '')
            }
        }
        
        return self.create_order(order_data)
    
    def create_service_order(self, service_id: str, booking_data: Dict[str, Any]) -> PaymentResponse:
        """Convenience method for service orders"""
        service = self.item_repository.get_item_by_id(service_id, PaymentType.SERVICE)
        if not service:
            return PaymentResponse(success=False, error_message="Service not found")
        
        order_data = {
            'item_id': service_id,
            'item_type': 'service',
            'amount': float(service.price),
            'currency': service.currency,
            'customer_name': booking_data.get('user_name', 'Guest User'),
            'customer_email': booking_data.get('email', ''),
            'customer_phone': booking_data.get('user_phone', ''),
            'additional_data': {
                'message': booking_data.get('message', ''),
                'preferred_contact_method': booking_data.get('preferred_contact_method', 'whatsapp'),
                'preferred_time': booking_data.get('preferred_time', '')
            }
        }
        
        return self.create_order(order_data)