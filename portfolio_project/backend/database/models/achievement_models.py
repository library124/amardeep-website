"""
Achievement-related SQLAlchemy Models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, Index, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.config import Base

class Achievement(Base):
    """Achievement model"""
    __tablename__ = 'portfolio_app_achievement'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    metrics = Column(JSON, nullable=True)  # e.g., {'profit': 1000, 'roi': 0.15}
    user_id = Column(Integer, ForeignKey('auth_user.id'), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    
    __table_args__ = (
        Index('idx_achievement_user', 'user_id'),
        Index('idx_achievement_date', 'date'),
    )
    
    def __repr__(self):
        return f"<Achievement {self.title} - {self.user.username if self.user else 'Unknown'}>"