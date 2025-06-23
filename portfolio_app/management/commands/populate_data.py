from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portfolio_app.models import Achievement, DigitalProduct
from datetime import date

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        # Create a test user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='testtrader',
            defaults={
                'email': 'trader@example.com',
                'first_name': 'Test',
                'last_name': 'Trader'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created test user: testtrader'))

        # Create sample achievements
        achievements_data = [
            {
                'title': 'First Profitable Month',
                'description': 'Achieved my first profitable month with consistent gains across multiple trading sessions.',
                'date': date(2024, 1, 15),
                'metrics': {'profit': 2500, 'roi': 0.12, 'win_rate': 0.68}
            },
            {
                'title': 'Risk Management Milestone',
                'description': 'Successfully implemented strict risk management rules, limiting losses to 2% per trade.',
                'date': date(2024, 2, 20),
                'metrics': {'max_drawdown': 0.08, 'sharpe_ratio': 1.45, 'trades': 45}
            },
            {
                'title': 'High-Volume Trading Day',
                'description': 'Executed 25 successful trades in a single day during high market volatility.',
                'date': date(2024, 3, 10),
                'metrics': {'profit': 1800, 'trades': 25, 'volume': 150000}
            }
        ]

        for achievement_data in achievements_data:
            achievement, created = Achievement.objects.get_or_create(
                title=achievement_data['title'],
                user=user,
                defaults=achievement_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created achievement: {achievement.title}'))

        # Create sample digital products
        products_data = [
            {
                'name': 'Intraday Trading Strategy Guide',
                'description': 'Comprehensive guide covering proven intraday trading strategies with real-world examples.',
                'price': 49.99,
                'download_link': 'https://example.com/download/strategy-guide'
            },
            {
                'name': 'Risk Management Calculator',
                'description': 'Excel-based calculator to help determine position sizes and risk levels for each trade.',
                'price': 29.99,
                'download_link': 'https://example.com/download/risk-calculator'
            },
            {
                'name': 'Market Analysis Templates',
                'description': 'Professional templates for technical and fundamental market analysis.',
                'price': 39.99,
                'download_link': 'https://example.com/download/analysis-templates'
            }
        ]

        for product_data in products_data:
            product, created = DigitalProduct.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))