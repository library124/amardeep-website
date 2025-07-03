from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, help_text="Phone number")
    date_of_birth = models.DateField(null=True, blank=True, help_text="Date of birth")
    bio = models.TextField(blank=True, help_text="Short bio")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    # Trading preferences
    trading_experience = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ],
        default='beginner',
        help_text="Trading experience level"
    )
    preferred_market = models.CharField(
        max_length=50,
        choices=[
            ('equity', 'Equity'),
            ('options', 'Options'),
            ('futures', 'Futures'),
            ('forex', 'Forex'),
            ('crypto', 'Cryptocurrency'),
        ],
        blank=True,
        help_text="Preferred trading market"
    )
    
    # Subscription and preferences
    email_notifications = models.BooleanField(default=True, help_text="Receive email notifications")
    sms_notifications = models.BooleanField(default=False, help_text="Receive SMS notifications")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def display_name(self):
        if self.user.first_name:
            return self.user.first_name
        return self.user.username

class PurchasedCourse(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_courses')
    course_name = models.CharField(max_length=255, help_text="Name of the purchased course")
    course_type = models.CharField(
        max_length=50,
        choices=[
            ('workshop', 'Workshop'),
            ('mentorship', 'Mentorship'),
            ('signals', 'Trading Signals'),
            ('course', 'Online Course'),
        ],
        help_text="Type of course"
    )
    description = models.TextField(blank=True, help_text="Course description")
    
    # Purchase details
    purchase_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(help_text="Course start date")
    end_date = models.DateTimeField(null=True, blank=True, help_text="Course end date")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Pricing
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount paid for the course")
    currency = models.CharField(max_length=3, default='INR')
    
    # Access details
    access_url = models.URLField(blank=True, help_text="URL to access the course")
    access_credentials = models.JSONField(default=dict, blank=True, help_text="Login credentials or access details")
    
    # Progress tracking
    progress_percentage = models.PositiveIntegerField(default=0, help_text="Course completion percentage")
    last_accessed = models.DateTimeField(null=True, blank=True, help_text="Last time user accessed the course")
    
    # Related objects
    workshop_application = models.ForeignKey('WorkshopApplication', on_delete=models.SET_NULL, null=True, blank=True)
    trading_service = models.ForeignKey('TradingService', on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-purchase_date']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['-purchase_date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.course_name}"

    @property
    def is_active(self):
        return self.status == 'active' and (not self.end_date or self.end_date > timezone.now())

    @property
    def days_remaining(self):
        if self.end_date and self.is_active:
            delta = self.end_date - timezone.now()
            return max(0, delta.days)
        return None

    @property
    def price_display(self):
        return f"{self.currency} {self.amount_paid:,.0f}"

    def mark_accessed(self):
        """Mark the course as accessed"""
        self.last_accessed = timezone.now()
        self.save(update_fields=['last_accessed'])

# Signal to create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

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
        return reverse('portfolio_app:blog_category', kwargs={'slug': self.slug})

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
        return reverse('portfolio_app:blog_tag', kwargs={'slug': self.slug})

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
        return reverse('portfolio_app:blog-post-detail', kwargs={'slug': self.slug})

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
        return reverse('portfolio_app:workshop-detail', kwargs={'slug': self.slug})

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
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Payment Pending'),
        ('completed', 'Payment Completed'),
        ('failed', 'Payment Failed'),
        ('refunded', 'Refunded'),
        ('not_required', 'Not Required'),
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
    
    # Payment fields
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUS_CHOICES, default='not_required')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_id = models.CharField(max_length=100, blank=True, help_text="Payment gateway transaction ID")
    payment_method = models.CharField(max_length=50, blank=True, help_text="Payment method used")
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text="Admin notes")

    class Meta:
        ordering = ['-applied_at']
        unique_together = ['workshop', 'email']  # Prevent duplicate applications
        indexes = [
            models.Index(fields=['-applied_at']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_status']),
            models.Index(fields=['workshop', 'status']),
        ]

    def __str__(self):
        return f"{self.name} - {self.workshop.title} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        # Set payment status based on workshop type
        if self.workshop.is_paid and self.payment_status == 'not_required':
            self.payment_status = 'pending'
            self.payment_amount = self.workshop.price
        elif not self.workshop.is_paid:
            self.payment_status = 'not_required'
            self.payment_amount = 0
        
        # Auto-approve free workshops or paid workshops with completed payment
        if (not self.workshop.is_paid or self.payment_status == 'completed') and self.status == 'pending':
            if not self.workshop.is_full:
                self.status = 'approved'
                # Increment registered count
                self.workshop.registered_count += 1
                self.workshop.save(update_fields=['registered_count'])
            else:
                self.status = 'waitlist'
        
        super().save(*args, **kwargs)

    def mark_payment_completed(self, payment_id, payment_method):
        """Mark payment as completed"""
        self.payment_status = 'completed'
        self.payment_id = payment_id
        self.payment_method = payment_method
        self.paid_at = timezone.now()
        if self.status == 'pending' and not self.workshop.is_full:
            self.status = 'approved'
            self.workshop.registered_count += 1
            self.workshop.save(update_fields=['registered_count'])
        self.save()

class TradingService(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('signals', 'Trading Signals'),
        ('mentorship', 'Mentorship'),
        ('consultation', 'Consultation'),
        ('course', 'Trading Course'),
    ]
    
    DURATION_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('one_time', 'One Time'),
    ]

    name = models.CharField(max_length=255, help_text="Service name (e.g., Basic Signals)")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, default='signals')
    description = models.TextField(help_text="Brief description of the service")
    detailed_description = models.TextField(blank=True, help_text="Detailed description for service page")
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Service price")
    currency = models.CharField(max_length=3, default='INR')
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default='monthly')
    
    # Features (JSON field to store list of features)
    features = models.JSONField(default=list, help_text="List of service features")
    
    # Visibility and Status
    is_active = models.BooleanField(default=True, help_text="Show on website")
    is_featured = models.BooleanField(default=False, help_text="Mark as popular/featured")
    is_popular = models.BooleanField(default=False, help_text="Show 'Most Popular' badge")
    
    # Contact and Booking
    booking_type = models.CharField(
        max_length=20,
        choices=[
            ('whatsapp', 'WhatsApp'),
            ('call', 'Phone Call'),
            ('email', 'Email'),
            ('form', 'Contact Form'),
        ],
        default='whatsapp',
        help_text="How users can book this service"
    )
    contact_info = models.CharField(max_length=255, blank=True, help_text="Contact number/email for booking")
    booking_url = models.URLField(blank=True, help_text="External booking URL if any")
    
    # Display Order
    display_order = models.PositiveIntegerField(default=0, help_text="Order to display services")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description")

    class Meta:
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['display_order']),
        ]

    def __str__(self):
        return f"{self.name} - {self.get_duration_display()}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.meta_title:
            self.meta_title = self.name[:60]
        if not self.meta_description:
            self.meta_description = self.description[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('portfolio_app:service-detail', kwargs={'slug': self.slug})

    @property
    def price_display(self):
        if self.duration == 'one_time':
            return f"{self.currency} {self.price:,.0f}"
        return f"{self.currency} {self.price:,.0f} / {self.get_duration_display().lower()}"

    def get_booking_url(self):
        """Generate booking URL based on booking type"""
        if self.booking_url:
            return self.booking_url
        
        if self.booking_type == 'whatsapp' and self.contact_info:
            message = f"Hi! I'm interested in the {self.name} service. Can you provide more details?"
            return f"https://wa.me/{self.contact_info}?text={message}"
        elif self.booking_type == 'call' and self.contact_info:
            return f"tel:{self.contact_info}"
        elif self.booking_type == 'email' and self.contact_info:
            subject = f"Inquiry about {self.name}"
            body = f"Hi! I'm interested in the {self.name} service. Can you provide more details?"
            return f"mailto:{self.contact_info}?subject={subject}&body={body}"
        
        return "/contact"  # Fallback to contact page

class ServiceBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    service = models.ForeignKey(TradingService, on_delete=models.CASCADE, related_name='bookings')
    name = models.CharField(max_length=100, help_text="Customer name")
    email = models.EmailField(help_text="Customer email")
    phone = models.CharField(max_length=20, help_text="Customer phone number")
    message = models.TextField(blank=True, help_text="Customer message/requirements")
    
    # Booking details
    preferred_contact_method = models.CharField(
        max_length=20,
        choices=[
            ('whatsapp', 'WhatsApp'),
            ('call', 'Phone Call'),
            ('email', 'Email'),
        ],
        default='whatsapp'
    )
    preferred_time = models.CharField(max_length=100, blank=True, help_text="Preferred contact time")
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, help_text="Internal notes")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contacted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['service']),
        ]

    def __str__(self):
        return f"{self.name} - {self.service.name} ({self.get_status_display()})"

