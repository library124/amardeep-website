"""
Workshop-related admin configurations
Following SRP and Clean Code principles
"""
from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta
from ..models import Workshop, WorkshopApplication


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    """Clean workshop admin with self-documenting methods"""
    list_display = [
        'title', 'workshop_type_badge', 'price_display', 'start_date', 
        'status_badge', 'participants_info', 'is_featured', 'is_active'
    ]
    list_display_links = ['title']
    list_filter = [
        'is_paid', 'status', 'is_featured', 'is_active', 
        'start_date', 'created_at', 'instructor'
    ]
    search_fields = ['title', 'description', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    list_per_page = 20
    
    fieldsets = (
        ('Workshop Information', {
            'fields': ('title', 'slug', 'instructor', 'featured_image'),
        }),
        ('Content & Description', {
            'fields': ('short_description', 'description', 'requirements', 'what_you_learn'),
        }),
        ('Pricing & Type', {
            'fields': ('is_paid', 'price', 'currency'),
        }),
        ('Schedule & Capacity', {
            'fields': ('start_date', 'end_date', 'duration_hours', 'max_participants'),
        }),
        ('Status & Visibility', {
            'fields': ('status', 'is_featured', 'is_active'),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ['registered_count', 'created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        """Auto-assign instructor for new workshops"""
        if not change:
            obj.instructor = request.user
            if obj.is_active is None:
                obj.is_active = True
        super().save_model(request, obj, form, change)
    
    def workshop_type_badge(self, obj):
        """Display workshop type with colored badge"""
        if obj.is_paid:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 3px 8px; '
                'border-radius: 12px; font-size: 11px; font-weight: bold;">💰 PAID</span>'
            )
        return format_html(
            '<span style="background: #17a2b8; color: white; padding: 3px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">🆓 FREE</span>'
        )
    workshop_type_badge.short_description = 'Type'
    
    def price_display(self, obj):
        """Display formatted price"""
        if obj.is_paid and obj.price:
            return format_html(
                '<strong style="color: #28a745;">{} {:,.0f}</strong>',
                obj.currency, obj.price
            )
        return format_html('<span style="color: #17a2b8; font-weight: bold;">Free</span>')
    price_display.short_description = 'Price'
    
    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'upcoming': '#007bff',
            'ongoing': '#28a745',
            'completed': '#6c757d',
            'cancelled': '#dc3545'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def participants_info(self, obj):
        """Display participant count with progress bar"""
        if obj.max_participants == 0:
            return "No limit"
        
        percentage = (obj.registered_count / obj.max_participants) * 100
        color = '#dc3545' if percentage >= 90 else '#ffc107' if percentage >= 70 else '#28a745'
        
        return format_html(
            '<div style="display: flex; align-items: center; gap: 5px;">'
            '<span style="font-weight: bold;">{}/{}</span>'
            '<div style="width: 50px; height: 8px; background: #e9ecef; border-radius: 4px; overflow: hidden;">'
            '<div style="width: {}%; height: 100%; background: {};"></div>'
            '</div>'
            '</div>',
            obj.registered_count, obj.max_participants, percentage, color
        )
    participants_info.short_description = 'Participants'
    
    actions = [
        'make_featured', 'remove_featured', 'activate_workshops', 
        'deactivate_workshops', 'update_dates_to_future'
    ]
    
    def make_featured(self, request, queryset):
        """Mark workshops as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} workshops marked as featured.', messages.SUCCESS)
    make_featured.short_description = "⭐ Mark as featured"
    
    def remove_featured(self, request, queryset):
        """Remove featured status"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} workshops removed from featured.', messages.SUCCESS)
    remove_featured.short_description = "❌ Remove from featured"
    
    def activate_workshops(self, request, queryset):
        """Activate workshops"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} workshops activated.', messages.SUCCESS)
    activate_workshops.short_description = "✅ Activate workshops"
    
    def deactivate_workshops(self, request, queryset):
        """Deactivate workshops"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} workshops deactivated.', messages.WARNING)
    deactivate_workshops.short_description = "🚫 Deactivate workshops"
    
    def update_dates_to_future(self, request, queryset):
        """Update workshop dates to future for visibility"""
        updated = 0
        for workshop in queryset:
            workshop.start_date = timezone.now() + timedelta(days=7)
            workshop.end_date = workshop.start_date + timedelta(hours=workshop.duration_hours)
            workshop.save()
            updated += 1
        
        self.message_user(request, f'{updated} workshops updated to future dates.', messages.SUCCESS)
    update_dates_to_future.short_description = "📅 Update dates to future"


@admin.register(WorkshopApplication)
class WorkshopApplicationAdmin(admin.ModelAdmin):
    """Clean workshop application admin"""
    list_display = [
        'name', 'email', 'workshop_title', 'experience_level', 
        'status_badge', 'applied_at'
    ]
    list_display_links = ['name']
    list_filter = [
        'status', 'experience_level', 'applied_at', 
        'workshop__title', 'workshop__start_date'
    ]
    search_fields = ['name', 'email', 'workshop__title', 'motivation']
    date_hierarchy = 'applied_at'
    list_per_page = 25
    
    fieldsets = (
        ('Applicant Information', {
            'fields': ('name', 'email', 'phone', 'experience_level'),
        }),
        ('Workshop & Application', {
            'fields': ('workshop', 'motivation', 'status'),
        }),
        ('Admin Notes', {
            'fields': ('notes', 'applied_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ['applied_at', 'updated_at']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('workshop')
    
    def workshop_title(self, obj):
        """Display workshop title"""
        return obj.workshop.title
    workshop_title.short_description = 'Workshop'
    workshop_title.admin_order_field = 'workshop__title'
    
    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'pending': '#ffc107',
            'approved': '#28a745',
            'rejected': '#dc3545',
            'waitlist': '#17a2b8'
        }
        icons = {
            'pending': '⏳',
            'approved': '✅',
            'rejected': '❌',
            'waitlist': '⏰'
        }
        color = colors.get(obj.status, '#6c757d')
        icon = icons.get(obj.status, '❓')
        
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{} {}</span>',
            color, icon, obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    actions = ['approve_applications', 'reject_applications', 'move_to_waitlist']
    
    def approve_applications(self, request, queryset):
        """Approve pending applications"""
        updated = 0
        for application in queryset.filter(status='pending'):
            if not application.workshop.is_full:
                application.status = 'approved'
                application.workshop.registered_count += 1
                application.workshop.save(update_fields=['registered_count'])
                application.save(update_fields=['status'])
                updated += 1
            else:
                application.status = 'waitlist'
                application.save(update_fields=['status'])
        
        self.message_user(request, f'{updated} applications approved.', messages.SUCCESS)
    approve_applications.short_description = "✅ Approve applications"
    
    def reject_applications(self, request, queryset):
        """Reject applications"""
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} applications rejected.', messages.WARNING)
    reject_applications.short_description = "❌ Reject applications"
    
    def move_to_waitlist(self, request, queryset):
        """Move applications to waitlist"""
        updated = queryset.update(status='waitlist')
        self.message_user(request, f'{updated} applications moved to waitlist.', messages.INFO)
    move_to_waitlist.short_description = "⏰ Move to waitlist"