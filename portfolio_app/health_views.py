# Health Check Views for API monitoring
# Following SOLID principles for robust health monitoring

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import time
import os
from datetime import datetime

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Simple health check endpoint
    Returns basic health status of the API
    """
    try:
        start_time = time.time()
        
        # Basic health checks
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "environment": "development" if settings.DEBUG else "production",
            "database": check_database_health(),
            "services": check_services_health(),
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }
        
        # Determine overall status
        if not health_data["database"]["healthy"]:
            health_data["status"] = "degraded"
        
        return JsonResponse(health_data, status=200)
        
    except Exception as e:
        return JsonResponse({
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }, status=503)

def check_database_health():
    """Check database connectivity"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return {
            "healthy": True,
            "message": "Database connection successful"
        }
    except Exception as e:
        return {
            "healthy": False,
            "message": f"Database connection failed: {str(e)}"
        }

def check_services_health():
    """Check external services health"""
    services = {}
    
    # Check Razorpay configuration
    services["razorpay"] = {
        "configured": bool(getattr(settings, 'RAZORPAY_KEY_ID', None)),
        "message": "Razorpay configured" if getattr(settings, 'RAZORPAY_KEY_ID', None) else "Razorpay not configured"
    }
    
    # Check email configuration
    services["email"] = {
        "configured": bool(getattr(settings, 'EMAIL_HOST', None)),
        "message": "Email configured" if getattr(settings, 'EMAIL_HOST', None) else "Email not configured"
    }
    
    return services

@csrf_exempt
@require_http_methods(["GET"])
def api_status(request):
    """
    Detailed API status endpoint
    Returns comprehensive status information
    """
    try:
        return JsonResponse({
            "api_version": "1.0.0",
            "django_version": getattr(settings, 'DJANGO_VERSION', 'Unknown'),
            "debug_mode": settings.DEBUG,
            "allowed_hosts": settings.ALLOWED_HOSTS,
            "cors_origins": getattr(settings, 'CORS_ALLOWED_ORIGINS', []),
            "installed_apps": [
                app for app in settings.INSTALLED_APPS 
                if not app.startswith('django.')
            ],
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def payment_status(request):
    """
    Payment system status endpoint
    Returns payment gateway configuration status
    """
    try:
        razorpay_configured = bool(getattr(settings, 'RAZORPAY_KEY_ID', None))
        
        return JsonResponse({
            "payment_gateway": "Razorpay",
            "configured": razorpay_configured,
            "test_mode": True,  # Assuming test mode for development
            "currency": getattr(settings, 'PAYMENT_CURRENCY', 'INR'),
            "status": "operational" if razorpay_configured else "not_configured",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }, status=500)