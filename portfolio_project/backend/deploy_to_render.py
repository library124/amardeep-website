#!/usr/bin/env python3
"""
Automated deployment preparation script for Render.com
Following SOLID principles for maintainable deployment automation
"""

import os
import sys
import subprocess
import secrets
import string
from pathlib import Path

class RenderDeploymentPrep:
    """
    Single Responsibility: Handle Render deployment preparation
    """
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backend_root = self.project_root  # We're already in the backend directory
        
    def generate_secret_key(self, length: int = 50) -> str:
        """Generate a secure Django secret key"""
        alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def check_requirements(self) -> bool:
        """Check if all required files exist"""
        required_files = [
            'requirements.txt',
            'build.sh',
            'render.yaml',
            'backend/settings_production.py',
            '.env.production'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not (self.backend_root / file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            print(f"❌ Missing required files: {', '.join(missing_files)}")
            return False
        
        print("✅ All required deployment files found")
        return True
    
    def update_settings(self):
        """Update main settings.py to include production settings"""
        settings_path = self.backend_root / "backend" / "settings.py"
        
        if not settings_path.exists():
            print("❌ settings.py not found")
            return False
        
        with open(settings_path, 'r') as f:
            content = f.read()
        
        production_import = """
# Production settings for Render deployment
import os
if 'RENDER' in os.environ:
    from .settings_production import *
"""
        
        if "settings_production" not in content:
            with open(settings_path, 'a') as f:
                f.write(production_import)
            print("✅ Updated settings.py with production configuration")
        else:
            print("✅ Production settings already configured")
        
        return True
    
    def create_env_template(self):
        """Create environment variables template"""
        secret_key = self.generate_secret_key()
        
        env_content = f"""# Environment Variables for Render Deployment
# Copy these values to your Render service environment variables

SECRET_KEY={secret_key}
DEBUG=False
DJANGO_SETTINGS_MODULE=backend.settings_production

# Database (will be provided by Render PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/database

# Frontend Configuration
FRONTEND_URL=https://your-frontend-domain.com

# Email Configuration (Update with your Brevo credentials)
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-brevo-smtp-password
BREVO_API_KEY=your-brevo-api-key

# Payment Gateway (Update with your Razorpay credentials)
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
RAZORPAY_WEBHOOK_SECRET=your-razorpay-webhook-secret

# Server Configuration
WEB_CONCURRENCY=4
"""
        
        env_file = self.backend_root / ".env.render"
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"✅ Created environment template: {env_file}")
        print(f"🔑 Generated SECRET_KEY: {secret_key}")
        
    def run_deployment_check(self):
        """Run Django deployment check"""
        try:
            os.chdir(self.backend_root)
            result = subprocess.run([
                sys.executable, 'manage.py', 'check', '--deploy'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Django deployment check passed")
            else:
                print("⚠️ Django deployment check warnings:")
                print(result.stdout)
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Could not run deployment check: {e}")
    
    def display_next_steps(self):
        """Display next steps for deployment"""
        print("\n" + "="*60)
        print("🚀 RENDER DEPLOYMENT PREPARATION COMPLETE")
        print("="*60)
        print("\n📋 NEXT STEPS:")
        print("1. Push your code to GitHub:")
        print("   git add .")
        print("   git commit -m 'Add Render deployment configuration'")
        print("   git push origin main")
        print("\n2. Go to Render Dashboard (https://dashboard.render.com)")
        print("3. Create a PostgreSQL database")
        print("4. Create a Web Service and connect your GitHub repo")
        print("5. Copy environment variables from .env.render to Render")
        print("\n📖 For detailed instructions, see: RENDER_DEPLOYMENT_GUIDE.md")
        print("\n🎯 Your backend will be live at: https://your-service.onrender.com")
    
    def prepare_deployment(self):
        """Main method to prepare deployment"""
        print("🔧 Preparing Django backend for Render deployment...")
        
        if not self.check_requirements():
            print("❌ Deployment preparation failed")
            return False
        
        self.update_settings()
        self.create_env_template()
        self.run_deployment_check()
        self.display_next_steps()
        
        return True

def main():
    """Main function following Single Responsibility Principle"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    deployment_prep = RenderDeploymentPrep(project_root)
    success = deployment_prep.prepare_deployment()
    
    if success:
        print("\n✅ Deployment preparation completed successfully!")
    else:
        print("\n❌ Deployment preparation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()