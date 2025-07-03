"""
Health Check System for Portfolio Application
Following SOLID principles for robust monitoring and diagnostics

Author: Amardeep Asode
"""

import os
import time
import logging
from typing import Dict, Any, List, Optional
from django.conf import settings
from django.db import connection
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import requests

logger = logging.getLogger(__name__)

class HealthCheckInterface:
    """Interface for health check implementations (Interface Segregation Principle)"""
    
    def check(self) -> Dict[str, Any]:
        """Perform health check and return status"""
        raise NotImplementedError

class DatabaseHealthCheck(HealthCheckInterface):
    """Single Responsibility: Database connectivity health check"""
    
    def check(self) -> Dict[str, Any]:
        """Check database connectivity and performance"""
        try:
            start_time = time.time()
            
            # Test database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            return {
                "status": "healthy",
                "response_time_ms": round(response_time, 2),
                "database_engine": settings.DATABASES['default']['ENGINE'],
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }

class CacheHealthCheck(HealthCheckInterface):
    """Single Responsibility: Cache system health check"""
    
    def check(self) -> Dict[str, Any]:
        """Check cache system functionality"""
        try:
            start_time = time.time()
            
            # Test cache write and read
            test_key = "health_check_test"
            test_value = f"test_{int(time.time())}"
            
            cache.set(test_key, test_value, 60)
            retrieved_value = cache.get(test_key)
            
            if retrieved_value != test_value:
                raise Exception("Cache write/read mismatch")
            
            # Clean up test data
            cache.delete(test_key)
            
            response_time = (time.time() - start_time) * 1000
            
            return {
                "status": "healthy",
                "response_time_ms": round(response_time, 2),
                "cache_backend": settings.CACHES['default']['BACKEND'],
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Cache health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }

class EmailHealthCheck(HealthCheckInterface):
    """Single Responsibility: Email service health check"""
    
    def check(self) -> Dict[str, Any]:
        """Check email service configuration"""
        try:
            # Check email configuration
            email_config = {
                "host": getattr(settings, 'EMAIL_HOST', None),
                "port": getattr(settings, 'EMAIL_PORT', None),
                "use_tls": getattr(settings, 'EMAIL_USE_TLS', None),
                "host_user": getattr(settings, 'EMAIL_HOST_USER', None),
            }
            
            # Validate required settings
            required_settings = ['EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_HOST_USER']
            missing_settings = [setting for setting in required_settings 
                              if not getattr(settings, setting, None)]
            
            if missing_settings:
                return {
                    "status": "misconfigured",
                    "error": f"Missing email settings: {missing_settings}",
                    "timestamp": time.time()
                }
            
            return {
                "status": "configured",
                "host": email_config["host"],
                "port": email_config["port"],
                "use_tls": email_config["use_tls"],
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Email health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }

class PaymentHealthCheck(HealthCheckInterface):
    """Single Responsibility: Payment gateway health check"""
    
    def check(self) -> Dict[str, Any]:
        """Check payment gateway configuration"""
        try:
            # Check Razorpay configuration
            razorpay_config = {
                "key_id": getattr(settings, 'RAZORPAY_KEY_ID', None),
                "key_secret": bool(getattr(settings, 'RAZORPAY_KEY_SECRET', None)),
                "webhook_secret": bool(getattr(settings, 'RAZORPAY_WEBHOOK_SECRET', None)),
            }
            
            # Validate configuration
            if not razorpay_config["key_id"]:
                return {
                    "status": "misconfigured",
                    "error": "Razorpay Key ID not configured",
                    "timestamp": time.time()
                }
            
            if not razorpay_config["key_secret"]:
                return {
                    "status": "misconfigured",
                    "error": "Razorpay Key Secret not configured",
                    "timestamp": time.time()
                }
            
            return {
                "status": "configured",
                "provider": "Razorpay",
                "key_id": razorpay_config["key_id"],
                "currency": getattr(settings, 'PAYMENT_CURRENCY', 'INR'),
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Payment health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }

