"""
Payment Service for Database Operations
"""
from sqlalchemy.orm import joinedload
from sqlalchemy import and_
from sqlalchemy.sql import func
from database.models.payment_models import Payment, PurchasedCourse
from database.models.contact_models import ContactMessage
from .base_service import BaseService
from typing import Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PaymentService(BaseService[Payment]):
    """Service for payment-related database operations"""
    
    def __init__(self):
        super().__init__(Payment)
    
    def create_payment(self, payment_id: str, amount: float, payment_type: str, **payment_data) -> Payment:
        """Create a new payment record"""
        try:
            payment = Payment(
                payment_id=payment_id,
                amount=amount,
                payment_type=payment_type,
                **payment_data
            )
            self.db.add(payment)
            self.db.commit()
            self.db.refresh(payment)
            return payment
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating payment {payment_id}: {e}")
            raise
    
    def get_payment_by_id(self, payment_id: str) -> Optional[Payment]:
        """Get payment by payment ID"""
        try:
            return self.db.query(Payment).filter(Payment.payment_id == payment_id).first()
        except Exception as e:
            logger.error(f"Error getting payment by ID {payment_id}: {e}")
            raise
    
    def get_payments_by_email(self, email: str) -> List[Payment]:
        """Get payments by customer email"""
        try:
            return self.db.query(Payment).filter(
                Payment.customer_email == email
            ).order_by(Payment.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting payments for email {email}: {e}")
            raise
    
    def get_payments_by_type(self, payment_type: str, skip: int = 0, limit: int = 10) -> List[Payment]:
        """Get payments by type"""
        try:
            return self.db.query(Payment).filter(
                Payment.payment_type == payment_type
            ).order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting payments by type {payment_type}: {e}")
            raise
    
    def mark_payment_completed(self, payment_id: str, gateway_payment_id: str, payment_method: str, gateway_response: dict = None) -> bool:
        """Mark payment as completed"""
        try:
            payment = self.get_payment_by_id(payment_id)
            if payment:
                payment.status = 'completed'
                payment.gateway_payment_id = gateway_payment_id
                payment.payment_method = payment_method
                payment.completed_at = datetime.now()
                if gateway_response:
                    payment.gateway_response = gateway_response
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error marking payment {payment_id} as completed: {e}")
            raise
    
    def mark_payment_failed(self, payment_id: str, reason: str = None) -> bool:
        """Mark payment as failed"""
        try:
            payment = self.get_payment_by_id(payment_id)
            if payment:
                payment.status = 'failed'
                if reason and payment.gateway_response:
                    payment.gateway_response['failure_reason'] = reason
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error marking payment {payment_id} as failed: {e}")
            raise
    
    # Purchased Course operations
    def create_purchased_course(self, user_id: int, course_name: str, course_type: str, amount_paid: float, **course_data) -> PurchasedCourse:
        """Create purchased course record"""
        try:
            course = PurchasedCourse(
                user_id=user_id,
                course_name=course_name,
                course_type=course_type,
                amount_paid=amount_paid,
                **course_data
            )
            self.db.add(course)
            self.db.commit()
            self.db.refresh(course)
            return course
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating purchased course: {e}")
            raise
    
    def get_user_courses(self, user_id: int) -> List[PurchasedCourse]:
        """Get user's purchased courses"""
        try:
            return self.db.query(PurchasedCourse).filter(
                PurchasedCourse.user_id == user_id
            ).order_by(PurchasedCourse.purchase_date.desc()).all()
        except Exception as e:
            logger.error(f"Error getting courses for user {user_id}: {e}")
            raise
    
    def get_active_courses(self, user_id: int) -> List[PurchasedCourse]:
        """Get user's active courses"""
        try:
            return self.db.query(PurchasedCourse).filter(
                and_(
                    PurchasedCourse.user_id == user_id,
                    PurchasedCourse.status == 'active'
                )
            ).order_by(PurchasedCourse.purchase_date.desc()).all()
        except Exception as e:
            logger.error(f"Error getting active courses for user {user_id}: {e}")
            raise
    
    def mark_course_accessed(self, course_id: int) -> bool:
        """Mark course as accessed"""
        try:
            course = self.db.query(PurchasedCourse).filter(
                PurchasedCourse.id == course_id
            ).first()
            
            if course:
                course.last_accessed = datetime.now()
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error marking course {course_id} as accessed: {e}")
            raise
    
    # Contact Message operations
    def create_contact_message(self, name: str, email: str, subject: str, message: str, **message_data) -> ContactMessage:
        """Create contact message"""
        try:
            contact = ContactMessage(
                name=name,
                email=email,
                subject=subject,
                message=message,
                **message_data
            )
            self.db.add(contact)
            self.db.commit()
            self.db.refresh(contact)
            return contact
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating contact message: {e}")
            raise
    
    def get_contact_messages(self, status: str = None, skip: int = 0, limit: int = 10) -> List[ContactMessage]:
        """Get contact messages"""
        try:
            query = self.db.query(ContactMessage)
            if status:
                query = query.filter(ContactMessage.status == status)
            return query.order_by(ContactMessage.created_at.desc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting contact messages: {e}")
            raise
    
    def mark_message_read(self, message_id: int, user_id: int = None) -> bool:
        """Mark contact message as read"""
        try:
            message = self.db.query(ContactMessage).filter(
                ContactMessage.id == message_id
            ).first()
            
            if message and message.status == 'new':
                message.status = 'read'
                message.read_at = datetime.now()
                if user_id:
                    message.assigned_to_id = user_id
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error marking message {message_id} as read: {e}")
            raise