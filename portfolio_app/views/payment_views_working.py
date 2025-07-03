"""
Working payment views with SOLID principles - simplified version
"""
import uuid
import requests
import logging
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from ..models import Workshop, WorkshopApplication, TradingService, ServiceBooking, Payment, Course, PurchasedCourse

logger = logging.getLogger(__name__)


class PaymentServiceSimple:
    """Simplified payment service following Single Responsibility Principle"""
    
    @staticmethod
    def create_beeceptor_order(amount, currency, receipt, notes):
        """Create order using Beeceptor mock API"""
        order_payload = {
            "amount": int(amount * 100),  # Amount in paise
            "currency": currency,
            "receipt": receipt,
            "notes": notes
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
    def create_payment_record(payment_data):
        """Create payment record in database"""
        return Payment.objects.create(**payment_data)


class WorkshopPaymentValidator:
    """Workshop payment validator following Single Responsibility Principle"""
    
    @staticmethod
    def validate_workshop_request(request_data):
        """Validate workshop payment request"""
        workshop_id = request_data.get('workshop_id')
        user_email = request_data.get('email', 'guest@example.com')
        
        if not workshop_id:
            return False, 'Workshop ID is required'
        
        if not user_email or '@' not in user_email:
            return False, 'Valid email is required'
        
        try:
            workshop = Workshop.objects.get(id=workshop_id, is_active=True)
        except Workshop.DoesNotExist:
            return False, 'Workshop not found'
        
        if workshop.is_full:
            return False, 'Workshop is full'
        
        # Check if user already applied
        existing_application = WorkshopApplication.objects.filter(
            workshop=workshop,
            email=user_email
        ).first()
        
        if existing_application:
            return False, 'You have already applied for this workshop'
        
        return True, workshop


class ServicePaymentValidator:
    """Service payment validator following Single Responsibility Principle"""
    
    @staticmethod
    def validate_service_request(request_data):
        """Validate service payment request"""
        service_id = request_data.get('service_id')
        user_email = request_data.get('email', 'guest@example.com')
        
        if not service_id:
            return False, 'Service ID is required'
        
        if not user_email or '@' not in user_email:
            return False, 'Valid email is required'
        
        try:
            service = TradingService.objects.get(id=service_id, is_active=True)
        except TradingService.DoesNotExist:
            return False, 'Service not found'
        
        return True, service


class CreateWorkshopOrderView(APIView):
    """Create order for workshop payment - SOLID compliant"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            # Validate request using validator (Single Responsibility)
            is_valid, result = WorkshopPaymentValidator.validate_workshop_request(request.data)
            if not is_valid:
                return Response({'error': result}, status=status.HTTP_400_BAD_REQUEST)
            
            workshop = result
            
            # Extract user data
            user_name = request.data.get('user_name', 'Guest User')
            user_email = request.data.get('email', 'guest@example.com')
            user_phone = request.data.get('user_phone', '')
            experience_level = request.data.get('experience_level', 'beginner')
            motivation = request.data.get('motivation', '')

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
                # Create order using service (Single Responsibility)
                receipt = f"workshop_{workshop.id}_{uuid.uuid4().hex[:8]}"
                notes = {
                    "workshop_id": str(workshop.id),
                    "workshop_title": workshop.title,
                    "user_name": user_name,
                    "user_email": user_email,
                    "application_id": str(application.id)
                }
                
                order_data, error = PaymentServiceSimple.create_beeceptor_order(
                    workshop.price, workshop.currency, receipt, notes
                )

                # Create payment record using service (Single Responsibility)
                payment_data = {
                    'payment_id': f"PAY_{uuid.uuid4().hex[:12].upper()}",
                    'razorpay_order_id': order_data.get('id') if order_data else f"order_mock_{uuid.uuid4().hex[:12]}",
                    'amount': workshop.price,
                    'currency': workshop.currency,
                    'payment_type': 'workshop',
                    'customer_name': user_name,
                    'customer_email': user_email,
                    'customer_phone': user_phone,
                    'workshop_application': application,
                    'gateway_response': order_data or {'mock': True}
                }
                
                payment = PaymentServiceSimple.create_payment_record(payment_data)

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


class CreateServiceOrderView(APIView):
    """Create order for service payment - SOLID compliant"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            # Validate request using validator (Single Responsibility)
            is_valid, result = ServicePaymentValidator.validate_service_request(request.data)
            if not is_valid:
                return Response({'error': result}, status=status.HTTP_400_BAD_REQUEST)
            
            service = result
            
            # Extract user data
            user_name = request.data.get('user_name', 'Guest User')
            user_email = request.data.get('email', 'guest@example.com')
            user_phone = request.data.get('user_phone', '')
            message = request.data.get('message', '')
            preferred_contact_method = request.data.get('preferred_contact_method', 'whatsapp')
            preferred_time = request.data.get('preferred_time', '')

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

            # Create order using service (Single Responsibility)
            receipt = f"service_{service.id}_{uuid.uuid4().hex[:8]}"
            notes = {
                "service_id": str(service.id),
                "service_name": service.name,
                "user_name": user_name,
                "user_email": user_email,
                "booking_id": str(booking.id)
            }
            
            order_data, error = PaymentServiceSimple.create_beeceptor_order(
                service.price, service.currency, receipt, notes
            )

            # Create payment record using service (Single Responsibility)
            payment_data = {
                'payment_id': f"PAY_{uuid.uuid4().hex[:12].upper()}",
                'razorpay_order_id': order_data.get('id') if order_data else f"order_mock_{uuid.uuid4().hex[:12]}",
                'amount': service.price,
                'currency': service.currency,
                'payment_type': 'service',
                'customer_name': user_name,
                'customer_email': user_email,
                'customer_phone': user_phone,
                'trading_service': service,
                'gateway_response': order_data or {'mock': True}
            }
            
            payment = PaymentServiceSimple.create_payment_record(payment_data)

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


class CreateCourseOrderView(APIView):
    """Create order for course payment - SOLID compliant"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            course_id = request.data.get('course_id')
            user = request.user if request.user.is_authenticated else None
            email = request.data.get('email', 'guest@example.com')

            if not course_id:
                return Response({'error': 'Course ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                course = Course.objects.get(id=course_id, is_active=True)
            except Course.DoesNotExist:
                return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

            if course.is_full:
                return Response({'error': 'Course is full'}, status=status.HTTP_400_BAD_REQUEST)

            # Create order using service (Single Responsibility)
            receipt = f"course_{course.id}_{uuid.uuid4().hex[:8]}"
            notes = {
                "course_id": str(course.id),
                "course_name": course.title,
                "user_id": user.id if user else None,
                "user_email": user.email if user else email
            }
            
            order_data, error = PaymentServiceSimple.create_beeceptor_order(
                course.price, course.currency, receipt, notes
            )

            # Create payment record using service (Single Responsibility)
            payment_data = {
                'payment_id': f"PAY_{uuid.uuid4().hex[:12].upper()}",
                'razorpay_order_id': order_data.get('id') if order_data else f"order_mock_{uuid.uuid4().hex[:12]}",
                'amount': course.price,
                'currency': course.currency,
                'payment_type': 'course',
                'customer_name': user.get_full_name() if user else "Guest User",
                'customer_email': user.email if user else email,
                'course': course,
                'gateway_response': order_data or {'mock': True}
            }
            
            payment = PaymentServiceSimple.create_payment_record(payment_data)

            return Response({
                'order_id': order_data.get('id') if order_data else payment.razorpay_order_id,
                'amount': order_data.get('amount') if order_data else int(course.price * 100),
                'currency': course.currency,
                'payment_id': payment.payment_id,
                'item_title': course.title,
                'item_price': course.price_display,
                'item_type': 'course',
                'mock': not bool(order_data)
            })

        except Exception as e:
            logger.error(f"Error creating course order: {e}")
            return Response({'error': 'Failed to create course order'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentSuccessView(APIView):
    """Handle payment success for all payment types - SOLID compliant"""
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

            # Handle post-payment actions based on payment type
            response_data = {
                'message': 'Payment successful!',
                'payment_id': payment.payment_id,
                'amount_paid': float(payment.amount),
                'currency': payment.currency,
                'access_instructions': 'Thank you for your payment!'
            }

            if payment.payment_type == 'course' and payment.course:
                response_data.update({
                    'item_title': payment.course.title,
                    'access_instructions': 'You can now access the course from your dashboard.',
                })
                
                # Create purchased course if needed
                if user:
                    PurchasedCourse.objects.get_or_create(
                        user=user,
                        course=payment.course,
                        defaults={
                            'course_name': payment.course.title,
                            'course_type': 'course',
                            'description': payment.course.short_description,
                            'purchase_date': timezone.now(),
                            'start_date': timezone.now(),
                            'amount_paid': payment.amount,
                            'currency': payment.currency,
                            'status': 'active'
                        }
                    )
                    
                    # Increment enrolled count
                    payment.course.enrolled_count += 1
                    payment.course.save(update_fields=['enrolled_count'])

            elif payment.payment_type == 'workshop' and payment.workshop_application:
                workshop = payment.workshop_application.workshop
                response_data.update({
                    'item_title': workshop.title,
                    'access_instructions': 'Workshop details will be sent to your email.',
                    'application_id': payment.workshop_application.id
                })
                
                # Update workshop application
                payment.workshop_application.status = 'approved'
                payment.workshop_application.payment_status = 'completed'
                payment.workshop_application.payment_id = razorpay_payment_id
                payment.workshop_application.payment_method = 'razorpay'
                payment.workshop_application.paid_at = timezone.now()
                payment.workshop_application.save()
                
                # Increment workshop registered count
                workshop.registered_count += 1
                workshop.save(update_fields=['registered_count'])

            elif payment.payment_type == 'service' and payment.trading_service:
                response_data.update({
                    'item_title': payment.trading_service.name,
                    'access_instructions': 'We will contact you soon to discuss the service details.',
                })

            return Response(response_data)

        except Exception as e:
            logger.error(f"Error processing payment success: {e}")
            return Response({'error': 'Failed to process payment'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)