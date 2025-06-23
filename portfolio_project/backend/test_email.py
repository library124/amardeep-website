#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    try:
        print("Testing email configuration...")
        print(f"Email Backend: {settings.EMAIL_BACKEND}")
        print(f"Email Host: {settings.EMAIL_HOST}")
        print(f"Email Host User: {settings.EMAIL_HOST_USER}")
        print(f"Default From Email: {settings.DEFAULT_FROM_EMAIL}")
        
        # Test email
        test_email_address = input("Enter your email address to test: ")
        
        send_mail(
            subject='Test Email from Amardeep Asode Trading Portfolio',
            message='''
Hello!

This is a test email from your Django newsletter system.

If you received this email, your email configuration is working correctly!

Best regards,
Amardeep Asode Trading Portfolio System
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email_address],
            fail_silently=False,
        )
        
        print(f"✅ Test email sent successfully to {test_email_address}")
        print("Check your inbox (and spam folder) for the test email.")
        
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        print("\nPossible issues:")
        print("1. Gmail App Password not set correctly")
        print("2. 2-Factor Authentication not enabled on Gmail")
        print("3. Network connectivity issues")
        print("4. Gmail account settings blocking less secure apps")

if __name__ == "__main__":
    test_email()