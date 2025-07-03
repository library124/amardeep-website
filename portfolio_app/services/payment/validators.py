"""
Validation services following SOLID principles
"""
from typing import Tuple, Optional
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .interfaces import IValidationService, PaymentRequest, PaymentType, IItemRepository


class PaymentValidationService(IValidationService):
    """Payment validation service implementation"""
    
    def __init__(self, item_repository: IItemRepository):
        self.item_repository = item_repository
    
    def validate_payment_request(self, request: PaymentRequest) -> Tuple[bool, Optional[str]]:
        """Validate payment request data"""
        # Validate required fields
        if not request.item_id:
            return False, "Item ID is required"
        
        if not request.customer_email:
            return False, "Customer email is required"
        
        # Validate email format
        try:
            validate_email(request.customer_email)
        except ValidationError:
            return False, "Invalid email format"
        
        # Validate amount
        if request.amount <= 0:
            return False, "Amount must be greater than zero"
        
        # Validate currency
        if request.currency not in ['INR', 'USD', 'EUR']:
            return False, "Invalid currency"
        
        return True, None
    
    def validate_item_availability(self, item_id: str, item_type: PaymentType, 
                                 customer_email: str) -> Tuple[bool, Optional[str]]:
        """Validate item availability and customer eligibility"""
        # Check if item exists
        item = self.item_repository.get_item_by_id(item_id, item_type)
        if not item:
            return False, f"{item_type.value.title()} not found"
        
        # Check if item is available
        if not self.item_repository.is_item_available(item_id, item_type):
            return False, f"{item_type.value.title()} is not available or full"
        
        # Workshop-specific validation
        if item_type == PaymentType.WORKSHOP:
            if hasattr(self.item_repository, 'check_duplicate_application'):
                if self.item_repository.check_duplicate_application(item_id, customer_email):
                    return False, "You have already applied for this workshop"
        
        return True, None


class WorkshopValidationService:
    """Workshop-specific validation service"""
    
    @staticmethod
    def validate_application_data(application_data: dict) -> Tuple[bool, Optional[str]]:
        """Validate workshop application data"""
        required_fields = ['name', 'email']
        
        for field in required_fields:
            if not application_data.get(field):
                return False, f"{field.title()} is required"
        
        # Validate email
        try:
            validate_email(application_data['email'])
        except ValidationError:
            return False, "Invalid email format"
        
        # Validate experience level
        valid_levels = ['beginner', 'intermediate', 'advanced']
        experience_level = application_data.get('experience_level', 'beginner')
        if experience_level not in valid_levels:
            return False, "Invalid experience level"
        
        return True, None


class ServiceValidationService:
    """Service-specific validation service"""
    
    @staticmethod
    def validate_booking_data(booking_data: dict) -> Tuple[bool, Optional[str]]:
        """Validate service booking data"""
        required_fields = ['name', 'email', 'phone']
        
        for field in required_fields:
            if not booking_data.get(field):
                return False, f"{field.title()} is required"
        
        # Validate email
        try:
            validate_email(booking_data['email'])
        except ValidationError:
            return False, "Invalid email format"
        
        # Validate contact method
        valid_methods = ['whatsapp', 'call', 'email']
        contact_method = booking_data.get('preferred_contact_method', 'whatsapp')
        if contact_method not in valid_methods:
            return False, "Invalid contact method"
        
        return True, None