from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from .models import Workshop

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'workshop_type_badge', 'price_display_admin', 'start_date', 
        'status', 'participants_info', 'is_featured', 'is_active'
    ]
    list_display_links = ['title']
    list_filter = [
        'is_paid', 'status', 'is_featured', 'is_active', 
        'start_date', 'created_at', 'instructor'
    ]
    search_fields = ['title', 'description', 'short_description', 'requirements']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    list_per_page = 20
    
    fieldsets = (
        ('Workshop Information', {
            'fields': ('title', 'slug', 'instructor', 'featured_image'),
            'description': 'Basic workshop information'
        }),
        ('Content & Description', {
            'fields': ('short_description', 'description', 'requirements', 'what_you_learn'),
            'description': 'Workshop content and learning outcomes'
        }),
        ('Pricing & Type', {
            'fields': ('is_paid', 'price', 'currency'),
            'description': 'Workshop pricing information'
        }),
        ('Schedule & Capacity', {
            'fields': ('start_date', 'end_date', 'duration_hours', 'max_participants'),
            'description': 'Workshop timing and capacity'
        }),
        ('Status & Visibility', {
            'fields': ('status', 'is_featured', 'is_active'),
            'description': 'Workshop visibility and status'
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
            'description': 'Search engine optimization'
        }),
        ('Statistics', {
            'fields': ('registered_count', 'created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Workshop statistics and timestamps'
        }),
    )
    
    readonly_fields = ['registered_count', 'created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new workshop
            obj.instructor = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(instructor=request.user)
    
    def workshop_type_badge(self, obj):
        if obj.is_paid:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">💰 PAID</span>'
            )
        else:
            return format_html(
                '<span style="background: #17a2b8; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">🆓 FREE</span>'
            )
    workshop_type_badge.short_description = 'Type'
    
    def price_display_admin(self, obj):
        if obj.is_paid and obj.price:
            return format_html(
                '<strong style="color: #28a745;">{} {:,.0f}</strong>',
                obj.currency, obj.price
            )
        return format_html('<span style="color: #17a2b8; font-weight: bold;">Free</span>')
    price_display_admin.short_description = 'Price'
    
    def participants_info(self, obj):
        percentage = (obj.registered_count / obj.max_participants) * 100 if obj.max_participants > 0 else 0
        color = '#dc3545' if percentage >= 90 else '#ffc107' if percentage >= 70 else '#28a745'
        
        return format_html(
            '<div style="display: flex; align-items: center; gap: 5px;">'
            '<span style="font-weight: bold;">{}/{}</span>'
            '<div style="width: 50px; height: 8px; background: #e9ecef; border-radius: 4px; overflow: hidden;">'
            '<div style="width: {}%; height: 100%; background: {}; transition: width 0.3s;"></div>'
            '</div>'
            '</div>',
            obj.registered_count, obj.max_participants, percentage, color
        )
    participants_info.short_description = 'Participants'
    
    actions = [
        'make_featured', 'remove_featured', 'activate_workshops', 'deactivate_workshops',
        'mark_as_upcoming', 'mark_as_completed'
    ]
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} workshops were marked as featured.', messages.SUCCESS)
    make_featured.short_description = "⭐ Mark as featured"
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} workshops were removed from featured.', messages.SUCCESS)
    remove_featured.short_description = "❌ Remove from featured"
    
    def activate_workshops(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} workshops were activated.', messages.SUCCESS)
    activate_workshops.short_description = "✅ Activate workshops"
    
    def deactivate_workshops(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} workshops were deactivated.', messages.WARNING)
    deactivate_workshops.short_description = "🚫 Deactivate workshops"
    
    def mark_as_upcoming(self, request, queryset):
        updated = queryset.update(status='upcoming')
        self.message_user(request, f'{updated} workshops were marked as upcoming.', messages.INFO)
    mark_as_upcoming.short_description = "🕐 Mark as upcoming"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} workshops were marked as completed.', messages.SUCCESS)
    mark_as_completed.short_description = "✅ Mark as completed"
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)