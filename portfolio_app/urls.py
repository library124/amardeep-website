from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import views from modular structure
from .views.auth_views import (
    UserRegistrationView, UserLoginView, UserProfileUpdateView,
    UserDetailUpdateView, ChangePasswordView
)
from .views.course_views import (
    CourseListView, CourseDetailView, FeaturedCoursesView, CourseViewSet
)
from .views.payment_views_razorpay import (
    CreateCourseOrderView, CreateWorkshopOrderView, CreateServiceOrderView, PaymentSuccessView, PaymentWebhookView
)
from .views.test_payment import TestWorkshopOrderView, TestServiceOrderView
from .views.blog_views import (
    BlogPostListView, BlogPostDetailView, BlogCategoryListView,
    BlogTagListView, FeaturedBlogPostsView, BlogCategoryViewSet,
    BlogTagViewSet, BlogPostViewSet
)
from .views.workshop_views import (
    WorkshopListView, WorkshopDetailView, FeaturedWorkshopsView,
    UpcomingWorkshopsView, ActiveWorkshopsView, WorkshopViewSet,
    WorkshopApplicationViewSet, PaymentViewSet
)
from .views.dashboard_views import (
    UserDashboardView, PurchasedCoursesView, CourseAccessView
)
from .views.trading_service_views import (
    TradingServiceListView, TradingServiceDetailView, FeaturedServicesView,
    ServiceBookingCreateView, TradingServiceViewSet, ServiceBookingViewSet
)
from .views.contact_views import (
    ContactMessageCreateView, ContactMessageViewSet
)
from .views.product_views import (
    AchievementListCreateView, AchievementDetailView, DigitalProductListView,
    DigitalProductDetailView, AchievementViewSet, DigitalProductViewSet
)
from .health_views import (
    health_check, api_status, payment_status
)
from .health_checks import (
    health_check as comprehensive_health_check,
    simple_health_check,
    readiness_check,
    liveness_check
)

# SQLAlchemy Views
from .sqlalchemy_views import (
    database_health_check,
    initialize_tidb_database,
    WorkshopListSQLAlchemyView,
    BlogPostListSQLAlchemyView,
    TradingServiceListSQLAlchemyView,
    user_dashboard_sqlalchemy,
    sqlalchemy_demo_data,
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
router.register(r'crud/services', TradingServiceViewSet)
router.register(r'crud/service-bookings', ServiceBookingViewSet)
router.register(r'crud/courses', CourseViewSet)
router.register(r'crud/contact-messages', ContactMessageViewSet)

urlpatterns = [
    # Include CRUD router URLs
    path('', include(router.urls)),
    
    # Health Check URLs
    path('health/', comprehensive_health_check, name='health-check'),
    path('health/simple/', simple_health_check, name='simple-health-check'),
    path('health/readiness/', readiness_check, name='readiness-check'),
    path('health/liveness/', liveness_check, name='liveness-check'),
    path('status/', api_status, name='api-status'),
    path('payment/status/', payment_status, name='payment-status'),
    
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
    
    # Course URLs
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/featured/', FeaturedCoursesView.as_view(), name='course-featured'),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='course-detail'),
    
    # Payment URLs (SOLID-compliant with service layer)
    path('api/create-course-order/', CreateCourseOrderView.as_view(), name='create-course-order'),
    path('api/create-workshop-order/', CreateWorkshopOrderView.as_view(), name='create-workshop-order'),
    path('api/create-service-order/', CreateServiceOrderView.as_view(), name='create-service-order'),
    path('api/payment-success/', PaymentSuccessView.as_view(), name='payment-success'),
    
    # Frontend-expected payment URLs (for frontend compatibility)
    path('api/workshop-order/', CreateWorkshopOrderView.as_view(), name='workshop-order'),
    path('api/service-order/', CreateServiceOrderView.as_view(), name='service-order'),
    
    # Legacy payment URLs (for backward compatibility)
    path('api/create-order/', CreateCourseOrderView.as_view(), name='create-order'),
    
    # Contact URLs
    path('contact/', ContactMessageCreateView.as_view(), name='contact-create'),
    
    # Legacy endpoints (for backward compatibility)
    path('achievements/', AchievementListCreateView.as_view(), name='achievement-list-create'),
    path('achievements/<int:pk>/', AchievementDetailView.as_view(), name='achievement-detail'),
    path('products/', DigitalProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', DigitalProductDetailView.as_view(), name='product-detail'),
    
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
    
    # SQLAlchemy + TiDB Cloud URLs
    path('tidb/health/', database_health_check, name='tidb-health-check'),
    path('tidb/initialize/', initialize_tidb_database, name='tidb-initialize'),
    path('tidb/workshops/', WorkshopListSQLAlchemyView.as_view(), name='workshops-sqlalchemy'),
    path('tidb/blog/', BlogPostListSQLAlchemyView.as_view(), name='blog-sqlalchemy'),
    path('tidb/services/', TradingServiceListSQLAlchemyView.as_view(), name='services-sqlalchemy'),
    path('tidb/dashboard/', user_dashboard_sqlalchemy, name='dashboard-sqlalchemy'),
    path('tidb/demo/', sqlalchemy_demo_data, name='sqlalchemy-demo'),
]