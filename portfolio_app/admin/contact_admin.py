"""
Contact message admin configurations
Following SRP and Clean Code principles
"""
from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django.utils import timezone
from ..models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Clean contact message admin with self-documenting methods"""
    list_display = [
        'name', 'email', 'subject', 'status_badge', 'priority_badge',
        'created_at', 'quick_actions'
    ]
    list_display_links = ['name']
    list_filter = [
        'status', 'priority', 'created_at', 'read_at', 'replied_at'
    ]
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject', 'message'),
        }),
        ('Classification', {
            'fields': ('status', 'priority', 'assigned_to'),
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'read_at', 'replied_at'),
            'classes': ('collapse',),
        }),
        ('Technical Info', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'read_at', 'replied_at', 'ip_address', 'user_agent']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('assigned_to')
    
    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'new': '#007bff',
            'read': '#6c757d',
            'replied': '#28a745',
            'resolved': '#20c997',
            'archived': '#6f42c1'
        }
        color = colors.get(obj.status, '#6c757d')
        
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def priority_badge(self, obj):
        """Display priority with colored badge"""
        colors = {
            'low': '#28a745',
            'normal': '#6c757d',
            'high': '#fd7e14',
            'urgent': '#dc3545'
        }
        color = colors.get(obj.priority, '#6c757d')
        
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.get_priority_display().upper()
        )
    priority_badge.short_description = 'Priority'
    
    def quick_actions(self, obj):
        """Display quick action links"""
        actions = []
        
        if obj.status == 'new':
            actions.append(
                f'<a href="mailto:{obj.email}?subject=Re: {obj.subject}" '
                f'style="color: #007bff; text-decoration: none; margin-right: 10px;">📧 Reply</a>'
            )
        
        actions.append(
            f'<a href="/admin/portfolio_app/contactmessage/{obj.id}/change/" '
            f'style="color: #28a745; text-decoration: none;">✏️ Edit</a>'
        )
        
        return format_html(' | '.join(actions))
    quick_actions.short_description = 'Actions'
    
    def save_model(self, request, obj, form, change):
        """Auto-mark as read when admin opens the message"""
        if obj.status == 'new' and change:
            obj.mark_as_read(request.user)
        super().save_model(request, obj, form, change)
    
    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_resolved', 'set_high_priority']
    
    def mark_as_read(self, request, queryset):
        """Mark messages as read"""
        updated = 0
        for message in queryset.filter(status='new'):
            message.mark_as_read(request.user)
            updated += 1
        self.message_user(request, f'{updated} messages marked as read.', messages.SUCCESS)
    mark_as_read.short_description = "👁️ Mark as read"
    
    def mark_as_replied(self, request, queryset):
        """Mark messages as replied"""
        updated = 0
        for message in queryset:
            message.mark_as_replied()
            updated += 1
        self.message_user(request, f'{updated} messages marked as replied.', messages.SUCCESS)
    mark_as_replied.short_description = "📧 Mark as replied"
    
    def mark_as_resolved(self, request, queryset):
        """Mark messages as resolved"""
        updated = queryset.update(status='resolved')
        self.message_user(request, f'{updated} messages marked as resolved.', messages.SUCCESS)
    mark_as_resolved.short_description = "✅ Mark as resolved"
    
    def set_high_priority(self, request, queryset):
        """Set messages to high priority"""
        updated = queryset.update(priority='high')
        self.message_user(request, f'{updated} messages set to high priority.', messages.INFO)
    set_high_priority.short_description = "🔥 Set high priority"