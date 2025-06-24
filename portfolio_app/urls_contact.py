from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_contact import ContactMessageCreateView, ContactMessageViewSet

# Create router for contact operations
contact_router = DefaultRouter()
contact_router.register(r'messages', ContactMessageViewSet, basename='contact-messages')

urlpatterns = [
    # Contact form submission (public endpoint)
    path('contact/', ContactMessageCreateView.as_view(), name='contact-create'),
    
    # Contact management (admin endpoints)
    path('contact/', include(contact_router.urls)),
]