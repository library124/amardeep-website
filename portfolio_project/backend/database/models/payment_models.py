"""
Payment-related SQLAlchemy Models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index, Numeric, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.config import Base

class Payment(Base):
    """Payment model"""
    __tablename__ = 'portfolio_app_payment'
    
    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(String(100), unique=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default='INR')
    status = Column(String(10), default='pending')
    payment_type = Column(String(15), nullable=False)
    
    # Customer details
    customer_name = Column(String(100), nullable=False)
    customer_email = Column(String(254), nullable=False)
    customer_phone = Column(String(20), nullable=True)
    
    # Payment gateway details
    gateway_payment_id = Column(String(100), nullable=True)
    payment_method = Column(String(50), nullable=True)
    gateway_response = Column(JSON, nullable=True)
    
    # Related objects (foreign keys)
    workshop_application_id = Column(Integer, ForeignKey('portfolio_app_workshopapplication.id'), nullable=True)
    digital_product_id = Column(Integer, ForeignKey('portfolio_app_digitalproduct.id'), nullable=True)
    trading_service_id = Column(Integer, ForeignKey('portfolio_app_tradingservice.id'), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    workshop_application = relationship("WorkshopApplication")
    digital_product = relationship("DigitalProduct")
    trading_service = relationship("TradingService")
    
    __table_args__ = (
        Index('idx_payment_status', 'status'),
        Index('idx_payment_type', 'payment_type'),
        Index('idx_payment_customer_email', 'customer_email'),
        Index('idx_payment_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Payment {self.payment_id} - {self.customer_name}>"

class PurchasedCourse(Base):
    """Purchased course model"""
    __tablename__ = 'portfolio_app_purchasedcourse'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('auth_user.id'), nullable=False)
    course_name = Column(String(255), nullable=False)
    course_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    
    # Purchase details
    purchase_date = Column(DateTime, default=func.now())
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    status = Column(String(20), default='active')
    
    # Pricing
    amount_paid = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default='INR')
    
    # Access details
    access_url = Column(String(500), nullable=True)
    access_credentials = Column(JSON, nullable=True)
    
    # Progress tracking
    progress_percentage = Column(Integer, default=0)
    last_accessed = Column(DateTime, nullable=True)
    
    # Related objects
    workshop_application_id = Column(Integer, ForeignKey('portfolio_app_workshopapplication.id'), nullable=True)
    trading_service_id = Column(Integer, ForeignKey('portfolio_app_tradingservice.id'), nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="purchased_courses")
    workshop_application = relationship("WorkshopApplication")
    trading_service = relationship("TradingService", back_populates="purchased_courses")
    
    __table_args__ = (
        Index('idx_purchased_course_user', 'user_id'),
        Index('idx_purchased_course_status', 'status'),
        Index('idx_purchased_course_purchase_date', 'purchase_date'),
    )
    
    @property
    def is_active(self):
        return self.status == 'active' and (not self.end_date or self.end_date > func.now())
    
    def __repr__(self):
        return f"<PurchasedCourse {self.course_name} - {self.user.username if self.user else 'Unknown'}>"