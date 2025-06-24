"""
Content Service for Database Operations
"""
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
from database.models.content_models import BlogPost, BlogCategory, BlogTag, Newsletter, Subscriber
from .base_service import BaseService
from typing import Optional, List
import logging
import uuid

logger = logging.getLogger(__name__)

class ContentService(BaseService[BlogPost]):
    """Service for content-related database operations"""
    
    def __init__(self):
        super().__init__(BlogPost)
    
    def get_published_posts(self, skip: int = 0, limit: int = 10) -> List[BlogPost]:
        """Get published blog posts"""
        try:
            return self.db.query(BlogPost).filter(
                BlogPost.status == 'published'
            ).order_by(BlogPost.publish_date.desc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting published posts: {e}")
            raise
    
    def get_post_by_slug(self, slug: str) -> Optional[BlogPost]:
        """Get blog post by slug"""
        try:
            return self.db.query(BlogPost).options(
                joinedload(BlogPost.category),
                joinedload(BlogPost.tags),
                joinedload(BlogPost.author)
            ).filter(BlogPost.slug == slug).first()
        except Exception as e:
            logger.error(f"Error getting post by slug {slug}: {e}")
            raise
    
    def get_featured_posts(self, limit: int = 5) -> List[BlogPost]:
        """Get featured blog posts"""
        try:
            return self.db.query(BlogPost).filter(
                BlogPost.is_featured == True,
                BlogPost.status == 'published'
            ).order_by(BlogPost.publish_date.desc()).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting featured posts: {e}")
            raise
    
    def get_posts_by_category(self, category_slug: str, skip: int = 0, limit: int = 10) -> List[BlogPost]:
        """Get posts by category"""
        try:
            return self.db.query(BlogPost).join(BlogCategory).filter(
                BlogCategory.slug == category_slug,
                BlogPost.status == 'published'
            ).order_by(BlogPost.publish_date.desc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting posts by category {category_slug}: {e}")
            raise
    
    def increment_views(self, post_id: int) -> bool:
        """Increment post views"""
        try:
            post = self.get(post_id)
            if post:
                post.views_count += 1
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error incrementing views for post {post_id}: {e}")
            raise
    
    # Category operations
    def get_categories(self) -> List[BlogCategory]:
        """Get all blog categories"""
        try:
            return self.db.query(BlogCategory).order_by(BlogCategory.name).all()
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            raise
    
    def get_category_by_slug(self, slug: str) -> Optional[BlogCategory]:
        """Get category by slug"""
        try:
            return self.db.query(BlogCategory).filter(BlogCategory.slug == slug).first()
        except Exception as e:
            logger.error(f"Error getting category by slug {slug}: {e}")
            raise
    
    # Tag operations
    def get_tags(self) -> List[BlogTag]:
        """Get all blog tags"""
        try:
            return self.db.query(BlogTag).order_by(BlogTag.name).all()
        except Exception as e:
            logger.error(f"Error getting tags: {e}")
            raise
    
    # Newsletter operations
    def create_subscriber(self, email: str, name: str = None, token: str = None) -> Subscriber:
        """Create newsletter subscriber"""
        try:
            subscriber = Subscriber(
                email=email,
                name=name,
                confirmation_token=token or str(uuid.uuid4())
            )
            self.db.add(subscriber)
            self.db.commit()
            self.db.refresh(subscriber)
            return subscriber
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating subscriber {email}: {e}")
            raise
    
    def get_subscriber_by_email(self, email: str) -> Optional[Subscriber]:
        """Get subscriber by email"""
        try:
            return self.db.query(Subscriber).filter(Subscriber.email == email).first()
        except Exception as e:
            logger.error(f"Error getting subscriber by email {email}: {e}")
            raise
    
    def confirm_subscriber(self, token: str) -> bool:
        """Confirm subscriber by token"""
        try:
            subscriber = self.db.query(Subscriber).filter(
                Subscriber.confirmation_token == token
            ).first()
            
            if subscriber:
                subscriber.is_confirmed = True
                subscriber.confirmed_at = func.now()
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error confirming subscriber with token {token}: {e}")
            raise