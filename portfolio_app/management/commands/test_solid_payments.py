"""
Management command to test SOLID payment architecture
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal

from ...services.payment.service import PaymentService
from ...services.payment.interfaces import PaymentType
from ...models import Course, Workshop, TradingService


class Command(BaseCommand):
    help = 'Test SOLID payment architecture'

    def add_arguments(self, parser):
        parser.add_argument(
            '--gateway',
            type=str,
            default='beeceptor',
            help='Payment gateway to use (beeceptor, razorpay)'
        )
        parser.add_argument(
            '--test-type',
            type=str,
            default='all',
            choices=['all', 'course', 'workshop', 'service'],
            help='Type of payment to test'
        )

    def handle(self, *args, **options):
        gateway_type = options['gateway']
        test_type = options['test_type']
        
        self.stdout.write(
            self.style.SUCCESS(f'Testing SOLID payment architecture with {gateway_type} gateway')
        )
        
        # Initialize payment service
        payment_service = PaymentService(gateway_type=gateway_type)
        
        if test_type in ['all', 'course']:
            self.test_course_payment(payment_service)
        
        if test_type in ['all', 'workshop']:
            self.test_workshop_payment(payment_service)
        
        if test_type in ['all', 'service']:
            self.test_service_payment(payment_service)
        
        self.stdout.write(
            self.style.SUCCESS('SOLID payment architecture test completed successfully!')
        )

    def test_course_payment(self, payment_service):
        """Test course payment workflow"""
        self.stdout.write('Testing course payment...')
        
        # Create or get a test course
        course, created = Course.objects.get_or_create(
            title='Test SOLID Course',
            defaults={
                'slug': 'test-solid-course',
                'description': 'Test course for SOLID architecture',
                'short_description': 'Test course',
                'price': Decimal('99.00'),
                'currency': 'INR',
                'difficulty_level': 'beginner',
                'duration_hours': 10,
                'what_you_learn': 'SOLID principles',
                'instructor_id': 1,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(f'Created test course: {course.title}')
        
        # Test order creation
        try:
            response = payment_service.create_course_order(
                course_id=str(course.id),
                email='test@example.com'
            )
            
            if response.success:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Course order created: {response.payment_id}')
                )
                
                # Test payment completion
                completion_response = payment_service.complete_payment({
                    'payment_id': response.payment_id,
                    'razorpay_payment_id': 'pay_test_123',
                    'razorpay_order_id': response.order_id,
                    'razorpay_signature': 'test_signature'
                })
                
                if completion_response.success:
                    self.stdout.write(
                        self.style.SUCCESS('✓ Course payment completed successfully')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Course payment completion failed: {completion_response.error_message}')
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(f'✗ Course order creation failed: {response.error_message}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Course payment test failed: {str(e)}')
            )

    def test_workshop_payment(self, payment_service):
        """Test workshop payment workflow"""
        self.stdout.write('Testing workshop payment...')
        
        # Create or get a test workshop
        workshop, created = Workshop.objects.get_or_create(
            title='Test SOLID Workshop',
            defaults={
                'slug': 'test-solid-workshop',
                'description': 'Test workshop for SOLID architecture',
                'short_description': 'Test workshop',
                'is_paid': True,
                'price': Decimal('199.00'),
                'currency': 'INR',
                'start_date': timezone.now() + timezone.timedelta(days=7),
                'end_date': timezone.now() + timezone.timedelta(days=7, hours=2),
                'duration_hours': 2,
                'max_participants': 50,
                'instructor_id': 1,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(f'Created test workshop: {workshop.title}')
        
        # Test order creation
        try:
            application_data = {
                'user_name': 'Test User',
                'email': 'test@example.com',
                'user_phone': '+1234567890',
                'experience_level': 'beginner',
                'motivation': 'Learning SOLID principles'
            }
            
            response = payment_service.create_workshop_order(
                workshop_id=str(workshop.id),
                application_data=application_data
            )
            
            if response.success:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Workshop order created: {response.payment_id}')
                )
                
                # Test payment completion
                completion_response = payment_service.complete_payment({
                    'payment_id': response.payment_id,
                    'razorpay_payment_id': 'pay_test_456',
                    'razorpay_order_id': response.order_id,
                    'razorpay_signature': 'test_signature'
                })
                
                if completion_response.success:
                    self.stdout.write(
                        self.style.SUCCESS('✓ Workshop payment completed successfully')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Workshop payment completion failed: {completion_response.error_message}')
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(f'✗ Workshop order creation failed: {response.error_message}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Workshop payment test failed: {str(e)}')
            )

    def test_service_payment(self, payment_service):
        """Test service payment workflow"""
        self.stdout.write('Testing service payment...')
        
        # Create or get a test service
        service, created = TradingService.objects.get_or_create(
            name='Test SOLID Service',
            defaults={
                'slug': 'test-solid-service',
                'service_type': 'consultation',
                'description': 'Test service for SOLID architecture',
                'detailed_description': 'Test service',
                'price': Decimal('299.00'),
                'currency': 'INR',
                'duration': 'one_time',
                'features': ['SOLID principles consultation', 'Code review'],
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(f'Created test service: {service.name}')
        
        # Test order creation
        try:
            booking_data = {
                'user_name': 'Test User',
                'email': 'test@example.com',
                'user_phone': '+1234567890',
                'message': 'Need help with SOLID principles',
                'preferred_contact_method': 'whatsapp',
                'preferred_time': 'Evening'
            }
            
            response = payment_service.create_service_order(
                service_id=str(service.id),
                booking_data=booking_data
            )
            
            if response.success:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Service order created: {response.payment_id}')
                )
                
                # Test payment completion
                completion_response = payment_service.complete_payment({
                    'payment_id': response.payment_id,
                    'razorpay_payment_id': 'pay_test_789',
                    'razorpay_order_id': response.order_id,
                    'razorpay_signature': 'test_signature'
                })
                
                if completion_response.success:
                    self.stdout.write(
                        self.style.SUCCESS('✓ Service payment completed successfully')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Service payment completion failed: {completion_response.error_message}')
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(f'✗ Service order creation failed: {response.error_message}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Service payment test failed: {str(e)}')
            )