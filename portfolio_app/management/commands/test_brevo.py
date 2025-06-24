from django.core.management.base import BaseCommand
from portfolio_app.services.brevo_service import brevo_service

class Command(BaseCommand):
    help = 'Test Brevo email service integration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Test email address to send to',
            default='test@example.com'
        )

    def handle(self, *args, **options):
        test_email = options['email']
        
        self.stdout.write("=== Testing Brevo Email Service ===")
        
        # Test basic email sending
        self.stdout.write(f"\n1. Testing basic email to {test_email}...")
        
        success = brevo_service.send_email(
            to_email=test_email,
            to_name="Test User",
            subject="Test Email from Brevo Integration",
            html_content="""
            <html>
            <body>
                <h2>Test Email</h2>
                <p>This is a test email sent via Brevo API integration.</p>
                <p>If you receive this, the integration is working correctly!</p>
            </body>
            </html>
            """,
            text_content="This is a test email sent via Brevo API integration. If you receive this, the integration is working correctly!"
        )
        
        if success:
            self.stdout.write(self.style.SUCCESS("✓ Basic email test passed"))
        else:
            self.stdout.write(self.style.ERROR("✗ Basic email test failed"))
        
        # Test service booking notification (mock data)
        self.stdout.write(f"\n2. Testing service booking notification...")
        
        # Create a mock booking object for testing
        class MockService:
            name = "Premium Mentorship"
            price_display = "INR 9,999 / month"
            description = "Complete trading mentorship with personalized guidance and advanced strategies for serious traders."
            def get_service_type_display(self):
                return "Mentorship"
        
        class MockBooking:
            id = 123
            name = "Test Customer"
            email = test_email
            phone = "+91 98765 43210"
            message = "I'm interested in learning advanced trading strategies."
            preferred_time = "Weekdays 10 AM - 6 PM"
            service = MockService()
            
            def get_preferred_contact_method_display(self):
                return "WhatsApp"
            
            from django.utils import timezone
            created_at = timezone.now()
        
        mock_booking = MockBooking()
        
        # Test admin notification
        admin_success = brevo_service.send_service_booking_notification(mock_booking)
        if admin_success:
            self.stdout.write(self.style.SUCCESS("✓ Admin notification test passed"))
        else:
            self.stdout.write(self.style.ERROR("✗ Admin notification test failed"))
        
        # Test customer confirmation
        customer_success = brevo_service.send_service_booking_confirmation(mock_booking)
        if customer_success:
            self.stdout.write(self.style.SUCCESS("✓ Customer confirmation test passed"))
        else:
            self.stdout.write(self.style.ERROR("✗ Customer confirmation test failed"))
        
        # Test newsletter confirmation
        self.stdout.write(f"\n3. Testing newsletter confirmation...")
        
        class MockSubscriber:
            email = test_email
            name = "Test Subscriber"
            confirmation_token = "test-token-123"
        
        mock_subscriber = MockSubscriber()
        newsletter_success = brevo_service.send_newsletter_confirmation(mock_subscriber)
        
        if newsletter_success:
            self.stdout.write(self.style.SUCCESS("✓ Newsletter confirmation test passed"))
        else:
            self.stdout.write(self.style.ERROR("✗ Newsletter confirmation test failed"))
        
        # Summary
        self.stdout.write(f"\n=== Test Summary ===")
        total_tests = 4
        passed_tests = sum([success, admin_success, customer_success, newsletter_success])
        
        self.stdout.write(f"Tests passed: {passed_tests}/{total_tests}")
        
        if passed_tests == total_tests:
            self.stdout.write(self.style.SUCCESS("🎉 All tests passed! Brevo integration is working correctly."))
        else:
            self.stdout.write(self.style.WARNING(f"⚠️  {total_tests - passed_tests} test(s) failed. Check your Brevo API key and configuration."))
        
        self.stdout.write(f"\nNote: Check the email inbox for {test_email} to verify email delivery.")