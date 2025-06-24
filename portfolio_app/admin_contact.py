from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.contrib import messages
from .models import ContactMessage
from .services.brevo_service import brevo_service

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'subject', 'status_badge', 'priority_badge', 
        'assigned_to', 'created_at', 'actions_column'
    ]
    list_display_links = ['name', 'subject']
    list_filter = [
        'status', 'priority', 'assigned_to', 'created_at', 'read_at', 'replied_at'
    ]
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject', 'message'),
            'description': 'Message details from the contact form'
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'assigned_to'),
            'description': 'Message classification and assignment'
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',),
            'description': 'Internal notes for tracking'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'read_at', 'replied_at'),
            'classes': ('collapse',),
            'description': 'Message timeline'
        }),
        ('Technical Details', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',),
            'description': 'Technical information about the sender'
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'read_at', 'replied_at', 'ip_address', 'user_agent']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('assigned_to')
    
    def status_badge(self, obj):
        colors = {
            'new': '#007bff',
            'read': '#6c757d',
            'replied': '#28a745',
            'resolved': '#20c997',
            'archived': '#6f42c1'
        }
        icons = {
            'new': '🆕',
            'read': '👁️',
            'replied': '✅',
            'resolved': '🎯',
            'archived': '📁'
        }
        color = colors.get(obj.status, '#6c757d')
        icon = icons.get(obj.status, '❓')
        
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">'
            '{} {}</span>',
            color, icon, obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def priority_badge(self, obj):
        colors = {
            'low': '#28a745',
            'normal': '#6c757d',
            'high': '#fd7e14',
            'urgent': '#dc3545'
        }
        icons = {
            'low': '🟢',
            'normal': '⚪',
            'high': '🟠',
            'urgent': '🔴'
        }
        color = colors.get(obj.priority, '#6c757d')
        icon = icons.get(obj.priority, '⚪')
        
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">'
            '{} {}</span>',
            color, icon, obj.get_priority_display().upper()
        )
    priority_badge.short_description = 'Priority'
    
    def actions_column(self, obj):
        actions = []
        
        if obj.status == 'new':
            actions.append(
                f'<a href="#" onclick="updateContactStatus({obj.id}, \'read\')" '
                f'style="color: #6c757d; text-decoration: none; margin-right: 10px;">👁️ Mark Read</a>'
            )
        
        if obj.status in ['new', 'read']:
            actions.append(
                f'<a href="#" onclick="updateContactStatus({obj.id}, \'replied\')" '
                f'style="color: #28a745; text-decoration: none; margin-right: 10px;">✅ Mark Replied</a>'
            )
        
        actions.append(
            f'<a href="mailto:{obj.email}?subject=Re: {obj.subject}" '
            f'style="color: #007bff; text-decoration: none; margin-right: 10px;">📧 Reply</a>'
        )
        
        if obj.priority in ['low', 'normal']:
            actions.append(
                f'<a href="#" onclick="updateContactPriority({obj.id}, \'high\')" '
                f'style="color: #fd7e14; text-decoration: none;">🔥 High Priority</a>'
            )
        
        return format_html(' | '.join(actions))
    actions_column.short_description = 'Quick Actions'
    
    actions = [
        'mark_as_read', 'mark_as_replied', 'mark_as_resolved', 'mark_as_archived',
        'set_high_priority', 'set_normal_priority', 'assign_to_me', 'send_reply_emails',
        'export_messages'
    ]
    
    def mark_as_read(self, request, queryset):
        updated = 0
        for message in queryset.filter(status='new'):
            message.mark_as_read(request.user)
            updated += 1
        self.message_user(request, f'{updated} messages marked as read.', messages.SUCCESS)
    mark_as_read.short_description = "👁️ Mark as read"
    
    def mark_as_replied(self, request, queryset):
        updated = 0
        for message in queryset.filter(status__in=['new', 'read']):
            message.mark_as_replied()
            updated += 1
        self.message_user(request, f'{updated} messages marked as replied.', messages.SUCCESS)
    mark_as_replied.short_description = "✅ Mark as replied"
    
    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(status='resolved')
        self.message_user(request, f'{updated} messages marked as resolved.', messages.SUCCESS)
    mark_as_resolved.short_description = "🎯 Mark as resolved"
    
    def mark_as_archived(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} messages archived.', messages.INFO)
    mark_as_archived.short_description = "📁 Archive messages"
    
    def set_high_priority(self, request, queryset):
        updated = queryset.update(priority='high')
        self.message_user(request, f'{updated} messages set to high priority.', messages.WARNING)
    set_high_priority.short_description = "🔥 Set high priority"
    
    def set_normal_priority(self, request, queryset):
        updated = queryset.update(priority='normal')
        self.message_user(request, f'{updated} messages set to normal priority.', messages.INFO)
    set_normal_priority.short_description = "⚪ Set normal priority"
    
    def assign_to_me(self, request, queryset):
        updated = queryset.update(assigned_to=request.user)
        self.message_user(request, f'{updated} messages assigned to you.', messages.SUCCESS)
    assign_to_me.short_description = "👤 Assign to me"
    
    def send_reply_emails(self, request, queryset):
        # This would integrate with your email system
        replied_count = queryset.filter(status='replied').count()
        self.message_user(
            request, 
            f'Email functionality ready. Would send acknowledgment emails to {replied_count} replied messages.',
            messages.INFO
        )
    send_reply_emails.short_description = "📧 Send acknowledgment emails"
    
    def export_messages(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contact_messages.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Name', 'Email', 'Subject', 'Message', 'Status', 'Priority', 
            'Assigned To', 'Created Date', 'Read Date', 'Replied Date'
        ])
        
        for message in queryset:
            writer.writerow([
                message.name, message.email, message.subject, message.message,
                message.get_status_display(), message.get_priority_display(),
                message.assigned_to.get_full_name() if message.assigned_to else '',
                message.created_at.strftime('%Y-%m-%d %H:%M'),
                message.read_at.strftime('%Y-%m-%d %H:%M') if message.read_at else '',
                message.replied_at.strftime('%Y-%m-%d %H:%M') if message.replied_at else ''
            ])
        
        return response
    export_messages.short_description = "📊 Export to CSV"
    
    def save_model(self, request, obj, form, change):
        # Auto-assign to current user if not assigned
        if not obj.assigned_to and obj.status != 'new':
            obj.assigned_to = request.user
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': ('admin/css/contact_admin.css',)
        }
        js = ('admin/js/contact_admin.js',)