import uuid
import requests
import logging
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from ..models import Course, Payment, PurchasedCourse, Workshop, WorkshopApplication, TradingService, ServiceBooking

logger = logging.getLogger(__name__)


class UnifiedPaymentService:
    """Unified service class for all payment operations following SRP"""
    
    @staticmethod
    def create_beeceptor_order(item, item_type, user=None, email=None, additional_notes=None):
        """Create order using Beeceptor mock API for any item type"""
        base_notes = {
            f"{item_type}_id": str(item.id),
            f"{item_type}_name": getattr(item, 'title', getattr(item, 'name', 'Unknown')),
            "user_id": user.id if user else None,
            "user_email": user.email if user else email
        }
        
        if additional_notes:
            base_notes.update(additional_notes)
        
        order_payload = {
            "amount": int(item.price * 100),  # Amount in paise
            "currency": getattr(item, 'currency', 'INR'),
            "receipt": f"{item_type}_{item.id}_{uuid.uuid4().hex[:8]}",
            "notes": base_notes
        }

        beeceptor_url = "https://razorpay-mock-api.proxy.beeceptor.com/orders"

        try:
            response = requests.post(beeceptor_url, json=order_payload, timeout=10)
            response.raise_for_status()
            return response.json(), None
        except requests.RequestException as e:
            logger.error(f"Beeceptor request failed: {e}")
            return None, str(e)

    @staticmethod
    def create_payment_record(item, item_type, order_data, user=None, email=None, 
                            user_name=None, user_phone=None, related_object=None, is_mock=False, error=None):
        """Create payment record in database for any item type"""
        payment_data = {
            'payment_id': f"PAY_{uuid.uuid4().hex[:12].upper()}",
            'razorpay_order_id': order_data.get('id') if order_data else f"order_mock_{uuid.uuid4().hex[:12]}",
            'amount': item.price,
            'currency': getattr(item, 'currency', 'INR'),
            'payment_type': item_type,
            'customer_name': user.get_full_name() if user else (user_name or "Guest User"),
            'customer_email': user.email if user else email,
            'customer_phone': user_phone or '',
            'gateway_response': order_data or {'mock': True, 'error': error}
        }
        
        # Add specific relationships based on item type
        if item_type == 'course':
            payment_data['course'] = item
        elif item_type == 'workshop':
            payment_data['workshop_application'] = related_object
        elif item_type == 'service':
            payment_data['trading_service'] = item
        
        return Payment.objects.create(**payment_data)


