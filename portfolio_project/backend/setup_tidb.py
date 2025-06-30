#!/usr/bin/env python
"""
TiDB Cloud Setup and Data Sync Script
This script will:
1. Create all necessary tables in TiDB Cloud
2. Sync data from Django SQLite to TiDB Cloud
3. Test the integration
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User as DjangoUser
from portfolio_app.models import *
from database.config import engine, Base, SessionLocal
from database.models.analytics_models import *
from database.sync import DataSyncManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tidb_tables():
    """Create all SQLAlchemy tables in TiDB Cloud"""
    try:
        print("🏗️  Creating TiDB Cloud tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ TiDB Cloud tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating TiDB tables: {e}")
        return False

def sync_django_to_tidb():
    """Sync Django data to TiDB Cloud"""
    try:
        print("🔄 Syncing Django data to TiDB Cloud...")
        
        with DataSyncManager() as sync_manager:
            print("  - Syncing user analytics...")
            sync_manager.sync_user_analytics()
            
            print("  - Syncing workshop analytics...")
            sync_manager.sync_workshop_analytics()
            
            print("  - Syncing content analytics...")
            sync_manager.sync_content_analytics()
            
            print("  - Syncing revenue analytics...")
            sync_manager.sync_revenue_analytics()
            
            print("  - Syncing newsletter analytics...")
            sync_manager.sync_newsletter_analytics()
            
            print("  - Syncing trading service analytics...")
            sync_manager.sync_trading_service_analytics()
        
        print("✅ Data sync completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Error syncing data: {e}")
        return False

def test_tidb_connection():
    """Test TiDB Cloud connection and data"""
    try:
        print("🧪 Testing TiDB Cloud connection...")
        
        with SessionLocal() as db:
            # Test basic connection
            from sqlalchemy import text
            result = db.execute(text("SELECT 1 as test")).fetchone()
            if result:
                print("✅ TiDB Cloud connection successful!")
            
            # Test data counts
            user_count = db.query(UserAnalytics).count()
            workshop_count = db.query(WorkshopAnalytics).count()
            content_count = db.query(ContentAnalytics).count()
            
            print(f"📊 TiDB Cloud Data Counts:")
            print(f"  - User Analytics: {user_count}")
            print(f"  - Workshop Analytics: {workshop_count}")
            print(f"  - Content Analytics: {content_count}")
            
        return True
    except Exception as e:
        print(f"❌ Error testing TiDB connection: {e}")
        return False

def create_sample_django_data():
    """Create some sample data in Django if needed"""
    try:
        print("📝 Checking Django sample data...")
        
        # Create a superuser if none exists
        if not DjangoUser.objects.filter(is_superuser=True).exists():
            print("  - Creating superuser...")
            DjangoUser.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
        
        # Create sample achievement if none exists
        if Achievement.objects.count() == 0:
            print("  - Creating sample achievements...")
            # Get a user for the achievement
            user = DjangoUser.objects.first()
            if user:
                Achievement.objects.create(
                    title="Trading Expert Certification",
                    description="Completed advanced trading course with 95% score",
                    date="2024-01-15",
                    user=user,
                    metrics={"profit": 1000, "roi": 0.15}
                )
                Achievement.objects.create(
                    title="Risk Management Specialist",
                    description="Mastered advanced risk management strategies",
                    date="2024-02-20",
                    user=user,
                    metrics={"risk_score": 0.05, "max_drawdown": 0.03}
                )
        
        print("✅ Django sample data ready!")
        return True
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 TiDB Cloud Setup and Integration")
    print("=" * 50)
    
    # Step 1: Create sample Django data if needed
    if not create_sample_django_data():
        return False
    
    # Step 2: Create TiDB tables
    if not create_tidb_tables():
        return False
    
    # Step 3: Sync data from Django to TiDB
    if not sync_django_to_tidb():
        return False
    
    # Step 4: Test the integration
    if not test_tidb_connection():
        return False
    
    print("\n🎉 TiDB Cloud setup completed successfully!")
    print("\n📋 Available API endpoints:")
    print("   GET  /api/tidb/health/           - Health check")
    print("   GET  /api/tidb/demo/             - Demo data from TiDB")
    print("   GET  /api/tidb/workshops/        - Workshops via SQLAlchemy")
    print("   GET  /api/tidb/blog/             - Blog posts via SQLAlchemy")
    print("   GET  /api/tidb/services/         - Trading services via SQLAlchemy")
    print("   GET  /api/tidb/dashboard/        - User dashboard via SQLAlchemy (requires auth)")
    
    return True

if __name__ == "__main__":
    main()