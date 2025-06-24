#!/usr/bin/env python
"""
Test TiDB Cloud Connection Script
Run this to verify SQLAlchemy + TiDB Cloud setup
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent.parent))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def test_tidb_connection():
    """Test TiDB Cloud connection"""
    print("🔍 Testing TiDB Cloud Connection...")
    
    try:
        from database.config import test_connection, init_db
        
        # Test connection
        print("📡 Testing database connection...")
        if test_connection():
            print("✅ TiDB Cloud connection successful!")
        else:
            print("❌ TiDB Cloud connection failed!")
            return False
        
        # Initialize database
        print("🏗️  Initializing database tables...")
        if init_db():
            print("✅ Database tables created successfully!")
        else:
            print("❌ Failed to create database tables!")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_services():
    """Test SQLAlchemy services"""
    print("\n🧪 Testing SQLAlchemy Services...")
    
    try:
        from database.services import UserService, ContentService, WorkshopService, ProductService
        
        # Test UserService
        print("👤 Testing UserService...")
        with UserService() as user_service:
            count = user_service.count()
            print(f"   Users in database: {count}")
        
        # Test ContentService
        print("📝 Testing ContentService...")
        with ContentService() as content_service:
            count = content_service.count()
            print(f"   Blog posts in database: {count}")
        
        # Test WorkshopService
        print("🎓 Testing WorkshopService...")
        with WorkshopService() as workshop_service:
            count = workshop_service.count()
            print(f"   Workshops in database: {count}")
        
        # Test ProductService
        print("🛍️  Testing ProductService...")
        with ProductService() as product_service:
            count = product_service.count()
            print(f"   Products in database: {count}")
        
        print("✅ All services working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Service test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 TiDB Cloud + SQLAlchemy Integration Test")
    print("=" * 50)
    
    # Test connection and initialization
    if not test_tidb_connection():
        print("\n❌ Connection test failed!")
        return
    
    # Test services
    if not test_services():
        print("\n❌ Service test failed!")
        return
    
    print("\n🎉 All tests passed! SQLAlchemy + TiDB Cloud integration is working!")
    print("\n📋 Available API endpoints:")
    print("   GET  /api/tidb/health/          - Check database health")
    print("   POST /api/tidb/initialize/      - Initialize database")
    print("   GET  /api/tidb/demo/            - Demo data from TiDB")
    print("   GET  /api/tidb/workshops/       - Workshops via SQLAlchemy")
    print("   GET  /api/tidb/blog/            - Blog posts via SQLAlchemy")
    print("   GET  /api/tidb/services/        - Trading services via SQLAlchemy")
    print("   GET  /api/tidb/dashboard/       - User dashboard via SQLAlchemy")

if __name__ == "__main__":
    main()