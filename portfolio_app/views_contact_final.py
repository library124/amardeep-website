from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import ContactMessage
from .serializers import (
    ContactMessageSerializer, ContactMessageCreateSerializer,
    ContactMessageUpdateSerializer
)
from .services.brevo_contact import contact_email_service

# Contact Views

class ContactMessageCreateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ContactMessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Get client IP and user agent
            ip_address = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            contact_message = serializer.save(
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            # Send notification emails using Brevo
            try:
                # Send notification to admin
                admin_email_sent = contact_email_service.send_contact_notification(contact_message)
                
                # Send confirmation to customer
                customer_email_sent = contact_email_service.send_contact_confirmation(contact_message)
                
                if not admin_email_sent:
                    print(f"Failed to send admin notification for contact message {contact_message.id}")
                if not customer_email_sent:
                    print(f"Failed to send customer confirmation for contact message {contact_message.id}")
                    
            except Exception as e:
                print(f"Failed to send contact emails: {e}")
            
            return Response({
                'message': 'Thank you for your message! I\'ll get back to you soon.',
                'contact_id': contact_message.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ContactMessageCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ContactMessageUpdateSerializer
        return ContactMessageSerializer
    
    def get_queryset(self):
        queryset = ContactMessage.objects.all().select_related('assigned_to')
        
        # Only allow authenticated users to see all messages
        if not self.request.user.is_authenticated:
            # For unauthenticated users, only allow creating messages
            return ContactMessage.objects.none()
        
        return queryset.order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        # Allow unauthenticated users to create contact messages
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get client IP and user agent
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        contact_message = serializer.save(
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Send notification emails
        try:
            admin_email_sent = contact_email_service.send_contact_notification(contact_message)
            customer_email_sent = contact_email_service.send_contact_confirmation(contact_message)
            
            if not admin_email_sent:
                print(f"Failed to send admin notification for contact message {contact_message.id}")
            if not customer_email_sent:
                print(f"Failed to send customer confirmation for contact message {contact_message.id}")
                
        except Exception as e:
            print(f"Failed to send contact emails: {e}")
        
        headers = self.get_success_headers(serializer.data)
        return Response({
            'message': 'Thank you for your message! I\'ll get back to you soon.',
            'contact_id': contact_message.id
        }, status=status.HTTP_201_CREATED, headers=headers)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Mark as read if it's new and user is authenticated
        if instance.is_new and request.user.is_authenticated:
            instance.mark_as_read(request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_read(self, request, pk=None):
        """Mark message as read"""
        message = self.get_object()
        message.mark_as_read(request.user)
        return Response({'message': 'Message marked as read'})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_replied(self, request, pk=None):
        """Mark message as replied"""
        message = self.get_object()
        message.mark_as_replied()
        return Response({'message': 'Message marked as replied'})
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def stats(self, request):
        """Get contact message statistics"""
        total = ContactMessage.objects.count()
        new = ContactMessage.objects.filter(status='new').count()
        urgent = ContactMessage.objects.filter(priority__in=['high', 'urgent']).count()
        replied = ContactMessage.objects.filter(status='replied').count()
        
        return Response({
            'total': total,
            'new': new,
            'urgent': urgent,
            'replied': replied,
            'response_rate': round((replied / total * 100) if total > 0 else 0, 1)
        })