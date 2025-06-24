#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection
from django.contrib.auth.models import User
from portfolio_app.models import *

def check_database():
    print("=== DATABASE STATUS CHECK ===")
    
    # Check SQLite tables
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"\n📊 SQLite Tables ({len(tables)}):")
    for table in sorted(tables):
        print(f"  - {table}")
    
    # Check data counts
    print(f"\n📈 Data Counts:")
    try:
        print(f"  - Users: {User.objects.count()}")
        print(f"  - Workshops: {Workshop.objects.count()}")
        print(f"  - Blog Posts: {BlogPost.objects.count()}")
        print(f"  - Trading Services: {TradingService.objects.count()}")
        print(f"  - Achievements: {Achievement.objects.count()}")
        print(f"  - Newsletter Subscribers: {Subscriber.objects.count()}")
    except Exception as e:
        print(f"  Error getting counts: {e}")
    
    # Check recent data
    print(f"\n🔍 Recent Data:")
    try:
        recent_workshops = Workshop.objects.order_by('-created_at')[:3]
        print(f"  Recent Workshops:")
        for w in recent_workshops:
            print(f"    - {w.title} ({w.status})")
        
        recent_posts = BlogPost.objects.order_by('-created_at')[:3]
        print(f"  Recent Blog Posts:")
        for p in recent_posts:
            print(f"    - {p.title} ({p.status})")
            
    except Exception as e:
        print(f"  Error getting recent data: {e}")

if __name__ == "__main__":
    check_database()