from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Achievement, DigitalProduct, Subscriber, Newsletter, BlogPost, BlogCategory, BlogTag
from .serializers import (
    UserRegistrationSerializer, AchievementSerializer, DigitalProductSerializer, 
    SubscriberSerializer, NewsletterSerializer, BlogPostListSerializer, 
    BlogPostDetailSerializer, BlogCategorySerializer, BlogTagSerializer
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
