"""
Trading service related admin configurations
Following SRP and Clean Code principles
"""
from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django.utils import timezone
from ..models import TradingService, ServiceBooking


@admin.register(TradingService)
class TradingServiceAdmin(admin.ModelAdmin):
    """Clean trading service admin with self-documenting methods"""
    list_display = [
        'name', 'service_type', 'price_display', 'duration', 
        'is_active', 'is_featured', 'is_popular', 'display_order'
    ]
    list_display_links = ['name']
    list_filter = [
        'service_type', 'duration', 'is_active', 'is_featured', 
        'is_popular', 'booking_type', 'created_at'
    ]
    search_fields = ['name', 'description', 'detailed_description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'is_featured', 'is_popular', 'display_order']
    list_per_page = 20
    
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'slug', 'service_type', 'description', 'detailed_description'),
        }),
        ('Pricing', {
            'fields': ('price', 'currency', 'duration'),
        }),
        ('Features', {
            'fields': ('features',),
            'description': 'Service features in JSON format: ["Feature 1", "Feature 2"]'
        }),
        ('Visibility & Status', {
            'fields': ('is_active', 'is_featured', 'is_popular', 'display_order'),
        }),
        ('Booking Configuration', {
            'fields': ('booking_type', 'contact_info', 'booking_url'),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def price_display(self, obj):
        """Display formatted price with currency"""
        return format_html(
            '<strong style="color: #28a745;">{}</strong>',
            obj.price_display
        )
    price_display.short_description = 'Price'
    
    actions = [
        'make_featured', 'remove_featured', 'make_popular', 'remove_popular',
        'activate_services', 'deactivate_services'
    ]
    
    def make_featured(self, request, queryset):
        """Mark services as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} services marked as featured.', messages.SUCCESS)
    make_featured.short_description = "⭐ Mark as featured"
    
    def remove_featured(self, request, queryset):
        """Remove featured status"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} services removed from featured.', messages.SUCCESS)
    remove_featured.short_description = "❌ Remove from featured"
    
    def make_popular(self, request, queryset):
        """Mark services as popular"""
        updated = queryset.update(is_popular=True)
        self.message_user(request, f'{updated} services marked as popular.', messages.SUCCESS)
    make_popular.short_description = "🔥 Mark as popular"
    
    def remove_popular(self, request, queryset):
        """Remove popular status"""
        updated = queryset.update(is_popular=False)
        self.message_user(request, f'{updated} services removed from popular.', messages.SUCCESS)
    remove_popular.short_description = "❌ Remove from popular"
    
    def activate_services(self, request, queryset):
        """Activate services"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} services activated.', messages.SUCCESS)
    activate_services.short_description = "✅ Activate services"
    
    def deactivate_services(self, request, queryset):
        """Deactivate services"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} services deactivated.', messages.WARNING)
    deactivate_services.short_description = "🚫 Deactivate services"


@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    """Clean service booking admin"""
    list_display = [
        'name', 'email', 'service_name', 'preferred_contact_method', 
        'status_badge', 'created_at'
    ]
    list_display_links = ['name']
    list_filter = [
        'status', 'preferred_contact_method', 'created_at', 
        'service__name', 'service__service_type'
    ]
    search_fields = ['name', 'email', 'phone', 'service__name', 'message']
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'email', 'phone', 'preferred_contact_method', 'preferred_time'),
        }),
        ('Service & Request', {
            'fields': ('service', 'message'),
        }),
        ('Status & Management', {
            'fields': ('status', 'admin_notes', 'contacted_at'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('service')
    
    def service_name(self, obj):
        """Display service name"""
        return obj.service.name
    service_name.short_description = 'Service'
    service_name.admin_order_field = 'service__name'
    
    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'pending': '#ffc107',
            'contacted': '#17a2b8',
            'confirmed': '#28a745',
            'completed': '#6f42c1',
            'cancelled': '#dc3545'
        }
        icons = {
            'pending': '⏳',
            'contacted': '📞',
            'confirmed': '✅',
            'completed': '🎉',
            'cancelled': '❌'
        }
        color = colors.get(obj.status, '#6c757d')
        icon = icons.get(obj.status, '❓')
        
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{} {}</span>',
            color, icon, obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    actions = ['mark_contacted', 'mark_confirmed', 'mark_completed']
    
    def mark_contacted(self, request, queryset):
        """Mark bookings as contacted"""
        updated = queryset.update(status='contacted', contacted_at=timezone.now())
        self.message_user(request, f'{updated} bookings marked as contacted.', messages.SUCCESS)
    mark_contacted.short_description = "📞 Mark as contacted"
    
    def mark_confirmed(self, request, queryset):
        """Mark bookings as confirmed"""
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} bookings confirmed.', messages.SUCCESS)
    mark_confirmed.short_description = "✅ Mark as confirmed"
    
    def mark_completed(self, request, queryset):
        """Mark bookings as completed"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} bookings completed.', messages.SUCCESS)
    mark_completed.short_description = "🎉 Mark as completed"