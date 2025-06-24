"""
SQLAlchemy Integration Views
These views demonstrate using SQLAlchemy with TiDB Cloud alongside Django
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status, generics
from database.services import UserService, ContentService, WorkshopService, ProductService, PaymentService
from database.django_integration import db_manager
from .models import Workshop, BlogPost, TradingService
from .serializers import WorkshopSerializer, BlogPostListSerializer, TradingServiceSerializer
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
def database_health_check(request):
    """Check TiDB Cloud database health"""
    try:
        health_status = db_manager.health_check()
        return Response({
            'success': True,
            'database_connected': health_status,
            'message': 'TiDB Cloud is healthy' if health_status else 'TiDB Cloud connection failed',
            'database_type': 'TiDB Cloud'
        })
    except Exception as e:
        logger.error(f"Database health check error: {e}")
        return Response({
            'success': False,
            'database_connected': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def initialize_tidb_database(request):
    """Initialize TiDB Cloud database"""
    try:
        success = db_manager.initialize_database()
        
        if success:
            return Response({
                'success': True,
                'message': 'TiDB Cloud database initialized successfully'
            })
        else:
            return Response({
                'success': False,
                'message': 'TiDB Cloud database initialization failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WorkshopListSQLAlchemyView(generics.ListAPIView):
    """Workshop list using SQLAlchemy for enhanced performance"""
    serializer_class = WorkshopSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        # Use SQLAlchemy for complex queries
        try:
            with WorkshopService() as workshop_service:
                # Get upcoming workshops using SQLAlchemy
                workshops = workshop_service.get_upcoming_workshops(limit=20)
                
                # Convert SQLAlchemy objects to Django model instances for serializer
                workshop_ids = [w.id for w in workshops]
                return Workshop.objects.filter(id__in=workshop_ids).select_related('instructor')
        except Exception as e:
            logger.error(f"Error getting workshops from SQLAlchemy: {e}")
            # Fallback to Django ORM
            return Workshop.objects.filter(
                is_active=True,
                start_date__gt=timezone.now() - timezone.timedelta(days=30)
            ).select_related('instructor').order_by('start_date')[:20]

class BlogPostListSQLAlchemyView(generics.ListAPIView):
    """Blog post list using SQLAlchemy for enhanced performance"""
    serializer_class = BlogPostListSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        # Use SQLAlchemy for complex queries
        try:
            with ContentService() as content_service:
                # Get published posts using SQLAlchemy
                posts = content_service.get_published_posts(limit=20)
                
                # Convert SQLAlchemy objects to Django model instances for serializer
                post_ids = [p.id for p in posts]
                return BlogPost.objects.filter(id__in=post_ids).select_related('author', 'category').prefetch_related('tags')
        except Exception as e:
            logger.error(f"Error getting blog posts from SQLAlchemy: {e}")
            # Fallback to Django ORM
            return BlogPost.objects.filter(
                status='published',
                publish_date__lte=timezone.now()
            ).select_related('author', 'category').prefetch_related('tags')[:20]

class TradingServiceListSQLAlchemyView(generics.ListAPIView):
    """Trading service list using SQLAlchemy for enhanced performance"""
    serializer_class = TradingServiceSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        # Use SQLAlchemy for complex queries
        try:
            with ProductService() as product_service:
                # Get active services using SQLAlchemy
                services = product_service.get_active_services(limit=20)
                
                # Convert SQLAlchemy objects to Django model instances for serializer
                service_ids = [s.id for s in services]
                return TradingService.objects.filter(id__in=service_ids)
        except Exception as e:
            logger.error(f"Error getting trading services from SQLAlchemy: {e}")
            # Fallback to Django ORM
            return TradingService.objects.filter(is_active=True).order_by('display_order', 'name')[:20]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard_sqlalchemy(request):
    """Enhanced user dashboard using SQLAlchemy"""
    try:
        user_id = request.user.id
        
        # Get user data using SQLAlchemy
        with UserService() as user_service:
            user_data = user_service.get_user_with_profile(user_id)
            achievements = user_service.get_user_achievements(user_id)
            courses = user_service.get_user_courses(user_id)
        
        # Prepare response data
        dashboard_data = {
            'user': {
                'id': user_data.id if user_data else request.user.id,
                'username': user_data.username if user_data else request.user.username,
                'email': user_data.email if user_data else request.user.email,
                'full_name': user_data.full_name if user_data else request.user.get_full_name(),
            },
            'profile': {
                'trading_experience': user_data.profile.trading_experience if user_data and user_data.profile else 'beginner',
                'preferred_market': user_data.profile.preferred_market if user_data and user_data.profile else None,
                'phone': user_data.profile.phone if user_data and user_data.profile else None,
                'bio': user_data.profile.bio if user_data and user_data.profile else None,
            } if user_data and user_data.profile else {},
            'achievements_count': len(achievements),
            'courses_count': len(courses),
            'active_courses_count': len([c for c in courses if c.is_active]),
            'total_spent': sum([float(c.amount_paid) for c in courses]),
        }
        
        return Response({
            'success': True,
            'data': dashboard_data,
            'source': 'SQLAlchemy + TiDB Cloud'
        })
        
    except Exception as e:
        logger.error(f"Error in SQLAlchemy dashboard: {e}")
        # Fallback to Django ORM
        from .models import UserProfile, PurchasedCourse
        from .serializers import UserProfileSerializer, UserDetailSerializer
        
        try:
            profile = request.user.profile
            profile_data = UserProfileSerializer(profile).data
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
            profile_data = UserProfileSerializer(profile).data
        
        purchased_courses = PurchasedCourse.objects.filter(user=request.user)
        
        return Response({
            'success': True,
            'data': {
                'user': UserDetailSerializer(request.user).data,
                'profile': profile_data,
                'courses_count': purchased_courses.count(),
                'active_courses_count': purchased_courses.filter(status='active').count(),
                'source': 'Django ORM (Fallback)'
            }
        })

@api_view(['GET'])
@permission_classes([AllowAny])
def sqlalchemy_demo_data(request):
    """Demo endpoint showing SQLAlchemy data retrieval"""
    try:
        demo_data = {}
        
        # Get workshops using SQLAlchemy
        with WorkshopService() as workshop_service:
            workshops = workshop_service.get_upcoming_workshops(limit=5)
            demo_data['workshops'] = [
                {
                    'id': w.id,
                    'title': w.title,
                    'is_paid': w.is_paid,
                    'price': float(w.price) if w.price else 0,
                    'start_date': w.start_date.isoformat(),
                    'spots_remaining': w.spots_remaining
                }
                for w in workshops
            ]
        
        # Get blog posts using SQLAlchemy
        with ContentService() as content_service:
            posts = content_service.get_published_posts(limit=5)
            demo_data['blog_posts'] = [
                {
                    'id': p.id,
                    'title': p.title,
                    'views_count': p.total_views,
                    'publish_date': p.publish_date.isoformat()
                }
                for p in posts
            ]
        
        # Get trading services using SQLAlchemy
        with ProductService() as product_service:
            services = product_service.get_active_services(limit=5)
            demo_data['trading_services'] = [
                {
                    'id': s.id,
                    'name': s.name,
                    'service_type': s.service_type,
                    'price': float(s.price),
                    'is_featured': s.is_featured
                }
                for s in services
            ]
        
        return Response({
            'success': True,
            'message': 'Data retrieved from TiDB Cloud using SQLAlchemy',
            'data': demo_data,
            'database_type': 'TiDB Cloud',
            'orm': 'SQLAlchemy'
        })
        
    except Exception as e:
        logger.error(f"Error in SQLAlchemy demo: {e}")
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve data from TiDB Cloud'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)