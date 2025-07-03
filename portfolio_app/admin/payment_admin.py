"""
Payment related admin configurations
Following SRP and Clean Code principles
"""
from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from ..models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Clean payment admin with self-documenting methods"""
    list_display = [
        'payment_id', 'customer_name', 'customer_email', 'amount_display', 
        'payment_type', 'status_badge', 'payment_method', 'created_at'
    ]
    list_display_links = ['payment_id']
    list_filter = [
        'status', 'payment_type', 'payment_method', 'created_at', 'completed_at'
    ]
    search_fields = [
        'payment_id', 'customer_name', 'customer_email', 'gateway_payment_id'
    ]
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_id', 'amount', 'currency', 'payment_type', 'status'),
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone'),
        }),
        ('Gateway Information', {
            'fields': ('gateway_payment_id', 'payment_method', 'gateway_response'),
        }),
        ('Related Objects', {
            'fields': ('workshop_application', 'digital_product'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ['payment_id', 'created_at', 'updated_at', 'completed_at']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related(
            'workshop_application__workshop', 'digital_product'
        )
    
    def amount_display(self, obj):
        """Display formatted amount with currency"""
        return format_html(
            '<strong style="color: #28a745;">{} {:,.2f}</strong>',
            obj.currency, obj.amount
        )
    amount_display.short_description = 'Amount'
    
    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'pending': '#ffc107',
            'completed': '#28a745',
            'failed': '#dc3545',
            'cancelled': '#6c757d',
            'refunded': '#17a2b8'
        }
        icons = {
            'pending': '⏳',
            'completed': '✅',
            'failed': '❌',
            'cancelled': '🚫',
            'refunded': '↩️'
        }
        color = colors.get(obj.status, '#6c757d')
        icon = icons.get(obj.status, '❓')
        
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{} {}</span>',
            color, icon, obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    actions = ['mark_completed', 'mark_failed']
    
    def mark_completed(self, request, queryset):
        """Mark payments as completed"""
        updated = 0
        for payment in queryset.filter(status='pending'):
            payment.mark_completed(
                gateway_payment_id=f"ADMIN_{payment.payment_id}",
                payment_method="admin_manual"
            )
            updated += 1
        
        self.message_user(request, f'{updated} payments marked as completed.', messages.SUCCESS)
    mark_completed.short_description = "✅ Mark as completed"
    
    def mark_failed(self, request, queryset):
        """Mark payments as failed"""
        updated = queryset.filter(status='pending').update(status='failed')
        self.message_user(request, f'{updated} payments marked as failed.', messages.WARNING)
    mark_failed.short_description = "❌ Mark as failed"