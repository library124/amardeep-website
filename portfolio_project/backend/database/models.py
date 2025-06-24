 """
SQLAlchemy Models for Analytics and Reporting
These models are optimized for analytics, reporting, and data warehousing
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Decimal, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.config import Base
import uuid
from datetime import datetime

class UserAnalytics(Base):
    """User analytics and behavior tracking"""
    __tablename__ = 'user_analytics'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # Reference to Django User ID
    username = Column(String(150), index=True)
    email = Column(String(254), index=True)
    
    # User profile data
    trading_experience = Column(String(20), index=True)
    preferred_market = Column(String(50), index=True)
    registration_date = Column(DateTime, index=True)
    last_login = Column(DateTime)
    
    # Engagement metrics
    total_logins = Column(Integer, default=0)
    total_sessions = Column(Integer, default=0)
    avg_session_duration = Column(Integer, default=0)  # in minutes
    last_activity = Column(DateTime)
    
    # Course/Workshop engagement
    workshops_attended = Column(Integer, default=0)
    courses_purchased = Column(Integer, default=0)
    total_spent = Column(Decimal(10, 2), default=0.00)
    
    # Content engagement
    blog_posts_read = Column(Integer, default=0)
    newsletter_opens = Column(Integer, default=0)
    newsletter_clicks = Column(Integer, default=0)
    
    # Behavioral data
    preferred_content_type = Column(String(50))
    most_active_time = Column(String(20))  # morning, afternoon, evening, night
    device_type = Column(String(20))  # mobile, desktop, tablet
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_user_engagement', 'user_id', 'last_activity'),
        Index('idx_trading_experience', 'trading_experience', 'preferred_market'),
    )

class WorkshopAnalytics(Base):
    """Workshop performance and analytics"""
    __tablename__ = 'workshop_analytics'
    
    id = Column(Integer, primary_key=True, index=True)
    workshop_id = Column(Integer, index=True)  # Reference to Django Workshop ID
    workshop_title = Column(String(255), index=True)
    workshop_type = Column(String(20), index=True)  # free, paid
    
    # Registration metrics
    total_registrations = Column(Integer, default=0)
    confirmed_attendees = Column(Integer, default=0)
    actual_attendees = Column(Integer, default=0)
    no_shows = Column(Integer, default=0)
    
    # Financial metrics
    revenue_generated = Column(Decimal(10, 2), default=0.00)
    average_ticket_price = Column(Decimal(10, 2), default=0.00)
    refunds_issued = Column(Decimal(10, 2), default=0.00)
    
    # Engagement metrics
    completion_rate = Column(Decimal(5, 2), default=0.00)  # percentage
    satisfaction_score = Column(Decimal(3, 2), default=0.00)  # 1-5 scale
    feedback_count = Column(Integer, default=0)
    
    # Marketing metrics
    conversion_rate = Column(Decimal(5, 2), default=0.00)  # views to registrations
    page_views = Column(Integer, default=0)
    social_shares = Column(Integer, default=0)
    
    # Timing data
    workshop_date = Column(DateTime, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_workshop_performance', 'workshop_date', 'workshop_type'),
        Index('idx_revenue_metrics', 'revenue_generated', 'workshop_date'),
    )

class ContentAnalytics(Base):
    """Blog posts and content performance analytics"""
    __tablename__ = 'content_analytics'
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, index=True)  # Reference to Django BlogPost ID
    content_type = Column(String(20), index=True)  # blog_post, newsletter, etc.
    title = Column(String(255), index=True)
    category = Column(String(100), index=True)
    
    # Engagement metrics
    total_views = Column(Integer, default=0)
    unique_views = Column(Integer, default=0)
    avg_time_on_page = Column(Integer, default=0)  # in seconds
    bounce_rate = Column(Decimal(5, 2), default=0.00)
    
    # Social metrics
    social_shares = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    
    # SEO metrics
    organic_traffic = Column(Integer, default=0)
    search_impressions = Column(Integer, default=0)
    click_through_rate = Column(Decimal(5, 2), default=0.00)
    
    # Performance over time
    views_last_7_days = Column(Integer, default=0)
    views_last_30_days = Column(Integer, default=0)
    trending_score = Column(Decimal(8, 2), default=0.00)
    
    publish_date = Column(DateTime, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_content_performance', 'total_views', 'publish_date'),
        Index('idx_trending_content', 'trending_score', 'views_last_7_days'),
    )

class RevenueAnalytics(Base):
    """Revenue and financial analytics"""
    __tablename__ = 'revenue_analytics'
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Time dimensions
    date = Column(DateTime, index=True)
    year = Column(Integer, index=True)
    month = Column(Integer, index=True)
    week = Column(Integer, index=True)
    day_of_week = Column(Integer, index=True)
    
    # Revenue breakdown
    workshop_revenue = Column(Decimal(10, 2), default=0.00)
    product_revenue = Column(Decimal(10, 2), default=0.00)
    service_revenue = Column(Decimal(10, 2), default=0.00)
    subscription_revenue = Column(Decimal(10, 2), default=0.00)
    total_revenue = Column(Decimal(10, 2), default=0.00)
    
    # Transaction metrics
    total_transactions = Column(Integer, default=0)
    successful_payments = Column(Integer, default=0)
    failed_payments = Column(Integer, default=0)
    refunds = Column(Integer, default=0)
    
    # Customer metrics
    new_customers = Column(Integer, default=0)
    returning_customers = Column(Integer, default=0)
    average_order_value = Column(Decimal(10, 2), default=0.00)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_revenue_time', 'date', 'total_revenue'),
        Index('idx_monthly_revenue', 'year', 'month', 'total_revenue'),
    )

class UserBehaviorLog(Base):
    """Detailed user behavior and activity logging"""
    __tablename__ = 'user_behavior_log'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    session_id = Column(String(100), index=True)
    
    # Activity details
    action_type = Column(String(50), index=True)  # page_view, click, download, etc.
    page_url = Column(String(500))
    referrer_url = Column(String(500))
    action_details = Column(JSON)  # Additional action-specific data
    
    # Context data
    user_agent = Column(Text)
    ip_address = Column(String(45))
    device_type = Column(String(20))
    browser = Column(String(50))
    operating_system = Column(String(50))
    
    # Timing
    timestamp = Column(DateTime, default=func.now(), index=True)
    session_duration = Column(Integer)  # in seconds
    
    __table_args__ = (
        Index('idx_user_activity', 'user_id', 'timestamp'),
        Index('idx_action_analysis', 'action_type', 'timestamp'),
    )

class MarketingCampaignAnalytics(Base):
    """Marketing campaign performance tracking"""
    __tablename__ = 'marketing_campaign_analytics'
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(String(100), unique=True, index=True)
    campaign_name = Column(String(255), index=True)
    campaign_type = Column(String(50), index=True)  # email, social, paid_ads, etc.
    
    # Campaign metrics
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    click_through_rate = Column(Decimal(5, 2), default=0.00)
    conversion_rate = Column(Decimal(5, 2), default=0.00)
    
    # Financial metrics
    cost = Column(Decimal(10, 2), default=0.00)
    revenue = Column(Decimal(10, 2), default=0.00)
    roi = Column(Decimal(8, 2), default=0.00)
    cost_per_click = Column(Decimal(8, 2), default=0.00)
    cost_per_conversion = Column(Decimal(8, 2), default=0.00)
    
    # Audience data
    target_audience = Column(JSON)
    demographics = Column(JSON)
    geographic_data = Column(JSON)
    
    # Campaign timing
    start_date = Column(DateTime, index=True)
    end_date = Column(DateTime, index=True)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_campaign_performance', 'campaign_type', 'conversion_rate'),
        Index('idx_campaign_roi', 'roi', 'start_date'),
    )

class NewsletterAnalytics(Base):
    """Newsletter performance and subscriber analytics"""
    __tablename__ = 'newsletter_analytics'
    
    id = Column(Integer, primary_key=True, index=True)
    newsletter_id = Column(Integer, index=True)  # Reference to Django Newsletter ID
    subject = Column(String(255), index=True)
    
    # Delivery metrics
    total_sent = Column(Integer, default=0)
    delivered = Column(Integer, default=0)
    bounced = Column(Integer, default=0)
    delivery_rate = Column(Decimal(5, 2), default=0.00)
    
    # Engagement metrics
    opens = Column(Integer, default=0)
    unique_opens = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    unique_clicks = Column(Integer, default=0)
    open_rate = Column(Decimal(5, 2), default=0.00)
    click_rate = Column(Decimal(5, 2), default=0.00)
    
    # Subscriber actions
    unsubscribes = Column(Integer, default=0)
    spam_reports = Column(Integer, default=0)
    forwards = Column(Integer, default=0)
    
    # Performance over time
    best_open_time = Column(String(20))
    peak_engagement_day = Column(String(20))
    
    sent_date = Column(DateTime, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_newsletter_performance', 'open_rate', 'click_rate'),
        Index('idx_newsletter_timing', 'sent_date', 'opens'),
    )

class TradingServiceAnalytics(Base):
    """Trading services performance and customer analytics"""
    __tablename__ = 'trading_service_analytics'
    
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, index=True)  # Reference to Django TradingService ID
    service_name = Column(String(255), index=True)
    service_type = Column(String(50), index=True)
    
    # Subscription metrics
    active_subscribers = Column(Integer, default=0)
    new_subscribers = Column(Integer, default=0)
    churned_subscribers = Column(Integer, default=0)
    churn_rate = Column(Decimal(5, 2), default=0.00)
    
    # Revenue metrics
    monthly_recurring_revenue = Column(Decimal(10, 2), default=0.00)
    average_revenue_per_user = Column(Decimal(10, 2), default=0.00)
    lifetime_value = Column(Decimal(10, 2), default=0.00)
    
    # Performance metrics
    signal_accuracy = Column(Decimal(5, 2), default=0.00)  # for trading signals
    customer_satisfaction = Column(Decimal(3, 2), default=0.00)
    support_tickets = Column(Integer, default=0)
    
    # Engagement metrics
    daily_active_users = Column(Integer, default=0)
    feature_usage = Column(JSON)  # Track which features are used most
    
    date = Column(DateTime, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_service_performance', 'service_type', 'active_subscribers'),
        Index('idx_revenue_tracking', 'monthly_recurring_revenue', 'date'),
    )