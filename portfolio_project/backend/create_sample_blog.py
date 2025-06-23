#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from portfolio_app.models import BlogCategory, BlogTag, BlogPost
from django.utils import timezone

def create_sample_blog_data():
    # Get or create admin user
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', '123')
    
    # Create categories
    categories_data = [
        {
            'name': 'Market Analysis',
            'description': 'In-depth analysis of market trends and movements'
        },
        {
            'name': 'Trading Strategies',
            'description': 'Proven trading strategies and techniques'
        },
        {
            'name': 'Risk Management',
            'description': 'Essential risk management principles for traders'
        },
        {
            'name': 'Trading Psychology',
            'description': 'Mental aspects of successful trading'
        }
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = BlogCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories[cat_data['name']] = category
        if created:
            print(f"Created category: {category.name}")
    
    # Create tags
    tags_data = [
        'Intraday Trading', 'Technical Analysis', 'Fundamental Analysis',
        'Options Trading', 'Swing Trading', 'Day Trading', 'Stock Market',
        'Nifty 50', 'Bank Nifty', 'Risk Management', 'Trading Tips',
        'Market Trends', 'Trading Psychology', 'Portfolio Management'
    ]
    
    tags = {}
    for tag_name in tags_data:
        tag, created = BlogTag.objects.get_or_create(name=tag_name)
        tags[tag_name] = tag
        if created:
            print(f"Created tag: {tag.name}")
    
    # Create blog posts
    posts_data = [
        {
            'title': 'Understanding Nifty 50 Trends: A Complete Guide for Intraday Traders',
            'excerpt': 'Learn how to analyze Nifty 50 trends and make profitable intraday trades with proper risk management techniques.',
            'content': '''
<h2>Introduction to Nifty 50 Trading</h2>

<p>The Nifty 50 is India's premier stock market index, representing the top 50 companies by market capitalization. For intraday traders, understanding Nifty trends is crucial for making profitable decisions.</p>

<h3>Key Technical Indicators</h3>

<p>When analyzing Nifty 50 for intraday trading, focus on these essential indicators:</p>

<ul>
<li><strong>Moving Averages (20, 50, 200 EMA)</strong> - Identify trend direction</li>
<li><strong>RSI (Relative Strength Index)</strong> - Spot overbought/oversold conditions</li>
<li><strong>MACD</strong> - Confirm trend changes and momentum</li>
<li><strong>Volume Analysis</strong> - Validate price movements</li>
</ul>

<h3>Trading Strategy</h3>

<p>Here's a proven strategy for Nifty 50 intraday trading:</p>

<ol>
<li><strong>Pre-market Analysis</strong> - Check global markets, news, and overnight developments</li>
<li><strong>Support and Resistance</strong> - Identify key levels from previous day's trading</li>
<li><strong>Entry Points</strong> - Look for breakouts or bounces from key levels</li>
<li><strong>Risk Management</strong> - Never risk more than 2% of capital per trade</li>
</ol>

<h3>Risk Management Rules</h3>

<p>Successful Nifty trading requires strict risk management:</p>

<blockquote>
<p>"Risk comes from not knowing what you're doing." - Warren Buffett</p>
</blockquote>

<ul>
<li>Set stop-loss at 1% below entry for long positions</li>
<li>Target 1:2 risk-reward ratio minimum</li>
<li>Avoid trading during high volatility news events</li>
<li>Use position sizing based on volatility</li>
</ul>

<h3>Conclusion</h3>

<p>Mastering Nifty 50 intraday trading takes time and practice. Start with small positions, focus on risk management, and gradually increase your position size as you gain confidence.</p>

<p>Remember: Consistency beats big wins. Focus on making small, consistent profits rather than trying to hit home runs.</p>
            ''',
            'category': 'Market Analysis',
            'tags': ['Intraday Trading', 'Nifty 50', 'Technical Analysis', 'Risk Management'],
            'is_featured': True
        },
        {
            'title': 'Top 5 Risk Management Strategies Every Trader Must Know',
            'excerpt': 'Discover the essential risk management strategies that separate successful traders from the rest. Protect your capital and trade with confidence.',
            'content': '''
<h2>Why Risk Management is Everything</h2>

<p>In trading, your ability to manage risk determines your long-term success more than your ability to pick winning trades. Here are the top 5 risk management strategies every trader must master.</p>

<h3>1. The 2% Rule</h3>

<p>Never risk more than 2% of your total trading capital on a single trade. This rule ensures you can survive a series of losing trades without depleting your account.</p>

<p><strong>Example:</strong> If you have ₹1,00,000 in your trading account, never risk more than ₹2,000 on any single trade.</p>

<h3>2. Position Sizing</h3>

<p>Calculate your position size based on your stop-loss distance and risk amount:</p>

<p><code>Position Size = Risk Amount ÷ (Entry Price - Stop Loss Price)</code></p>

<h3>3. Stop-Loss Orders</h3>

<p>Always use stop-loss orders to limit your downside. Types of stop-losses:</p>

<ul>
<li><strong>Fixed Percentage:</strong> 2-3% below entry price</li>
<li><strong>Technical Stop:</strong> Below support levels</li>
<li><strong>Volatility-based:</strong> Using ATR (Average True Range)</li>
</ul>

<h3>4. Diversification</h3>

<p>Don't put all your eggs in one basket:</p>

<ul>
<li>Trade different sectors</li>
<li>Use different timeframes</li>
<li>Avoid correlated positions</li>
</ul>

<h3>5. Risk-Reward Ratio</h3>

<p>Maintain a minimum 1:2 risk-reward ratio. For every ₹1 you risk, aim to make ₹2.</p>

<p>This means you can be wrong 60% of the time and still be profitable!</p>

<h3>Conclusion</h3>

<p>Risk management isn't glamorous, but it's what keeps you in the game long enough to become profitable. Master these strategies and watch your trading transform.</p>
            ''',
            'category': 'Risk Management',
            'tags': ['Risk Management', 'Trading Tips', 'Portfolio Management'],
            'is_featured': True
        },
        {
            'title': 'Bank Nifty Options Trading: Advanced Strategies for Consistent Profits',
            'excerpt': 'Master Bank Nifty options trading with these advanced strategies. Learn when to use straddles, strangles, and iron condors for maximum profitability.',
            'content': '''
<h2>Bank Nifty Options: The Trader's Playground</h2>

<p>Bank Nifty options offer excellent opportunities for traders due to high liquidity and volatility. Here are advanced strategies for consistent profits.</p>

<h3>Strategy 1: Long Straddle</h3>

<p>Use when expecting high volatility but uncertain about direction:</p>

<ul>
<li>Buy ATM Call and Put options</li>
<li>Profit from large moves in either direction</li>
<li>Best before earnings or major announcements</li>
</ul>

<h3>Strategy 2: Iron Condor</h3>

<p>Perfect for range-bound markets:</p>

<ol>
<li>Sell ATM Call and Put (collect premium)</li>
<li>Buy OTM Call and Put (limit risk)</li>
<li>Profit when Bank Nifty stays within the range</li>
</ol>

<h3>Strategy 3: Bull Call Spread</h3>

<p>For moderately bullish outlook:</p>

<ul>
<li>Buy ITM Call option</li>
<li>Sell OTM Call option</li>
<li>Limited risk, limited reward</li>
</ul>

<h3>Key Tips for Bank Nifty Options</h3>

<p><strong>Timing is Everything:</strong></p>

<ul>
<li>First hour: High volatility, good for breakout trades</li>
<li>Mid-day: Lower volatility, good for range trading</li>
<li>Last hour: Increased activity, good for momentum trades</li>
</ul>

<p><strong>Greeks to Watch:</strong></p>

<ul>
<li><strong>Delta:</strong> Price sensitivity</li>
<li><strong>Theta:</strong> Time decay</li>
<li><strong>Vega:</strong> Volatility sensitivity</li>
<li><strong>Gamma:</strong> Delta sensitivity</li>
</ul>

<h3>Risk Management in Options</h3>

<p>Options can lose value quickly due to time decay. Always:</p>

<ul>
<li>Set profit targets (50-70% of maximum profit)</li>
<li>Cut losses early (don't let options expire worthless)</li>
<li>Avoid holding options overnight unless part of strategy</li>
</ul>

<h3>Conclusion</h3>

<p>Bank Nifty options trading requires skill, patience, and strict risk management. Start with paper trading, master the basics, then gradually implement these advanced strategies.</p>
            ''',
            'category': 'Trading Strategies',
            'tags': ['Options Trading', 'Bank Nifty', 'Trading Strategies', 'Advanced Trading'],
            'is_featured': False
        },
        {
            'title': 'The Psychology of Trading: Overcoming Fear and Greed',
            'excerpt': 'Discover how to master your emotions and develop the mental discipline required for successful trading. Learn to overcome fear, greed, and other psychological barriers.',
            'content': '''
<h2>The Mental Game of Trading</h2>

<p>Trading is 80% psychology and 20% strategy. Your ability to control emotions often determines your success more than your technical analysis skills.</p>

<h3>Common Psychological Traps</h3>

<h4>1. Fear of Missing Out (FOMO)</h4>

<p>FOMO leads to:</p>
<ul>
<li>Chasing trades after they've already moved</li>
<li>Entering positions without proper analysis</li>
<li>Overtrading and increased risk</li>
</ul>

<p><strong>Solution:</strong> Stick to your trading plan. There's always another opportunity.</p>

<h4>2. Revenge Trading</h4>

<p>After a loss, traders often try to "get even" by:</p>
<ul>
<li>Increasing position sizes</li>
<li>Taking unnecessary risks</li>
<li>Abandoning their strategy</li>
</ul>

<p><strong>Solution:</strong> Take a break after significant losses. Come back with a clear mind.</p>

<h4>3. Overconfidence</h4>

<p>After a winning streak, traders may:</p>
<ul>
<li>Increase risk beyond their comfort zone</li>
<li>Skip proper analysis</li>
<li>Ignore risk management rules</li>
</ul>

<h3>Building Mental Discipline</h3>

<h4>1. Develop a Trading Plan</h4>

<p>Your trading plan should include:</p>
<ul>
<li>Entry and exit criteria</li>
<li>Risk management rules</li>
<li>Position sizing guidelines</li>
<li>Daily/weekly goals</li>
</ul>

<h4>2. Keep a Trading Journal</h4>

<p>Record:</p>
<ul>
<li>Trade setups and reasoning</li>
<li>Emotions before, during, and after trades</li>
<li>Lessons learned from each trade</li>
<li>Areas for improvement</li>
</ul>

<h4>3. Practice Mindfulness</h4>

<p>Techniques to stay centered:</p>
<ul>
<li>Deep breathing exercises</li>
<li>Meditation before trading sessions</li>
<li>Regular breaks during trading</li>
<li>Physical exercise to manage stress</li>
</ul>

<h3>The Winning Mindset</h3>

<blockquote>
<p>"The goal of a successful trader is to make the best trades. Money is secondary." - Alexander Elder</p>
</blockquote>

<p>Characteristics of successful traders:</p>
<ul>
<li><strong>Patience:</strong> Wait for the right setups</li>
<li><strong>Discipline:</strong> Follow the plan regardless of emotions</li>
<li><strong>Adaptability:</strong> Adjust to changing market conditions</li>
<li><strong>Humility:</strong> Accept losses as part of the game</li>
</ul>

<h3>Conclusion</h3>

<p>Mastering trading psychology is a lifelong journey. Focus on developing good habits, maintaining discipline, and continuously learning from your experiences.</p>

<p>Remember: The market will always be there, but your capital won't if you don't protect it.</p>
            ''',
            'category': 'Trading Psychology',
            'tags': ['Trading Psychology', 'Mental Discipline', 'Trading Tips'],
            'is_featured': False
        }
    ]
    
    for post_data in posts_data:
        # Check if post already exists
        if BlogPost.objects.filter(title=post_data['title']).exists():
            print(f"Post already exists: {post_data['title']}")
            continue
            
        post = BlogPost.objects.create(
            title=post_data['title'],
            excerpt=post_data['excerpt'],
            content=post_data['content'],
            author=admin_user,
            category=categories[post_data['category']],
            status='published',
            is_featured=post_data['is_featured']
        )
        
        # Add tags
        for tag_name in post_data['tags']:
            if tag_name in tags:
                post.tags.add(tags[tag_name])
        
        print(f"Created blog post: {post.title}")
    
    print("\nBlog setup completed!")
    print(f"Categories created: {len(categories)}")
    print(f"Tags created: {len(tags)}")
    print(f"Blog posts created: {BlogPost.objects.count()}")

if __name__ == "__main__":
    create_sample_blog_data()