from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import ContactMessage
from .serializers import ContactMessageCreateSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def contact_create_view(request):
    """
    Simple contact form API endpoint
    """
    serializer = ContactMessageCreateSerializer(data=request.data)
    if serializer.is_valid():
        # Get client IP and user agent
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        contact_message = serializer.save(
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Send notification emails (optional - can be added later)
        try:
            from .services.brevo_contact import contact_email_service
            contact_email_service.send_contact_notification(contact_message)
            contact_email_service.send_contact_confirmation(contact_message)
        except Exception as e:
            print(f"Failed to send contact emails: {e}")
        
        return Response({
            'message': 'Thank you for your message! I\'ll get back to you soon.',
            'contact_id': contact_message.id
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_client_ip(request):
    """Get the client's IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip