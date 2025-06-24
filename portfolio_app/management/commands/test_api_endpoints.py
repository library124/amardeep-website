from django.core.management.base import BaseCommand
from django.test import Client
import json

class Command(BaseCommand):
    help = 'Test API endpoints to verify they work correctly'

    def handle(self, *args, **options):
        client = Client()
        
        self.stdout.write("=== Testing API Endpoints ===")
        
        # Test upcoming workshops
        self.stdout.write("\n--- Testing /api/workshops/upcoming/ ---")
        response = client.get('/api/workshops/upcoming/')
        self.stdout.write(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            self.stdout.write(f"Workshop Count: {len(data)}")
            for workshop in data:
                self.stdout.write(f"- {workshop['title']}")
        
        # Test active workshops
        self.stdout.write("\n--- Testing /api/workshops/active/ ---")
        response = client.get('/api/workshops/active/')
        self.stdout.write(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            self.stdout.write(f"Workshop Count: {len(data)}")
            for workshop in data:
                self.stdout.write(f"- {workshop['title']}")
        
        # Test featured blog posts
        self.stdout.write("\n--- Testing /api/blog/featured/ ---")
        response = client.get('/api/blog/featured/')
        self.stdout.write(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            self.stdout.write(f"Blog Post Count: {len(data)}")
            for post in data:
                self.stdout.write(f"- {post['title']}")
        
        # Test all blog posts
        self.stdout.write("\n--- Testing /api/blog/ ---")
        response = client.get('/api/blog/')
        self.stdout.write(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            self.stdout.write(f"Blog Post Count: {len(data)}")
            for post in data:
                self.stdout.write(f"- {post['title']}")
        
        self.stdout.write("\n=== API Testing Complete ===")