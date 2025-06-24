from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
import uuid
from .services.brevo_service import brevo_service
from database.services import UserService, ContentService, WorkshopService, ProductService, PaymentService
from database.django_integration import db_manager
import logging

logger = logging.getLogger(__name__)
from .models import (
    Achievement, DigitalProduct, Subscriber, Newsletter, BlogPost, 
    BlogCategory, BlogTag, Workshop, WorkshopApplication, Payment,
    TradingService, ServiceBooking, UserProfile, PurchasedCourse,
    ContactMessage
)
from .serializers import (
    UserRegistrationSerializer, AchievementSerializer, DigitalProductSerializer, 
    SubscriberSerializer, NewsletterSerializer, BlogPostListSerializer, 
    BlogPostDetailSerializer, BlogCategorySerializer, BlogTagSerializer, 
    WorkshopSerializer, WorkshopApplicationSerializer, PaymentSerializer,
    BlogPostCreateUpdateSerializer, WorkshopCreateUpdateSerializer,
    TradingServiceSerializer, TradingServiceCreateUpdateSerializer,
    ServiceBookingSerializer, ServiceBookingCreateSerializer,
    UserProfileSerializer, UserDetailSerializer, PurchasedCourseSerializer,
    ChangePasswordSerializer
)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Find user by email since frontend sends email
        try:
            user = User.objects.get(email=email)
            # Use Django's built-in authenticate with username
            user = authenticate(username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class AchievementListCreateView(generics.ListCreateAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AchievementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class DigitalProductListView(generics.ListAPIView):
    queryset = DigitalProduct.objects.all()
    serializer_class = DigitalProductSerializer
    permission_classes = (permissions.AllowAny,)

class DigitalProductDetailView(generics.RetrieveAPIView):
    queryset = DigitalProduct.objects.all()
    serializer_class = DigitalProductSerializer
    permission_classes = (permissions.AllowAny,)

class SubscribeNewsletterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SubscriberSerializer(data=request.data)
        if serializer.is_valid():
            subscriber = serializer.save()
            
            # Send confirmation email using Brevo
            try:
                email_sent = brevo_service.send_newsletter_confirmation(subscriber)
                
                if email_sent:
                    return Response({
                        'message': 'Subscription successful! Please check your email to confirm.',
                        'email': subscriber.email
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        'message': 'Subscription created but confirmation email failed to send. Please contact support.',
                        'email': subscriber.email
                    }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                print(f"Email sending failed: {e}")  # Log the error
                return Response({
                    'message': f'Subscription created but confirmation email failed to send. Please contact support.',
                    'email': subscriber.email
                }, status=status.HTTP_201_CREATED)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmSubscriptionView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, token):
        try:
            subscriber = Subscriber.objects.get(confirmation_token=token, is_active=True)
            if not subscriber.is_confirmed:
                subscriber.confirm_subscription()
                return Response({
                    'message': 'Subscription confirmed successfully! Welcome to Amardeep\'s Trading Insights.',
                    'email': subscriber.email
                })
            else:
                return Response({
                    'message': 'Subscription already confirmed.',
                    'email': subscriber.email
                })
        except Subscriber.DoesNotExist:
            return Response({
                'error': 'Invalid confirmation token.'
            }, status=status.HTTP_404_NOT_FOUND)

class UnsubscribeView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, token):
        try:
            subscriber = Subscriber.objects.get(confirmation_token=token)
            subscriber.is_active = False
            subscriber.save()
            return Response({
                'message': 'Successfully unsubscribed from newsletter.',
                'email': subscriber.email
            })
        except Subscriber.DoesNotExist:
            return Response({
                'error': 'Invalid unsubscribe token.'
            }, status=status.HTTP_404_NOT_FOUND)

class NewsletterListView(generics.ListAPIView):
    queryset = Newsletter.objects.filter(is_sent=True)
    serializer_class = NewsletterSerializer
    permission_classes = (permissions.AllowAny,)

# Blog Views
class BlogPostListView(generics.ListAPIView):
    serializer_class = BlogPostListSerializer
    permission_classes = (permissions.AllowAny,)
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(
            status='published',
            publish_date__lte=timezone.now()
        ).select_related('author', 'category').prefetch_related('tags')
        
        # Filter by category
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by tag
        tag_slug = self.request.query_params.get('tag', None)
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        # Filter featured posts
        featured = self.request.query_params.get('featured', None)
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset

# Dashboard Views

class UserDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Get user profile
        try:
            profile = user.profile
            profile_data = UserProfileSerializer(profile).data
        except UserProfile.DoesNotExist:
            # Create profile if it doesn't exist
            profile = UserProfile.objects.create(user=user)
            profile_data = UserProfileSerializer(profile).data
        
        # Get purchased courses
        purchased_courses = PurchasedCourse.objects.filter(user=user).order_by('-purchase_date')
        courses_data = PurchasedCourseSerializer(purchased_courses, many=True).data
        
        # Get user details
        user_data = UserDetailSerializer(user).data
        
        return Response({
            'user': user_data,
            'profile': profile_data,
            'purchased_courses': courses_data,
            'courses_count': purchased_courses.count(),
            'active_courses_count': purchased_courses.filter(status='active').count()
        })

class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

class UserDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchasedCoursesView(generics.ListAPIView):
    serializer_class = PurchasedCourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PurchasedCourse.objects.filter(user=self.request.user).order_by('-purchase_date')

class CourseAccessView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, course_id):
        try:
            course = PurchasedCourse.objects.get(id=course_id, user=request.user)
            if course.is_active:
                course.mark_accessed()
                return Response({
                    'message': 'Course accessed successfully',
                    'access_url': course.access_url,
                    'access_credentials': course.access_credentials
                })
            else:
                return Response({
                    'error': 'Course is not active or has expired'
                }, status=status.HTTP_403_FORBIDDEN)
        except PurchasedCourse.DoesNotExist:
            return Response({
                'error': 'Course not found'
            }, status=status.HTTP_404_NOT_FOUND)

class BlogPostDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.filter(
        status='published',
        publish_date__lte=timezone.now()
    ).select_related('author', 'category').prefetch_related('tags')
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny,)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class BlogCategoryListView(generics.ListAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = (permissions.AllowAny,)

class BlogTagListView(generics.ListAPIView):
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    permission_classes = (permissions.AllowAny,)

class FeaturedBlogPostsView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(
        status='published',
        publish_date__lte=timezone.now(),
        is_featured=True
    ).select_related('author', 'category').prefetch_related('tags')[:3]
    serializer_class = BlogPostListSerializer
    permission_classes = (permissions.AllowAny,)

# Workshop Views
class WorkshopListView(generics.ListAPIView):
    serializer_class = WorkshopSerializer
    permission_classes = (permissions.AllowAny,)
    
    def get_queryset(self):
        queryset = Workshop.objects.filter(
            is_active=True
        ).select_related('instructor')
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by type (paid/free)
        workshop_type = self.request.query_params.get('type', None)
        if workshop_type == 'free':
            queryset = queryset.filter(is_paid=False)
        elif workshop_type == 'paid':
            queryset = queryset.filter(is_paid=True)
        
        # Filter featured workshops
        featured = self.request.query_params.get('featured', None)
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset.order_by('-start_date')

class WorkshopDetailView(generics.RetrieveAPIView):
    queryset = Workshop.objects.filter(is_active=True).select_related('instructor')
    serializer_class = WorkshopSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny,)

class FeaturedWorkshopsView(generics.ListAPIView):
    queryset = Workshop.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('instructor')[:3]
    serializer_class = WorkshopSerializer
    permission_classes = (permissions.AllowAny,)

