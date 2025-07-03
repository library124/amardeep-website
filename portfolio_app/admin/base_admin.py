"""
Base admin configurations for core models
Following KISS and SRP principles
"""
from django.contrib import admin
from django.utils.html import format_html
from ..models import Achievement, DigitalProduct


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """Clean, simple admin for Achievement model"""
    list_display = ['title', 'date', 'user']
    list_filter = ['date', 'user']
    search_fields = ['title', 'description']
    
    class Meta:
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"


@admin.register(DigitalProduct)
class DigitalProductAdmin(admin.ModelAdmin):
    """Clean, simple admin for DigitalProduct model"""
    list_display = ['name', 'price_display']
    search_fields = ['name', 'description']
    
    def price_display(self, obj):
        """Self-documenting method for price display"""
        return format_html(
            '<strong style="color: #28a745;">₹{:,.0f}</strong>',
            obj.price
        )
    price_display.short_description = 'Price'
    
    class Meta:
        verbose_name = "Digital Product"
        verbose_name_plural = "Digital Products"