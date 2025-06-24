"""
Data Synchronization between Django ORM and SQLAlchemy Analytics
This module handles syncing data from Django models to SQLAlchemy analytics models
"""
from django.contrib.auth.models import User
from portfolio_app.models import (
    UserProfile, Workshop, WorkshopApplication, BlogPost, 
    Newsletter, TradingService, Payment, PurchasedCourse
)
from database.config import SessionLocal
from database.models import (
    UserAnalytics, WorkshopAnalytics, ContentAnalytics, 
    RevenueAnalytics, NewsletterAnalytics, TradingServiceAnalytics
)
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DataSyncManager:
    """Manages data synchronization between Django and SQLAlchemy"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
    
    def sync_user_analytics(self):
        """Sync user data to analytics"""
        try:
            users = User.objects.select_related('profile').all()
            
            for user in users:
                # Get or create user analytics record
                user_analytics = self.db.query(UserAnalytics).filter(
                    UserAnalytics.user_id == user.id
                ).first()
                
                if not user_analytics:
                    user_analytics = UserAnalytics(user_id=user.id)
                    self.db.add(user_analytics)
                
                # Update user data
                user_analytics.username = user.username
                user_analytics.email = user.email
                user_analytics.registration_date = user.date_joined
                user_analytics.last_login = user.last_login
                
                # Update profile data if exists
                if hasattr(user, 'profile'):
                    profile = user.profile
                    user_analytics.trading_experience = profile.trading_experience
                    user_analytics.preferred_market = profile.preferred_market
                
                # Calculate engagement metrics
                purchased_courses = PurchasedCourse.objects.filter(user=user)
                user_analytics.courses_purchased = purchased_courses.count()
                user_analytics.total_spent = purchased_courses.aggregate(
                    total=Sum('amount_paid')
                )['total'] or 0
                
                # Workshop attendance
                workshop_apps = WorkshopApplication.objects.filter(
                    email=user.email, status='approved'
                )
                user_analytics.workshops_attended = workshop_apps.count()
                
                user_analytics.updated_at = datetime.now()
            
            self.db.commit()
            logger.info(f"Synced {users.count()} user analytics records")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error syncing user analytics: {e}")
            raise
    
    def sync_workshop_analytics(self):
        """Sync workshop performance data"""
        try:
            workshops = Workshop.objects.all()
            
            for workshop in workshops:
                # Get or create workshop analytics record
                workshop_analytics = self.db.query(WorkshopAnalytics).filter(
                    WorkshopAnalytics.workshop_id == workshop.id
                ).first()
                
                if not workshop_analytics:
                    workshop_analytics = WorkshopAnalytics(workshop_id=workshop.id)
                    self.db.add(workshop_analytics)
                
                # Update workshop data
                workshop_analytics.workshop_title = workshop.title
                workshop_analytics.workshop_type = 'paid' if workshop.is_paid else 'free'
                workshop_analytics.workshop_date = workshop.start_date
                
                # Calculate metrics from applications
                applications = WorkshopApplication.objects.filter(workshop=workshop)
                workshop_analytics.total_registrations = applications.count()
                workshop_analytics.confirmed_attendees = applications.filter(
                    status='approved'
                ).count()
                
                # Revenue calculations for paid workshops
                if workshop.is_paid:
                    paid_applications = applications.filter(payment_status='completed')
                    workshop_analytics.revenue_generated = paid_applications.aggregate(
                        total=Sum('payment_amount')
                    )['total'] or 0
                    workshop_analytics.average_ticket_price = workshop.price or 0
                
                workshop_analytics.updated_at = datetime.now()
            
            self.db.commit()
            logger.info(f"Synced {workshops.count()} workshop analytics records")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error syncing workshop analytics: {e}")
            raise
    
    def sync_content_analytics(self):
        """Sync blog post and content analytics"""
        try:
            blog_posts = BlogPost.objects.filter(status='published')
            
            for post in blog_posts:
                # Get or create content analytics record
                content_analytics = self.db.query(ContentAnalytics).filter(
                    ContentAnalytics.content_id == post.id,
                    ContentAnalytics.content_type == 'blog_post'
                ).first()
                
                if not content_analytics:
                    content_analytics = ContentAnalytics(
                        content_id=post.id,
                        content_type='blog_post'
                    )
                    self.db.add(content_analytics)
                
                # Update content data
                content_analytics.title = post.title
                content_analytics.category = post.category.name if post.category else 'Uncategorized'
                content_analytics.total_views = post.views_count
                content_analytics.publish_date = post.publish_date
                
                # Calculate trending score (simple algorithm)
                days_since_publish = (timezone.now() - post.publish_date).days
                if days_since_publish > 0:
                    content_analytics.trending_score = post.views_count / max(days_since_publish, 1)
                
                content_analytics.updated_at = datetime.now()
            
            self.db.commit()
            logger.info(f"Synced {blog_posts.count()} content analytics records")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error syncing content analytics: {e}")
            raise
    
    def sync_revenue_analytics(self, date=None):
        """Sync daily revenue analytics"""
        try:
            if not date:
                date = timezone.now().date()
            
            # Get or create revenue analytics record for the date
            revenue_analytics = self.db.query(RevenueAnalytics).filter(
                RevenueAnalytics.date == date
            ).first()
            
            if not revenue_analytics:
                revenue_analytics = RevenueAnalytics(date=date)
                self.db.add(revenue_analytics)
            
            # Set time dimensions
            revenue_analytics.year = date.year
            revenue_analytics.month = date.month
            revenue_analytics.week = date.isocalendar()[1]
            revenue_analytics.day_of_week = date.weekday()
            
            # Calculate revenue from different sources
            start_date = datetime.combine(date, datetime.min.time())
            end_date = start_date + timedelta(days=1)
            
            # Workshop revenue
            workshop_payments = Payment.objects.filter(
                payment_type='workshop',
                status='completed',
                completed_at__gte=start_date,
                completed_at__lt=end_date
            )
            revenue_analytics.workshop_revenue = workshop_payments.aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            # Product revenue
            product_payments = Payment.objects.filter(
                payment_type='product',
                status='completed',
                completed_at__gte=start_date,
                completed_at__lt=end_date
            )
            revenue_analytics.product_revenue = product_payments.aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            # Service revenue
            service_payments = Payment.objects.filter(
                payment_type='service',
                status='completed',
                completed_at__gte=start_date,
                completed_at__lt=end_date
            )
            revenue_analytics.service_revenue = service_payments.aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            # Calculate totals
            revenue_analytics.total_revenue = (
                revenue_analytics.workshop_revenue +
                revenue_analytics.product_revenue +
                revenue_analytics.service_revenue
            )
            
            # Transaction metrics
            all_payments = Payment.objects.filter(
                created_at__gte=start_date,
                created_at__lt=end_date
            )
            revenue_analytics.total_transactions = all_payments.count()
            revenue_analytics.successful_payments = all_payments.filter(
                status='completed'
            ).count()
            revenue_analytics.failed_payments = all_payments.filter(
                status='failed'
            ).count()
            
            revenue_analytics.updated_at = datetime.now()
            
            self.db.commit()
            logger.info(f"Synced revenue analytics for {date}")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error syncing revenue analytics: {e}")
            raise
    
    def sync_newsletter_analytics(self):
        """Sync newsletter performance data"""
        try:
            newsletters = Newsletter.objects.filter(is_sent=True)
            
            for newsletter in newsletters:
                # Get or create newsletter analytics record
                newsletter_analytics = self.db.query(NewsletterAnalytics).filter(
                    NewsletterAnalytics.newsletter_id == newsletter.id
                ).first()
                
                if not newsletter_analytics:
                    newsletter_analytics = NewsletterAnalytics(
                        newsletter_id=newsletter.id
                    )
                    self.db.add(newsletter_analytics)
                
                # Update newsletter data
                newsletter_analytics.subject = newsletter.subject
                newsletter_analytics.total_sent = newsletter.sent_to_count
                newsletter_analytics.sent_date = newsletter.sent_at
                
                # Note: Actual email metrics would come from your email service provider
                # This is a placeholder for integration with services like Brevo, Mailchimp, etc.
                
                newsletter_analytics.updated_at = datetime.now()
            
            self.db.commit()
            logger.info(f"Synced {newsletters.count()} newsletter analytics records")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error syncing newsletter analytics: {e}")
            raise
    
    def sync_trading_service_analytics(self):
        """Sync trading service performance data"""
        try:
            services = TradingService.objects.filter(is_active=True)
            
            for service in services:
                # Get or create service analytics record for today
                today = timezone.now().date()
                service_analytics = self.db.query(TradingServiceAnalytics).filter(
                    TradingServiceAnalytics.service_id == service.id,
                    TradingServiceAnalytics.date == today
                ).first()
                
                if not service_analytics:
                    service_analytics = TradingServiceAnalytics(
                        service_id=service.id,
                        date=today
                    )
                    self.db.add(service_analytics)
                
                # Update service data
                service_analytics.service_name = service.name
                service_analytics.service_type = service.service_type
                
                # Calculate subscriber metrics from purchased courses
                active_subscriptions = PurchasedCourse.objects.filter(
                    trading_service=service,
                    status='active'
                )
                service_analytics.active_subscribers = active_subscriptions.count()
                
                # Revenue calculations
                if service_analytics.active_subscribers > 0:
                    total_revenue = active_subscriptions.aggregate(
                        total=Sum('amount_paid')
                    )['total'] or 0
                    service_analytics.average_revenue_per_user = (
                        total_revenue / service_analytics.active_subscribers
                    )
                
                service_analytics.updated_at = datetime.now()
            
            self.db.commit()
            logger.info(f"Synced {services.count()} trading service analytics records")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error syncing trading service analytics: {e}")
            raise
    
    def full_sync(self):
        """Perform a full synchronization of all analytics data"""
        try:
            logger.info("Starting full analytics sync...")
            
            self.sync_user_analytics()
            self.sync_workshop_analytics()
            self.sync_content_analytics()
            self.sync_revenue_analytics()
            self.sync_newsletter_analytics()
            self.sync_trading_service_analytics()
            
            logger.info("Full analytics sync completed successfully")
            
        except Exception as e:
            logger.error(f"Error during full sync: {e}")
            raise

# Utility functions for easy access
def sync_all_analytics():
    """Convenience function to sync all analytics data"""
    with DataSyncManager() as sync_manager:
        sync_manager.full_sync()

def sync_daily_revenue(date=None):
    """Convenience function to sync daily revenue"""
    with DataSyncManager() as sync_manager:
        sync_manager.sync_revenue_analytics(date)

def sync_user_data():
    """Convenience function to sync user analytics"""
    with DataSyncManager() as sync_manager:
        sync_manager.sync_user_analytics()