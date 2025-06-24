"""
Workshop-related SQLAlchemy Models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.config import Base

class Workshop(Base):
    """Workshop model"""
    __tablename__ = 'portfolio_app_workshop'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    short_description = Column(Text, nullable=False)
    
    # Media
    featured_image = Column(String(255), nullable=False)
    
    # Pricing
    is_paid = Column(Boolean, default=False)
    price = Column(Numeric(10, 2), nullable=True)
    currency = Column(String(3), default='INR')
    
    # Scheduling
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    duration_hours = Column(Integer, nullable=False)
    
    # Capacity and Registration
    max_participants = Column(Integer, default=50)
    registered_count = Column(Integer, default=0)
    
    # Status and Visibility
    status = Column(String(10), default='upcoming')
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Additional Information
    requirements = Column(Text, nullable=True)
    what_you_learn = Column(Text, nullable=True)
    instructor_id = Column(Integer, ForeignKey('auth_user.id'), nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # SEO
    meta_title = Column(String(60), nullable=True)
    meta_description = Column(String(160), nullable=True)
    
    # Relationships
    instructor = relationship("User")
    applications = relationship("WorkshopApplication", back_populates="workshop")
    
    __table_args__ = (
        Index('idx_workshop_start_date', 'start_date'),
        Index('idx_workshop_status', 'status'),
        Index('idx_workshop_featured', 'is_featured'),
        Index('idx_workshop_paid', 'is_paid'),
        Index('idx_workshop_active', 'is_active'),
    )
    
    @property
    def is_upcoming(self):
        return self.start_date > func.now()
    
    @property
    def is_full(self):
        return self.registered_count >= self.max_participants
    
    @property
    def spots_remaining(self):
        return max(0, self.max_participants - self.registered_count)
    
    def __repr__(self):
        return f"<Workshop {self.title}>"

class WorkshopApplication(Base):
    """Workshop application model"""
    __tablename__ = 'portfolio_app_workshopapplication'
    
    id = Column(Integer, primary_key=True, index=True)
    workshop_id = Column(Integer, ForeignKey('portfolio_app_workshop.id'), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(254), nullable=False)
    phone = Column(String(20), nullable=True)
    experience_level = Column(String(50), default='beginner')
    motivation = Column(Text, nullable=True)
    status = Column(String(10), default='pending')
    
    # Payment fields
    payment_status = Column(String(15), default='not_required')
    payment_amount = Column(Numeric(10, 2), nullable=True)
    payment_id = Column(String(100), nullable=True)
    payment_method = Column(String(50), nullable=True)
    paid_at = Column(DateTime, nullable=True)
    
    # Timestamps
    applied_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    notes = Column(Text, nullable=True)
    
    # Relationships
    workshop = relationship("Workshop", back_populates="applications")
    
    __table_args__ = (
        Index('idx_application_workshop', 'workshop_id'),
        Index('idx_application_status', 'status'),
        Index('idx_application_payment_status', 'payment_status'),
        Index('idx_application_email', 'email'),
        Index('idx_application_applied_at', 'applied_at'),
    )
    
    def __repr__(self):
        return f"<WorkshopApplication {self.name} - {self.workshop.title if self.workshop else 'Unknown'}>"