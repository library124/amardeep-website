"""
Blog-related admin configurations
Following SRP and Clean Code principles
"""
from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from ..models import BlogCategory, BlogTag, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    """Clean admin for blog categories with self-documenting methods"""
    list_display = ['name', 'slug', 'post_count', 'created_at']
    list_display_links = ['name']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    list_per_page = 20
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def post_count(self, obj):
        """Display published post count with link"""
        count = obj.posts.filter(status='published').count()
        if count > 0:
            return format_html(
                '<a href="/admin/portfolio_app/blogpost/?category__id__exact={}">{} posts</a>',
                obj.id, count
            )
        return '0 posts'
    post_count.short_description = 'Published Posts'


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    """Clean admin for blog tags"""
    list_display = ['name', 'slug', 'post_count', 'created_at']
    list_display_links = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    list_per_page = 30
    
    def post_count(self, obj):
        """Display published post count with link"""
        count = obj.posts.filter(status='published').count()
        if count > 0:
            return format_html(
                '<a href="/admin/portfolio_app/blogpost/?tags__id__exact={}">{} posts</a>',
                obj.id, count
            )
        return '0 posts'
    post_count.short_description = 'Published Posts'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Comprehensive blog post admin with clean organization"""
    list_display = [
        'title', 'author', 'category', 'status', 'is_featured', 
        'publish_date', 'views_count'
    ]
    list_display_links = ['title']
    list_filter = [
        'status', 'is_featured', 'category', 'tags', 
        'publish_date', 'created_at', 'author'
    ]
    search_fields = ['title', 'excerpt', 'content', 'meta_title']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'publish_date'
    list_per_page = 25
    list_editable = ['is_featured']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'tags'),
            'description': 'Basic post information and categorization'
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image'),
            'description': 'Main content and featured image'
        }),
        ('SEO Optimization', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
            'description': 'Search engine optimization fields'
        }),
        ('Publishing Options', {
            'fields': ('status', 'publish_date', 'is_featured'),
            'description': 'Control when and how the post is published'
        }),
        ('Statistics', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Post statistics and timestamps'
        }),
    )
    
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        """Auto-assign author for new posts"""
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Filter posts by author for non-superusers"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    
    actions = ['make_published', 'make_draft', 'make_featured', 'remove_featured']
    
    def make_published(self, request, queryset):
        """Bulk action to publish posts"""
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} posts published successfully.')
    make_published.short_description = "✅ Publish selected posts"
    
    def make_draft(self, request, queryset):
        """Bulk action to move posts to draft"""
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} posts moved to draft.')
    make_draft.short_description = "📝 Move to draft"
    
    def make_featured(self, request, queryset):
        """Bulk action to feature posts"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} posts marked as featured.')
    make_featured.short_description = "⭐ Mark as featured"
    
    def remove_featured(self, request, queryset):
        """Bulk action to unfeature posts"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} posts removed from featured.')
    remove_featured.short_description = "❌ Remove from featured"