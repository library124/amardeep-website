from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Achievement, DigitalProduct, BlogPost, 
    BlogCategory, BlogTag, Workshop, WorkshopApplication, Payment,
    TradingService, ServiceBooking, UserProfile, PurchasedCourse,
    ContactMessage, Course
)
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'

class DigitalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalProduct
        fields = '__all__'


class BlogCategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'description', 'post_count']

    def get_post_count(self, obj):
        return obj.posts.filter(status='published').count()

class BlogTagSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogTag
        fields = ['id', 'name', 'slug', 'post_count']

    def get_post_count(self, obj):
        return obj.posts.filter(status='published').count()

class BlogPostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'author_name', 'category_name', 'tags', 'publish_date',
            'views_count', 'reading_time', 'is_featured'
        ]

    def get_reading_time(self, obj):
        return obj.get_reading_time()

class BlogPostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    reading_time = serializers.SerializerMethodField()
    related_posts = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'author_name', 'category', 'tags', 'publish_date', 'updated_at',
            'views_count', 'reading_time', 'meta_title', 'meta_description',
            'related_posts'
        ]

    def get_reading_time(self, obj):
        return obj.get_reading_time()

    def get_related_posts(self, obj):
        related = obj.get_related_posts()
        return BlogPostListSerializer(related, many=True, context=self.context).data

class WorkshopSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    price_display = serializers.SerializerMethodField()
    duration_display = serializers.SerializerMethodField()
    spots_remaining = serializers.SerializerMethodField()
    is_full = serializers.SerializerMethodField()
    is_upcoming = serializers.SerializerMethodField()
    is_ongoing = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Workshop
        fields = [
            'id', 'title', 'slug', 'short_description', 'description',
            'featured_image', 'instructor_name', 'is_paid', 'price',
            'currency', 'price_display', 'start_date', 'end_date',
            'duration_hours', 'duration_display', 'max_participants',
            'registered_count', 'spots_remaining', 'is_full', 'status',
            'is_featured', 'requirements', 'what_you_learn',
            'is_upcoming', 'is_ongoing', 'is_completed', 'created_at'
        ]

    def get_price_display(self, obj):
        return obj.price_display

    def get_duration_display(self, obj):
        return obj.get_duration_display()

    def get_spots_remaining(self, obj):
        return obj.spots_remaining

    def get_is_full(self, obj):
        return obj.is_full

    def get_is_upcoming(self, obj):
        return obj.is_upcoming

    def get_is_ongoing(self, obj):
        return obj.is_ongoing

    def get_is_completed(self, obj):
        return obj.is_completed

# CRUD Serializers for comprehensive management

class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=BlogTag.objects.all(), required=False)
    
    class Meta:
        model = BlogPost
        fields = [
            'title', 'slug', 'category', 'tags', 'excerpt', 'content', 
            'featured_image', 'meta_title', 'meta_description', 'status', 
            'publish_date', 'is_featured'
        ]
        extra_kwargs = {
            'slug': {'required': False}
        }

class WorkshopCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = [
            'title', 'slug', 'description', 'short_description', 'featured_image',
            'is_paid', 'price', 'currency', 'start_date', 'end_date', 'duration_hours',
            'max_participants', 'status', 'is_featured', 'is_active', 'requirements',
            'what_you_learn', 'meta_title', 'meta_description'
        ]
        extra_kwargs = {
            'slug': {'required': False}
        }

class WorkshopApplicationSerializer(serializers.ModelSerializer):
    workshop_title = serializers.CharField(source='workshop.title', read_only=True)
    workshop_slug = serializers.CharField(source='workshop.slug', read_only=True)
    payment_required = serializers.SerializerMethodField()
    
    class Meta:
        model = WorkshopApplication
        fields = [
            'id', 'name', 'email', 'phone', 'experience_level', 'motivation',
            'status', 'payment_status', 'payment_amount', 'payment_id', 
            'payment_method', 'paid_at', 'applied_at', 'workshop_title', 
            'workshop_slug', 'payment_required'
        ]
        read_only_fields = [
            'id', 'status', 'payment_status', 'payment_amount', 'payment_id',
            'payment_method', 'paid_at', 'applied_at', 'workshop_title', 
            'workshop_slug', 'payment_required'
        ]
    
    def get_payment_required(self, obj):
        return obj.workshop.is_paid if obj.workshop else False

class PaymentSerializer(serializers.ModelSerializer):
    workshop_title = serializers.CharField(source='workshop_application.workshop.title', read_only=True)
    product_name = serializers.CharField(source='digital_product.name', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'payment_id', 'amount', 'currency', 'status', 'payment_type',
            'customer_name', 'customer_email', 'customer_phone', 'gateway_payment_id',
            'payment_method', 'created_at', 'updated_at', 'completed_at',
            'workshop_title', 'product_name'
        ]
        read_only_fields = [
            'id', 'payment_id', 'status', 'gateway_payment_id', 'payment_method',
            'created_at', 'updated_at', 'completed_at', 'workshop_title', 'product_name'
        ]

