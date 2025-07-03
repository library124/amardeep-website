#!/usr/bin/env python3
"""
Simple Django startup test
Tests if Django can import all modules and start properly
"""

import os
import sys
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

def test_django_setup():
    """Test Django setup and imports"""
    try:
        print("🔧 Testing Django setup...")
        
        # Setup Django
        django.setup()
        print("✅ Django setup successful")
        
        # Test imports
        print("🔧 Testing imports...")
        
        # Test Django core imports
        from django.conf import settings
        from django.urls import reverse
        from django.http import JsonResponse
        print("✅ Django core imports successful")
        
        # Test app imports
        from portfolio_app.models import Workshop, Course, TradingService
        from portfolio_app.views.payment_views_razorpay import CreateWorkshopOrderView
        from portfolio_app.health_views import health_check
        print("✅ App imports successful")
        
        # Test URL configuration
        from django.urls import get_resolver
        resolver = get_resolver()
        print("✅ URL configuration valid")
        
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        print("✅ Database connection successful")
        
        print("\n🎉 All tests passed! Django is ready to start.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health_endpoints():
    """Test health check endpoints"""
    try:
        print("\n🔧 Testing health endpoints...")
        
        from django.test import RequestFactory
        from portfolio_app.health_views import health_check, api_status, payment_status
        
        factory = RequestFactory()
        
        # Test health check
        request = factory.get('/api/health/')
        response = health_check(request)
        print(f"✅ Health check: {response.status_code}")
        
        # Test API status
        request = factory.get('/api/status/')
        response = api_status(request)
        print(f"✅ API status: {response.status_code}")
        
        # Test payment status
        request = factory.get('/api/payment/status/')
        response = payment_status(request)
        print(f"✅ Payment status: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Django Startup Test")
    print("=" * 50)
    
    success = True
    
    # Test Django setup
    if not test_django_setup():
        success = False
    
    # Test health endpoints
    if not test_health_endpoints():
        success = False
    
    if success:
        print("\n✅ All tests passed! You can now start the Django server with:")
        print("   python manage.py runserver")
    else:
        print("\n❌ Some tests failed. Please fix the issues before starting the server.")
    
    return success

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)