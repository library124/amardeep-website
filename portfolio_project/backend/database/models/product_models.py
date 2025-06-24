"""
Product and Service-related SQLAlchemy Models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index, Numeric, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.config import Base

class DigitalProduct(Base):
    """Digital product model"""
    __tablename__ = 'portfolio_app_digitalproduct'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    download_link = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<DigitalProduct {self.name}>"

class TradingService(Base):
    """Trading service model"""
    __tablename__ = 'portfolio_app_tradingservice'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    service_type = Column(String(20), default='signals')
    description = Column(Text, nullable=False)
    detailed_description = Column(Text, nullable=True)
    
    # Pricing
    price = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default='INR')
    duration = Column(String(20), default='monthly')
    
    # Features (JSON field to store list of features)
    features = Column(JSON, nullable=True)
    
    # Visibility and Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_popular = Column(Boolean, default=False)
    
    # Contact and Booking
    booking_type = Column(String(20), default='whatsapp')
    contact_info = Column(String(255), nullable=True)
    booking_url = Column(String(500), nullable=True)
    
    # Display Order
    display_order = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # SEO
    meta_title = Column(String(60), nullable=True)
    meta_description = Column(String(160), nullable=True)
    
    # Relationships
    bookings = relationship("ServiceBooking", back_populates="service")
    purchased_courses = relationship("PurchasedCourse", back_populates="trading_service")
    
    __table_args__ = (
        Index('idx_service_active', 'is_active'),
        Index('idx_service_featured', 'is_featured'),
        Index('idx_service_display_order', 'display_order'),
        Index('idx_service_type', 'service_type'),
    )
    
    def __repr__(self):
        return f"<TradingService {self.name}>"

class ServiceBooking(Base):
    """Service booking model"""
    __tablename__ = 'portfolio_app_servicebooking'
    
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('portfolio_app_tradingservice.id'), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(254), nullable=False)
    phone = Column(String(20), nullable=False)
    message = Column(Text, nullable=True)
    
    # Booking details
    preferred_contact_method = Column(String(20), default='whatsapp')
    preferred_time = Column(String(100), nullable=True)
    
    # Status and tracking
    status = Column(String(20), default='pending')
    admin_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    contacted_at = Column(DateTime, nullable=True)
    
    # Relationships
    service = relationship("TradingService", back_populates="bookings")
    
    __table_args__ = (
        Index('idx_booking_service', 'service_id'),
        Index('idx_booking_status', 'status'),
        Index('idx_booking_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<ServiceBooking {self.name} - {self.service.name if self.service else 'Unknown'}>"