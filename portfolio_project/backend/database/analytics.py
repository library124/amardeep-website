"""
Analytics Services for Business Intelligence and Reporting
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
from database.config import SessionLocal
from database.models import (
    UserAnalytics, WorkshopAnalytics, ContentAnalytics, 
    RevenueAnalytics, NewsletterAnalytics, TradingServiceAnalytics,
    UserBehaviorLog, MarketingCampaignAnalytics
)
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Main analytics service for business intelligence"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
    
    def get_dashboard_metrics(self, days: int = 30) -> Dict:
        """Get key metrics for dashboard"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        try:
            # Revenue metrics
            revenue_data = self.db.query(
                func.sum(RevenueAnalytics.total_revenue).label('total_revenue'),
                func.avg(RevenueAnalytics.total_revenue).label('avg_daily_revenue'),
                func.sum(RevenueAnalytics.total_transactions).label('total_transactions')
            ).filter(
                RevenueAnalytics.date >= start_date.date()
            ).first()
            
            # User metrics
            user_metrics = self.db.query(
                func.count(UserAnalytics.id).label('total_users'),
                func.sum(UserAnalytics.workshops_attended).label('total_workshop_attendees'),
                func.sum(UserAnalytics.courses_purchased).label('total_course_purchases')
            ).first()
            
            # Workshop metrics
            workshop_metrics = self.db.query(
                func.count(WorkshopAnalytics.id).label('total_workshops'),
                func.sum(WorkshopAnalytics.total_registrations).label('total_registrations'),
                func.avg(WorkshopAnalytics.completion_rate).label('avg_completion_rate')
            ).filter(
                WorkshopAnalytics.workshop_date >= start_date
            ).first()
            
            # Content metrics
            content_metrics = self.db.query(
                func.sum(ContentAnalytics.total_views).label('total_content_views'),
                func.avg(ContentAnalytics.avg_time_on_page).label('avg_time_on_page'),
                func.count(ContentAnalytics.id).label('total_content_pieces')
            ).first()
            
            return {
                'revenue': {
                    'total': float(revenue_data.total_revenue or 0),
                    'daily_average': float(revenue_data.avg_daily_revenue or 0),
                    'transactions': int(revenue_data.total_transactions or 0)
                },
                'users': {
                    'total': int(user_metrics.total_users or 0),
                    'workshop_attendees': int(user_metrics.total_workshop_attendees or 0),
                    'course_purchases': int(user_metrics.total_course_purchases or 0)
                },
                'workshops': {
                    'total': int(workshop_metrics.total_workshops or 0),
                    'registrations': int(workshop_metrics.total_registrations or 0),
                    'completion_rate': float(workshop_metrics.avg_completion_rate or 0)
                },
                'content': {
                    'total_views': int(content_metrics.total_content_views or 0),
                    'avg_time_on_page': int(content_metrics.avg_time_on_page or 0),
                    'total_pieces': int(content_metrics.total_content_pieces or 0)
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard metrics: {e}")
            return {}
    
    def get_revenue_trends(self, days: int = 90) -> List[Dict]:
        """Get revenue trends over time"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        try:
            revenue_trends = self.db.query(
                RevenueAnalytics.date,
                RevenueAnalytics.total_revenue,
                RevenueAnalytics.workshop_revenue,
                RevenueAnalytics.product_revenue,
                RevenueAnalytics.service_revenue
            ).filter(
                RevenueAnalytics.date >= start_date.date()
            ).order_by(RevenueAnalytics.date).all()
            
            return [
                {
                    'date': trend.date.isoformat(),
                    'total_revenue': float(trend.total_revenue),
                    'workshop_revenue': float(trend.workshop_revenue),
                    'product_revenue': float(trend.product_revenue),
                    'service_revenue': float(trend.service_revenue)
                }
                for trend in revenue_trends
            ]
            
        except Exception as e:
            logger.error(f"Error getting revenue trends: {e}")
            return []
    
    def get_top_performing_content(self, limit: int = 10) -> List[Dict]:
        """Get top performing content by views"""
        try:
            top_content = self.db.query(ContentAnalytics).order_by(
                desc(ContentAnalytics.total_views)
            ).limit(limit).all()
            
            return [
                {
                    'title': content.title,
                    'category': content.category,
                    'total_views': content.total_views,
                    'unique_views': content.unique_views,
                    'avg_time_on_page': content.avg_time_on_page,
                    'social_shares': content.social_shares,
                    'trending_score': float(content.trending_score)
                }
                for content in top_content
            ]
            
        except Exception as e:
            logger.error(f"Error getting top content: {e}")
            return []

# Convenience functions
def get_analytics_dashboard(days: int = 30):
    """Get dashboard analytics"""
    with AnalyticsService() as analytics:
        return analytics.get_dashboard_metrics(days)

def get_revenue_analysis(days: int = 90):
    """Get revenue analysis"""
    with AnalyticsService() as analytics:
        return analytics.get_revenue_trends(days)

def get_content_performance(limit: int = 10):
    """Get top content performance"""
    with AnalyticsService() as analytics:
        return analytics.get_top_performing_content(limit)