# Enhanced serializers with image handling
class AchievementCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['title', 'description', 'date', 'metrics']

class DigitalProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalProduct
        fields = ['name', 'description', 'price', 'download_link']


class TradingServiceSerializer(serializers.ModelSerializer):
    price_display = serializers.ReadOnlyField()
    booking_url = serializers.ReadOnlyField(source='get_booking_url')
    
    class Meta:
        model = TradingService
        fields = [
            'id', 'name', 'slug', 'service_type', 'description', 'detailed_description',
            'price', 'currency', 'duration', 'price_display', 'features',
            'is_active', 'is_featured', 'is_popular', 'booking_type', 'contact_info',
            'booking_url', 'display_order', 'meta_title', 'meta_description'
        ]

class TradingServiceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingService
        fields = [
            'name', 'service_type', 'description', 'detailed_description',
            'price', 'currency', 'duration', 'features', 'is_active', 'is_featured',
            'is_popular', 'booking_type', 'contact_info', 'booking_url', 'display_order',
            'meta_title', 'meta_description'
        ]

class ServiceBookingSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = ServiceBooking
        fields = [
            'id', 'service', 'service_name', 'name', 'email', 'phone', 'message',
            'preferred_contact_method', 'preferred_time', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'service_name', 'status', 'created_at']

class ServiceBookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceBooking
        fields = [
            'service', 'name', 'email', 'phone', 'message',
            'preferred_contact_method', 'preferred_time'
        ]

class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    display_name = serializers.ReadOnlyField()
    
    class Meta:
        model = UserProfile
        fields = [
            'phone', 'date_of_birth', 'bio', 'profile_picture',
            'trading_experience', 'preferred_market',
            'email_notifications', 'sms_notifications', 'full_name', 'display_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class UserDetailSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_joined', 'profile'
        ]
        read_only_fields = ['id', 'username', 'date_joined']

class PurchasedCourseSerializer(serializers.ModelSerializer):
    is_active = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    price_display = serializers.ReadOnlyField()
    
    class Meta:
        model = PurchasedCourse
        fields = [
            'id', 'course_name', 'course_type', 'description', 'purchase_date',
            'start_date', 'end_date', 'status', 'amount_paid', 'currency',
            'price_display', 'access_url', 'progress_percentage', 'last_accessed',
            'is_active', 'days_remaining', 'created_at'
        ]
        read_only_fields = ['id', 'purchase_date', 'created_at']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

class ContactMessageSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    response_time = serializers.ReadOnlyField()
    is_new = serializers.ReadOnlyField()
    is_urgent = serializers.ReadOnlyField()
    
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'subject', 'message', 'status', 'status_display',
            'priority', 'priority_display', 'admin_notes', 'assigned_to', 'assigned_to_name',
            'created_at', 'updated_at', 'read_at', 'replied_at', 'ip_address',
            'response_time', 'is_new', 'is_urgent'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'read_at', 'replied_at', 'ip_address',
            'status_display', 'priority_display', 'assigned_to_name', 'response_time',
            'is_new', 'is_urgent'
        ]

class ContactMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        
    def validate_email(self, value):
        # Basic email validation (Django already handles format)
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value.lower()
    
    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters long.")
        return value.strip()
    
    def validate_subject(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Subject must be at least 3 characters long.")
        return value.strip()
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value.strip()

class ContactMessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['status', 'priority', 'admin_notes', 'assigned_to']

# Course Serializers
class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    price_display = serializers.ReadOnlyField()
    original_price_display = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()
    duration_display = serializers.ReadOnlyField(source='get_duration_display')
    is_full = serializers.ReadOnlyField()
    spots_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'short_description', 'description',
            'featured_image', 'preview_video', 'course_type', 'difficulty_level',
            'duration_hours', 'duration_display', 'lessons_count', 'price',
            'original_price', 'currency', 'price_display', 'original_price_display',
            'discount_percentage', 'what_you_learn', 'requirements', 'course_content',
            'instructor_name', 'is_active', 'is_featured', 'max_students',
            'enrolled_count', 'is_full', 'spots_remaining', 'created_at'
        ]

class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'title', 'slug', 'short_description', 'description', 'featured_image',
            'preview_video', 'course_type', 'difficulty_level', 'duration_hours',
            'lessons_count', 'price', 'original_price', 'currency', 'what_you_learn',
            'requirements', 'course_content', 'is_active', 'is_featured',
            'max_students', 'meta_title', 'meta_description'
        ]
        extra_kwargs = {
            'slug': {'required': False}
        }

class CourseDetailSerializer(CourseSerializer):
    """Extended course serializer with additional details for course detail page"""
    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['meta_title', 'meta_description']