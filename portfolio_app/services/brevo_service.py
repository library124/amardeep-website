import requests
import logging
from django.conf import settings
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class BrevoEmailService:
    """
    Service class for sending emails via Brevo API
    """
    
    def __init__(self):
        self.api_key = settings.BREVO_API_KEY
        self.api_url = settings.BREVO_API_URL
        self.headers = {
            'accept': 'application/json',
            'api-key': self.api_key,
            'content-type': 'application/json'
        }
    
    def send_email(
        self, 
        to_email: str, 
        to_name: str, 
        subject: str, 
        html_content: str, 
        text_content: Optional[str] = None,
        sender_email: Optional[str] = None,
        sender_name: Optional[str] = None,
        reply_to: Optional[str] = None
    ) -> bool:
        """
        Send a single email via Brevo API
        
        Args:
            to_email: Recipient email address
            to_name: Recipient name
            subject: Email subject
            html_content: HTML content of the email
            text_content: Plain text content (optional)
            sender_email: Sender email (defaults to DEFAULT_FROM_EMAIL)
            sender_name: Sender name (defaults to "Amardeep Asode Trading")
            reply_to: Reply-to email address
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        
        if not sender_email:
            sender_email = settings.DEFAULT_FROM_EMAIL.split('<')[1].split('>')[0] if '<' in settings.DEFAULT_FROM_EMAIL else settings.DEFAULT_FROM_EMAIL
        
        if not sender_name:
            sender_name = "Amardeep Asode Trading"
        
        data = {
            "sender": {
                "name": sender_name,
                "email": sender_email
            },
            "to": [
                {
                    "email": to_email,
                    "name": to_name
                }
            ],
            "subject": subject,
            "htmlContent": html_content
        }
        
        if text_content:
            data["textContent"] = text_content
            
        if reply_to:
            data["replyTo"] = {
                "email": reply_to,
                "name": sender_name
            }
        
        try:
            response = requests.post(
                f"{self.api_url}/smtp/email",
                headers=self.headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 201:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email to {to_email}. Status: {response.status_code}, Response: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error sending email to {to_email}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending email to {to_email}: {str(e)}")
            return False
    
    def send_service_booking_notification(self, booking) -> bool:
        """
        Send service booking notification to admin
        """
        subject = f"New Service Booking: {booking.service.name}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2563eb; border-bottom: 2px solid #2563eb; padding-bottom: 10px;">
                    New Service Booking Received
                </h2>
                
                <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #1e40af;">Service Details</h3>
                    <p><strong>Service:</strong> {booking.service.name}</p>
                    <p><strong>Price:</strong> {booking.service.price_display}</p>
                    <p><strong>Type:</strong> {booking.service.get_service_type_display()}</p>
                </div>
                
                <div style="background: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #1e40af;">Customer Information</h3>
                    <p><strong>Name:</strong> {booking.name}</p>
                    <p><strong>Email:</strong> <a href="mailto:{booking.email}">{booking.email}</a></p>
                    <p><strong>Phone:</strong> <a href="tel:{booking.phone}">{booking.phone}</a></p>
                    <p><strong>Preferred Contact:</strong> {booking.get_preferred_contact_method_display()}</p>
                    {f'<p><strong>Preferred Time:</strong> {booking.preferred_time}</p>' if booking.preferred_time else ''}
                </div>
                
                {f'''
                <div style="background: #fefce8; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #a16207;">Customer Message</h3>
                    <p style="font-style: italic;">"{booking.message}"</p>
                </div>
                ''' if booking.message else ''}
                
                <div style="background: #ecfdf5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #059669;">Quick Actions</h3>
                    <p>
                        <a href="https://wa.me/{booking.phone.replace('+', '')}?text=Hi {booking.name}! Thank you for your interest in {booking.service.name}. How can I help you?" 
                           style="background: #25d366; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; margin-right: 10px;">
                            💬 WhatsApp
                        </a>
                        <a href="tel:{booking.phone}" 
                           style="background: #2563eb; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; margin-right: 10px;">
                            📞 Call
                        </a>
                        <a href="mailto:{booking.email}?subject=Re: {booking.service.name} Inquiry" 
                           style="background: #7c3aed; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;">
                            📧 Email
                        </a>
                    </p>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #6b7280;">
                    <p>This notification was sent from your Trading Portfolio website.</p>
                    <p>Booking ID: #{booking.id} | Received: {booking.created_at.strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        New Service Booking Received
        
        Service: {booking.service.name}
        Price: {booking.service.price_display}
        
        Customer Information:
        Name: {booking.name}
        Email: {booking.email}
        Phone: {booking.phone}
        Preferred Contact: {booking.get_preferred_contact_method_display()}
        {f'Preferred Time: {booking.preferred_time}' if booking.preferred_time else ''}
        
        {f'Message: {booking.message}' if booking.message else ''}
        
        Please contact the customer as soon as possible.
        
        Booking ID: #{booking.id}
        Received: {booking.created_at.strftime('%B %d, %Y at %I:%M %p')}
        """
        
        return self.send_email(
            to_email=settings.ADMIN_EMAIL,
            to_name="Admin",
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            reply_to=booking.email
        )
    
    def send_service_booking_confirmation(self, booking) -> bool:
        """
        Send booking confirmation to customer
        """
        subject = f"Booking Confirmation: {booking.service.name}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2563eb; margin-bottom: 10px;">Booking Confirmation</h1>
                    <p style="color: #6b7280; font-size: 18px;">Thank you for choosing Amardeep Asode Trading!</p>
                </div>
                
                <div style="background: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h2 style="margin-top: 0; color: #1e40af;">Hi {booking.name}!</h2>
                    <p>We've received your booking request for <strong>{booking.service.name}</strong> and will contact you soon.</p>
                </div>
                
                <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #1e40af;">Service Details</h3>
                    <p><strong>Service:</strong> {booking.service.name}</p>
                    <p><strong>Price:</strong> {booking.service.price_display}</p>
                    <p><strong>Description:</strong> {booking.service.description}</p>
                </div>
                
                <div style="background: #ecfdf5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #059669;">What Happens Next?</h3>
                    <ul style="margin: 0; padding-left: 20px;">
                        <li>Our team will review your request within 24 hours</li>
                        <li>We'll contact you via {booking.get_preferred_contact_method_display().lower()}</li>
                        <li>We'll discuss your requirements and schedule a consultation</li>
                        <li>You'll receive detailed information about the service</li>
                    </ul>
                </div>
                
                <div style="background: #fefce8; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #a16207;">Need Immediate Assistance?</h3>
                    <p>If you have urgent questions, feel free to contact us directly:</p>
                    <p>
                        📱 WhatsApp: <a href="https://wa.me/919876543210">+91 98765 43210</a><br>
                        📞 Phone: <a href="tel:+919876543210">+91 98765 43210</a><br>
                        📧 Email: <a href="mailto:amardeepasode.trading@gmail.com">amardeepasode.trading@gmail.com</a>
                    </p>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #6b7280;">
                    <p>Thank you for trusting Amardeep Asode Trading with your trading journey!</p>
                    <p style="font-size: 12px;">Booking Reference: #{booking.id}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Booking Confirmation - {booking.service.name}
        
        Hi {booking.name}!
        
        Thank you for choosing Amardeep Asode Trading! We've received your booking request for {booking.service.name} and will contact you soon.
        
        Service Details:
        - Service: {booking.service.name}
        - Price: {booking.service.price_display}
        - Description: {booking.service.description}
        
        What Happens Next?
        - Our team will review your request within 24 hours
        - We'll contact you via {booking.get_preferred_contact_method_display().lower()}
        - We'll discuss your requirements and schedule a consultation
        - You'll receive detailed information about the service
        
        Need Immediate Assistance?
        WhatsApp: +91 98765 43210
        Phone: +91 98765 43210
        Email: amardeepasode.trading@gmail.com
        
        Thank you for trusting Amardeep Asode Trading with your trading journey!
        
        Booking Reference: #{booking.id}
        """
        
        return self.send_email(
            to_email=booking.email,
            to_name=booking.name,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )
    
    def send_newsletter_confirmation(self, subscriber) -> bool:
        """
        Send newsletter subscription confirmation
        """
        confirmation_url = f"{settings.FRONTEND_URL}/newsletter/confirm/{subscriber.confirmation_token}/"
        
        subject = "Confirm Your Newsletter Subscription - Amardeep Asode Trading"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2563eb; margin-bottom: 10px;">Welcome to Trading Insights!</h1>
                    <p style="color: #6b7280; font-size: 18px;">Confirm your subscription to get started</p>
                </div>
                
                <div style="background: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h2 style="margin-top: 0; color: #1e40af;">Hi {subscriber.name or 'Trader'}!</h2>
                    <p>Thank you for subscribing to Amardeep Asode's Trading Insights newsletter!</p>
                    <p>To complete your subscription and start receiving valuable trading insights, please confirm your email address by clicking the button below:</p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{confirmation_url}" 
                       style="background: #2563eb; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
                        Confirm Subscription
                    </a>
                </div>
                
                <div style="background: #ecfdf5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #059669;">What You'll Receive:</h3>
                    <ul style="margin: 0; padding-left: 20px;">
                        <li>📈 Weekly market analysis and insights</li>
                        <li>💡 Trading tips and strategies</li>
                        <li>🎯 Exclusive trading signals and setups</li>
                        <li>📊 Performance updates and achievements</li>
                        <li>🚀 Early access to workshops and courses</li>
                    </ul>
                </div>
                
                <div style="background: #fefce8; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 0; font-size: 14px; color: #a16207;">
                        <strong>Note:</strong> If you didn't subscribe to this newsletter, please ignore this email. 
                        The subscription will not be activated without confirmation.
                    </p>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #6b7280;">
                    <p>Best regards,<br><strong>Amardeep Asode</strong><br>Stock & Intraday Trader</p>
                    <p style="font-size: 12px;">
                        If the button doesn't work, copy and paste this link: {confirmation_url}
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Welcome to Trading Insights!
        
        Hi {subscriber.name or 'Trader'}!
        
        Thank you for subscribing to Amardeep Asode's Trading Insights newsletter!
        
        To complete your subscription, please click the link below:
        {confirmation_url}
        
        You'll receive:
        - Weekly market analysis and insights
        - Trading tips and strategies
        - Exclusive trading signals and setups
        - Performance updates and achievements
        - Early access to workshops and courses
        
        If you didn't subscribe to this newsletter, please ignore this email.
        
        Best regards,
        Amardeep Asode
        Stock & Intraday Trader
        """
        
        return self.send_email(
            to_email=subscriber.email,
            to_name=subscriber.name or "Trader",
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

# Create a global instance
brevo_service = BrevoEmailService()