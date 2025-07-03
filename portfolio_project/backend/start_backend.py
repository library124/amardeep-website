#!/usr/bin/env python3
"""
Backend Startup Script
Checks if Django server is running and starts it if needed
Following SOLID principles for robust startup management
"""

import os
import sys
import subprocess
import time
import requests
import signal
from pathlib import Path

class BackendManager:
    """
    Single Responsibility: Manages Django backend startup and health
    Open/Closed: Extensible for different server types
    """
    
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.base_url = f'http://{host}:{port}'
        self.health_url = f'{self.base_url}/api/health/'
        self.backend_dir = Path(__file__).parent
        self.manage_py = self.backend_dir / 'manage.py'
        
    def is_server_running(self):
        """Check if Django server is already running"""
        try:
            response = requests.get(self.health_url, timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        try:
            import django
            import rest_framework
            import corsheaders
            print(f"✅ Django {django.get_version()} installed")
            print(f"✅ Django REST Framework installed")
            print(f"✅ Django CORS Headers installed")
            return True
        except ImportError as e:
            print(f"❌ Missing dependency: {e}")
            return False
    
    def run_migrations(self):
        """Run Django migrations"""
        try:
            print("🔄 Running Django migrations...")
            result = subprocess.run([
                sys.executable, str(self.manage_py), 'migrate'
            ], cwd=self.backend_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Migrations completed successfully")
                return True
            else:
                print(f"❌ Migration failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error running migrations: {e}")
            return False
    
    def collect_static(self):
        """Collect static files"""
        try:
            print("🔄 Collecting static files...")
            result = subprocess.run([
                sys.executable, str(self.manage_py), 'collectstatic', '--noinput'
            ], cwd=self.backend_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Static files collected successfully")
                return True
            else:
                print(f"⚠️ Static collection warning: {result.stderr}")
                return True  # Non-critical for development
        except Exception as e:
            print(f"⚠️ Error collecting static files: {e}")
            return True  # Non-critical for development
    
    def start_server(self):
        """Start Django development server"""
        try:
            print(f"🚀 Starting Django server on {self.host}:{self.port}...")
            
            # Start server in background
            process = subprocess.Popen([
                sys.executable, str(self.manage_py), 'runserver', 
                f'{self.host}:{self.port}'
            ], cwd=self.backend_dir)
            
            # Wait for server to start
            print("⏳ Waiting for server to start...")
            for i in range(30):  # Wait up to 30 seconds
                time.sleep(1)
                if self.is_server_running():
                    print(f"✅ Django server is running at {self.base_url}")
                    return process
                print(f"   Checking... ({i+1}/30)")
            
            print("❌ Server failed to start within 30 seconds")
            process.terminate()
            return None
            
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return None
    
    def setup_and_start(self):
        """Complete setup and startup process"""
        print("🔧 Django Backend Manager")
        print("=" * 50)
        
        # Check if server is already running
        if self.is_server_running():
            print(f"✅ Django server is already running at {self.base_url}")
            return True
        
        # Check dependencies
        if not self.check_dependencies():
            print("\n💡 To install dependencies, run:")
            print("   pip install -r requirements.txt")
            return False
        
        # Run migrations
        if not self.run_migrations():
            return False
        
        # Collect static files
        self.collect_static()
        
        # Start server
        process = self.start_server()
        if process:
            print("\n🎉 Backend is ready!")
            print(f"   API Base URL: {self.base_url}/api/")
            print(f"   Health Check: {self.health_url}")
            print(f"   Admin Panel: {self.base_url}/admin/")
            print("\n💡 Press Ctrl+C to stop the server")
            
            try:
                # Keep script running
                while True:
                    time.sleep(1)
                    if not self.is_server_running():
                        print("⚠️ Server appears to have stopped")
                        break
            except KeyboardInterrupt:
                print("\n🛑 Stopping server...")
                process.terminate()
                process.wait()
                print("✅ Server stopped")
            
            return True
        
        return False

def main():
    """Main entry point"""
    manager = BackendManager()
    
    try:
        success = manager.setup_and_start()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()