class UpcomingWorkshopsView(generics.ListAPIView):
    serializer_class = WorkshopSerializer
    permission_classes = (permissions.AllowAny,)
    
    def get_queryset(self):
        # Show upcoming workshops (future dates) and also recent workshops (within last 30 days)
        # This ensures workshops are visible even if the date is slightly in the past
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        
        return Workshop.objects.filter(
            is_active=True,
            status='upcoming',
            start_date__gt=thirty_days_ago  # Changed from timezone.now() to be more lenient
        ).select_related('instructor').order_by('start_date')[:5]

class ActiveWorkshopsView(generics.ListAPIView):
    """View for all active workshops regardless of date - useful for frontend display"""
    serializer_class = WorkshopSerializer
    permission_classes = (permissions.AllowAny,)
    
    def get_queryset(self):
        return Workshop.objects.filter(
            is_active=True
        ).select_related('instructor').order_by('-is_featured', 'start_date')[:10]

# CRUD ViewSets for comprehensive management

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DigitalProductViewSet(viewsets.ModelViewSet):
    queryset = DigitalProduct.objects.all()
    serializer_class = DigitalProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class BlogTagViewSet(viewsets.ModelViewSet):
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BlogPostCreateUpdateSerializer
        elif self.action == 'retrieve':
            return BlogPostDetailSerializer
        return BlogPostListSerializer
    
    def get_queryset(self):
        queryset = BlogPost.objects.all().select_related('author', 'category').prefetch_related('tags')
        
        # Filter published posts for non-authenticated users
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published', publish_date__lte=timezone.now())
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count for published posts
        if instance.status == 'published':
            instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class WorkshopViewSet(viewsets.ModelViewSet):
    queryset = Workshop.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return WorkshopCreateUpdateSerializer
        return WorkshopSerializer
    
    def get_queryset(self):
        queryset = Workshop.objects.all().select_related('instructor')
        
        # Filter active workshops for non-authenticated users
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_active=True)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def apply(self, request, slug=None):
        """Apply for a workshop"""
        workshop = self.get_object()
        serializer = WorkshopApplicationSerializer(data=request.data)
        
        if serializer.is_valid():
            # Check if user already applied
            existing_application = WorkshopApplication.objects.filter(
                workshop=workshop,
                email=serializer.validated_data['email']
            ).first()
            
            if existing_application:
                return Response({
                    'error': 'You have already applied for this workshop.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            application = serializer.save(workshop=workshop)
            
            # Create payment if workshop is paid
            if workshop.is_paid:
                payment = Payment.objects.create(
                    payment_id=f"PAY_{uuid.uuid4().hex[:12].upper()}",
                    amount=workshop.price,
                    currency=workshop.currency,
                    payment_type='workshop',
                    customer_name=application.name,
                    customer_email=application.email,
                    customer_phone=application.phone,
                    workshop_application=application
                )
                
                return Response({
                    'message': 'Application submitted successfully. Please complete payment.',
                    'application_id': application.id,
                    'payment_id': payment.payment_id,
                    'amount': payment.amount,
                    'currency': payment.currency,
                    'requires_payment': True
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message': 'Application submitted successfully for free workshop.',
                    'application_id': application.id,
                    'requires_payment': False
                }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WorkshopApplicationViewSet(viewsets.ModelViewSet):
    queryset = WorkshopApplication.objects.all()
    serializer_class = WorkshopApplicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = WorkshopApplication.objects.all().select_related('workshop')
        
        # Filter by workshop if specified
        workshop_slug = self.request.query_params.get('workshop', None)
        if workshop_slug:
            queryset = queryset.filter(workshop__slug=workshop_slug)
        
        # Filter by email for non-authenticated users
        email = self.request.query_params.get('email', None)
        if email and not self.request.user.is_authenticated:
            queryset = queryset.filter(email=email)
        
        return queryset

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def complete(self, request, pk=None):
        """Mark payment as completed"""
        payment = self.get_object()
        
        gateway_payment_id = request.data.get('gateway_payment_id')
        payment_method = request.data.get('payment_method', 'online')
        gateway_response = request.data.get('gateway_response', {})
        
        if not gateway_payment_id:
            return Response({
                'error': 'Gateway payment ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        payment.mark_completed(gateway_payment_id, payment_method, gateway_response)
        
        return Response({
            'message': 'Payment completed successfully',
            'payment_id': payment.payment_id,
            'status': payment.status
        })
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def verify(self, request):
        """Verify payment status"""
        payment_id = request.data.get('payment_id')
        
        if not payment_id:
            return Response({
                'error': 'Payment ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payment = Payment.objects.get(payment_id=payment_id)
            return Response({
                'payment_id': payment.payment_id,
                'status': payment.status,
                'amount': payment.amount,
                'currency': payment.currency,
                'customer_name': payment.customer_name,
                'customer_email': payment.customer_email
            })
        except Payment.DoesNotExist:
            return Response({
                'error': 'Payment not found'
            }, status=status.HTTP_404_NOT_FOUND)

# Newsletter CRUD
class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Newsletter.objects.all()
        
        # Show only sent newsletters for non-authenticated users
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_sent=True)
        
        return queryset

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Subscriber.objects.all()
        
        # Filter by email for non-authenticated users
        email = self.request.query_params.get('email', None)
        if email and not self.request.user.is_authenticated:
            queryset = queryset.filter(email=email)
        
        return queryset

# Trading Service Views

class TradingServiceListView(generics.ListAPIView):
    serializer_class = TradingServiceSerializer
    permission_classes = (permissions.AllowAny,)
    
    def get_queryset(self):
        queryset = TradingService.objects.filter(is_active=True)
        
        # Filter by service type
        service_type = self.request.query_params.get('type', None)
        if service_type:
            queryset = queryset.filter(service_type=service_type)
        
        # Filter featured services
        featured = self.request.query_params.get('featured', None)
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset.order_by('display_order', 'name')

class TradingServiceDetailView(generics.RetrieveAPIView):
    queryset = TradingService.objects.filter(is_active=True)
    serializer_class = TradingServiceSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny,)

class FeaturedServicesView(generics.ListAPIView):
    queryset = TradingService.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by('display_order', 'name')[:3]
    serializer_class = TradingServiceSerializer
    permission_classes = (permissions.AllowAny,)

class ServiceBookingCreateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ServiceBookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            
            # Send notification emails using Brevo
            try:
                # Send notification to admin
                admin_email_sent = brevo_service.send_service_booking_notification(booking)
                
                # Send confirmation to customer
                customer_email_sent = brevo_service.send_service_booking_confirmation(booking)
                
                if not admin_email_sent:
                    print(f"Failed to send admin notification for booking {booking.id}")
                if not customer_email_sent:
                    print(f"Failed to send customer confirmation for booking {booking.id}")
                    
            except Exception as e:
                print(f"Failed to send booking emails: {e}")
            
            return Response({
                'message': 'Booking request submitted successfully! We will contact you soon.',
                'booking_id': booking.id,
                'service_name': booking.service.name
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# CRUD ViewSets for Trading Services

class TradingServiceViewSet(viewsets.ModelViewSet):
    queryset = TradingService.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TradingServiceCreateUpdateSerializer
        return TradingServiceSerializer
    
    def get_queryset(self):
        queryset = TradingService.objects.all()
        
        # Filter active services for non-authenticated users
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_active=True)
        
        return queryset.order_by('display_order', 'name')

class ServiceBookingViewSet(viewsets.ModelViewSet):
    queryset = ServiceBooking.objects.all()
    serializer_class = ServiceBookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = ServiceBooking.objects.all().select_related('service')
        
        # Filter by service if specified
        service_slug = self.request.query_params.get('service', None)
        if service_slug:
            queryset = queryset.filter(service__slug=service_slug)
        
        # Filter by email for non-authenticated users
        email = self.request.query_params.get('email', None)
        if email and not self.request.user.is_authenticated:
            queryset = queryset.filter(email=email)
        
        return queryset
 
 #   C o n t a c t   V i e w s  
 f r o m   r e s t _ f r a m e w o r k   i m p o r t   g e n e r i c s ,   p e r m i s s i o n s ,   s t a t u s ,   v i e w s e t s  
 f r o m   r e s t _ f r a m e w o r k . r e s p o n s e   i m p o r t   R e s p o n s e  
 f r o m   r e s t _ f r a m e w o r k . v i e w s   i m p o r t   A P I V i e w  
 f r o m   r e s t _ f r a m e w o r k . d e c o r a t o r s   i m p o r t   a c t i o n  
 f r o m   . m o d e l s   i m p o r t   C o n t a c t M e s s a g e  
 f r o m   . s e r i a l i z e r s   i m p o r t   (  
         C o n t a c t M e s s a g e S e r i a l i z e r ,   C o n t a c t M e s s a g e C r e a t e S e r i a l i z e r ,  
         C o n t a c t M e s s a g e U p d a t e S e r i a l i z e r  
 )  
 f r o m   . s e r v i c e s . b r e v o _ s e r v i c e   i m p o r t   b r e v o _ s e r v i c e  
  
 #   C o n t a c t   V i e w s  
  
 c l a s s   C o n t a c t M e s s a g e C r e a t e V i e w ( A P I V i e w ) :  
         p e r m i s s i o n _ c l a s s e s   =   ( p e r m i s s i o n s . A l l o w A n y , )  
  
         d e f   p o s t ( s e l f ,   r e q u e s t ) :  
                 s e r i a l i z e r   =   C o n t a c t M e s s a g e C r e a t e S e r i a l i z e r ( d a t a = r e q u e s t . d a t a )  
                 i f   s e r i a l i z e r . i s _ v a l i d ( ) :  
                         #   G e t   c l i e n t   I P   a n d   u s e r   a g e n t  
                         i p _ a d d r e s s   =   s e l f . g e t _ c l i e n t _ i p ( r e q u e s t )  
                         u s e r _ a g e n t   =   r e q u e s t . M E T A . g e t ( ' H T T P _ U S E R _ A G E N T ' ,   ' ' )  
                          
                         c o n t a c t _ m e s s a g e   =   s e r i a l i z e r . s a v e (  
                                 i p _ a d d r e s s = i p _ a d d r e s s ,  
                                 u s e r _ a g e n t = u s e r _ a g e n t  
                         )  
                          
                         #   S e n d   n o t i f i c a t i o n   e m a i l s   u s i n g   B r e v o  
                         t r y :  
                                 #   S e n d   n o t i f i c a t i o n   t o   a d m i n  
                                 a d m i n _ e m a i l _ s e n t   =   b r e v o _ s e r v i c e . s e n d _ c o n t a c t _ n o t i f i c a t i o n ( c o n t a c t _ m e s s a g e )  
                                  
                                 #   S e n d   c o n f i r m a t i o n   t o   c u s t o m e r  
                                 c u s t o m e r _ e m a i l _ s e n t   =   b r e v o _ s e r v i c e . s e n d _ c o n t a c t _ c o n f i r m a t i o n ( c o n t a c t _ m e s s a g e )  
                                  
                                 i f   n o t   a d m i n _ e m a i l _ s e n t :  
                                         p r i n t ( f " F a i l e d   t o   s e n d   a d m i n   n o t i f i c a t i o n   f o r   c o n t a c t   m e s s a g e   { c o n t a c t _ m e s s a g e . i d } " )  
                                 i f   n o t   c u s t o m e r _ e m a i l _ s e n t :  
                                         p r i n t ( f " F a i l e d   t o   s e n d   c u s t o m e r   c o n f i r m a t i o n   f o r   c o n t a c t   m e s s a g e   { c o n t a c t _ m e s s a g e . i d } " )  
                                          
                         e x c e p t   E x c e p t i o n   a s   e :  
                                 p r i n t ( f " F a i l e d   t o   s e n d   c o n t a c t   e m a i l s :   { e } " )  
                          
                         r e t u r n   R e s p o n s e ( {  
                                 ' m e s s a g e ' :   ' T h a n k   y o u   f o r   y o u r   m e s s a g e !   I \ ' l l   g e t   b a c k   t o   y o u   s o o n . ' ,  
                                 ' c o n t a c t _ i d ' :   c o n t a c t _ m e s s a g e . i d  
                         } ,   s t a t u s = s t a t u s . H T T P _ 2 0 1 _ C R E A T E D )  
                  
                 r e t u r n   R e s p o n s e ( s e r i a l i z e r . e r r o r s ,   s t a t u s = s t a t u s . H T T P _ 4 0 0 _ B A D _ R E Q U E S T )  
          
         d e f   g e t _ c l i e n t _ i p ( s e l f ,   r e q u e s t ) :  
                 " " " G e t   t h e   c l i e n t ' s   I P   a d d r e s s " " "  
                 x _ f o r w a r d e d _ f o r   =   r e q u e s t . M E T A . g e t ( ' H T T P _ X _ F O R W A R D E D _ F O R ' )  
                 i f   x _ f o r w a r d e d _ f o r :  
                         i p   =   x _ f o r w a r d e d _ f o r . s p l i t ( ' , ' ) [ 0 ]  
                 e l s e :  
                         i p   =   r e q u e s t . M E T A . g e t ( ' R E M O T E _ A D D R ' )  
                 r e t u r n   i p  
  
 c l a s s   C o n t a c t M e s s a g e V i e w S e t ( v i e w s e t s . M o d e l V i e w S e t ) :  
         q u e r y s e t   =   C o n t a c t M e s s a g e . o b j e c t s . a l l ( )  
         p e r m i s s i o n _ c l a s s e s   =   [ p e r m i s s i o n s . I s A u t h e n t i c a t e d O r R e a d O n l y ]  
          
         d e f   g e t _ s e r i a l i z e r _ c l a s s ( s e l f ) :  
                 i f   s e l f . a c t i o n   = =   ' c r e a t e ' :  
                         r e t u r n   C o n t a c t M e s s a g e C r e a t e S e r i a l i z e r  
                 e l i f   s e l f . a c t i o n   i n   [ ' u p d a t e ' ,   ' p a r t i a l _ u p d a t e ' ] :  
                         r e t u r n   C o n t a c t M e s s a g e U p d a t e S e r i a l i z e r  
                 r e t u r n   C o n t a c t M e s s a g e S e r i a l i z e r  
          
         d e f   g e t _ q u e r y s e t ( s e l f ) :  
                 q u e r y s e t   =   C o n t a c t M e s s a g e . o b j e c t s . a l l ( ) . s e l e c t _ r e l a t e d ( ' a s s i g n e d _ t o ' )  
                  
                 #   O n l y   a l l o w   a u t h e n t i c a t e d   u s e r s   t o   s e e   a l l   m e s s a g e s  
                 i f   n o t   s e l f . r e q u e s t . u s e r . i s _ a u t h e n t i c a t e d :  
                         #   F o r   u n a u t h e n t i c a t e d   u s e r s ,   o n l y   a l l o w   c r e a t i n g   m e s s a g e s  
                         r e t u r n   C o n t a c t M e s s a g e . o b j e c t s . n o n e ( )  
                  
                 r e t u r n   q u e r y s e t . o r d e r _ b y ( ' - c r e a t e d _ a t ' )  
          
         d e f   c r e a t e ( s e l f ,   r e q u e s t ,   * a r g s ,   * * k w a r g s ) :  
                 #   A l l o w   u n a u t h e n t i c a t e d   u s e r s   t o   c r e a t e   c o n t a c t   m e s s a g e s  
                 s e r i a l i z e r   =   s e l f . g e t _ s e r i a l i z e r ( d a t a = r e q u e s t . d a t a )  
                 s e r i a l i z e r . i s _ v a l i d ( r a i s e _ e x c e p t i o n = T r u e )  
                  
                 #   G e t   c l i e n t   I P   a n d   u s e r   a g e n t  
                 i p _ a d d r e s s   =   s e l f . g e t _ c l i e n t _ i p ( r e q u e s t )  
                 u s e r _ a g e n t   =   r e q u e s t . M E T A . g e t ( ' H T T P _ U S E R _ A G E N T ' ,   ' ' )  
                  
                 c o n t a c t _ m e s s a g e   =   s e r i a l i z e r . s a v e (  
                         i p _ a d d r e s s = i p _ a d d r e s s ,  
                         u s e r _ a g e n t = u s e r _ a g e n t  
                 )  
                  
                 #   S e n d   n o t i f i c a t i o n   e m a i l s  
                 t r y :  
                         a d m i n _ e m a i l _ s e n t   =   b r e v o _ s e r v i c e . s e n d _ c o n t a c t _ n o t i f i c a t i o n ( c o n t a c t _ m e s s a g e )  
                         c u s t o m e r _ e m a i l _ s e n t   =   b r e v o _ s e r v i c e . s e n d _ c o n t a c t _ c o n f i r m a t i o n ( c o n t a c t _ m e s s a g e )  
                          
                         i f   n o t   a d m i n _ e m a i l _ s e n t :  
                                 p r i n t ( f " F a i l e d   t o   s e n d   a d m i n   n o t i f i c a t i o n   f o r   c o n t a c t   m e s s a g e   { c o n t a c t _ m e s s a g e . i d } " )  
                         i f   n o t   c u s t o m e r _ e m a i l _ s e n t :  
                                 p r i n t ( f " F a i l e d   t o   s e n d   c u s t o m e r   c o n f i r m a t i o n   f o r   c o n t a c t   m e s s a g e   { c o n t a c t _ m e s s a g e . i d } " )  
                                  
                 e x c e p t   E x c e p t i o n   a s   e :  
                         p r i n t ( f " F a i l e d   t o   s e n d   c o n t a c t   e m a i l s :   { e } " )  
                  
                 h e a d e r s   =   s e l f . g e t _ s u c c e s s _ h e a d e r s ( s e r i a l i z e r . d a t a )  
                 r e t u r n   R e s p o n s e ( {  
                         ' m e s s a g e ' :   ' T h a n k   y o u   f o r   y o u r   m e s s a g e !   I \ ' l l   g e t   b a c k   t o   y o u   s o o n . ' ,  
                         ' c o n t a c t _ i d ' :   c o n t a c t _ m e s s a g e . i d  
                 } ,   s t a t u s = s t a t u s . H T T P _ 2 0 1 _ C R E A T E D ,   h e a d e r s = h e a d e r s )  
          
         d e f   r e t r i e v e ( s e l f ,   r e q u e s t ,   * a r g s ,   * * k w a r g s ) :  
                 i n s t a n c e   =   s e l f . g e t _ o b j e c t ( )  
                 #   M a r k   a s   r e a d   i f   i t ' s   n e w   a n d   u s e r   i s   a u t h e n t i c a t e d  
                 i f   i n s t a n c e . i s _ n e w   a n d   r e q u e s t . u s e r . i s _ a u t h e n t i c a t e d :  
                         i n s t a n c e . m a r k _ a s _ r e a d ( r e q u e s t . u s e r )  
                 s e r i a l i z e r   =   s e l f . g e t _ s e r i a l i z e r ( i n s t a n c e )  
                 r e t u r n   R e s p o n s e ( s e r i a l i z e r . d a t a )  
          
         d e f   g e t _ c l i e n t _ i p ( s e l f ,   r e q u e s t ) :  
                 " " " G e t   t h e   c l i e n t ' s   I P   a d d r e s s " " "  
                 x _ f o r w a r d e d _ f o r   =   r e q u e s t . M E T A . g e t ( ' H T T P _ X _ F O R W A R D E D _ F O R ' )  
                 i f   x _ f o r w a r d e d _ f o r :  
                         i p   =   x _ f o r w a r d e d _ f o r . s p l i t ( ' , ' ) [ 0 ]  
                 e l s e :  
                         i p   =   r e q u e s t . M E T A . g e t ( ' R E M O T E _ A D D R ' )  
                 r e t u r n   i p  
          
         @ a c t i o n ( d e t a i l = T r u e ,   m e t h o d s = [ ' p o s t ' ] ,   p e r m i s s i o n _ c l a s s e s = [ p e r m i s s i o n s . I s A u t h e n t i c a t e d ] )  
         d e f   m a r k _ r e a d ( s e l f ,   r e q u e s t ,   p k = N o n e ) :  
                 " " " M a r k   m e s s a g e   a s   r e a d " " "  
                 m e s s a g e   =   s e l f . g e t _ o b j e c t ( )  
                 m e s s a g e . m a r k _ a s _ r e a d ( r e q u e s t . u s e r )  
                 r e t u r n   R e s p o n s e ( { ' m e s s a g e ' :   ' M e s s a g e   m a r k e d   a s   r e a d ' } )  
          
         @ a c t i o n ( d e t a i l = T r u e ,   m e t h o d s = [ ' p o s t ' ] ,   p e r m i s s i o n _ c l a s s e s = [ p e r m i s s i o n s . I s A u t h e n t i c a t e d ] )  
         d e f   m a r k _ r e p l i e d ( s e l f ,   r e q u e s t ,   p k = N o n e ) :  
                 " " " M a r k   m e s s a g e   a s   r e p l i e d " " "  
                 m e s s a g e   =   s e l f . g e t _ o b j e c t ( )  
                 m e s s a g e . m a r k _ a s _ r e p l i e d ( )  
                 r e t u r n   R e s p o n s e ( { ' m e s s a g e ' :   ' M e s s a g e   m a r k e d   a s   r e p l i e d ' } )  
          
         @ a c t i o n ( d e t a i l = F a l s e ,   m e t h o d s = [ ' g e t ' ] ,   p e r m i s s i o n _ c l a s s e s = [ p e r m i s s i o n s . I s A u t h e n t i c a t e d ] )  
         d e f   s t a t s ( s e l f ,   r e q u e s t ) :  
                 " " " G e t   c o n t a c t   m e s s a g e   s t a t i s t i c s " " "  
                 t o t a l   =   C o n t a c t M e s s a g e . o b j e c t s . c o u n t ( )  
                 n e w   =   C o n t a c t M e s s a g e . o b j e c t s . f i l t e r ( s t a t u s = ' n e w ' ) . c o u n t ( )  
                 u r g e n t   =   C o n t a c t M e s s a g e . o b j e c t s . f i l t e r ( p r i o r i t y _ _ i n = [ ' h i g h ' ,   ' u r g e n t ' ] ) . c o u n t ( )  
                 r e p l i e d   =   C o n t a c t M e s s a g e . o b j e c t s . f i l t e r ( s t a t u s = ' r e p l i e d ' ) . c o u n t ( )  
                  
                 r e t u r n   R e s p o n s e ( {  
                         ' t o t a l ' :   t o t a l ,  
                         ' n e w ' :   n e w ,  
                         ' u r g e n t ' :   u r g e n t ,  
                         ' r e p l i e d ' :   r e p l i e d ,  
                         ' r e s p o n s e _ r a t e ' :   r o u n d ( ( r e p l i e d   /   t o t a l   *   1 0 0 )   i f   t o t a l   >   0   e l s e   0 ,   1 )  
                 } )  
 