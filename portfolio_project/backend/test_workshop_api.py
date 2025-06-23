#!/usr/bin/env python
"""
Test script to verify Workshop API endpoints are working correctly
"""
import requests
import json
from datetime import datetime

# API base URL
BASE_URL = 'http://localhost:8000/api'

def test_api_endpoint(url, description):
    """Test an API endpoint and display results"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS - Received {len(data) if isinstance(data, list) else 1} item(s)")
            
            # Display first item details if it's a list
            if isinstance(data, list) and len(data) > 0:
                first_item = data[0]
                print(f"\nFirst item details:")
                print(f"  Title: {first_item.get('title', 'N/A')}")
                print(f"  Slug: {first_item.get('slug', 'N/A')}")
                print(f"  Price: {first_item.get('price_display', 'N/A')}")
                print(f"  Status: {first_item.get('status', 'N/A')}")
                print(f"  Featured: {first_item.get('is_featured', 'N/A')}")
            elif not isinstance(data, list):
                print(f"\nItem details:")
                print(f"  Title: {data.get('title', 'N/A')}")
                print(f"  Description: {data.get('short_description', 'N/A')[:100]}...")
                
        else:
            print(f"❌ FAILED - Status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR - Make sure Django server is running on localhost:8000")
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT ERROR - Request took too long")
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")

def main():
    """Run all API tests"""
    print("🚀 Workshop API Testing Suite")
    print("Make sure Django server is running: python manage.py runserver")
    
    # Test all workshop endpoints
    endpoints = [
        (f"{BASE_URL}/workshops/", "All Workshops"),
        (f"{BASE_URL}/workshops/featured/", "Featured Workshops"),
        (f"{BASE_URL}/workshops/upcoming/", "Upcoming Workshops"),
        (f"{BASE_URL}/workshops/?type=free", "Free Workshops"),
        (f"{BASE_URL}/workshops/?type=paid", "Paid Workshops"),
        (f"{BASE_URL}/workshops/?status=upcoming", "Workshops by Status"),
        (f"{BASE_URL}/workshops/stock-market-fundamentals-for-beginners/", "Workshop Detail (Free)"),
        (f"{BASE_URL}/workshops/advanced-intraday-trading-strategies/", "Workshop Detail (Paid)"),
    ]
    
    for url, description in endpoints:
        test_api_endpoint(url, description)
    
    print(f"\n{'='*60}")
    print("🎯 API Testing Complete!")
    print("If all tests passed, your Workshop system is fully functional!")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()