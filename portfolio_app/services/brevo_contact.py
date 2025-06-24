from .brevo_service import BrevoEmailService
from django.conf import settings

class ContactEmailService(BrevoEmailService):
    """
    Extended service for contact form emails
    """
    
    def send_contact_notification(self, contact_message) -> bool:
        """
        Send contact form notification to admin
        """
        subject = f"New Contact Message: {contact_message.subject}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2563eb; border-bottom: 2px solid #2563eb; padding-bottom: 10px;">
                    New Contact Message Received
                </h2>
                
                <div style="background: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #1e40af;">Contact Information</h3>
                    <p><strong>Name:</strong> {contact_message.name}</p>
                    <p><strong>Email:</strong> <a href="mailto:{contact_message.email}">{contact_message.email}</a></p>
                    <p><strong>Subject:</strong> {contact_message.subject}</p>
                </div>
                
                <div style="background: #fefce8; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #a16207;">Message</h3>
                    <p style="font-style: italic; white-space: pre-wrap;">{contact_message.message}</p>
                </div>
                
                <div style="background: #ecfdf5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #059669;">Quick Actions</h3>
                    <p>
                        <a href="mailto:{contact_message.email}?subject=Re: {contact_message.subject}" 
                           style="background: #2563eb; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; margin-right: 10px;">
                            📧 Reply
                        </a>
                    </p>
                </div>
                
                <div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin: 20px 0; font-size: 12px; color: #6b7280;">
                    <h4 style="margin-top: 0; color: #374151;">Technical Details</h4>
                    <p><strong>Message ID:</strong> #{contact_message.id}</p>
                    <p><strong>Received:</strong> {contact_message.created_at.strftime('%B %d, %Y at %I:%M %p')}</p>
                    {f'<p><strong>IP Address:</strong> {contact_message.ip_address}</p>' if contact_message.ip_address else ''}
                    <p><strong>Priority:</strong> {contact_message.get_priority_display()}</p>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #6b7280;">
                    <p>This notification was sent from your Trading Portfolio contact form.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        New Contact Message Received
        
        Contact Information:
        Name: {contact_message.name}
        Email: {contact_message.email}
        Subject: {contact_message.subject}
        
        Message:
        {contact_message.message}
        
        Technical Details:
        Message ID: #{contact_message.id}
        Received: {contact_message.created_at.strftime('%B %d, %Y at %I:%M %p')}
        {f'IP Address: {contact_message.ip_address}' if contact_message.ip_address else ''}
        Priority: {contact_message.get_priority_display()}
        
        Please reply to this message as soon as possible.
        """
        
        return self.send_email(
            to_email=settings.ADMIN_EMAIL,
            to_name="Admin",
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            reply_to=contact_message.email
        )
    
    def send_contact_confirmation(self, contact_message) -> bool:
        """
        Send contact form confirmation to customer
        """
        subject = f"Message Received: {contact_message.subject}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2563eb; margin-bottom: 10px;">Message Received</h1>
                    <p style="color: #6b7280; font-size: 18px;">Thank you for contacting us!</p>
                </div>
                
                <div style="background: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h2 style="margin-top: 0; color: #1e40af;">Hi {contact_message.name}!</h2>
                    <p>Thank you for reaching out to Amardeep Asode Trading. We've received your message and will get back to you as soon as possible.</p>
                </div>
                
                <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #1e40af;">Your Message Summary</h3>
                    <p><strong>Subject:</strong> {contact_message.subject}</p>
                    <p><strong>Message:</strong></p>
                    <div style="background: white; padding: 15px; border-left: 4px solid #2563eb; margin: 10px 0;">
                        <p style="margin: 0; font-style: italic; white-space: pre-wrap;">{contact_message.message}</p>
                    </div>
                </div>
                
                <div style="background: #ecfdf5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #059669;">What Happens Next?</h3>
                    <ul style="margin: 0; padding-left: 20px;">
                        <li>We typically respond within 24 hours</li>
                        <li>For urgent matters, we'll prioritize your message</li>
                        <li>You'll receive a detailed response to your inquiry</li>
                        <li>We may follow up with additional questions if needed</li>
                    </ul>
                </div>
                
                <div style="background: #fefce8; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #a16207;">Need Immediate Assistance?</h3>
                    <p>If your inquiry is urgent, feel free to contact us directly:</p>
                    <p>
                        📧 Email: <a href="mailto:amardipasode@gmail.com">amardipasode@gmail.com</a>
                    </p>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #6b7280;">
                    <p>Best regards,<br><strong>Amardeep Asode</strong><br>Stock & Intraday Trader</p>
                    <p style="font-size: 12px;">Message Reference: #{contact_message.id}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Message Received - Thank you for contacting us!
        
        Hi {contact_message.name}!
        
        Thank you for reaching out to Amardeep Asode Trading. We've received your message and will get back to you as soon as possible.
        
        Your Message Summary:
        Subject: {contact_message.subject}
        Message: {contact_message.message}
        
        What Happens Next?
        - We typically respond within 24 hours
        - For urgent matters, we'll prioritize your message
        - You'll receive a detailed response to your inquiry
        - We may follow up with additional questions if needed
        
        Need Immediate Assistance?
        Email: amardipasode@gmail.com
        
        Best regards,
        Amardeep Asode
        Stock & Intraday Trader
        
        Message Reference: #{contact_message.id}
        """
        
        return self.send_email(
            to_email=contact_message.email,
            to_name=contact_message.name,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

# Create contact email service instance
contact_email_service = ContactEmailService()