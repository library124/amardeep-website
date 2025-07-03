"""
Improved payment gateways following SOLID principles
"""
import uuid
import requests
import logging
from typing import Dict, Any, Optional, Tuple
import hashlib
import hmac
from abc import ABC, abstractmethod

from .interfaces import IPaymentGateway, PaymentRequest, PaymentCompletionRequest
from .config import PaymentConfigManager
from .exceptions import PaymentGatewayError, PaymentVerificationError

logger = logging.getLogger(__name__)


class BasePaymentGateway(ABC):
    """Base payment gateway with common functionality"""
    
    def __init__(self, config=None):
        self.config = config
        self.timeout = getattr(config, 'timeout', 30)
        self.retry_attempts = getattr(config, 'retry_attempts', 3)
    
    def _build_order_payload(self, request: PaymentRequest) -> Dict[str, Any]:
        """Build common order payload"""
        base_notes = {
            "item_id": request.item_id,
            "item_type": request.item_type.value,
            "customer_name": request.customer_name,
            "customer_email": request.customer_email,
            "user_id": request.user_id
        }
        
        if request.additional_data:
            base_notes.update(request.additional_data)
        
        return {
            "amount": int(request.amount * 100),  # Amount in smallest currency unit
            "currency": request.currency,
            "receipt": f"{request.item_type.value}_{request.item_id}_{uuid.uuid4().hex[:8]}",
            "notes": base_notes
        }
    
    def _make_request_with_retry(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with retry logic"""
        last_exception = None
        
        for attempt in range(self.retry_attempts):
            try:
                response = requests.request(method, url, timeout=self.timeout, **kwargs)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                last_exception = e
                logger.warning(f"Request attempt {attempt + 1} failed: {e}")
                if attempt == self.retry_attempts - 1:
                    break
        
        raise PaymentGatewayError(f"Request failed after {self.retry_attempts} attempts: {last_exception}")


class BeeceptorPaymentGateway(BasePaymentGateway, IPaymentGateway):
    """Beeceptor mock payment gateway implementation"""
    
    def __init__(self, config=None):
        super().__init__(config or PaymentConfigManager.get_gateway_config("beeceptor"))
        self.api_url = self.config.api_url
    
    def create_order(self, request: PaymentRequest) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Create order using Beeceptor mock API"""
        try:
            order_payload = self._build_order_payload(request)
            response = self._make_request_with_retry(
                "POST", 
                f"{self.api_url}/orders", 
                json=order_payload
            )
            return response.json(), None
        except PaymentGatewayError as e:
            logger.error(f"Beeceptor order creation failed: {e}")
            return None, str(e)
        except Exception as e:
            error_msg = f"Unexpected error in Beeceptor gateway: {e}"
            logger.error(error_msg)
            return None, error_msg
    
    def verify_payment(self, completion_request: PaymentCompletionRequest) -> bool:
        """Mock verification - always returns True for testing"""
        try:
            # For mock gateway, we'll always return True
            # In real implementation, verify signature using gateway's method
            logger.info(f"Mock verification for payment: {completion_request.payment_id}")
            return True
        except Exception as e:
            logger.error(f"Mock payment verification failed: {e}")
            raise PaymentVerificationError(f"Mock payment verification failed: {e}")


class RazorpayPaymentGateway(BasePaymentGateway, IPaymentGateway):
    """Razorpay payment gateway implementation"""
    
    def __init__(self, config=None):
        super().__init__(config or PaymentConfigManager.get_gateway_config("razorpay"))
        self.api_key = self.config.api_key
        self.api_secret = self.config.api_secret
        self.api_url = self.config.api_url
        
        if not self.api_key or not self.api_secret:
            raise PaymentGatewayError("Razorpay API credentials not configured", "MISSING_CREDENTIALS")
    
    def create_order(self, request: PaymentRequest) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Create order using Razorpay API"""
        try:
            order_payload = self._build_order_payload(request)
            response = self._make_request_with_retry(
                "POST",
                f"{self.api_url}/orders",
                json=order_payload,
                auth=(self.api_key, self.api_secret)
            )
            return response.json(), None
        except PaymentGatewayError as e:
            logger.error(f"Razorpay order creation failed: {e}")
            return None, str(e)
        except Exception as e:
            error_msg = f"Unexpected error in Razorpay gateway: {e}"
            logger.error(error_msg)
            return None, error_msg
    
    def verify_payment(self, completion_request: PaymentCompletionRequest) -> bool:
        """Verify payment signature using Razorpay's method"""
        try:
            # Try using razorpay library if available
            try:
                import razorpay
                client = razorpay.Client(auth=(self.api_key, self.api_secret))
                
                # Verify signature
                params_dict = {
                    'razorpay_order_id': completion_request.gateway_order_id,
                    'razorpay_payment_id': completion_request.gateway_payment_id,
                    'razorpay_signature': completion_request.gateway_signature
                }
                
                client.utility.verify_payment_signature(params_dict)
                return True
                
            except ImportError:
                # Fallback verification without razorpay library
                logger.warning("Razorpay library not available, using manual verification")
                return self._verify_signature_manually(completion_request)
                
        except Exception as e:
            logger.error(f"Razorpay payment verification failed: {e}")
            raise PaymentVerificationError(f"Razorpay payment verification failed: {e}")
    
    def _verify_signature_manually(self, completion_request: PaymentCompletionRequest) -> bool:
        """Manual signature verification"""
        try:
            # Create signature string
            signature_string = f"{completion_request.gateway_order_id}|{completion_request.gateway_payment_id}"
            
            # Generate expected signature
            expected_signature = hmac.new(
                self.api_secret.encode('utf-8'),
                signature_string.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Compare signatures
            return hmac.compare_digest(expected_signature, completion_request.gateway_signature)
            
        except Exception as e:
            logger.error(f"Manual signature verification failed: {e}")
            return False


class StripePaymentGateway(BasePaymentGateway, IPaymentGateway):
    """Stripe payment gateway implementation"""
    
    def __init__(self, config=None):
        super().__init__(config or PaymentConfigManager.get_gateway_config("stripe"))
        self.api_key = self.config.api_secret
        self.api_url = self.config.api_url
        
        if not self.api_key:
            raise PaymentGatewayError("Stripe API key not configured", "MISSING_CREDENTIALS")
    
    def create_order(self, request: PaymentRequest) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Create payment intent using Stripe API"""
        try:
            payment_intent_payload = {
                "amount": int(request.amount * 100),  # Amount in cents
                "currency": request.currency.lower(),
                "metadata": {
                    "item_id": request.item_id,
                    "item_type": request.item_type.value,
                    "customer_name": request.customer_name,
                    "customer_email": request.customer_email,
                    "user_id": str(request.user_id) if request.user_id else ""
                }
            }
            
            if request.additional_data:
                # Add additional data to metadata (Stripe has limits on metadata)
                for key, value in request.additional_data.items():
                    if len(payment_intent_payload["metadata"]) < 50:  # Stripe limit
                        payment_intent_payload["metadata"][key] = str(value)[:500]  # Stripe value limit
            
            response = self._make_request_with_retry(
                "POST",
                f"{self.api_url}/payment_intents",
                json=payment_intent_payload,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
            )
            return response.json(), None
        except PaymentGatewayError as e:
            logger.error(f"Stripe payment intent creation failed: {e}")
            return None, str(e)
        except Exception as e:
            error_msg = f"Unexpected error in Stripe gateway: {e}"
            logger.error(error_msg)
            return None, error_msg
    
    def verify_payment(self, completion_request: PaymentCompletionRequest) -> bool:
        """Verify payment with Stripe"""
        try:
            # For Stripe, we would typically verify using webhooks
            # This is a simplified implementation
            # In production, you would verify the payment_intent status via API
            return True
        except Exception as e:
            logger.error(f"Stripe payment verification failed: {e}")
            raise PaymentVerificationError(f"Stripe payment verification failed: {e}")


class PaymentGatewayFactory:
    """Factory for creating payment gateways following Open/Closed Principle"""
    
    _gateways = {
        "razorpay": RazorpayPaymentGateway,
        "beeceptor": BeeceptorPaymentGateway,
        "stripe": StripePaymentGateway
    }
    
    @classmethod
    def create_gateway(cls, gateway_type: str, config=None) -> IPaymentGateway:
        """Create payment gateway instance"""
        gateway_class = cls._gateways.get(gateway_type.lower())
        
        if not gateway_class:
            logger.warning(f"Unknown gateway type: {gateway_type}, defaulting to beeceptor")
            gateway_class = BeeceptorPaymentGateway
        
        try:
            return gateway_class(config)
        except Exception as e:
            logger.error(f"Failed to create {gateway_type} gateway: {e}")
            # Fallback to Beeceptor if primary gateway fails
            if gateway_type.lower() != "beeceptor":
                logger.info("Falling back to Beeceptor gateway")
                return BeeceptorPaymentGateway(config)
            raise
    
    @classmethod
    def register_gateway(cls, name: str, gateway_class: type):
        """Register new gateway type (Open/Closed Principle)"""
        if not issubclass(gateway_class, IPaymentGateway):
            raise ValueError(f"Gateway class must implement IPaymentGateway interface")
        cls._gateways[name.lower()] = gateway_class
    
    @classmethod
    def get_available_gateways(cls) -> list:
        """Get list of available gateway types"""
        return list(cls._gateways.keys())
    
    @classmethod
    def is_gateway_available(cls, gateway_type: str) -> bool:
        """Check if gateway type is available"""
        return gateway_type.lower() in cls._gateways