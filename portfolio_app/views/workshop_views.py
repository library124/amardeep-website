import uuid
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone

from ..models import Workshop, WorkshopApplication, Payment
from ..serializers import (
    WorkshopSerializer, WorkshopCreateUpdateSerializer, 
    WorkshopApplicationSerializer, PaymentSerializer
)


class WorkshopListView(generics.ListAPIView):
    """List active workshops with filtering"""
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
    """Get workshop details by slug"""
    queryset = Workshop.objects.filter(is_active=True).select_related('instructor')
    serializer_class = WorkshopSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny,)


class FeaturedWorkshopsView(generics.ListAPIView):
    """List featured workshops"""
    queryset = Workshop.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('instructor')[:3]
    serializer_class = WorkshopSerializer
    permission_classes = (permissions.AllowAny,)


class UpcomingWorkshopsView(generics.ListAPIView):
    """List upcoming workshops"""
    serializer_class = WorkshopSerializer
    permission_classes = (permissions.AllowAny,)
    
    def get_queryset(self):
        # Show upcoming workshops (future dates) and also recent workshops (within last 30 days)
        # This ensures workshops are visible even if the date is slightly in the past
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        
        return Workshop.objects.filter(
            is_active=True,
            status='upcoming',
            start_date__gt=thirty_days_ago  # Changed from timezone.now() to be more lenient
        ).select_related('instructor').order_by('start_date')[:5]


class ActiveWorkshopsView(generics.ListAPIView):
    """View for all active workshops regardless of date - useful for frontend display"""
    serializer_class = WorkshopSerializer
    permission_classes = (permissions.AllowAny,)
    
    def get_queryset(self):
        return Workshop.objects.filter(
            is_active=True
        ).select_related('instructor').order_by('-is_featured', 'start_date')[:10]


# CRUD ViewSets
class WorkshopViewSet(viewsets.ModelViewSet):
    """CRUD operations for workshops"""
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
    """CRUD operations for workshop applications"""
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
    """CRUD operations for payments"""
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