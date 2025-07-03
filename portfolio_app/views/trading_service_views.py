from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import TradingService, ServiceBooking
from ..serializers import (
    TradingServiceSerializer, TradingServiceCreateUpdateSerializer,
    ServiceBookingSerializer, ServiceBookingCreateSerializer
)
from ..services.brevo_service import brevo_service


class TradingServiceListView(generics.ListAPIView):
    """List active trading services with filtering"""
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
    """Get trading service details by slug"""
    queryset = TradingService.objects.filter(is_active=True)
    serializer_class = TradingServiceSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny,)


class FeaturedServicesView(generics.ListAPIView):
    """List featured trading services"""
    queryset = TradingService.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by('display_order', 'name')[:3]
    serializer_class = TradingServiceSerializer
    permission_classes = (permissions.AllowAny,)


class ServiceBookingCreateView(APIView):
    """Create service booking with email notifications"""
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


# CRUD ViewSets
class TradingServiceViewSet(viewsets.ModelViewSet):
    """CRUD operations for trading services"""
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
    """CRUD operations for service bookings"""
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