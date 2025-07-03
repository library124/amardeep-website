"""
Main admin configuration file
Following Clean Code principles and modular architecture
"""
from django.contrib import admin

# Import all modular admin configurations
# This follows the SRP (Single Responsibility Principle) and SoC (Separation of Concerns)
from .admin.base_admin import *
from .admin.blog_admin import *
from .admin.workshop_admin import *
from .admin.trading_admin import *
from .admin.payment_admin import *
from .admin.contact_admin import *
from .admin.user_admin import *

# Customize admin site header and titles
# Following the principle of self-documenting code
admin.site.site_header = "Amardeep Asode Trading Portfolio Admin"
admin.site.site_title = "Trading Portfolio Admin"
admin.site.index_title = "Welcome to Trading Portfolio Administration"

# Note: Newsletter functionality has been completely removed
# This admin interface now focuses on core business functionality:
# - Achievements and Digital Products
# - Blog management
# - Workshop management
# - Trading services
# - Payment processing
# - Contact message handling