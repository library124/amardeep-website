"""
Analytics API Views using SQLAlchemy and TiDB Cloud
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from database.analytics import AnalyticsService
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def dashboard_analytics(request):
    """Get dashboard analytics data"""
    try:
        days = int(request.GET.get('days', 30))
        
        with AnalyticsService() as analytics:
            data = analytics.get_dashboard_metrics(days)
        
        return Response({
            'success': True,
            'data': data,
            'period_days': days
        })
        
    except Exception as e:
        logger.error(f"Error in dashboard_analytics: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def revenue_trends(request):
    """Get revenue trends over time"""
    try:
        days = int(request.GET.get('days', 90))
        
        with AnalyticsService() as analytics:
            data = analytics.get_revenue_trends(days)
        
        return Response({
            'success': True,
            'data': data,
            'period_days': days
        })
        
    except Exception as e:
        logger.error(f"Error in revenue_trends: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def top_content(request):
    """Get top performing content"""
    try:
        limit = int(request.GET.get('limit', 10))
        
        with AnalyticsService() as analytics:
            data = analytics.get_top_performing_content(limit)
        
        return Response({
            'success': True,
            'data': data,
            'limit': limit
        })
        
    except Exception as e:
        logger.error(f"Error in top_content: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def user_engagement(request):
    """Get user engagement metrics"""
    try:
        with AnalyticsService() as analytics:
            data = analytics.get_user_engagement_metrics()
        
        return Response({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        logger.error(f"Error in user_engagement: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def workshop_performance(request):
    """Get workshop performance analytics"""
    try:
        with AnalyticsService() as analytics:
            data = analytics.get_workshop_performance()
        
        return Response({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        logger.error(f"Error in workshop_performance: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def newsletter_performance(request):
    """Get newsletter performance metrics"""
    try:
        with AnalyticsService() as analytics:
            data = analytics.get_newsletter_performance()
        
        return Response({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        logger.error(f"Error in newsletter_performance: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def trading_service_metrics(request):
    """Get trading service performance metrics"""
    try:
        with AnalyticsService() as analytics:
            data = analytics.get_trading_service_metrics()
        
        return Response({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        logger.error(f"Error in trading_service_metrics: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def monthly_report(request):
    """Get monthly analytics report"""
    try:
        year = int(request.GET.get('year', 2024))
        month = int(request.GET.get('month', 1))
        
        with AnalyticsService() as analytics:
            data = analytics.get_monthly_report(year, month)
        
        return Response({
            'success': True,
            'data': data,
            'year': year,
            'month': month
        })
        
    except Exception as e:
        logger.error(f"Error in monthly_report: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def sync_analytics_data(request):
    """Trigger analytics data sync"""
    try:
        from database.sync import DataSyncManager
        
        sync_type = request.data.get('type', 'all')
        
        with DataSyncManager() as sync_manager:
            if sync_type == 'all':
                sync_manager.full_sync()
            elif sync_type == 'users':
                sync_manager.sync_user_analytics()
            elif sync_type == 'workshops':
                sync_manager.sync_workshop_analytics()
            elif sync_type == 'content':
                sync_manager.sync_content_analytics()
            elif sync_type == 'revenue':
                sync_manager.sync_revenue_analytics()
            elif sync_type == 'newsletters':
                sync_manager.sync_newsletter_analytics()
            elif sync_type == 'services':
                sync_manager.sync_trading_service_analytics()
        
        return Response({
            'success': True,
            'message': f'{sync_type.title()} analytics data synced successfully'
        })
        
    except Exception as e:
        logger.error(f"Error in sync_analytics_data: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)