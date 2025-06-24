"""
Django management command to initialize TiDB Cloud database
"""
from django.core.management.base import BaseCommand
from database.config import init_db, test_connection

class Command(BaseCommand):
    help = 'Initialize TiDB Cloud database and create tables'

    def handle(self, *args, **options):
        self.stdout.write('Initializing TiDB Cloud database...')
        
        # Test connection first
        if test_connection():
            self.stdout.write(
                self.style.SUCCESS('✅ Database connection successful!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Database connection failed!')
            )
            return
        
        # Initialize database
        if init_db():
            self.stdout.write(
                self.style.SUCCESS('✅ Database tables created successfully!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Failed to create database tables!')
            )