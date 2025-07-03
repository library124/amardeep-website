from rest_framework import generics, permissions, viewsets

from ..models import Achievement, DigitalProduct
from ..serializers import (
    AchievementSerializer, DigitalProductSerializer
)


class AchievementListCreateView(generics.ListCreateAPIView):
    """List and create achievements"""
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AchievementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, delete achievement"""
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class DigitalProductListView(generics.ListAPIView):
    """List all digital products"""
    queryset = DigitalProduct.objects.all()
    serializer_class = DigitalProductSerializer
    permission_classes = (permissions.AllowAny,)


class DigitalProductDetailView(generics.RetrieveAPIView):
    """Get digital product details"""
    queryset = DigitalProduct.objects.all()
    serializer_class = DigitalProductSerializer
    permission_classes = (permissions.AllowAny,)


# CRUD ViewSets
class AchievementViewSet(viewsets.ModelViewSet):
    """CRUD operations for achievements"""
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DigitalProductViewSet(viewsets.ModelViewSet):
    """CRUD operations for digital products"""
    queryset = DigitalProduct.objects.all()
    serializer_class = DigitalProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]