class Course(models.Model):
    """Model for courses that can be purchased"""
    COURSE_TYPE_CHOICES = [
        ('video', 'Video Course'),
        ('live', 'Live Course'),
        ('workshop', 'Workshop'),
        ('mentorship', 'Mentorship'),
        ('signals', 'Trading Signals'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    title = models.CharField(max_length=255, help_text="Course title")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(help_text="Detailed course description")
    short_description = models.TextField(max_length=300, help_text="Brief description for cards/listings")
    
    # Media
    featured_image = models.ImageField(upload_to='courses/images/', help_text="Course cover image")
    preview_video = models.URLField(blank=True, help_text="Preview video URL")
    
    # Course Details
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES, default='video')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    duration_hours = models.PositiveIntegerField(help_text="Course duration in hours")
    lessons_count = models.PositiveIntegerField(default=0, help_text="Number of lessons")
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Course price")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Original price (for discounts)")
    currency = models.CharField(max_length=3, default='INR')
    
    # Content and Requirements
    what_you_learn = models.TextField(help_text="What students will learn")
    requirements = models.TextField(blank=True, help_text="Prerequisites or requirements")
    course_content = models.JSONField(default=list, help_text="Course modules and lessons")
    
    # Instructor and Status
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    is_active = models.BooleanField(default=True, help_text="Show on website")
    is_featured = models.BooleanField(default=False, help_text="Feature on homepage")
    
    # Enrollment
    max_students = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum number of students (null = unlimited)")
    enrolled_count = models.PositiveIntegerField(default=0, help_text="Current number of enrollments")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description")

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['course_type']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.meta_description:
            self.meta_description = self.short_description[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('portfolio_app:course-detail', kwargs={'slug': self.slug})

    @property
    def price_display(self):
        return f"{self.currency} {self.price:,.0f}"

    @property
    def original_price_display(self):
        if self.original_price:
            return f"{self.currency} {self.original_price:,.0f}"
        return None

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    @property
    def is_full(self):
        if self.max_students:
            return self.enrolled_count >= self.max_students
        return False

    @property
    def spots_remaining(self):
        if self.max_students:
            return max(0, self.max_students - self.enrolled_count)
        return None

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

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_TYPE_CHOICES = [
        ('workshop', 'Workshop'),
        ('product', 'Digital Product'),
        ('subscription', 'Subscription'),
        ('service', 'Trading Service'),
        ('course', 'Course'),
    ]

    # Payment details
    payment_id = models.CharField(max_length=100, unique=True, help_text="Unique payment identifier")
    razorpay_order_id = models.CharField(max_length=100, blank=True, help_text="Razorpay order ID")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_type = models.CharField(max_length=15, choices=PAYMENT_TYPE_CHOICES)
    
    # Customer details
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    
    # Payment gateway details
    gateway_payment_id = models.CharField(max_length=100, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    
    # Related objects
    workshop_application = models.ForeignKey(WorkshopApplication, on_delete=models.SET_NULL, null=True, blank=True)
    digital_product = models.ForeignKey(DigitalProduct, on_delete=models.SET_NULL, null=True, blank=True)
    trading_service = models.ForeignKey(TradingService, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_type']),
            models.Index(fields=['customer_email']),
            models.Index(fields=['razorpay_order_id']),
        ]

    def __str__(self):
        return f"Payment {self.payment_id} - {self.customer_name} ({self.get_status_display()})"

    def mark_completed(self, gateway_payment_id, payment_method, gateway_response=None):
        """Mark payment as completed"""
        self.status = 'completed'
        self.gateway_payment_id = gateway_payment_id
        self.payment_method = payment_method
        self.completed_at = timezone.now()
        if gateway_response:
            self.gateway_response = gateway_response
        self.save()

        # Update related application if exists
        if self.workshop_application:
            self.workshop_application.mark_payment_completed(gateway_payment_id, payment_method)
        
        # Create purchased course if course payment
        if self.course:
            PurchasedCourse.objects.create(
                user_id=self.gateway_response.get('user_id') if self.gateway_response else None,
                course_name=self.course.title,
                course_type='course',
                description=self.course.short_description,
                purchase_date=timezone.now(),
                start_date=timezone.now(),
                amount_paid=self.amount,
                currency=self.currency,
                status='active',
                course=self.course
            )
            
            # Increment enrolled count
            self.course.enrolled_count += 1
            self.course.save(update_fields=['enrolled_count'])

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('resolved', 'Resolved'),
        ('archived', 'Archived'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    # Contact details
    name = models.CharField(max_length=100, help_text="Sender's name")
    email = models.EmailField(help_text="Sender's email address")
    subject = models.CharField(max_length=255, help_text="Message subject")
    message = models.TextField(help_text="Message content")
    
    # Classification and status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    
    # Admin fields
    admin_notes = models.TextField(blank=True, help_text="Internal admin notes")
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_contacts',
        help_text="Admin user assigned to handle this message"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_at = models.DateTimeField(null=True, blank=True, help_text="When the message was first read")
    replied_at = models.DateTimeField(null=True, blank=True, help_text="When a reply was sent")
    
    # Additional metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True, help_text="Sender's IP address")
    user_agent = models.TextField(blank=True, help_text="Sender's browser user agent")

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.get_status_display()})"

    def mark_as_read(self, user=None):
        """Mark the message as read"""
        if self.status == 'new':
            self.status = 'read'
            self.read_at = timezone.now()
            if user:
                self.assigned_to = user
            self.save(update_fields=['status', 'read_at', 'assigned_to'])

    def mark_as_replied(self):
        """Mark the message as replied"""
        self.status = 'replied'
        self.replied_at = timezone.now()
        self.save(update_fields=['status', 'replied_at'])

    @property
    def is_new(self):
        return self.status == 'new'

    @property
    def is_urgent(self):
        return self.priority in ['high', 'urgent']

    @property
    def response_time(self):
        """Calculate response time if replied"""
        if self.replied_at:
            delta = self.replied_at - self.created_at
            return delta
        return None

    def get_priority_color(self):
        """Get color for priority display"""
        colors = {
            'low': '#28a745',      # Green
            'normal': '#6c757d',   # Gray
            'high': '#fd7e14',     # Orange
            'urgent': '#dc3545',   # Red
        }
        return colors.get(self.priority, '#6c757d')

    def get_status_color(self):
        """Get color for status display"""
        colors = {
            'new': '#007bff',      # Blue
            'read': '#6c757d',     # Gray
            'replied': '#28a745',  # Green
            'resolved': '#20c997', # Teal
            'archived': '#6f42c1', # Purple
        }
        return colors.get(self.status, '#6c757d')
