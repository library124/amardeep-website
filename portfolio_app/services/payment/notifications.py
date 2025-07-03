"""
Notification services following SOLID principles
"""
import logging
from typing import Any
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .interfaces import INotificationService, PaymentType

logger = logging.getLogger(__name__)


class EmailNotificationService(INotificationService):
    """Email notification service implementation"""
    
    def __init__(self):
        self.from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
        self.admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@example.com')
    
    def send_payment_confirmation(self, payment: Any, customer_email: str) -> bool:
        """Send payment confirmation email"""
        try:
            subject = f"Payment Confirmation - {payment.payment_id}"
            
            context = {
                'payment_id': payment.payment_id,
                'amount': payment.amount,
                'currency': payment.currency,
                'customer_name': payment.customer_name,
                'payment_type': payment.payment_type.title(),
                'item_name': self._get_item_name(payment)
            }
            
            # Try to render template, fallback to plain text
            try:
                message = render_to_string('emails/payment_confirmation.html', context)
                html_message = message
                message = render_to_string('emails/payment_confirmation.txt', context)
            except:
                message = self._get_plain_text_confirmation(context)
                html_message = None
            
            send_mail(
                subject=subject,
                message=message,
                from_email=self.from_email,
                recipient_list=[customer_email],
                html_message=html_message,
                fail_silently=False
            )
            
            logger.info(f"Payment confirmation sent to {customer_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send payment confirmation: {e}")
            return False
    
    def send_enrollment_notification(self, customer_email: str, item: Any, item_type: PaymentType) -> bool:
        """Send enrollment/access notification"""
        try:
            subject = f"Access Details - {getattr(item, 'title', getattr(item, 'name', 'Your Purchase'))}"
            
            context = {
                'item_name': getattr(item, 'title', getattr(item, 'name', 'Your Purchase')),
                'item_type': item_type.value.title(),
                'customer_email': customer_email,
                'access_instructions': self._get_access_instructions(item_type)
            }
            
            # Try to render template, fallback to plain text
            try:
                message = render_to_string('emails/enrollment_notification.html', context)
                html_message = message
                message = render_to_string('emails/enrollment_notification.txt', context)
            except:
                message = self._get_plain_text_enrollment(context)
                html_message = None
            
            send_mail(
                subject=subject,
                message=message,
                from_email=self.from_email,
                recipient_list=[customer_email],
                html_message=html_message,
                fail_silently=False
            )
            
            logger.info(f"Enrollment notification sent to {customer_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send enrollment notification: {e}")
            return False
    
    def _get_item_name(self, payment: Any) -> str:
        """Get item name from payment"""
        if hasattr(payment, 'course') and payment.course:
            return payment.course.title
        elif hasattr(payment, 'workshop_application') and payment.workshop_application:
            return payment.workshop_application.workshop.title
        elif hasattr(payment, 'trading_service') and payment.trading_service:
            return payment.trading_service.name
        return "Unknown Item"
    
    def _get_access_instructions(self, item_type: PaymentType) -> str:
        """Get access instructions based on item type"""
        instructions = {
            PaymentType.COURSE: "You can now access your course from the dashboard. Login to your account and navigate to 'My Courses'.",
            PaymentType.WORKSHOP: "Workshop details and joining instructions will be sent to you closer to the workshop date.",
            PaymentType.SERVICE: "Our team will contact you within 24 hours to discuss your service requirements.",
            PaymentType.PRODUCT: "Your download link has been sent to your email address."
        }
        return instructions.get(item_type, "Thank you for your purchase!")
    
    def _get_plain_text_confirmation(self, context: dict) -> str:
        """Generate plain text payment confirmation"""
        return f"""
Payment Confirmation

Dear {context['customer_name']},

Your payment has been successfully processed!

Payment Details:
- Payment ID: {context['payment_id']}
- Amount: {context['currency']} {context['amount']}
- Item: {context['item_name']}
- Type: {context['payment_type']}

Thank you for your purchase!

Best regards,
The Team
        """.strip()
    
    def _get_plain_text_enrollment(self, context: dict) -> str:
        """Generate plain text enrollment notification"""
        return f"""
Access Details

Dear Customer,

You now have access to: {context['item_name']}

{context['access_instructions']}

If you have any questions, please don't hesitate to contact us.

Best regards,
The Team
        """.strip()


class SMSNotificationService(INotificationService):
    """SMS notification service implementation (placeholder)"""
    
    def send_payment_confirmation(self, payment: Any, customer_email: str) -> bool:
        """Send SMS payment confirmation (not implemented)"""
        logger.info(f"SMS confirmation would be sent for payment {payment.payment_id}")
        return True
    
    def send_enrollment_notification(self, customer_email: str, item: Any, item_type: PaymentType) -> bool:
        """Send SMS enrollment notification (not implemented)"""
        logger.info(f"SMS enrollment notification would be sent for {item_type.value}")
        return True


class NotificationServiceFactory:
    """Factory for creating notification services"""
    
    @staticmethod
    def create_service(service_type: str = "email") -> INotificationService:
        """Create notification service instance"""
        if service_type == "sms":
            return SMSNotificationService()
        return EmailNotificationService()  # Default to email