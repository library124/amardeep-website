"""
Django Integration Layer for SQLAlchemy
This module provides utilities to integrate SQLAlchemy with Django
"""
from django.conf import settings
from database.config import test_connection, init_db
from database.services import UserService, ContentService, WorkshopService, ProductService, PaymentService
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manager class for database operations"""
    
    def __init__(self):
        self._user_service = None
        self._content_service = None
        self._workshop_service = None
        self._product_service = None
        self._payment_service = None
    
    @property
    def users(self):
        """Get user service"""
        if not self._user_service:
            self._user_service = UserService()
        return self._user_service
    
    @property
    def content(self):
        """Get content service"""
        if not self._content_service:
            self._content_service = ContentService()
        return self._content_service
    
    @property
    def workshops(self):
        """Get workshop service"""
        if not self._workshop_service:
            self._workshop_service = WorkshopService()
        return self._workshop_service
    
    @property
    def products(self):
        """Get product service"""
        if not self._product_service:
            self._product_service = ProductService()
        return self._product_service
    
    @property
    def payments(self):
        """Get payment service"""
        if not self._payment_service:
            self._payment_service = PaymentService()
        return self._payment_service
    
    def initialize_database(self):
        """Initialize the database"""
        try:
            if test_connection():
                logger.info("✅ TiDB Cloud connection successful")
                if init_db():
                    logger.info("✅ Database tables created successfully")
                    return True
                else:
                    logger.error("❌ Failed to create database tables")
                    return False
            else:
                logger.error("❌ TiDB Cloud connection failed")
                return False
        except Exception as e:
            logger.error(f"❌ Database initialization error: {e}")
            return False
    
    def health_check(self):
        """Check database health"""
        try:
            return test_connection()
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

# Global database manager instance
db_manager = DatabaseManager()

# Convenience functions for easy access
def get_user_service():
    """Get user service instance"""
    return UserService()

def get_content_service():
    """Get content service instance"""
    return ContentService()

def get_workshop_service():
    """Get workshop service instance"""
    return WorkshopService()

def get_product_service():
    """Get product service instance"""
    return ProductService()

def get_payment_service():
    """Get payment service instance"""
    return PaymentService()

# Django middleware integration
class SQLAlchemyMiddleware:
    """Middleware to handle SQLAlchemy sessions"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Add database manager to request
        request.db = db_manager
        
        response = self.get_response(request)
        
        # Clean up any open sessions
        # (Services handle their own session cleanup)
        
        return response