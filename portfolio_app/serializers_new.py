from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Achievement, DigitalProduct, Subscriber, Newsletter, BlogPost, BlogCategory, BlogTag, Workshop

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