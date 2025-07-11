# Generated by Django 5.2.3 on 2025-06-24 08:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0007_alter_payment_payment_type_tradingservice_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, help_text='Phone number', max_length=20)),
                ('date_of_birth', models.DateField(blank=True, help_text='Date of birth', null=True)),
                ('bio', models.TextField(blank=True, help_text='Short bio')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('trading_experience', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'), ('expert', 'Expert')], default='beginner', help_text='Trading experience level', max_length=20)),
                ('preferred_market', models.CharField(blank=True, choices=[('equity', 'Equity'), ('options', 'Options'), ('futures', 'Futures'), ('forex', 'Forex'), ('crypto', 'Cryptocurrency')], help_text='Preferred trading market', max_length=50)),
                ('newsletter_subscribed', models.BooleanField(default=False, help_text='Subscribed to newsletter')),
                ('email_notifications', models.BooleanField(default=True, help_text='Receive email notifications')),
                ('sms_notifications', models.BooleanField(default=False, help_text='Receive SMS notifications')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.CreateModel(
            name='PurchasedCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(help_text='Name of the purchased course', max_length=255)),
                ('course_type', models.CharField(choices=[('workshop', 'Workshop'), ('mentorship', 'Mentorship'), ('signals', 'Trading Signals'), ('course', 'Online Course')], help_text='Type of course', max_length=50)),
                ('description', models.TextField(blank=True, help_text='Course description')),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField(help_text='Course start date')),
                ('end_date', models.DateTimeField(blank=True, help_text='Course end date', null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('completed', 'Completed'), ('expired', 'Expired'), ('cancelled', 'Cancelled')], default='active', max_length=20)),
                ('amount_paid', models.DecimalField(decimal_places=2, help_text='Amount paid for the course', max_digits=10)),
                ('currency', models.CharField(default='INR', max_length=3)),
                ('access_url', models.URLField(blank=True, help_text='URL to access the course')),
                ('access_credentials', models.JSONField(blank=True, default=dict, help_text='Login credentials or access details')),
                ('progress_percentage', models.PositiveIntegerField(default=0, help_text='Course completion percentage')),
                ('last_accessed', models.DateTimeField(blank=True, help_text='Last time user accessed the course', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('trading_service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='portfolio_app.tradingservice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchased_courses', to=settings.AUTH_USER_MODEL)),
                ('workshop_application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='portfolio_app.workshopapplication')),
            ],
            options={
                'ordering': ['-purchase_date'],
                'indexes': [models.Index(fields=['user', 'status'], name='portfolio_a_user_id_e19739_idx'), models.Index(fields=['-purchase_date'], name='portfolio_a_purchas_a10801_idx')],
            },
        ),
    ]
