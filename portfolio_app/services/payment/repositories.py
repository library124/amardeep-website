"""
Repository implementations for payment data access following SOLID principles
"""
import uuid
from typing import Dict, Any, Optional
from django.utils import timezone

from .interfaces import IPaymentRepository, IItemRepository, PaymentRequest, PaymentType, PaymentStatus
from ...models import Payment, Course, Workshop, TradingService, WorkshopApplication, ServiceBooking


class PaymentRepository(IPaymentRepository):
    """Payment repository implementation"""
    
    def create_payment_record(self, request: PaymentRequest, order_data: Dict[str, Any], 
                            related_object: Any = None) -> Payment:
        """Create payment record in database"""
        payment_data = {
            'payment_id': f"PAY_{uuid.uuid4().hex[:12].upper()}",
            'razorpay_order_id': order_data.get('id') if order_data else f"order_mock_{uuid.uuid4().hex[:12]}",
            'amount': request.amount,
            'currency': request.currency,
            'payment_type': request.item_type.value,
            'customer_name': request.customer_name,
            'customer_email': request.customer_email,
            'customer_phone': request.customer_phone,
            'gateway_response': order_data or {'mock': True}
        }
        
        # Add specific relationships based on item type
        if request.item_type == PaymentType.COURSE:
            item = self._get_course(request.item_id)
            payment_data['course'] = item
        elif request.item_type == PaymentType.WORKSHOP:
            payment_data['workshop_application'] = related_object
        elif request.item_type == PaymentType.SERVICE:
            item = self._get_service(request.item_id)
            payment_data['trading_service'] = item
        
        return Payment.objects.create(**payment_data)
    
    def get_payment_by_id(self, payment_id: str) -> Optional[Payment]:
        """Get payment record by ID"""
        try:
            return Payment.objects.get(payment_id=payment_id)
        except Payment.DoesNotExist:
            return None
    
    def update_payment_status(self, payment_id: str, status: PaymentStatus, 
                            gateway_data: Dict[str, Any]) -> bool:
        """Update payment status"""
        try:
            payment = self.get_payment_by_id(payment_id)
            if not payment:
                return False
            
            payment.status = status.value
            payment.gateway_response.update(gateway_data)
            
            if status == PaymentStatus.COMPLETED:
                payment.completed_at = timezone.now()
                payment.gateway_payment_id = gateway_data.get('razorpay_payment_id', '')
                payment.payment_method = gateway_data.get('payment_method', 'razorpay')
            
            payment.save()
            return True
        except Exception:
            return False
    
    def _get_course(self, course_id: str) -> Optional[Course]:
        """Get course by ID"""
        try:
            return Course.objects.get(id=course_id, is_active=True)
        except Course.DoesNotExist:
            return None
    
    def _get_service(self, service_id: str) -> Optional[TradingService]:
        """Get service by ID"""
        try:
            return TradingService.objects.get(id=service_id, is_active=True)
        except TradingService.DoesNotExist:
            return None


class ItemRepository(IItemRepository):
    """Item repository implementation"""
    
    def get_item_by_id(self, item_id: str, item_type: PaymentType) -> Optional[Any]:
        """Get item by ID and type"""
        try:
            if item_type == PaymentType.COURSE:
                return Course.objects.get(id=item_id, is_active=True)
            elif item_type == PaymentType.WORKSHOP:
                return Workshop.objects.get(id=item_id, is_active=True)
            elif item_type == PaymentType.SERVICE:
                return TradingService.objects.get(id=item_id, is_active=True)
            return None
        except Exception:
            return None
    
    def is_item_available(self, item_id: str, item_type: PaymentType) -> bool:
        """Check if item is available for purchase"""
        item = self.get_item_by_id(item_id, item_type)
        if not item:
            return False
        
        # Check specific availability conditions
        if item_type == PaymentType.WORKSHOP:
            return not item.is_full
        elif item_type == PaymentType.COURSE:
            return not item.is_full
        
        return True
    
    def create_workshop_application(self, workshop_id: str, application_data: Dict[str, Any]) -> Optional[WorkshopApplication]:
        """Create workshop application"""
        try:
            workshop = Workshop.objects.get(id=workshop_id, is_active=True)
            return WorkshopApplication.objects.create(
                workshop=workshop,
                **application_data
            )
        except Exception:
            return None
    
    def create_service_booking(self, service_id: str, booking_data: Dict[str, Any]) -> Optional[ServiceBooking]:
        """Create service booking"""
        try:
            service = TradingService.objects.get(id=service_id, is_active=True)
            return ServiceBooking.objects.create(
                service=service,
                **booking_data
            )
        except Exception:
            return None
    
    def check_duplicate_application(self, workshop_id: str, email: str) -> bool:
        """Check if user already applied for workshop"""
        return WorkshopApplication.objects.filter(
            workshop_id=workshop_id,
            email=email
        ).exists()