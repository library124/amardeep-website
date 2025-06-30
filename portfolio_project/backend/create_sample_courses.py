#!/usr/bin/env python
import os
import sys
import django
from decimal import Decimal

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from portfolio_app.models import Course

def create_sample_courses():
    # Get or create a user to be the instructor
    instructor, created = User.objects.get_or_create(
        username='instructor',
        defaults={
            'email': 'instructor@example.com',
            'first_name': 'Trading',
            'last_name': 'Expert'
        }
    )
    
    if created:
        instructor.set_password('password123')
        instructor.save()
        print(f"Created instructor user: {instructor.username}")
    
    # Sample courses data
    courses_data = [
        {
            'title': 'Complete Trading Fundamentals',
            'short_description': 'Master the basics of trading with comprehensive fundamentals course covering market analysis, risk management, and trading psychology.',
            'description': '''This comprehensive course covers all the essential fundamentals of trading that every successful trader needs to know.

You'll learn about market structure, technical analysis, fundamental analysis, risk management, and trading psychology. This course is perfect for beginners who want to start their trading journey with a solid foundation.

The course includes practical examples, real market scenarios, and hands-on exercises to help you apply what you learn immediately.''',
            'course_type': 'video',
            'difficulty_level': 'beginner',
            'duration_hours': 20,
            'lessons_count': 25,
            'price': Decimal('4999.00'),
            'original_price': Decimal('7999.00'),
            'what_you_learn': '''Understanding market structure and how markets work
Technical analysis and chart reading
Fundamental analysis basics
Risk management strategies
Trading psychology and mindset
Creating a trading plan
Position sizing and money management''',
            'requirements': '''Basic understanding of financial markets
Computer with internet connection
Willingness to learn and practice
No prior trading experience required''',
            'course_content': [
                {'module': 'Introduction to Trading', 'lessons': 5},
                {'module': 'Market Analysis', 'lessons': 8},
                {'module': 'Risk Management', 'lessons': 6},
                {'module': 'Trading Psychology', 'lessons': 4},
                {'module': 'Practical Application', 'lessons': 2}
            ],
            'is_featured': True,
            'is_active': True
        },
        {
            'title': 'Advanced Options Trading Strategies',
            'short_description': 'Learn sophisticated options trading strategies including spreads, straddles, and advanced risk management techniques.',
            'description': '''Take your options trading to the next level with advanced strategies and techniques used by professional traders.

This course covers complex options strategies, Greeks, volatility trading, and advanced risk management. You'll learn how to construct profitable trades in any market condition.

Perfect for traders who already have basic options knowledge and want to expand their toolkit with professional-grade strategies.''',
            'course_type': 'video',
            'difficulty_level': 'advanced',
            'duration_hours': 30,
            'lessons_count': 35,
            'price': Decimal('9999.00'),
            'original_price': Decimal('14999.00'),
            'what_you_learn': '''Advanced options strategies
Understanding Greeks and their applications
Volatility trading techniques
Complex spread strategies
Risk management for options
Portfolio hedging strategies
Professional trading setups''',
            'requirements': '''Basic options trading knowledge
Understanding of calls and puts
Experience with trading platforms
Intermediate level trading experience''',
            'course_content': [
                {'module': 'Options Greeks Deep Dive', 'lessons': 8},
                {'module': 'Advanced Spread Strategies', 'lessons': 10},
                {'module': 'Volatility Trading', 'lessons': 7},
                {'module': 'Risk Management', 'lessons': 6},
                {'module': 'Portfolio Strategies', 'lessons': 4}
            ],
            'is_featured': True,
            'is_active': True
        },
        {
            'title': 'Cryptocurrency Trading Masterclass',
            'short_description': 'Complete guide to cryptocurrency trading covering technical analysis, DeFi, and risk management in crypto markets.',
            'description': '''Master the exciting world of cryptocurrency trading with this comprehensive course designed for both beginners and intermediate traders.

Learn about blockchain technology, different cryptocurrencies, technical analysis specific to crypto markets, and how to navigate the volatile crypto landscape safely.

This course includes real-world examples, case studies, and practical trading strategies that work in crypto markets.''',
            'course_type': 'live',
            'difficulty_level': 'intermediate',
            'duration_hours': 25,
            'lessons_count': 30,
            'price': Decimal('7999.00'),
            'what_you_learn': '''Blockchain and cryptocurrency fundamentals
Crypto market analysis techniques
DeFi and yield farming strategies
Risk management in volatile markets
Crypto trading psychology
Portfolio diversification with crypto
Security and wallet management''',
            'requirements': '''Basic trading knowledge
Understanding of financial markets
Computer with reliable internet
Willingness to learn new technology''',
            'course_content': [
                {'module': 'Crypto Fundamentals', 'lessons': 6},
                {'module': 'Technical Analysis for Crypto', 'lessons': 8},
                {'module': 'DeFi and Advanced Concepts', 'lessons': 7},
                {'module': 'Risk Management', 'lessons': 5},
                {'module': 'Practical Trading', 'lessons': 4}
            ],
            'is_featured': False,
            'is_active': True
        },
        {
            'title': 'Day Trading Bootcamp',
            'short_description': 'Intensive day trading course covering scalping, momentum trading, and intraday strategies for consistent profits.',
            'description': '''Intensive bootcamp designed to teach you everything you need to know about day trading.

Learn proven day trading strategies, risk management techniques, and the psychology needed to be a successful day trader. This course focuses on practical, actionable strategies that you can implement immediately.

Includes live trading sessions, market analysis, and one-on-one mentoring sessions.''',
            'course_type': 'workshop',
            'difficulty_level': 'intermediate',
            'duration_hours': 40,
            'lessons_count': 45,
            'price': Decimal('12999.00'),
            'original_price': Decimal('19999.00'),
            'what_you_learn': '''Day trading strategies and setups
Scalping techniques
Momentum trading
Intraday risk management
Market psychology
Live trading practice
Professional trading tools''',
            'requirements': '''Intermediate trading knowledge
Dedicated trading setup
Minimum capital for practice
Full-time availability during market hours''',
            'course_content': [
                {'module': 'Day Trading Fundamentals', 'lessons': 10},
                {'module': 'Scalping Strategies', 'lessons': 12},
                {'module': 'Momentum Trading', 'lessons': 10},
                {'module': 'Risk Management', 'lessons': 8},
                {'module': 'Live Trading Practice', 'lessons': 5}
            ],
            'is_featured': True,
            'is_active': True,
            'max_students': 20
        },
        {
            'title': 'Forex Trading for Beginners',
            'short_description': 'Complete beginner-friendly course on forex trading covering currency pairs, analysis, and trading strategies.',
            'description': '''Start your forex trading journey with this comprehensive beginner course.

Learn about currency pairs, forex market structure, fundamental and technical analysis specific to forex, and develop profitable trading strategies.

This course is designed for complete beginners with no prior forex experience.''',
            'course_type': 'video',
            'difficulty_level': 'beginner',
            'duration_hours': 15,
            'lessons_count': 20,
            'price': Decimal('3999.00'),
            'what_you_learn': '''Forex market fundamentals
Currency pair analysis
Technical indicators for forex
Fundamental analysis
Risk management
Trading platform usage
Creating a trading plan''',
            'requirements': '''No prior trading experience needed
Computer with internet connection
Basic understanding of economics helpful
Willingness to learn and practice''',
            'course_content': [
                {'module': 'Forex Basics', 'lessons': 5},
                {'module': 'Technical Analysis', 'lessons': 6},
                {'module': 'Fundamental Analysis', 'lessons': 4},
                {'module': 'Trading Strategies', 'lessons': 3},
                {'module': 'Risk Management', 'lessons': 2}
            ],
            'is_featured': False,
            'is_active': True
        },
        {
            'title': 'Algorithmic Trading with Python',
            'short_description': 'Learn to build automated trading systems using Python, covering backtesting, strategy development, and deployment.',
            'description': '''Learn to build sophisticated algorithmic trading systems using Python.

This course covers everything from basic Python programming for trading to advanced strategy development, backtesting, and deployment of automated trading systems.

Perfect for traders who want to automate their strategies and developers interested in quantitative finance.''',
            'course_type': 'video',
            'difficulty_level': 'expert',
            'duration_hours': 50,
            'lessons_count': 60,
            'price': Decimal('15999.00'),
            'original_price': Decimal('24999.00'),
            'what_you_learn': '''Python programming for trading
Data analysis with pandas
Strategy development and backtesting
API integration with brokers
Risk management systems
Portfolio optimization
Machine learning for trading''',
            'requirements': '''Basic programming knowledge
Understanding of trading concepts
Python development environment
Mathematical and statistical background helpful''',
            'course_content': [
                {'module': 'Python for Trading', 'lessons': 15},
                {'module': 'Data Analysis', 'lessons': 12},
                {'module': 'Strategy Development', 'lessons': 15},
                {'module': 'Backtesting Systems', 'lessons': 10},
                {'module': 'Deployment and Automation', 'lessons': 8}
            ],
            'is_featured': True,
            'is_active': True
        }
    ]
    
    created_courses = []
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            title=course_data['title'],
            defaults={
                **course_data,
                'instructor': instructor,
                'slug': course_data['title'].lower().replace(' ', '-').replace(',', ''),
                'currency': 'INR'
            }
        )
        
        if created:
            created_courses.append(course)
            print(f"Created course: {course.title}")
        else:
            print(f"Course already exists: {course.title}")
    
    print(f"\nCreated {len(created_courses)} new courses")
    print(f"Total courses in database: {Course.objects.count()}")
    
    # Display featured courses
    featured_courses = Course.objects.filter(is_featured=True)
    print(f"\nFeatured courses ({featured_courses.count()}):")
    for course in featured_courses:
        print(f"- {course.title} ({course.price_display})")

if __name__ == '__main__':
    create_sample_courses()