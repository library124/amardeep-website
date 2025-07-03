"""
User-related admin configurations
Following SRP and Clean Code principles
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from ..models import UserProfile, PurchasedCourse


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('phone', 'date_of_birth', 'bio', 'profile_picture')
        }),
        ('Trading Preferences', {
            'fields': ('trading_experience', 'preferred_market')
        }),
        ('Notifications', {
            'fields': ('email_notifications', 'sms_notifications')
        }),
    )


class CustomUserAdmin(BaseUserAdmin):
    """Extended User admin with profile inline"""
    inlines = (UserProfileInline,)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Clean admin for UserProfile model"""
    list_display = [
        'user_display', 'phone', 'trading_experience', 'preferred_market',
        'email_notifications', 'sms_notifications', 'created_at'
    ]
    list_display_links = ['user_display']
    list_filter = [
        'trading_experience', 'preferred_market', 'email_notifications',
        'sms_notifications', 'created_at'
    ]
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone']
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('phone', 'date_of_birth', 'bio', 'profile_picture')
        }),
        ('Trading Preferences', {
            'fields': ('trading_experience', 'preferred_market')
        }),
        ('Notification Settings', {
            'fields': ('email_notifications', 'sms_notifications')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('user')
    
    def user_display(self, obj):
        """Display user with full name and email"""
        full_name = obj.user.get_full_name()
        if full_name:
            return format_html(
                '<strong>{}</strong><br><small>{}</small>',
                full_name, obj.user.email
            )
        return format_html(
            '<strong>{}</strong><br><small>{}</small>',
            obj.user.username, obj.user.email
        )
    user_display.short_description = 'User'


@admin.register(PurchasedCourse)
class PurchasedCourseAdmin(admin.ModelAdmin):
    """Clean admin for PurchasedCourse model"""
    list_display = [
        'user_display', 'course_name', 'course_type', 'status_badge',
        'progress_display', 'purchase_date', 'amount_display'
    ]
    list_display_links = ['course_name']
    list_filter = [
        'course_type', 'status', 'purchase_date', 'start_date', 'end_date'
    ]
    search_fields = [
        'user__username', 'user__email', 'course_name', 'description'
    ]
    date_hierarchy = 'purchase_date'
    list_per_page = 25
    
    fieldsets = (
        ('Course Information', {
            'fields': ('user', 'course_name', 'course_type', 'description')
        }),
        ('Purchase Details', {
            'fields': ('purchase_date', 'start_date', 'end_date', 'status')
        }),
        ('Pricing', {
            'fields': ('amount_paid', 'currency')
        }),
        ('Access Details', {
            'fields': ('access_url', 'access_credentials')
        }),
        ('Progress Tracking', {
            'fields': ('progress_percentage', 'last_accessed')
        }),
        ('Related Objects', {
            'fields': ('workshop_application', 'trading_service'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['purchase_date', 'created_at', 'updated_at']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related(
            'user', 'workshop_application', 'trading_service'
        )
    
    def user_display(self, obj):
        """Display user information"""
        return format_html(
            '<strong>{}</strong><br><small>{}</small>',
            obj.user.get_full_name() or obj.user.username,
            obj.user.email
        )
    user_display.short_description = 'User'
    
    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'active': '#28a745',
            'completed': '#17a2b8',
            'expired': '#ffc107',
            'cancelled': '#dc3545'
        }
        color = colors.get(obj.status, '#6c757d')
        
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def progress_display(self, obj):
        """Display progress with progress bar"""
        color = '#28a745' if obj.progress_percentage >= 80 else '#ffc107' if obj.progress_percentage >= 50 else '#dc3545'
        
        return format_html(
            '<div style="display: flex; align-items: center; gap: 5px;">'
            '<span style="font-weight: bold;">{}%</span>'
            '<div style="width: 60px; height: 8px; background: #e9ecef; border-radius: 4px; overflow: hidden;">'
            '<div style="width: {}%; height: 100%; background: {};"></div>'
            '</div>'
            '</div>',
            obj.progress_percentage, obj.progress_percentage, color
        )
    progress_display.short_description = 'Progress'
    
    def amount_display(self, obj):
        """Display formatted amount"""
        return format_html(
            '<strong style="color: #28a745;">{}</strong>',
            obj.price_display
        )
    amount_display.short_description = 'Amount'
    
    actions = ['mark_as_active', 'mark_as_completed', 'update_progress']
    
    def mark_as_active(self, request, queryset):
        """Mark courses as active"""
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} courses marked as active.')
    mark_as_active.short_description = "✅ Mark as active"
    
    def mark_as_completed(self, request, queryset):
        """Mark courses as completed"""
        updated = queryset.update(status='completed', progress_percentage=100)
        self.message_user(request, f'{updated} courses marked as completed.')
    mark_as_completed.short_description = "🎉 Mark as completed"
    
    def update_progress(self, request, queryset):
        """Update last accessed time"""
        from django.utils import timezone
        updated = queryset.update(last_accessed=timezone.now())
        self.message_user(request, f'{updated} courses updated with current access time.')
    update_progress.short_description = "🕐 Update access time"