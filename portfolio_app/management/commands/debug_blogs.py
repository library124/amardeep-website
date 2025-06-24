from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio_app.models import BlogPost

class Command(BaseCommand):
    help = 'Debug blog post visibility issues'

    def handle(self, *args, **options):
        self.stdout.write("=== Blog Post Debug Information ===")
        
        # Get all blog posts
        all_posts = BlogPost.objects.all()
        self.stdout.write(f"Total blog posts in database: {all_posts.count()}")
        
        if all_posts.count() == 0:
            self.stdout.write("No blog posts found in database!")
            return
        
        for post in all_posts:
            self.stdout.write(f"\n--- Blog Post: {post.title} ---")
            self.stdout.write(f"ID: {post.id}")
            self.stdout.write(f"Slug: {post.slug}")
            self.stdout.write(f"Status: {post.status}")
            self.stdout.write(f"Is Featured: {post.is_featured}")
            self.stdout.write(f"Publish Date: {post.publish_date}")
            self.stdout.write(f"Current Time: {timezone.now()}")
            self.stdout.write(f"Publish Date <= Now: {post.publish_date <= timezone.now()}")
            self.stdout.write(f"Author: {post.author}")
            self.stdout.write(f"Category: {post.category}")
            
            # Check if it meets published criteria
            meets_published_criteria = (
                post.status == 'published' and 
                post.publish_date <= timezone.now()
            )
            self.stdout.write(f"Meets published criteria: {meets_published_criteria}")
        
        # Test the actual query used by FeaturedBlogPostsView
        featured_posts = BlogPost.objects.filter(
            status='published',
            publish_date__lte=timezone.now(),
            is_featured=True
        ).select_related('author', 'category').prefetch_related('tags')[:3]
        
        self.stdout.write(f"\n=== Featured Blog Posts Query Result ===")
        self.stdout.write(f"Count: {featured_posts.count()}")
        
        for post in featured_posts:
            self.stdout.write(f"- {post.title} ({post.publish_date})")
        
        # Test the general blog list query
        published_posts = BlogPost.objects.filter(
            status='published',
            publish_date__lte=timezone.now()
        )
        self.stdout.write(f"\n=== Published Blog Posts ===")
        self.stdout.write(f"Count: {published_posts.count()}")
        
        for post in published_posts:
            self.stdout.write(f"- {post.title} (Status: {post.status}, Published: {post.publish_date}, Featured: {post.is_featured})")