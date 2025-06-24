"""
User Service for Database Operations
"""
from sqlalchemy.orm import joinedload
from database.models.user_models import User, UserProfile
from database.models.achievement_models import Achievement
from database.models.payment_models import PurchasedCourse
from .base_service import BaseService
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class UserService(BaseService[User]):
    """Service for user-related database operations"""
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            return self.db.query(User).filter(User.username == username).first()
        except Exception as e:
            logger.error(f"Error getting user by username {username}: {e}")
            raise
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            return self.db.query(User).filter(User.email == email).first()
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            raise
    
    def create_user(self, username: str, email: str, password: str, **kwargs) -> User:
        """Create a new user with profile"""
        try:
            # Create user
            user = User(
                username=username,
                email=email,
                **kwargs
            )
            user.set_password(password)
            self.db.add(user)
            self.db.flush()  # Get the user ID
            
            # Create user profile
            profile = UserProfile(user_id=user.id)
            self.db.add(profile)
            
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating user {username}: {e}")
            raise
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate user"""
        try:
            user = self.get_by_username(username)
            if user and user.check_password(password):
                return user
            return None
        except Exception as e:
            logger.error(f"Error authenticating user {username}: {e}")
            raise
    
    def get_user_with_profile(self, user_id: int) -> Optional[User]:
        """Get user with profile data"""
        try:
            return self.db.query(User).options(
                joinedload(User.profile)
            ).filter(User.id == user_id).first()
        except Exception as e:
            logger.error(f"Error getting user with profile {user_id}: {e}")
            raise
    
    def update_profile(self, user_id: int, **profile_data) -> Optional[UserProfile]:
        """Update user profile"""
        try:
            profile = self.db.query(UserProfile).filter(
                UserProfile.user_id == user_id
            ).first()
            
            if profile:
                for key, value in profile_data.items():
                    if hasattr(profile, key):
                        setattr(profile, key, value)
                self.db.commit()
                self.db.refresh(profile)
            
            return profile
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating profile for user {user_id}: {e}")
            raise
    
    def get_user_achievements(self, user_id: int) -> List[Achievement]:
        """Get user achievements"""
        try:
            return self.db.query(Achievement).filter(
                Achievement.user_id == user_id
            ).order_by(Achievement.date.desc()).all()
        except Exception as e:
            logger.error(f"Error getting achievements for user {user_id}: {e}")
            raise
    
    def get_user_courses(self, user_id: int) -> List[PurchasedCourse]:
        """Get user purchased courses"""
        try:
            return self.db.query(PurchasedCourse).filter(
                PurchasedCourse.user_id == user_id
            ).order_by(PurchasedCourse.purchase_date.desc()).all()
        except Exception as e:
            logger.error(f"Error getting courses for user {user_id}: {e}")
            raise
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate user account"""
        try:
            user = self.get(user_id)
            if user:
                user.is_active = False
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deactivating user {user_id}: {e}")
            raise
    
    def activate_user(self, user_id: int) -> bool:
        """Activate user account"""
        try:
            user = self.get(user_id)
            if user:
                user.is_active = True
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error activating user {user_id}: {e}")
            raise