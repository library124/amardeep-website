from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Achievement, DigitalProduct, Subscriber, Newsletter, BlogPost, BlogCategory, BlogTag

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
