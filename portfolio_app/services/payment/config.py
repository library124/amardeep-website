"""
Payment service configuration following SOLID principles
"""
from dataclasses import dataclass
from typing import Dict, Any
import os


@dataclass
class PaymentGatewayConfig:
    """Payment gateway configuration"""
    name: str
    api_url: str
    api_key: str = ""
    api_secret: str = ""
    webhook_secret: str = ""
    timeout: int = 30
    retry_attempts: int = 3
    additional_config: Dict[str, Any] = None


@dataclass
class PaymentServiceConfig:
    """Payment service configuration"""
    default_currency: str = "INR"
    default_gateway: str = "razorpay"
    enable_notifications: bool = True
    enable_webhooks: bool = True
    payment_timeout_minutes: int = 30


class PaymentConfigManager:
    """Payment configuration manager"""
    
    @staticmethod
    def get_gateway_config(gateway_name: str) -> PaymentGatewayConfig:
        """Get gateway configuration"""
        configs = {
            "razorpay": PaymentGatewayConfig(
                name="razorpay",
                api_url="https://api.razorpay.com/v1",
                api_key=os.getenv("RAZORPAY_KEY_ID", ""),
                api_secret=os.getenv("RAZORPAY_KEY_SECRET", ""),
                webhook_secret=os.getenv("RAZORPAY_WEBHOOK_SECRET", ""),
                timeout=30,
                retry_attempts=3
            ),
            "stripe": PaymentGatewayConfig(
                name="stripe",
                api_url="https://api.stripe.com/v1",
                api_key=os.getenv("STRIPE_PUBLISHABLE_KEY", ""),
                api_secret=os.getenv("STRIPE_SECRET_KEY", ""),
                webhook_secret=os.getenv("STRIPE_WEBHOOK_SECRET", ""),
                timeout=30,
                retry_attempts=3
            )
        }
        
        return configs.get(gateway_name, configs["razorpay"])
    
    @staticmethod
    def get_service_config() -> PaymentServiceConfig:
        """Get service configuration"""
        return PaymentServiceConfig(
            default_currency=os.getenv("DEFAULT_CURRENCY", "INR"),
            default_gateway=os.getenv("DEFAULT_PAYMENT_GATEWAY", "razorpay"),
            enable_notifications=os.getenv("ENABLE_PAYMENT_NOTIFICATIONS", "true").lower() == "true",
            enable_webhooks=os.getenv("ENABLE_PAYMENT_WEBHOOKS", "true").lower() == "true",
            payment_timeout_minutes=int(os.getenv("PAYMENT_TIMEOUT_MINUTES", "30"))
        )