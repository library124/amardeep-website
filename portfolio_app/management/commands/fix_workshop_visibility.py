from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from portfolio_app.models import Workshop

class Command(BaseCommand):
    help = 'Fix workshop visibility issues by updating dates and ensuring proper settings'

    def add_arguments(self, parser):
        parser.add_argument(
            '--update-dates',
            action='store_true',
            help='Update workshop dates to future dates for visibility',
        )
        parser.add_argument(
            '--days-ahead',
            type=int,
            default=7,
            help='Number of days ahead to set workshop dates (default: 7)',
        )

    def handle(self, *args, **options):
        self.stdout.write("=== Workshop Visibility Fix ===")
        
        workshops = Workshop.objects.all()
        self.stdout.write(f"Found {workshops.count()} workshops")
        
        if workshops.count() == 0:
            self.stdout.write("No workshops to fix!")
            return
        
        fixed_count = 0
        
        for workshop in workshops:
            self.stdout.write(f"\nProcessing: {workshop.title}")
            
            # Ensure workshop is active
            if not workshop.is_active:
                workshop.is_active = True
                self.stdout.write("  ✓ Set is_active = True")
                fixed_count += 1
            
            # Ensure workshop has upcoming status
            if workshop.status != 'upcoming':
                workshop.status = 'upcoming'
                self.stdout.write("  ✓ Set status = 'upcoming'")
                fixed_count += 1
            
            # Update dates if requested
            if options['update_dates']:
                days_ahead = options['days_ahead']
                new_start_date = timezone.now() + timedelta(days=days_ahead)
                new_end_date = new_start_date + timedelta(hours=workshop.duration_hours)
                
                workshop.start_date = new_start_date
                workshop.end_date = new_end_date
                self.stdout.write(f"  ✓ Updated dates: Start = {new_start_date}, End = {new_end_date}")
                fixed_count += 1
            
            workshop.save()
            
            # Check if workshop will now be visible
            will_be_visible = (
                workshop.is_active and 
                workshop.status == 'upcoming' and 
                workshop.start_date > (timezone.now() - timedelta(days=30))
            )
            
            self.stdout.write(f"  → Will be visible on frontend: {'YES' if will_be_visible else 'NO'}")
        
        self.stdout.write(f"\n=== Fix Complete ===")
        self.stdout.write(f"Workshops processed: {workshops.count()}")
        self.stdout.write(f"Changes made: {fixed_count}")
        
        # Test the API endpoints
        self.stdout.write(f"\n=== Testing Visibility ===")
        
        # Test upcoming workshops (with 30-day buffer)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        upcoming_workshops = Workshop.objects.filter(
            is_active=True,
            status='upcoming',
            start_date__gt=thirty_days_ago
        )
        self.stdout.write(f"Upcoming workshops (with 30-day buffer): {upcoming_workshops.count()}")
        
        # Test active workshops
        active_workshops = Workshop.objects.filter(is_active=True)
        self.stdout.write(f"Active workshops: {active_workshops.count()}")
        
        if active_workshops.count() > 0:
            self.stdout.write("\n✅ Workshops should now be visible on the frontend!")
            self.stdout.write("Frontend will use /api/workshops/active/ endpoint which shows all active workshops.")
        else:
            self.stdout.write("\n❌ No active workshops found. Please check workshop settings in admin.")