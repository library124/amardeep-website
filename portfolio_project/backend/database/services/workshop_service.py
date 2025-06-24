"""
Workshop Service for Database Operations
"""
from sqlalchemy.orm import joinedload
from sqlalchemy import and_
from database.models.workshop_models import Workshop, WorkshopApplication
from .base_service import BaseService
from typing import Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class WorkshopService(BaseService[Workshop]):
    """Service for workshop-related database operations"""
    
    def __init__(self):
        super().__init__(Workshop)
    
    def get_active_workshops(self, skip: int = 0, limit: int = 10) -> List[Workshop]:
        """Get active workshops"""
        try:
            return self.db.query(Workshop).filter(
                Workshop.is_active == True
            ).order_by(Workshop.start_date.desc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting active workshops: {e}")
            raise
    
    def get_upcoming_workshops(self, skip: int = 0, limit: int = 10) -> List[Workshop]:
        """Get upcoming workshops"""
        try:
            return self.db.query(Workshop).filter(
                and_(
                    Workshop.is_active == True,
                    Workshop.start_date > datetime.now(),
                    Workshop.status == 'upcoming'
                )
            ).order_by(Workshop.start_date.asc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting upcoming workshops: {e}")
            raise
    
    def get_featured_workshops(self, limit: int = 5) -> List[Workshop]:
        """Get featured workshops"""
        try:
            return self.db.query(Workshop).filter(
                and_(
                    Workshop.is_featured == True,
                    Workshop.is_active == True
                )
            ).order_by(Workshop.start_date.asc()).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting featured workshops: {e}")
            raise
    
    def get_workshop_by_slug(self, slug: str) -> Optional[Workshop]:
        """Get workshop by slug"""
        try:
            return self.db.query(Workshop).options(
                joinedload(Workshop.instructor),
                joinedload(Workshop.applications)
            ).filter(Workshop.slug == slug).first()
        except Exception as e:
            logger.error(f"Error getting workshop by slug {slug}: {e}")
            raise
    
    def get_paid_workshops(self, skip: int = 0, limit: int = 10) -> List[Workshop]:
        """Get paid workshops"""
        try:
            return self.db.query(Workshop).filter(
                and_(
                    Workshop.is_paid == True,
                    Workshop.is_active == True
                )
            ).order_by(Workshop.start_date.asc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting paid workshops: {e}")
            raise
    
    def get_free_workshops(self, skip: int = 0, limit: int = 10) -> List[Workshop]:
        """Get free workshops"""
        try:
            return self.db.query(Workshop).filter(
                and_(
                    Workshop.is_paid == False,
                    Workshop.is_active == True
                )
            ).order_by(Workshop.start_date.asc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting free workshops: {e}")
            raise
    
    # Workshop Application operations
    def create_application(self, workshop_id: int, **application_data) -> WorkshopApplication:
        """Create workshop application"""
        try:
            application = WorkshopApplication(
                workshop_id=workshop_id,
                **application_data
            )
            self.db.add(application)
            self.db.commit()
            self.db.refresh(application)
            return application
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating workshop application: {e}")
            raise
    
    def get_application_by_email(self, workshop_id: int, email: str) -> Optional[WorkshopApplication]:
        """Get application by workshop and email"""
        try:
            return self.db.query(WorkshopApplication).filter(
                and_(
                    WorkshopApplication.workshop_id == workshop_id,
                    WorkshopApplication.email == email
                )
            ).first()
        except Exception as e:
            logger.error(f"Error getting application for workshop {workshop_id} and email {email}: {e}")
            raise
    
    def get_workshop_applications(self, workshop_id: int) -> List[WorkshopApplication]:
        """Get all applications for a workshop"""
        try:
            return self.db.query(WorkshopApplication).filter(
                WorkshopApplication.workshop_id == workshop_id
            ).order_by(WorkshopApplication.applied_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting applications for workshop {workshop_id}: {e}")
            raise
    
    def approve_application(self, application_id: int) -> bool:
        """Approve workshop application"""
        try:
            application = self.db.query(WorkshopApplication).filter(
                WorkshopApplication.id == application_id
            ).first()
            
            if application and application.status == 'pending':
                # Check if workshop has space
                workshop = application.workshop
                if workshop.registered_count < workshop.max_participants:
                    application.status = 'approved'
                    workshop.registered_count += 1
                    self.db.commit()
                    return True
                else:
                    application.status = 'waitlist'
                    self.db.commit()
                    return False
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error approving application {application_id}: {e}")
            raise
    
    def reject_application(self, application_id: int, reason: str = None) -> bool:
        """Reject workshop application"""
        try:
            application = self.db.query(WorkshopApplication).filter(
                WorkshopApplication.id == application_id
            ).first()
            
            if application:
                application.status = 'rejected'
                if reason:
                    application.notes = reason
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error rejecting application {application_id}: {e}")
            raise
    
    def update_workshop_status(self, workshop_id: int, status: str) -> bool:
        """Update workshop status"""
        try:
            workshop = self.get(workshop_id)
            if workshop:
                workshop.status = status
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating workshop {workshop_id} status: {e}")
            raise