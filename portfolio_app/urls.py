from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView,
    UserLoginView,
    AchievementListCreateView,
    AchievementDetailView,
    DigitalProductListView,
    DigitalProductDetailView,
    SubscribeNewsletterView,
    ConfirmSubscriptionView,
    UnsubscribeView,
    NewsletterListView,
    BlogPostListView,
    BlogPostDetailView,
    BlogCategoryListView,
    BlogTagListView,
    FeaturedBlogPostsView,
    WorkshopListView,
    WorkshopDetailView,
    FeaturedWorkshopsView,
    UpcomingWorkshopsView,
    ActiveWorkshopsView,
    # Trading Service Views
    TradingServiceListView,
    TradingServiceDetailView,
    FeaturedServicesView,
    ServiceBookingCreateView,
    # Dashboard Views
    UserDashboardView,
    UserProfileUpdateView,
    UserDetailUpdateView,
    ChangePasswordView,
    PurchasedCoursesView,
    CourseAccessView,
    # CRUD ViewSets
    AchievementViewSet,
    DigitalProductViewSet,
    BlogCategoryViewSet,
    BlogTagViewSet,
    BlogPostViewSet,
    WorkshopViewSet,
    WorkshopApplicationViewSet,
    PaymentViewSet,
    NewsletterViewSet,
    SubscriberViewSet,
    TradingServiceViewSet,
    ServiceBookingViewSet,
)

# App namespace for URL reversing
app_name = 'portfolio_app'

# Create router for CRUD operations
router = DefaultRouter()
router.register(r'crud/achievements', AchievementViewSet)
router.register(r'crud/products', DigitalProductViewSet)
router.register(r'crud/blog/categories', BlogCategoryViewSet)
router.register(r'crud/blog/tags', BlogTagViewSet)
router.register(r'crud/blog/posts', BlogPostViewSet)
router.register(r'crud/workshops', WorkshopViewSet)
router.register(r'crud/workshop-applications', WorkshopApplicationViewSet)
router.register(r'crud/payments', PaymentViewSet)
router.register(r'crud/newsletters', NewsletterViewSet)
router.register(r'crud/subscribers', SubscriberViewSet)
router.register(r'crud/services', TradingServiceViewSet)
router.register(r'crud/service-bookings', ServiceBookingViewSet)

urlpatterns = [
    # Include CRUD router URLs
    path('', include(router.urls)),
    
    # Authentication
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    
    # Dashboard URLs
    path('dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
    path('dashboard/profile/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('dashboard/user/', UserDetailUpdateView.as_view(), name='user-detail-update'),
    path('dashboard/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('dashboard/courses/', PurchasedCoursesView.as_view(), name='purchased-courses'),
    path('dashboard/courses/<int:course_id>/access/', CourseAccessView.as_view(), name='course-access'),
    
    # Legacy endpoints (for backward compatibility)
    path('achievements/', AchievementListCreateView.as_view(), name='achievement-list-create'),
    path('achievements/<int:pk>/', AchievementDetailView.as_view(), name='achievement-detail'),
    path('products/', DigitalProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', DigitalProductDetailView.as_view(), name='product-detail'),
    
    # Newsletter
    path('newsletter/subscribe/', SubscribeNewsletterView.as_view(), name='newsletter-subscribe'),
    path('newsletter/confirm/<uuid:token>/', ConfirmSubscriptionView.as_view(), name='newsletter-confirm'),
    path('newsletter/unsubscribe/<uuid:token>/', UnsubscribeView.as_view(), name='newsletter-unsubscribe'),
    path('newsletters/', NewsletterListView.as_view(), name='newsletter-list'),
    
    # Blog URLs (legacy)
    path('blog/', BlogPostListView.as_view(), name='blog-list'),
    path('blog/post/<slug:slug>/', BlogPostDetailView.as_view(), name='blog-post-detail'),
    path('blog/categories/', BlogCategoryListView.as_view(), name='blog-categories'),
    path('blog/category/<slug:slug>/', BlogCategoryListView.as_view(), name='blog_category'),
    path('blog/tags/', BlogTagListView.as_view(), name='blog-tags'),
    path('blog/tag/<slug:slug>/', BlogTagListView.as_view(), name='blog_tag'),
    path('blog/featured/', FeaturedBlogPostsView.as_view(), name='blog-featured'),
    
    # Workshop URLs (legacy)
    path('workshops/', WorkshopListView.as_view(), name='workshop-list'),
    path('workshops/featured/', FeaturedWorkshopsView.as_view(), name='workshop-featured'),
    path('workshops/upcoming/', UpcomingWorkshopsView.as_view(), name='workshop-upcoming'),
    path('workshops/active/', ActiveWorkshopsView.as_view(), name='workshop-active'),
    path('workshops/<slug:slug>/', WorkshopDetailView.as_view(), name='workshop-detail'),
    
    # Trading Service URLs
    path('services/', TradingServiceListView.as_view(), name='service-list'),
    path('services/featured/', FeaturedServicesView.as_view(), name='service-featured'),
    path('services/<slug:slug>/', TradingServiceDetailView.as_view(), name='service-detail'),
    path('services/book/', ServiceBookingCreateView.as_view(), name='service-booking-create'),
]
