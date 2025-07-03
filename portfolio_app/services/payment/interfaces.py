"""
Payment service interfaces following SOLID principles
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class PaymentStatus(Enum):
    """Payment status enumeration"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentType(Enum):
    """Payment type enumeration"""
    COURSE = "course"
    WORKSHOP = "workshop"
    SERVICE = "service"
    PRODUCT = "product"


@dataclass
class PaymentRequest:
    """Payment request data structure"""
    item_id: str
    item_type: PaymentType
    amount: float
    currency: str = "INR"
    customer_name: str = "Guest User"
    customer_email: str = ""
    customer_phone: str = ""
    user_id: Optional[int] = None
    additional_data: Optional[Dict[str, Any]] = None


@dataclass
class PaymentResponse:
    """Payment response data structure"""
    success: bool
    order_id: Optional[str] = None
    payment_id: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    error_message: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None


@dataclass
class PaymentCompletionRequest:
    """Payment completion request data structure"""
    payment_id: str
    gateway_payment_id: str
    gateway_order_id: str
    gateway_signature: str
    user_id: Optional[int] = None


class IPaymentGateway(ABC):
    """Interface for payment gateway implementations"""
    
    @abstractmethod
    def create_order(self, request: PaymentRequest) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Create order with payment gateway"""
        pass
    
    @abstractmethod
    def verify_payment(self, completion_request: PaymentCompletionRequest) -> bool:
        """Verify payment signature/authenticity"""
        pass


class IPaymentRepository(ABC):
    """Interface for payment data access"""
    
    @abstractmethod
    def create_payment_record(self, request: PaymentRequest, order_data: Dict[str, Any], 
                            related_object: Any = None) -> Any:
        """Create payment record in database"""
        pass
    
    @abstractmethod
    def get_payment_by_id(self, payment_id: str) -> Optional[Any]:
        """Get payment record by ID"""
        pass
    
    @abstractmethod
    def update_payment_status(self, payment_id: str, status: PaymentStatus, 
                            gateway_data: Dict[str, Any]) -> bool:
        """Update payment status"""
        pass


class IItemRepository(ABC):
    """Interface for item data access (courses, workshops, services)"""
    
    @abstractmethod
    def get_item_by_id(self, item_id: str, item_type: PaymentType) -> Optional[Any]:
        """Get item by ID and type"""
        pass
    
    @abstractmethod
    def is_item_available(self, item_id: str, item_type: PaymentType) -> bool:
        """Check if item is available for purchase"""
        pass


class IPaymentProcessor(ABC):
    """Interface for payment processing logic"""
    
    @abstractmethod
    def process_payment_request(self, request: PaymentRequest) -> PaymentResponse:
        """Process payment request"""
        pass
    
    @abstractmethod
    def complete_payment(self, completion_request: PaymentCompletionRequest) -> PaymentResponse:
        """Complete payment after gateway confirmation"""
        pass


class IPostPaymentHandler(ABC):
    """Interface for post-payment actions"""
    
    @abstractmethod
    def handle_successful_payment(self, payment: Any, item: Any, item_type: PaymentType) -> None:
        """Handle actions after successful payment"""
        pass


class INotificationService(ABC):
    """Interface for notification services"""
    
    @abstractmethod
    def send_payment_confirmation(self, payment: Any, customer_email: str) -> bool:
        """Send payment confirmation notification"""
        pass
    
    @abstractmethod
    def send_enrollment_notification(self, customer_email: str, item: Any, item_type: PaymentType) -> bool:
        """Send enrollment/access notification"""
        pass


class IValidationService(ABC):
    """Interface for validation services"""
    
    @abstractmethod
    def validate_payment_request(self, request: PaymentRequest) -> Tuple[bool, Optional[str]]:
        """Validate payment request data"""
        pass
    
    @abstractmethod
    def validate_item_availability(self, item_id: str, item_type: PaymentType, 
                                 customer_email: str) -> Tuple[bool, Optional[str]]:
        """Validate item availability and customer eligibility"""
        pass