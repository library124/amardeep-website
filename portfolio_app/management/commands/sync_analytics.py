"""
Django management command to sync analytics data
"""
from django.core.management.base import BaseCommand
from database.sync import DataSyncManager

class Command(BaseCommand):
    help = 'Sync analytics data from Django to TiDB Cloud'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['all', 'users', 'workshops', 'content', 'revenue', 'newsletters', 'services'],
            default='all',
            help='Type of data to sync'
        )

    def handle(self, *args, **options):
        sync_type = options['type']
        
        self.stdout.write(f'Starting {sync_type} analytics sync...')
        
        try:
            with DataSyncManager() as sync_manager:
                if sync_type == 'all':
                    sync_manager.full_sync()
                elif sync_type == 'users':
                    sync_manager.sync_user_analytics()
                elif sync_type == 'workshops':
                    sync_manager.sync_workshop_analytics()
                elif sync_type == 'content':
                    sync_manager.sync_content_analytics()
                elif sync_type == 'revenue':
                    sync_manager.sync_revenue_analytics()
                elif sync_type == 'newsletters':
                    sync_manager.sync_newsletter_analytics()
                elif sync_type == 'services':
                    sync_manager.sync_trading_service_analytics()
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ {sync_type.title()} analytics sync completed!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Analytics sync failed: {e}')
            )