# Workshop Payment Views
class WorkshopOrderView(APIView):
    """Create order for workshop payment"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            workshop_id = request.data.get('workshop_id')
            user_name = request.data.get('user_name', 'Guest User')
            user_email = request.data.get('email', 'guest@example.com')
            user_phone = request.data.get('user_phone', '')
            
            # Application data
            experience_level = request.data.get('experience_level', 'beginner')
            motivation = request.data.get('motivation', '')

            if not workshop_id:
                return Response({'error': 'Workshop ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                workshop = Workshop.objects.get(id=workshop_id, is_active=True)
            except Workshop.DoesNotExist:
                return Response({'error': 'Workshop not found'}, status=status.HTTP_404_NOT_FOUND)

            if workshop.is_full:
                return Response({'error': 'Workshop is full'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user already applied
            existing_application = WorkshopApplication.objects.filter(
                workshop=workshop,
                email=user_email
            ).first()
            
            if existing_application:
                return Response({'error': 'You have already applied for this workshop'}, status=status.HTTP_400_BAD_REQUEST)

            # Create workshop application
            application = WorkshopApplication.objects.create(
                workshop=workshop,
                name=user_name,
                email=user_email,
                phone=user_phone,
                experience_level=experience_level,
                motivation=motivation
            )

            if workshop.is_paid:
                # Create order for paid workshop
                additional_notes = {
                    "application_id": str(application.id),
                    "user_name": user_name
                }
                
                order_data, error = UnifiedPaymentService.create_beeceptor_order(
                    workshop, 'workshop', None, user_email, additional_notes
                )

                # Create payment record
                payment = UnifiedPaymentService.create_payment_record(
                    workshop, 'workshop', order_data, None, user_email, 
                    user_name, user_phone, application, not bool(order_data), error
                )

                return Response({
                    'order_id': order_data.get('id') if order_data else payment.razorpay_order_id,
                    'amount': order_data.get('amount') if order_data else int(workshop.price * 100),
                    'currency': workshop.currency,
                    'payment_id': payment.payment_id,
                    'item_title': workshop.title,
                    'item_price': workshop.price_display,
                    'item_type': 'workshop',
                    'application_id': application.id,
                    'mock': not bool(order_data)
                })
            else:
                # Free workshop - auto approve
                application.status = 'approved'
                application.save()
                workshop.registered_count += 1
                workshop.save()

                return Response({
                    'message': 'Successfully registered for free workshop',
                    'application_id': application.id,
                    'requires_payment': False
                })

        except Exception as e:
            logger.error(f"Error creating workshop order: {e}")
            return Response({'error': 'Failed to create workshop order'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Service Payment Views  
class ServiceOrderView(APIView):
    """Create order for service payment"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            service_id = request.data.get('service_id')
            user_name = request.data.get('user_name', 'Guest User')
            user_email = request.data.get('email', 'guest@example.com')
            user_phone = request.data.get('user_phone', '')
            message = request.data.get('message', '')
            preferred_contact_method = request.data.get('preferred_contact_method', 'whatsapp')
            preferred_time = request.data.get('preferred_time', '')

            if not service_id:
                return Response({'error': 'Service ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                service = TradingService.objects.get(id=service_id, is_active=True)
            except TradingService.DoesNotExist:
                return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)

            # Create service booking
            booking = ServiceBooking.objects.create(
                service=service,
                name=user_name,
                email=user_email,
                phone=user_phone,
                message=message,
                preferred_contact_method=preferred_contact_method,
                preferred_time=preferred_time
            )

            # Create order for service payment
            additional_notes = {
                "booking_id": str(booking.id),
                "user_name": user_name,
                "preferred_contact": preferred_contact_method
            }
            
            order_data, error = UnifiedPaymentService.create_beeceptor_order(
                service, 'service', None, user_email, additional_notes
            )

            # Create payment record
            payment = UnifiedPaymentService.create_payment_record(
                service, 'service', order_data, None, user_email, 
                user_name, user_phone, None, not bool(order_data), error
            )

            return Response({
                'order_id': order_data.get('id') if order_data else payment.razorpay_order_id,
                'amount': order_data.get('amount') if order_data else int(service.price * 100),
                'currency': service.currency,
                'payment_id': payment.payment_id,
                'item_title': service.name,
                'item_price': service.price_display,
                'item_type': 'service',
                'booking_id': booking.id,
                'mock': not bool(order_data)
            })

        except Exception as e:
            logger.error(f"Error creating service order: {e}")
            return Response({'error': 'Failed to create service order'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Enhanced Payment Success View
class EnhancedPaymentSuccessView(APIView):
    """Handle payment success for all item types"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            payment_id = request.data.get('payment_id')
            razorpay_payment_id = request.data.get('razorpay_payment_id', f"pay_mock_{uuid.uuid4().hex[:12]}")
            razorpay_order_id = request.data.get('razorpay_order_id')
            razorpay_signature = request.data.get('razorpay_signature', 'mock_signature')
            user = request.user if request.user.is_authenticated else None

            if not payment_id:
                return Response({'error': 'Payment ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Get payment record
            try:
                payment = Payment.objects.get(payment_id=payment_id)
            except Payment.DoesNotExist:
                return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

            if payment.status == 'completed':
                return Response({'error': 'Payment already processed'}, status=status.HTTP_400_BAD_REQUEST)

            # Mark payment as completed
            gateway_response = {
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_signature': razorpay_signature,
                'user_id': user.id if user else None,
                'timestamp': timezone.now().isoformat()
            }

            payment.mark_completed(
                gateway_payment_id=razorpay_payment_id,
                payment_method='razorpay',
                gateway_response=gateway_response
            )

            # Handle different payment types
            response_data = {
                'message': 'Payment successful!',
                'payment_id': payment.payment_id,
                'amount_paid': payment.amount,
                'currency': payment.currency,
            }

            if payment.payment_type == 'course':
                response_data.update({
                    'item_title': payment.course.title if payment.course else 'Unknown Course',
                    'access_instructions': 'You can now access the course from your dashboard.',
                })
                # Get the created purchased course
                purchased_course = PurchasedCourse.objects.filter(
                    course=payment.course,
                    user=user
                ).order_by('-created_at').first()
                if purchased_course:
                    response_data['enrollment_id'] = purchased_course.id

            elif payment.payment_type == 'workshop':
                response_data.update({
                    'item_title': payment.workshop_application.workshop.title if payment.workshop_application else 'Unknown Workshop',
                    'access_instructions': 'Workshop details will be sent to your email.',
                    'application_id': payment.workshop_application.id if payment.workshop_application else None
                })

            elif payment.payment_type == 'service':
                response_data.update({
                    'item_title': payment.trading_service.name if payment.trading_service else 'Unknown Service',
                    'access_instructions': 'We will contact you soon to discuss the service details.',
                })

            return Response(response_data)

        except Exception as e:
            logger.error(f"Error processing payment success: {e}")
            return Response({'error': 'Failed to process payment'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)