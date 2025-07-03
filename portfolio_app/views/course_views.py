from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from django.utils import timezone

from ..models import Course
from ..serializers import (
    CourseSerializer, CourseCreateUpdateSerializer, CourseDetailSerializer
)


class CourseListView(generics.ListAPIView):
    """List all active courses with filtering"""
    serializer_class = CourseSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True)

        # Filter by course type
        course_type = self.request.query_params.get('type', None)
        if course_type:
            queryset = queryset.filter(course_type=course_type)

        # Filter by difficulty level
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)

        # Filter featured courses
        featured = self.request.query_params.get('featured', None)
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)

        return queryset.select_related('instructor').order_by('-created_at')


class CourseDetailView(generics.RetrieveAPIView):
    """Get course details by slug"""
    queryset = Course.objects.filter(is_active=True).select_related('instructor')
    serializer_class = CourseDetailSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny,)


class FeaturedCoursesView(generics.ListAPIView):
    """List featured courses"""
    queryset = Course.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('instructor')[:6]
    serializer_class = CourseSerializer
    permission_classes = (permissions.AllowAny,)


class CourseViewSet(viewsets.ModelViewSet):
    """CRUD operations for courses"""
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CourseCreateUpdateSerializer
        elif self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.all().select_related('instructor')

        # Filter active courses for non-authenticated users
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_active=True)

        return queryset

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)