class ExternalServiceHealthCheck(HealthCheckInterface):
    """Single Responsibility: External services health check"""
    
    def check(self) -> Dict[str, Any]:
        """Check external service connectivity"""
        try:
            services_status = {}
            
            # Check frontend connectivity
            frontend_url = getattr(settings, 'FRONTEND_URL', None)
            if frontend_url:
                try:
                    start_time = time.time()
                    response = requests.get(frontend_url, timeout=10)
                    response_time = (time.time() - start_time) * 1000
                    
                    services_status["frontend"] = {
                        "status": "healthy" if response.status_code == 200 else "unhealthy",
                        "status_code": response.status_code,
                        "response_time_ms": round(response_time, 2),
                        "url": frontend_url
                    }
                except Exception as e:
                    services_status["frontend"] = {
                        "status": "unreachable",
                        "error": str(e),
                        "url": frontend_url
                    }
            
            # Check Brevo API connectivity
            brevo_api_key = getattr(settings, 'BREVO_API_KEY', None)
            if brevo_api_key:
                try:
                    start_time = time.time()
                    headers = {
                        'accept': 'application/json',
                        'api-key': brevo_api_key
                    }
                    response = requests.get(
                        'https://api.brevo.com/v3/account',
                        headers=headers,
                        timeout=10
                    )
                    response_time = (time.time() - start_time) * 1000
                    
                    services_status["brevo"] = {
                        "status": "healthy" if response.status_code == 200 else "unhealthy",
                        "status_code": response.status_code,
                        "response_time_ms": round(response_time, 2)
                    }
                except Exception as e:
                    services_status["brevo"] = {
                        "status": "unreachable",
                        "error": str(e)
                    }
            
            return {
                "status": "checked",
                "services": services_status,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"External services health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }

class HealthCheckAggregator:
    """Single Responsibility: Aggregates all health checks (Dependency Inversion Principle)"""
    
    def __init__(self):
        self.health_checks = {
            "database": DatabaseHealthCheck(),
            "cache": CacheHealthCheck(),
            "email": EmailHealthCheck(),
            "payment": PaymentHealthCheck(),
            "external_services": ExternalServiceHealthCheck()
        }
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all health checks and aggregate results"""
        results = {}
        overall_status = "healthy"
        
        for check_name, health_check in self.health_checks.items():
            try:
                result = health_check.check()
                results[check_name] = result
                
                # Determine overall status
                if result.get("status") in ["unhealthy", "misconfigured", "unreachable"]:
                    overall_status = "degraded"
                    
            except Exception as e:
                logger.error(f"Health check {check_name} failed: {str(e)}")
                results[check_name] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": time.time()
                }
                overall_status = "degraded"
        
        return {
            "overall_status": overall_status,
            "timestamp": time.time(),
            "checks": results,
            "version": "1.0.0",
            "environment": "production" if not settings.DEBUG else "development"
        }

# Health check views
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Main health check endpoint"""
    try:
        aggregator = HealthCheckAggregator()
        health_data = aggregator.run_all_checks()
        
        # Determine HTTP status code based on overall health
        status_code = 200 if health_data["overall_status"] == "healthy" else 503
        
        return JsonResponse(health_data, status=status_code)
        
    except Exception as e:
        logger.error(f"Health check endpoint failed: {str(e)}")
        return JsonResponse({
            "overall_status": "error",
            "error": str(e),
            "timestamp": time.time()
        }, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def simple_health_check(request):
    """Simple health check for load balancers"""
    try:
        # Quick database check
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            "status": "ok",
            "timestamp": time.time()
        })
        
    except Exception as e:
        logger.error(f"Simple health check failed: {str(e)}")
        return JsonResponse({
            "status": "error",
            "error": str(e),
            "timestamp": time.time()
        }, status=503)

@api_view(['GET'])
@permission_classes([AllowAny])
def readiness_check(request):
    """Readiness check for Kubernetes/container orchestration"""
    try:
        # Check if application is ready to serve traffic
        checks = {
            "database": DatabaseHealthCheck().check(),
            "cache": CacheHealthCheck().check()
        }
        
        # Application is ready if critical services are healthy
        is_ready = all(
            check.get("status") == "healthy" 
            for check in checks.values()
        )
        
        status_code = 200 if is_ready else 503
        
        return JsonResponse({
            "ready": is_ready,
            "checks": checks,
            "timestamp": time.time()
        }, status=status_code)
        
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return JsonResponse({
            "ready": False,
            "error": str(e),
            "timestamp": time.time()
        }, status=503)

@api_view(['GET'])
@permission_classes([AllowAny])
def liveness_check(request):
    """Liveness check for Kubernetes/container orchestration"""
    try:
        # Simple check to verify the application is alive
        return JsonResponse({
            "alive": True,
            "timestamp": time.time(),
            "version": "1.0.0"
        })
        
    except Exception as e:
        logger.error(f"Liveness check failed: {str(e)}")
        return JsonResponse({
            "alive": False,
            "error": str(e),
            "timestamp": time.time()
        }, status=503)