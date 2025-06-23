from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Achievement, DigitalProduct, Subscriber, Newsletter, BlogPost, 
    BlogCategory, BlogTag, Workshop, WorkshopApplication, Payment
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

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['email', 'name']
        
    def validate_email(self, value):
        if Subscriber.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("This email is already subscribed.")
        return value

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['id', 'subject', 'content_html', 'created_at', 'is_sent', 'sent_to_count']
        read_only_fields = ['created_at', 'is_sent', 'sent_to_count']

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

class NewsletterCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['subject', 'content_html', 'content_text']

class SubscriberCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['email', 'name', 'is_active']
        
    def validate_email(self, value):
        # Allow updating existing subscriber
        if self.instance and self.instance.email == value:
            return value
        if Subscriber.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("This email is already subscribed.")
        return value