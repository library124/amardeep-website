from django.urls import path
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
)

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('achievements/', AchievementListCreateView.as_view(), name='achievement-list-create'),
    path('achievements/<int:pk>/', AchievementDetailView.as_view(), name='achievement-detail'),
    path('products/', DigitalProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', DigitalProductDetailView.as_view(), name='product-detail'),
    path('newsletter/subscribe/', SubscribeNewsletterView.as_view(), name='newsletter-subscribe'),
    path('newsletter/confirm/<uuid:token>/', ConfirmSubscriptionView.as_view(), name='newsletter-confirm'),
    path('newsletter/unsubscribe/<uuid:token>/', UnsubscribeView.as_view(), name='newsletter-unsubscribe'),
    path('newsletters/', NewsletterListView.as_view(), name='newsletter-list'),
    
    # Blog URLs
    path('blog/', BlogPostListView.as_view(), name='blog-list'),
    path('blog/post/<slug:slug>/', BlogPostDetailView.as_view(), name='blog-post-detail'),
    path('blog/categories/', BlogCategoryListView.as_view(), name='blog-categories'),
    path('blog/tags/', BlogTagListView.as_view(), name='blog-tags'),
    path('blog/featured/', FeaturedBlogPostsView.as_view(), name='blog-featured'),
]
