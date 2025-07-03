"""
Post-payment handlers following SOLID principles
"""
import logging
from typing import Any
from django.utils import timezone

from .interfaces import IPostPaymentHandler, PaymentType, INotificationService
from .notifications import NotificationServiceFactory
from ...models import PurchasedCourse, WorkshopApplication

logger = logging.getLogger(__name__)


class CoursePaymentHandler(IPostPaymentHandler):
    """Handler for course payment completion"""
    
    def __init__(self, notification_service: INotificationService = None):
        self.notification_service = notification_service or NotificationServiceFactory.create_service()
    
    def handle_successful_payment(self, payment: Any, item: Any, item_type: PaymentType) -> None:
        """Handle successful course payment"""
        try:
            # Create purchased course record
            user_id = payment.gateway_response.get('user_id') if payment.gateway_response else None
            
            PurchasedCourse.objects.create(
                user_id=user_id,
                course_name=item.title,
                course_type='course',
                description=item.short_description,
                purchase_date=timezone.now(),
                start_date=timezone.now(),
                amount_paid=payment.amount,
                currency=payment.currency,
                status='active',
                course=item
            )
            
            # Increment enrolled count
            item.enrolled_count += 1
            item.save(update_fields=['enrolled_count'])
            
            # Send notifications
            self.notification_service.send_payment_confirmation(payment, payment.customer_email)
            self.notification_service.send_enrollment_notification(payment.customer_email, item, item_type)
            
            logger.info(f"Course enrollment created for payment {payment.payment_id}")
            
        except Exception as e:
            logger.error(f"Error handling course payment completion: {e}")


class WorkshopPaymentHandler(IPostPaymentHandler):
    """Handler for workshop payment completion"""
    
    def __init__(self, notification_service: INotificationService = None):
        self.notification_service = notification_service or NotificationServiceFactory.create_service()
    
    def handle_successful_payment(self, payment: Any, item: Any, item_type: PaymentType) -> None:
        """Handle successful workshop payment"""
        try:
            # Update workshop application status
            if payment.workshop_application:
                application = payment.workshop_application
                application.status = 'approved'
                application.payment_status = 'completed'
                application.payment_id = payment.gateway_payment_id
                application.payment_method = payment.payment_method
                application.paid_at = timezone.now()
                application.save()
                
                # Increment workshop registered count
                workshop = application.workshop
                workshop.registered_count += 1
                workshop.save(update_fields=['registered_count'])
                
                # Send notifications
                self.notification_service.send_payment_confirmation(payment, payment.customer_email)
                self.notification_service.send_enrollment_notification(payment.customer_email, item, item_type)
                
                logger.info(f"Workshop application approved for payment {payment.payment_id}")
            
        except Exception as e:
            logger.error(f"Error handling workshop payment completion: {e}")


class ServicePaymentHandler(IPostPaymentHandler):
    """Handler for service payment completion"""
    
    def __init__(self, notification_service: INotificationService = None):
        self.notification_service = notification_service or NotificationServiceFactory.create_service()
    
    def handle_successful_payment(self, payment: Any, item: Any, item_type: PaymentType) -> None:
        """Handle successful service payment"""
        try:
            # Send notifications
            self.notification_service.send_payment_confirmation(payment, payment.customer_email)
            self.notification_service.send_enrollment_notification(payment.customer_email, item, item_type)
            
            logger.info(f"Service payment completed for payment {payment.payment_id}")
            
        except Exception as e:
            logger.error(f"Error handling service payment completion: {e}")


class PaymentHandlerFactory:
    """Factory for creating payment handlers"""
    
    @staticmethod
    def create_handler(item_type: PaymentType) -> IPostPaymentHandler:
        """Create appropriate payment handler based on item type"""
        if item_type == PaymentType.COURSE:
            return CoursePaymentHandler()
        elif item_type == PaymentType.WORKSHOP:
            return WorkshopPaymentHandler()
        elif item_type == PaymentType.SERVICE:
            return ServicePaymentHandler()
        else:
            # Default handler that does nothing
            return DefaultPaymentHandler()


class DefaultPaymentHandler(IPostPaymentHandler):
    """Default payment handler that does nothing"""
    
    def handle_successful_payment(self, payment: Any, item: Any, item_type: PaymentType) -> None:
        """Default implementation - no action"""
        logger.info(f"Payment completed for {item_type.value}: {payment.payment_id}")