# Generated by Django 5.2.3 on 2025-06-23 18:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0005_workshopapplication'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(help_text='Unique payment identifier', max_length=100, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='INR', max_length=3)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ('cancelled', 'Cancelled'), ('refunded', 'Refunded')], default='pending', max_length=10)),
                ('payment_type', models.CharField(choices=[('workshop', 'Workshop'), ('product', 'Digital Product'), ('subscription', 'Subscription')], max_length=15)),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_email', models.EmailField(max_length=254)),
                ('customer_phone', models.CharField(blank=True, max_length=20)),
                ('gateway_payment_id', models.CharField(blank=True, max_length=100)),
                ('payment_method', models.CharField(blank=True, max_length=50)),
                ('gateway_response', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='workshopapplication',
            name='paid_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workshopapplication',
            name='payment_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='workshopapplication',
            name='payment_id',
            field=models.CharField(blank=True, help_text='Payment gateway transaction ID', max_length=100),
        ),
        migrations.AddField(
            model_name='workshopapplication',
            name='payment_method',
            field=models.CharField(blank=True, help_text='Payment method used', max_length=50),
        ),
        migrations.AddField(
            model_name='workshopapplication',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Payment Pending'), ('completed', 'Payment Completed'), ('failed', 'Payment Failed'), ('refunded', 'Refunded'), ('not_required', 'Not Required')], default='not_required', max_length=15),
        ),
        migrations.AlterField(
            model_name='workshopapplication',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('waitlist', 'Waitlist'), ('paid', 'Paid'), ('cancelled', 'Cancelled')], default='pending', max_length=10),
        ),
        migrations.AddIndex(
            model_name='workshopapplication',
            index=models.Index(fields=['payment_status'], name='portfolio_a_payment_dfd300_idx'),
        ),
        migrations.AddField(
            model_name='payment',
            name='digital_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='portfolio_app.digitalproduct'),
        ),
        migrations.AddField(
            model_name='payment',
            name='workshop_application',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='portfolio_app.workshopapplication'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['-created_at'], name='portfolio_a_created_c32cf7_idx'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['status'], name='portfolio_a_status_fcb838_idx'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['payment_type'], name='portfolio_a_payment_cfd9ea_idx'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['customer_email'], name='portfolio_a_custome_215366_idx'),
        ),
    ]
