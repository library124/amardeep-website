from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import UserProfile, PurchasedCourse
from ..serializers import (
    UserProfileSerializer, UserDetailSerializer, PurchasedCourseSerializer
)


class UserDashboardView(APIView):
    """Main dashboard view with user data and purchased courses"""
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


class PurchasedCoursesView(generics.ListAPIView):
    """List user's purchased courses"""
    serializer_class = PurchasedCourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PurchasedCourse.objects.filter(user=self.request.user).order_by('-purchase_date')


class CourseAccessView(APIView):
    """Handle course access for purchased courses"""
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