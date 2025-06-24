"""
Contact and Communication-related SQLAlchemy Models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.config import Base

class ContactMessage(Base):
    """Contact message model"""
    __tablename__ = 'portfolio_app_contactmessage'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(254), nullable=False)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    
    # Classification and status
    status = Column(String(10), default='new')
    priority = Column(String(10), default='normal')
    
    # Admin fields
    admin_notes = Column(Text, nullable=True)
    assigned_to_id = Column(Integer, ForeignKey('auth_user.id'), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    read_at = Column(DateTime, nullable=True)
    replied_at = Column(DateTime, nullable=True)
    
    # Additional metadata
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Relationships
    assigned_to = relationship("User")
    
    __table_args__ = (
        Index('idx_contact_status', 'status'),
        Index('idx_contact_priority', 'priority'),
        Index('idx_contact_email', 'email'),
        Index('idx_contact_created_at', 'created_at'),
    )
    
    @property
    def is_new(self):
        return self.status == 'new'
    
    @property
    def is_urgent(self):
        return self.priority in ['high', 'urgent']
    
    def __repr__(self):
        return f"<ContactMessage {self.name} - {self.subject}>"