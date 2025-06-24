"""
Product and Service Operations
"""
from sqlalchemy.orm import joinedload
from sqlalchemy import and_
from sqlalchemy.sql import func
from database.models.product_models import DigitalProduct, TradingService, ServiceBooking
from .base_service import BaseService
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class ProductService(BaseService[DigitalProduct]):
    """Service for product and trading service operations"""
    
    def __init__(self):
        super().__init__(DigitalProduct)
    
    # Digital Product operations
    def get_active_products(self, skip: int = 0, limit: int = 10) -> List[DigitalProduct]:
        """Get active digital products"""
        try:
            return self.db.query(DigitalProduct).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting active products: {e}")
            raise
    
    # Trading Service operations
    def get_active_services(self, skip: int = 0, limit: int = 10) -> List[TradingService]:
        """Get active trading services"""
        try:
            return self.db.query(TradingService).filter(
                TradingService.is_active == True
            ).order_by(TradingService.display_order.asc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting active services: {e}")
            raise
    
    def get_featured_services(self, limit: int = 5) -> List[TradingService]:
        """Get featured trading services"""
        try:
            return self.db.query(TradingService).filter(
                and_(
                    TradingService.is_featured == True,
                    TradingService.is_active == True
                )
            ).order_by(TradingService.display_order.asc()).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting featured services: {e}")
            raise
    
    def get_popular_services(self, limit: int = 5) -> List[TradingService]:
        """Get popular trading services"""
        try:
            return self.db.query(TradingService).filter(
                and_(
                    TradingService.is_popular == True,
                    TradingService.is_active == True
                )
            ).order_by(TradingService.display_order.asc()).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting popular services: {e}")
            raise
    
    def get_service_by_slug(self, slug: str) -> Optional[TradingService]:
        """Get trading service by slug"""
        try:
            return self.db.query(TradingService).options(
                joinedload(TradingService.bookings)
            ).filter(TradingService.slug == slug).first()
        except Exception as e:
            logger.error(f"Error getting service by slug {slug}: {e}")
            raise
    
    def get_services_by_type(self, service_type: str, skip: int = 0, limit: int = 10) -> List[TradingService]:
        """Get services by type"""
        try:
            return self.db.query(TradingService).filter(
                and_(
                    TradingService.service_type == service_type,
                    TradingService.is_active == True
                )
            ).order_by(TradingService.display_order.asc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting services by type {service_type}: {e}")
            raise
    
    # Service Booking operations
    def create_booking(self, service_id: int, **booking_data) -> ServiceBooking:
        """Create service booking"""
        try:
            booking = ServiceBooking(
                service_id=service_id,
                **booking_data
            )
            self.db.add(booking)
            self.db.commit()
            self.db.refresh(booking)
            return booking
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating service booking: {e}")
            raise
    
    def get_service_bookings(self, service_id: int) -> List[ServiceBooking]:
        """Get all bookings for a service"""
        try:
            return self.db.query(ServiceBooking).filter(
                ServiceBooking.service_id == service_id
            ).order_by(ServiceBooking.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting bookings for service {service_id}: {e}")
            raise
    
    def get_pending_bookings(self) -> List[ServiceBooking]:
        """Get pending service bookings"""
        try:
            return self.db.query(ServiceBooking).filter(
                ServiceBooking.status == 'pending'
            ).order_by(ServiceBooking.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting pending bookings: {e}")
            raise
    
    def update_booking_status(self, booking_id: int, status: str, notes: str = None) -> bool:
        """Update booking status"""
        try:
            booking = self.db.query(ServiceBooking).filter(
                ServiceBooking.id == booking_id
            ).first()
            
            if booking:
                booking.status = status
                if notes:
                    booking.admin_notes = notes
                if status == 'contacted':
                    booking.contacted_at = func.now()
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating booking {booking_id} status: {e}")
            raise