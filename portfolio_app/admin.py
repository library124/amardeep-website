from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils.html import format_html
from django.utils import timezone
from .models import Achievement, DigitalProduct, Subscriber, Newsletter, BlogPost, BlogCategory, BlogTag, Workshop, WorkshopApplication

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'user']
    list_filter = ['date', 'user']
    search_fields = ['title', 'description']

@admin.register(DigitalProduct)
class DigitalProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name', 'description']

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_confirmed', 'is_active', 'subscribed_at']
    list_filter = ['is_confirmed', 'is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    readonly_fields = ['confirmation_token', 'subscribed_at', 'confirmed_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-subscribed_at')

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['subject', 'is_sent', 'sent_to_count', 'created_at', 'sent_at']
    list_filter = ['is_sent', 'created_at']
    search_fields = ['subject']
    readonly_fields = ['created_at', 'sent_at', 'is_sent', 'sent_to_count']
    
    fieldsets = (
        ('Newsletter Content', {
            'fields': ('subject', 'content_html', 'content_text')
        }),
        ('Status', {
            'fields': ('is_sent', 'sent_to_count', 'created_at', 'sent_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['send_newsletter']
    
    def send_newsletter(self, request, queryset):
        sent_count = 0
        failed_count = 0
        
        for newsletter in queryset:
            if newsletter.is_sent:
                messages.warning(request, f'Newsletter "{newsletter.subject}" has already been sent.')
                continue
                
            # Get confirmed subscribers
            subscribers = Subscriber.objects.filter(is_confirmed=True, is_active=True)
            
            if not subscribers.exists():
                messages.warning(request, 'No confirmed subscribers found.')
                continue
            
            # Send emails
            for subscriber in subscribers:
                try:
                    # Create unsubscribe link
                    unsubscribe_url = f"{settings.FRONTEND_URL}/newsletter/unsubscribe/{subscriber.confirmation_token}/"
                    
                    # Prepare email content
                    html_content = newsletter.content_html
                    if unsubscribe_url:
                        html_content += f'''
                        <hr>
                        <p style="font-size: 12px; color: #666;">
                        You received this email because you subscribed to Amardeep Asode's Trading Insights.<br>
                        <a href="{unsubscribe_url}">Unsubscribe</a> from future emails.
                        </p>
                        '''
                    
                    text_content = newsletter.content_text or "Please view this email in HTML format."
                    text_content += f"\n\nUnsubscribe: {unsubscribe_url}"
                    
                    send_mail(
                        subject=newsletter.subject,
                        message=text_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[subscriber.email],
                        html_message=html_content,
                        fail_silently=False,
                    )
                    sent_count += 1
                    
                except Exception as e:
                    failed_count += 1
                    print(f"Failed to send to {subscriber.email}: {e}")
            
            # Mark newsletter as sent
            newsletter.mark_as_sent(sent_count)
            
        if sent_count > 0:
            messages.success(request, f'Newsletter sent to {sent_count} subscribers.')
        if failed_count > 0:
            messages.error(request, f'Failed to send to {failed_count} subscribers.')
    
    send_newsletter.short_description = "Send selected newsletters to confirmed subscribers"
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at', 'edit_link']
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
        count = obj.posts.filter(status='published').count()
        if count > 0:
            return format_html(
                '<a href="/admin/portfolio_app/blogpost/?category__id__exact={}">{} posts</a>',
                obj.id, count
            )
        return '0 posts'
    post_count.short_description = 'Published Posts'
    
    def edit_link(self, obj):
        return format_html(
            '<a href="/admin/portfolio_app/blogcategory/{}/change/" class="button">Edit</a>',
            obj.id
        )
    edit_link.short_description = 'Actions'
    
    def delete_queryset(self, request, queryset):
        for category in queryset:
            posts_count = category.posts.count()
            if posts_count > 0:
                messages.warning(
                    request, 
                    f'Cannot delete category "{category.name}" - it has {posts_count} posts. Move posts to another category first.'
                )
            else:
                category.delete()
                messages.success(request, f'Category "{category.name}" deleted successfully.')

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at', 'edit_link']
    list_display_links = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    list_per_page = 30
    
    fieldsets = (
        ('Tag Information', {
            'fields': ('name', 'slug')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def post_count(self, obj):
        count = obj.posts.filter(status='published').count()
        if count > 0:
            return format_html(
                '<a href="/admin/portfolio_app/blogpost/?tags__id__exact={}">{} posts</a>',
                obj.id, count
            )
        return '0 posts'
    post_count.short_description = 'Published Posts'
    
    def edit_link(self, obj):
        return format_html(
            '<a href="/admin/portfolio_app/blogtag/{}/change/" class="button">Edit</a>',
            obj.id
        )
    edit_link.short_description = 'Actions'
    
    def delete_queryset(self, request, queryset):
        for tag in queryset:
            posts_count = tag.posts.count()
            if posts_count > 0:
                messages.warning(
                    request, 
                    f'Tag "{tag.name}" is used in {posts_count} posts. Remove from posts before deleting.'
                )
            else:
                tag.delete()
                messages.success(request, f'Tag "{tag.name}" deleted successfully.')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'category', 'status', 'is_featured', 
        'publish_date', 'views_count', 'edit_link', 'view_on_site'
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
    list_editable = ['status', 'is_featured']
    
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
        ('Statistics & Metadata', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Post statistics and timestamps'
        }),
    )
    
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new post
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    
    def status_colored(self, obj):
        colors = {
            'published': 'green',
            'draft': 'orange', 
            'scheduled': 'blue'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_colored.short_description = 'Status'
    
    def edit_link(self, obj):
        return format_html(
            '<a href="/admin/portfolio_app/blogpost/{}/change/" class="button">Edit</a>',
            obj.id
        )
    edit_link.short_description = 'Quick Edit'
    
    def view_on_site(self, obj):
        if obj.status == 'published':
            return format_html(
                '<a href="/blog/{}" target="_blank" class="button">View Live</a>',
                obj.slug
            )
        return format_html('<span style="color: gray;">Not Published</span>')
    view_on_site.short_description = 'View Live'
    
    def delete_queryset(self, request, queryset):
        for post in queryset:
            post.delete()
            messages.success(request, f'Post "{post.title}" deleted successfully.')
    
    def delete_model(self, request, obj):
        messages.success(request, f'Post "{obj.title}" deleted successfully.')
        super().delete_model(request, obj)
    
    actions = [
        'make_published', 'make_draft', 'make_featured', 'remove_featured',
        'duplicate_posts', 'export_posts'
    ]
    
    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} posts were successfully published.')
    make_published.short_description = "✅ Publish selected posts"
    
    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} posts were moved to draft.')
    make_draft.short_description = "📝 Move to draft"
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} posts were marked as featured.')
    make_featured.short_description = "⭐ Mark as featured"
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} posts were removed from featured.')
    remove_featured.short_description = "❌ Remove from featured"
    
    def duplicate_posts(self, request, queryset):
        for post in queryset:
            post.pk = None
            post.title = f"Copy of {post.title}"
            post.slug = f"copy-of-{post.slug}"
            post.status = 'draft'
            post.save()
        self.message_user(request, f'{queryset.count()} posts duplicated as drafts.')
    duplicate_posts.short_description = "📋 Duplicate as drafts"
    
    def export_posts(self, request, queryset):
        # Simple export functionality
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="blog_posts.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Title', 'Status', 'Category', 'Publish Date', 'Views'])
        
        for post in queryset:
            writer.writerow([
                post.title, post.status, post.category.name if post.category else '',
                post.publish_date, post.views_count
            ])
        
        return response
    export_posts.short_description = "📊 Export to CSV"
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)

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
                '<strong style="color: #28a745;">{} {}</strong>',
                obj.currency, f'{obj.price:,.0f}'
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

@admin.register(WorkshopApplication)
class WorkshopApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'workshop_title', 'experience_level', 
        'status_badge', 'applied_at', 'actions_column'
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
            'description': 'Basic applicant details'
        }),
        ('Workshop & Application', {
            'fields': ('workshop', 'motivation', 'status'),
            'description': 'Workshop selection and application details'
        }),
        ('Admin Notes & Timestamps', {
            'fields': ('notes', 'applied_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Administrative information'
        }),
    )
    
    readonly_fields = ['applied_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('workshop')
    
    def workshop_title(self, obj):
        return obj.workshop.title
    workshop_title.short_description = 'Workshop'
    workshop_title.admin_order_field = 'workshop__title'
    
    def status_badge(self, obj):
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
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">'
            '{} {}</span>',
            color, icon, obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def actions_column(self, obj):
        actions = []
        
        if obj.status == 'pending':
            actions.append(
                f'<a href="#" onclick="updateStatus({obj.id}, \'approved\')" '
                f'style="color: #28a745; text-decoration: none; margin-right: 10px;">✅ Approve</a>'
            )
            actions.append(
                f'<a href="#" onclick="updateStatus({obj.id}, \'rejected\')" '
                f'style="color: #dc3545; text-decoration: none; margin-right: 10px;">❌ Reject</a>'
            )
        
        actions.append(
            f'<a href="mailto:{obj.email}?subject=Workshop Application - {obj.workshop.title}" '
            f'style="color: #007bff; text-decoration: none;">📧 Email</a>'
        )
        
        return format_html(' | '.join(actions))
    actions_column.short_description = 'Quick Actions'
    
    actions = [
        'approve_applications', 'reject_applications', 'move_to_waitlist',
        'send_approval_emails', 'export_applications'
    ]
    
    def approve_applications(self, request, queryset):
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
    approve_applications.short_description = "✅ Approve selected applications"
    
    def reject_applications(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} applications rejected.', messages.WARNING)
    reject_applications.short_description = "❌ Reject selected applications"
    
    def move_to_waitlist(self, request, queryset):
        updated = queryset.update(status='waitlist')
        self.message_user(request, f'{updated} applications moved to waitlist.', messages.INFO)
    move_to_waitlist.short_description = "⏰ Move to waitlist"
    
    def send_approval_emails(self, request, queryset):
        # This would integrate with your email system
        approved_count = queryset.filter(status='approved').count()
        self.message_user(
            request, 
            f'Email functionality not implemented yet. Would send emails to {approved_count} approved applicants.',
            messages.INFO
        )
    send_approval_emails.short_description = "📧 Send approval emails"
    
    def export_applications(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="workshop_applications.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Name', 'Email', 'Phone', 'Workshop', 'Experience Level', 
            'Status', 'Applied Date', 'Motivation'
        ])
        
        for app in queryset:
            writer.writerow([
                app.name, app.email, app.phone, app.workshop.title,
                app.get_experience_level_display(), app.get_status_display(),
                app.applied_at.strftime('%Y-%m-%d %H:%M'), app.motivation
            ])
        
        return response
    export_applications.short_description = "📊 Export to CSV"
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/workshop_admin.js',)

# Customize admin site
admin.site.site_header = "Amardeep Asode Trading Portfolio Admin"
admin.site.site_title = "Trading Portfolio Admin"
admin.site.index_title = "Welcome to Trading Portfolio Administration"