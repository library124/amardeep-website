#!/usr/bin/env python
import os
import sys
import django
import requests

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from portfolio_app.models import Course

def test_course_api():
    print("Testing Course API...")
    
    # Check if courses exist in database
    courses = Course.objects.all()
    print(f"Courses in database: {courses.count()}")
    
    for course in courses[:3]:  # Show first 3 courses
        print(f"- {course.title} ({course.price_display})")
    
    # Test API endpoints (assuming server is running on port 8000)
    base_url = "http://localhost:8000/api"
    
    endpoints_to_test = [
        "/courses/",
        "/courses/featured/",
        "/api/create-order/",
    ]
    
    for endpoint in endpoints_to_test:
        try:
            url = base_url + endpoint
            print(f"\nTesting: {url}")
            
            if endpoint == "/api/create-order/":
                # Test POST endpoint
                data = {
                    "course_id": courses.first().id if courses.exists() else 1,
                    "email": "test@example.com"
                }
                response = requests.post(url, json=data, timeout=5)
            else:
                # Test GET endpoint
                response = requests.get(url, timeout=5)
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"Response: {len(data)} items")
                    if data:
                        print(f"First item keys: {list(data[0].keys())}")
                else:
                    print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            else:
                print(f"Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    test_course_api()