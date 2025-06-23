#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from portfolio_app.models import Newsletter

# Create sample newsletter
newsletter = Newsletter.objects.create(
    subject="Weekly Market Analysis - Nifty Outlook & Trading Opportunities",
    content_html="""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h1 style="color: #0ea5e9; text-align: center;">Weekly Trading Insights</h1>
            <h2 style="color: #1e293b;">Hello Fellow Traders!</h2>
            
            <p>Welcome to this week's market analysis. Here are the key insights for the upcoming trading sessions:</p>
            
            <h3 style="color: #0ea5e9;">Market Overview</h3>
            <ul>
                <li><strong>Nifty 50:</strong> Currently trading at 19,850 with strong support at 19,700</li>
                <li><strong>Bank Nifty:</strong> Showing bullish momentum above 45,000 levels</li>
                <li><strong>Volatility:</strong> VIX at 12.5, indicating low volatility environment</li>
            </ul>
            
            <h3 style="color: #0ea5e9;">Key Trading Opportunities</h3>
            <div style="background-color: #f8fafc; padding: 15px; border-left: 4px solid #0ea5e9; margin: 15px 0;">
                <h4>RELIANCE - Bullish Setup</h4>
                <p><strong>Entry:</strong> Above 2,450<br>
                <strong>Target:</strong> 2,520<br>
                <strong>Stop Loss:</strong> 2,420</p>
            </div>
            
            <div style="background-color: #f8fafc; padding: 15px; border-left: 4px solid #0ea5e9; margin: 15px 0;">
                <h4>HDFC BANK - Breakout Play</h4>
                <p><strong>Entry:</strong> Above 1,680<br>
                <strong>Target:</strong> 1,720<br>
                <strong>Stop Loss:</strong> 1,660</p>
            </div>
            
            <h3 style="color: #0ea5e9;">Risk Management Tips</h3>
            <ol>
                <li>Never risk more than 2% of your capital per trade</li>
                <li>Use proper position sizing based on stop loss distance</li>
                <li>Book partial profits at first target</li>
                <li>Trail stop losses for remaining positions</li>
            </ol>
            
            <h3 style="color: #0ea5e9;">This Week's Performance</h3>
            <p>Our signals achieved:</p>
            <ul>
                <li>✅ 8 out of 10 trades profitable</li>
                <li>✅ 80% win rate</li>
                <li>✅ Average return: 2.3% per trade</li>
            </ul>
            
            <div style="background-color: #0ea5e9; color: white; padding: 20px; text-align: center; margin: 20px 0; border-radius: 8px;">
                <h3>Want More Detailed Analysis?</h3>
                <p>Join our Premium Mentorship program for live trading sessions and personalized guidance.</p>
                <a href="http://localhost:3001/#pricing" style="background-color: white; color: #0ea5e9; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">View Plans</a>
            </div>
            
            <p>Happy Trading!<br>
            <strong>Amardeep Asode</strong><br>
            Stock & Intraday Trader</p>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #e2e8f0;">
            <p style="font-size: 12px; color: #64748b; text-align: center;">
                <strong>Disclaimer:</strong> This is for educational purposes only. Please consult your financial advisor before making investment decisions.
            </p>
        </div>
    </body>
    </html>
    """,
    content_text="""
Weekly Trading Insights - Amardeep Asode

Hello Fellow Traders!

Welcome to this week's market analysis. Here are the key insights for the upcoming trading sessions:

MARKET OVERVIEW:
- Nifty 50: Currently trading at 19,850 with strong support at 19,700
- Bank Nifty: Showing bullish momentum above 45,000 levels
- Volatility: VIX at 12.5, indicating low volatility environment

KEY TRADING OPPORTUNITIES:

RELIANCE - Bullish Setup
Entry: Above 2,450
Target: 2,520
Stop Loss: 2,420

HDFC BANK - Breakout Play
Entry: Above 1,680
Target: 1,720
Stop Loss: 1,660

RISK MANAGEMENT TIPS:
1. Never risk more than 2% of your capital per trade
2. Use proper position sizing based on stop loss distance
3. Book partial profits at first target
4. Trail stop losses for remaining positions

THIS WEEK'S PERFORMANCE:
- 8 out of 10 trades profitable
- 80% win rate
- Average return: 2.3% per trade

Want more detailed analysis? Join our Premium Mentorship program for live trading sessions and personalized guidance.

Happy Trading!
Amardeep Asode
Stock & Intraday Trader

Disclaimer: This is for educational purposes only. Please consult your financial advisor before making investment decisions.
    """
)

print(f"Sample newsletter created: {newsletter.subject}")
print(f"Newsletter ID: {newsletter.id}")