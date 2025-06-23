from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
import uuid
from .models import (
    Achievement, DigitalProduct, Subscriber, Newsletter, BlogPost, 
    BlogCategory, BlogTag, Workshop, WorkshopApplication, Payment
)
from .serializers import (
    UserRegistrationSerializer, AchievementSerializer, DigitalProductSerializer, 
    SubscriberSerializer, NewsletterSerializer, BlogPostListSerializer, 
    BlogPostDetailSerializer, BlogCategorySerializer, BlogTagSerializer, 
    WorkshopSerializer, WorkshopApplicationSerializer, PaymentSerializer,
    BlogPostCreateUpdateSerializer, WorkshopCreateUpdateSerializer
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
            
            # Send confirmation email
            confirmation_url = f"{settings.FRONTEND_URL}/newsletter/confirm/{subscriber.confirmation_token}/"
            
            try:
                send_mail(
                    subject='Confirm Your Newsletter Subscription - Amardeep Asode Trading Insights',
                    message=f'''
Hello {subscriber.name or 'Trader'},

Thank you for subscribing to Amardeep Asode's Trading Insights newsletter!

To complete your subscription, please click the link below:
{confirmation_url}

You'll receive:
- Weekly market analysis
- Trading tips and strategies
- Exclusive insights from Amardeep
- Performance updates and achievements

If you didn't subscribe to this newsletter, please ignore this email.

Best regards,
Amardeep Asode
Stock & Intraday Trader
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )
                
                return Response({
                    'message': 'Subscription successful! Please check your email to confirm.',
                    'email': subscriber.email
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                print(f"Email sending failed: {e}")  # Log the error
                # If email fails, still create subscriber but inform user
                return Response({
                    'message': f'Subscription created but confirmation email failed to send. Error: {str(e)}. Please contact support or check email configuration.',
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
        return Workshop.objects.filter(
            is_active=True,
            status='upcoming',
            start_date__gt=timezone.now()
        ).select_related('instructor').order_by('start_date')[:5]

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