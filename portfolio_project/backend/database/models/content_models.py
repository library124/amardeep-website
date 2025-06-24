"""
Content-related SQLAlchemy Models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.config import Base
import uuid

# Association table for blog post tags (many-to-many)
blog_post_tags = Table(
    'portfolio_app_blogpost_tags',
    Base.metadata,
    Column('blogpost_id', Integer, ForeignKey('portfolio_app_blogpost.id')),
    Column('blogtag_id', Integer, ForeignKey('portfolio_app_blogtag.id'))
)

class BlogCategory(Base):
    """Blog category model"""
    __tablename__ = 'portfolio_app_blogcategory'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    posts = relationship("BlogPost", back_populates="category")
    
    def __repr__(self):
        return f"<BlogCategory {self.name}>"

class BlogTag(Base):
    """Blog tag model"""
    __tablename__ = 'portfolio_app_blogtag'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    posts = relationship("BlogPost", secondary=blog_post_tags, back_populates="tags")
    
    def __repr__(self):
        return f"<BlogTag {self.name}>"

class BlogPost(Base):
    """Blog post model"""
    __tablename__ = 'portfolio_app_blogpost'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    author_id = Column(Integer, ForeignKey('auth_user.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('portfolio_app_blogcategory.id'), nullable=True)
    
    # Content fields
    excerpt = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    featured_image = Column(String(255), nullable=True)
    
    # SEO fields
    meta_title = Column(String(60), nullable=True)
    meta_description = Column(String(160), nullable=True)
    
    # Status and timing
    status = Column(String(10), default='draft')
    publish_date = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Engagement
    views_count = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    
    # Relationships
    author = relationship("User")
    category = relationship("BlogCategory", back_populates="posts")
    tags = relationship("BlogTag", secondary=blog_post_tags, back_populates="posts")
    
    __table_args__ = (
        Index('idx_blogpost_status', 'status'),
        Index('idx_blogpost_publish_date', 'publish_date'),
        Index('idx_blogpost_featured', 'is_featured'),
        Index('idx_blogpost_author', 'author_id'),
    )
    
    @property
    def is_published(self):
        return self.status == 'published' and self.publish_date <= func.now()
    
    def __repr__(self):
        return f"<BlogPost {self.title}>"

class Subscriber(Base):
    """Newsletter subscriber model"""
    __tablename__ = 'portfolio_app_subscriber'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(254), unique=True, nullable=False)
    name = Column(String(100), nullable=True)
    confirmation_token = Column(String(36), unique=True, nullable=False)
    is_confirmed = Column(Boolean, default=False)
    subscribed_at = Column(DateTime, default=func.now())
    confirmed_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    __table_args__ = (
        Index('idx_subscriber_email', 'email'),
        Index('idx_subscriber_confirmed', 'is_confirmed'),
        Index('idx_subscriber_active', 'is_active'),
    )
    
    def __repr__(self):
        return f"<Subscriber {self.email}>"

class Newsletter(Base):
    """Newsletter model"""
    __tablename__ = 'portfolio_app_newsletter'
    
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255), nullable=False)
    content_html = Column(Text, nullable=False)
    content_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    sent_at = Column(DateTime, nullable=True)
    is_sent = Column(Boolean, default=False)
    sent_to_count = Column(Integer, default=0)
    
    __table_args__ = (
        Index('idx_newsletter_sent', 'is_sent'),
        Index('idx_newsletter_created', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Newsletter {self.subject}>"