"""
Analytics-related SQLAlchemy Models
These models are optimized for analytics, reporting, and data warehousing
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, Index, Date, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.config import Base

class UserAnalytics(Base):
    """User analytics and behavior tracking"""
    __tablename__ = 'user_analytics'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # Reference to Django User ID
    username = Column(String(150), index=True)
    email = Column(String(254), index=True)
    registration_date = Column(DateTime)
    last_login = Column(DateTime)
    
    # Profile information
    trading_experience = Column(String(50))
    preferred_market = Column(String(100))
    
    # Engagement metrics
    courses_purchased = Column(Integer, default=0)
    workshops_attended = Column(Integer, default=0)
    total_spent = Column(Numeric(10, 2), default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_user_analytics_user_id', 'user_id'),
        Index('idx_user_analytics_email', 'email'),
        Index('idx_user_analytics_registration', 'registration_date'),
    )

class WorkshopAnalytics(Base):
    """Workshop performance and attendance analytics"""
    __tablename__ = 'workshop_analytics'
    
    id = Column(Integer, primary_key=True, index=True)
    workshop_id = Column(Integer, index=True)  # Reference to Django Workshop ID
    workshop_title = Column(String(200))
    workshop_type = Column(String(50))  # 'paid', 'free'
    workshop_date = Column(DateTime)
    
    # Performance metrics
    total_registrations = Column(Integer, default=0)
    confirmed_attendees = Column(Integer, default=0)
    revenue_generated = Column(Numeric(10, 2), default=0)
    average_ticket_price = Column(Numeric(10, 2), default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_workshop_analytics_workshop_id', 'workshop_id'),
        Index('idx_workshop_analytics_date', 'workshop_date'),
        Index('idx_workshop_analytics_type', 'workshop_type'),
    )

class ContentAnalytics(Base):
    """Blog post and content performance analytics"""
    __tablename__ = 'content_analytics'
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, index=True)  # Reference to Django content ID
    content_type = Column(String(50))  # 'blog_post', 'newsletter', etc.
    title = Column(String(200))
    category = Column(String(100))
    
    # Performance metrics
    total_views = Column(Integer, default=0)
    unique_visitors = Column(Integer, default=0)
    average_time_on_page = Column(Integer, default=0)  # seconds
    bounce_rate = Column(Numeric(5, 2), default=0)  # percentage
    trending_score = Column(Numeric(10, 2), default=0)
    
    # SEO metrics
    organic_traffic = Column(Integer, default=0)
    social_shares = Column(Integer, default=0)
    
    # Timestamps
    publish_date = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_content_analytics_content_id', 'content_id'),
        Index('idx_content_analytics_type', 'content_type'),
        Index('idx_content_analytics_views', 'total_views'),
        Index('idx_content_analytics_trending', 'trending_score'),
    )

class RevenueAnalytics(Base):
    """Daily revenue and financial analytics"""
    __tablename__ = 'revenue_analytics'
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True)
    
    # Time dimensions
    year = Column(Integer, index=True)
    month = Column(Integer, index=True)
    week = Column(Integer, index=True)
    day_of_week = Column(Integer, index=True)
    
    # Revenue by source
    workshop_revenue = Column(Numeric(10, 2), default=0)
    product_revenue = Column(Numeric(10, 2), default=0)
    service_revenue = Column(Numeric(10, 2), default=0)
    total_revenue = Column(Numeric(10, 2), default=0)
    
    # Transaction metrics
    total_transactions = Column(Integer, default=0)
    successful_payments = Column(Integer, default=0)
    failed_payments = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_revenue_analytics_date', 'date'),
        Index('idx_revenue_analytics_year_month', 'year', 'month'),
        Index('idx_revenue_analytics_total', 'total_revenue'),
    )

class NewsletterAnalytics(Base):
    """Newsletter performance analytics"""
    __tablename__ = 'newsletter_analytics'
    
    id = Column(Integer, primary_key=True, index=True)
    newsletter_id = Column(Integer, index=True)  # Reference to Django Newsletter ID
    subject = Column(String(200))
    
    # Delivery metrics
    total_sent = Column(Integer, default=0)
    delivered = Column(Integer, default=0)
    bounced = Column(Integer, default=0)
    
    # Engagement metrics
    opened = Column(Integer, default=0)
    clicked = Column(Integer, default=0)
    unsubscribed = Column(Integer, default=0)
    
    # Calculated rates
    delivery_rate = Column(Numeric(5, 2), default=0)  # percentage
    open_rate = Column(Numeric(5, 2), default=0)  # percentage
    click_rate = Column(Numeric(5, 2), default=0)  # percentage
    unsubscribe_rate = Column(Numeric(5, 2), default=0)  # percentage
    
    # Timestamps
    sent_date = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_newsletter_analytics_newsletter_id', 'newsletter_id'),
        Index('idx_newsletter_analytics_sent_date', 'sent_date'),
        Index('idx_newsletter_analytics_open_rate', 'open_rate'),
    )

class TradingServiceAnalytics(Base):
    """Trading service performance analytics"""
    __tablename__ = 'trading_service_analytics'
    
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, index=True)  # Reference to Django TradingService ID
    service_name = Column(String(200))
    service_type = Column(String(100))
    date = Column(Date, index=True)
    
    # Subscription metrics
    active_subscribers = Column(Integer, default=0)
    new_subscribers = Column(Integer, default=0)
    churned_subscribers = Column(Integer, default=0)
    
    # Revenue metrics
    monthly_recurring_revenue = Column(Numeric(10, 2), default=0)
    average_revenue_per_user = Column(Numeric(10, 2), default=0)
    
    # Performance metrics
    service_uptime = Column(Numeric(5, 2), default=100)  # percentage
    customer_satisfaction = Column(Numeric(3, 2), default=0)  # 1-5 scale
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_trading_service_analytics_service_id', 'service_id'),
        Index('idx_trading_service_analytics_date', 'date'),
        Index('idx_trading_service_analytics_revenue', 'monthly_recurring_revenue'),
    )