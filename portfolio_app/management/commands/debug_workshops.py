from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio_app.models import Workshop

class Command(BaseCommand):
    help = 'Debug workshop visibility issues'

    def handle(self, *args, **options):
        self.stdout.write("=== Workshop Debug Information ===")
        
        # Get all workshops
        all_workshops = Workshop.objects.all()
        self.stdout.write(f"Total workshops in database: {all_workshops.count()}")
        
        if all_workshops.count() == 0:
            self.stdout.write("No workshops found in database!")
            return
        
        for workshop in all_workshops:
            self.stdout.write(f"\n--- Workshop: {workshop.title} ---")
            self.stdout.write(f"ID: {workshop.id}")
            self.stdout.write(f"Slug: {workshop.slug}")
            self.stdout.write(f"Status: {workshop.status}")
            self.stdout.write(f"Is Active: {workshop.is_active}")
            self.stdout.write(f"Is Featured: {workshop.is_featured}")
            self.stdout.write(f"Start Date: {workshop.start_date}")
            self.stdout.write(f"Current Time: {timezone.now()}")
            self.stdout.write(f"Start Date > Now: {workshop.start_date > timezone.now()}")
            self.stdout.write(f"Is Paid: {workshop.is_paid}")
            self.stdout.write(f"Price: {workshop.price}")
            
            # Check if it meets upcoming criteria
            meets_upcoming_criteria = (
                workshop.is_active and 
                workshop.status == 'upcoming' and 
                workshop.start_date > timezone.now()
            )
            self.stdout.write(f"Meets upcoming criteria: {meets_upcoming_criteria}")
        
        # Test the actual query used by UpcomingWorkshopsView
        upcoming_workshops = Workshop.objects.filter(
            is_active=True,
            status='upcoming',
            start_date__gt=timezone.now()
        ).select_related('instructor').order_by('start_date')[:5]
        
        self.stdout.write(f"\n=== Upcoming Workshops Query Result ===")
        self.stdout.write(f"Count: {upcoming_workshops.count()}")
        
        for workshop in upcoming_workshops:
            self.stdout.write(f"- {workshop.title} ({workshop.start_date})")
        
        # Test the general workshop list query
        active_workshops = Workshop.objects.filter(is_active=True)
        self.stdout.write(f"\n=== Active Workshops ===")
        self.stdout.write(f"Count: {active_workshops.count()}")
        
        for workshop in active_workshops:
            self.stdout.write(f"- {workshop.title} (Status: {workshop.status}, Start: {workshop.start_date})")