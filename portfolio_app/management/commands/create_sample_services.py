from django.core.management.base import BaseCommand
from portfolio_app.models import TradingService

class Command(BaseCommand):
    help = 'Create sample trading services for testing'

    def handle(self, *args, **options):
        self.stdout.write("Creating sample trading services...")
        
        # Basic Signals Service
        basic_service, created = TradingService.objects.get_or_create(
            name="Basic Signals",
            defaults={
                'service_type': 'signals',
                'description': 'Get started with essential trading signals and market insights for consistent intraday profits.',
                'detailed_description': 'Our Basic Signals package provides you with 5-7 high-probability trading signals daily, along with weekly market analysis and basic WhatsApp support during market hours.',
                'price': 2999,
                'currency': 'INR',
                'duration': 'monthly',
                'features': [
                    'Daily Trading Signals - 5-7 high-probability signals daily',
                    'Market Analysis - Weekly market outlook and trends',
                    'WhatsApp Support - Basic support during market hours'
                ],
                'is_active': True,
                'is_featured': False,
                'is_popular': False,
                'booking_type': 'whatsapp',
                'contact_info': '919876543210',  # Replace with actual number
                'display_order': 1
            }
        )
        if created:
            self.stdout.write(f"✓ Created: {basic_service.name}")
        else:
            self.stdout.write(f"- Already exists: {basic_service.name}")
        
        # Premium Mentorship Service
        premium_service, created = TradingService.objects.get_or_create(
            name="Premium Mentorship",
            defaults={
                'service_type': 'mentorship',
                'description': 'Complete trading mentorship with personalized guidance and advanced strategies for serious traders.',
                'detailed_description': 'Our Premium Mentorship program includes 10-15 high-accuracy signals with detailed analysis, weekly live trading sessions, one-on-one guidance, and advanced risk management tools.',
                'price': 9999,
                'currency': 'INR',
                'duration': 'monthly',
                'features': [
                    'Premium Signals - 10-15 high-accuracy signals with detailed analysis',
                    'Live Trading Sessions - Weekly live trading and strategy sessions',
                    'Personal Mentorship - One-on-one guidance and portfolio review',
                    'Risk Management Tools - Advanced calculators and position sizing'
                ],
                'is_active': True,
                'is_featured': True,
                'is_popular': True,
                'booking_type': 'whatsapp',
                'contact_info': '919876543210',  # Replace with actual number
                'display_order': 2
            }
        )
        if created:
            self.stdout.write(f"✓ Created: {premium_service.name}")
        else:
            self.stdout.write(f"- Already exists: {premium_service.name}")
        
        # VIP Elite Service
        vip_service, created = TradingService.objects.get_or_create(
            name="VIP Elite",
            defaults={
                'service_type': 'consultation',
                'description': 'Exclusive access to Amardeep\'s personal trading strategies and direct mentorship for elite traders.',
                'detailed_description': 'Our VIP Elite package provides exclusive access to Amardeep\'s personal trading methods, direct WhatsApp and call access, and complete portfolio management services.',
                'price': 24999,
                'currency': 'INR',
                'duration': 'monthly',
                'features': [
                    'Exclusive Strategies - Access to Amardeep\'s personal trading methods',
                    'Direct Access - Direct WhatsApp and call access to Amardeep',
                    'Portfolio Management - Complete portfolio analysis and optimization'
                ],
                'is_active': True,
                'is_featured': False,
                'is_popular': False,
                'booking_type': 'call',
                'contact_info': '919876543210',  # Replace with actual number
                'display_order': 3
            }
        )
        if created:
            self.stdout.write(f"✓ Created: {vip_service.name}")
        else:
            self.stdout.write(f"- Already exists: {vip_service.name}")
        
        self.stdout.write("\n=== Sample Services Created Successfully ===")
        self.stdout.write("You can now:")
        self.stdout.write("1. View services in Django admin")
        self.stdout.write("2. Test API endpoints:")
        self.stdout.write("   - GET /api/services/")
        self.stdout.write("   - GET /api/services/featured/")
        self.stdout.write("3. Update contact_info with real phone numbers")
        self.stdout.write("4. Customize features and descriptions as needed")