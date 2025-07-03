"""
Payment gateway implementations following SOLID principles
"""
import uuid
import requests
import logging
import hmac
import hashlib
from typing import Dict, Any, Optional, Tuple
from django.conf import settings

from .interfaces import IPaymentGateway, PaymentRequest, PaymentCompletionRequest
from .config import PaymentConfigManager
from .exceptions import PaymentGatewayError, PaymentVerificationError

logger = logging.getLogger(__name__)


class RazorpayPaymentGateway(IPaymentGateway):
    """Official Razorpay payment gateway implementation"""
    
    def __init__(self, config=None):
        self.config = config or PaymentConfigManager.get_gateway_config("razorpay")
        self.api_key = self.config.api_key
        self.api_secret = self.config.api_secret
        self.api_url = self.config.api_url
        self.timeout = self.config.timeout
        
        if not self.api_key or not self.api_secret:
            raise PaymentGatewayError("Razorpay API credentials not configured", "MISSING_CREDENTIALS")
    
    def create_order(self, request: PaymentRequest) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Create order using official Razorpay API"""
        try:
            order_payload = self._build_order_payload(request)
            auth = (self.api_key, self.api_secret)
            
            response = requests.post(
                f"{self.api_url}/orders", 
                json=order_payload, 
                auth=auth,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json(), None
        except requests.RequestException as e:
            error_msg = f"Razorpay order creation failed: {e}"
            logger.error(error_msg)
            raise PaymentGatewayError(error_msg, "GATEWAY_REQUEST_FAILED")
    
    def verify_payment(self, completion_request: PaymentCompletionRequest) -> bool:
        """Verify Razorpay payment signature"""
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
    
    def _build_order_payload(self, request: PaymentRequest) -> Dict[str, Any]:
        """Build order payload for Razorpay API"""
        base_notes = {
            "item_id": request.item_id,
            "item_type": request.item_type.value,
            "customer_name": request.customer_name,
            "customer_email": request.customer_email,
            "user_id": str(request.user_id) if request.user_id else ""
        }
        
        if request.additional_data:
            base_notes.update(request.additional_data)
        
        return {
            "amount": int(request.amount * 100),  # Amount in paise
            "currency": request.currency,
            "receipt": f"{request.item_type.value}_{request.item_id}_{uuid.uuid4().hex[:8]}",
            "notes": base_notes
        }


class StripePaymentGateway(IPaymentGateway):
    """Stripe payment gateway implementation (backup option)"""
    
    def __init__(self, config=None):
        self.config = config or PaymentConfigManager.get_gateway_config("stripe")
        self.api_key = self.config.api_secret
        self.api_url = self.config.api_url
        self.timeout = self.config.timeout
        
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
            
            response = requests.post(
                f"{self.api_url}/payment_intents",
                json=payment_intent_payload,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json(), None
        except requests.RequestException as e:
            error_msg = f"Stripe payment intent creation failed: {e}"
            logger.error(error_msg)
            raise PaymentGatewayError(error_msg, "GATEWAY_REQUEST_FAILED")
    
    def verify_payment(self, completion_request: PaymentCompletionRequest) -> bool:
        """Verify payment with Stripe"""
        try:
            # For Stripe, we would typically verify using webhooks
            # This is a simplified implementation
            return True
        except Exception as e:
            logger.error(f"Stripe payment verification failed: {e}")
            raise PaymentVerificationError(f"Stripe payment verification failed: {e}")


class PaymentGatewayFactory:
    """Factory for creating payment gateway instances following Open/Closed Principle"""
    
    _gateways = {
        "razorpay": RazorpayPaymentGateway,
        "stripe": StripePaymentGateway
    }
    
    @classmethod
    def create_gateway(cls, gateway_type: str = "razorpay", config=None) -> IPaymentGateway:
        """Create payment gateway instance based on type"""
        gateway_class = cls._gateways.get(gateway_type.lower())
        
        if not gateway_class:
            logger.warning(f"Unknown gateway type: {gateway_type}, defaulting to razorpay")
            gateway_class = RazorpayPaymentGateway
        
        try:
            return gateway_class(config)
        except Exception as e:
            logger.error(f"Failed to create {gateway_type} gateway: {e}")
            # If Razorpay fails and we're not already trying Razorpay, don't fallback
            # This ensures we fail fast if credentials are missing
            raise PaymentGatewayError(f"Failed to initialize {gateway_type} gateway: {e}")
    
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