from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from django.utils import timezone

from ..models import BlogPost, BlogCategory, BlogTag
from ..serializers import (
    BlogPostListSerializer, BlogPostDetailSerializer, BlogCategorySerializer, 
    BlogTagSerializer, BlogPostCreateUpdateSerializer
)


class BlogPostListView(generics.ListAPIView):
    """List published blog posts with filtering"""
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
    """Get blog post details and increment view count"""
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
    """List all blog categories"""
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = (permissions.AllowAny,)


class BlogTagListView(generics.ListAPIView):
    """List all blog tags"""
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    permission_classes = (permissions.AllowAny,)


class FeaturedBlogPostsView(generics.ListAPIView):
    """List featured blog posts"""
    queryset = BlogPost.objects.filter(
        status='published',
        publish_date__lte=timezone.now(),
        is_featured=True
    ).select_related('author', 'category').prefetch_related('tags')[:3]
    serializer_class = BlogPostListSerializer
    permission_classes = (permissions.AllowAny,)


# CRUD ViewSets
class BlogCategoryViewSet(viewsets.ModelViewSet):
    """CRUD operations for blog categories"""
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class BlogTagViewSet(viewsets.ModelViewSet):
    """CRUD operations for blog tags"""
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class BlogPostViewSet(viewsets.ModelViewSet):
    """CRUD operations for blog posts"""
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