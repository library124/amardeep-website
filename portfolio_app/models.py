from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
import uuid

class Achievement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    metrics = models.JSONField(default=dict) # e.g., {'profit': 1000, 'roi': 0.15}
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')

    def __str__(self):
        return self.title

class DigitalProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    download_link = models.URLField(blank=True, null=True)
    # Add fields for product files, images, etc.

    def __str__(self):
        return self.name

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_confirmed = models.BooleanField(default=False)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return f"{self.email} ({'Confirmed' if self.is_confirmed else 'Pending'})"

    def confirm_subscription(self):
        self.is_confirmed = True
        self.confirmed_at = timezone.now()
        self.save()

class Newsletter(models.Model):
    subject = models.CharField(max_length=255)
    content_html = models.TextField(help_text="HTML content of the newsletter")
    content_text = models.TextField(blank=True, help_text="Plain text version (optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)
    sent_to_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        status = "Sent" if self.is_sent else "Draft"
        return f"{self.subject} ({status})"

    def mark_as_sent(self, count):
        self.is_sent = True
        self.sent_at = timezone.now()
        self.sent_to_count = count
        self.save()

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_category', kwargs={'slug': self.slug})

class BlogTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_tag', kwargs={'slug': self.slug})

class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('scheduled', 'Scheduled'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField(BlogTag, blank=True, related_name='posts')
    
    # Content fields
    excerpt = models.TextField(max_length=500, help_text="Brief description of the post")
    content = models.TextField(help_text="Main content of the blog post")
    featured_image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title (max 60 chars)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description (max 160 chars)")
    
    # Status and timing
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    publish_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Engagement
    views_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False, help_text="Feature this post on homepage")

    class Meta:
        ordering = ['-publish_date']
        indexes = [
            models.Index(fields=['-publish_date']),
            models.Index(fields=['status']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.meta_description:
            self.meta_description = self.excerpt[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_post_detail', kwargs={'slug': self.slug})

    @property
    def is_published(self):
        return self.status == 'published' and self.publish_date <= timezone.now()

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def get_reading_time(self):
        """Estimate reading time based on word count"""
        word_count = len(self.content.split())
        reading_time = max(1, word_count // 200)  # Assume 200 words per minute
        return reading_time

    def get_related_posts(self, count=3):
        """Get related posts based on category and tags"""
        related = BlogPost.objects.filter(
            status='published',
            publish_date__lte=timezone.now()
        ).exclude(id=self.id)
        
        if self.category:
            related = related.filter(category=self.category)
        
        return related[:count]

class Workshop(models.Model):
    WORKSHOP_TYPE_CHOICES = [
        ('free', 'Free'),
        ('paid', 'Paid'),
    ]
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=255, help_text="Workshop title")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(help_text="Detailed workshop description")
    short_description = models.TextField(max_length=300, help_text="Brief description for cards/listings")
    
    # Media
    featured_image = models.ImageField(upload_to='workshops/images/', help_text="Workshop cover image")
    
    # Pricing
    is_paid = models.BooleanField(default=False, help_text="Is this a paid workshop?")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Price (required for paid workshops)")
    currency = models.CharField(max_length=3, default='INR', help_text="Currency code (e.g., INR, USD)")
    
    # Scheduling
    start_date = models.DateTimeField(help_text="Workshop start date and time")
    end_date = models.DateTimeField(help_text="Workshop end date and time")
    duration_hours = models.PositiveIntegerField(help_text="Duration in hours")
    
    # Capacity and Registration
    max_participants = models.PositiveIntegerField(default=50, help_text="Maximum number of participants")
    registered_count = models.PositiveIntegerField(default=0, help_text="Current number of registrations")
    
    # Status and Visibility
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    is_featured = models.BooleanField(default=False, help_text="Feature on homepage")
    is_active = models.BooleanField(default=True, help_text="Show on website")
    
    # Additional Information
    requirements = models.TextField(blank=True, help_text="Prerequisites or requirements")
    what_you_learn = models.TextField(blank=True, help_text="What participants will learn")
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workshops')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description")

    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['-start_date']),
            models.Index(fields=['status']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['is_paid']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.meta_description:
            self.meta_description = self.short_description[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('workshop_detail', kwargs={'slug': self.slug})

    @property
    def is_upcoming(self):
        return self.start_date > timezone.now()

    @property
    def is_ongoing(self):
        return self.start_date <= timezone.now() <= self.end_date

    @property
    def is_completed(self):
        return self.end_date < timezone.now()

    @property
    def spots_remaining(self):
        return max(0, self.max_participants - self.registered_count)

    @property
    def is_full(self):
        return self.registered_count >= self.max_participants

    @property
    def price_display(self):
        if self.is_paid and self.price:
            return f"{self.currency} {self.price:,.0f}"
        return "Free"

    def get_duration_display(self):
        if self.duration_hours == 1:
            return "1 hour"
        elif self.duration_hours < 24:
            return f"{self.duration_hours} hours"
        else:
            days = self.duration_hours // 24
            remaining_hours = self.duration_hours % 24
            if remaining_hours == 0:
                return f"{days} day{'s' if days > 1 else ''}"
            else:
                return f"{days} day{'s' if days > 1 else ''} {remaining_hours} hour{'s' if remaining_hours > 1 else ''}"

class WorkshopApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('waitlist', 'Waitlist'),
    ]

    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=100, help_text="Applicant's full name")
    email = models.EmailField(help_text="Applicant's email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Phone number (optional)")
    experience_level = models.CharField(
        max_length=50, 
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner',
        help_text="Trading experience level"
    )
    motivation = models.TextField(
        blank=True, 
        help_text="Why do you want to join this workshop? (optional)"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text="Admin notes")

    class Meta:
        ordering = ['-applied_at']
        unique_together = ['workshop', 'email']  # Prevent duplicate applications
        indexes = [
            models.Index(fields=['-applied_at']),
            models.Index(fields=['status']),
            models.Index(fields=['workshop', 'status']),
        ]

    def __str__(self):
        return f"{self.name} - {self.workshop.title} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        # Auto-approve if workshop has available spots and is not full
        if self.status == 'pending' and not self.workshop.is_full:
            self.status = 'approved'
            # Increment registered count
            self.workshop.registered_count += 1
            self.workshop.save(update_fields=['registered_count'])
        elif self.status == 'pending' and self.workshop.is_full:
            self.status = 'waitlist'
        
        super().save(*args, **kwargs)
