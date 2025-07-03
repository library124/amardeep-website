#!/usr/bin/env python3
"""
Comprehensive deployment script for Amardeep Portfolio Project
Deploys backend to Render.com and frontend to Vercel
Following SOLID principles for maintainable deployment automation

Author: Amardeep Asode
"""

import os
import sys
import json
import subprocess
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import secrets
import string

class DeploymentConfig:
    """Single Responsibility: Manages deployment configuration"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_path = self.project_root / "backend"
        self.frontend_path = self.project_root / "frontend"
        
    def get_backend_env_vars(self) -> Dict[str, str]:
        """Get backend environment variables for production"""
        return {
            'DJANGO_SETTINGS_MODULE': 'backend.settings_production',
            'DEBUG': 'False',
            'ALLOWED_HOSTS': '.onrender.com,localhost,127.0.0.1',
            'SECRET_KEY': self._generate_secret_key(),
            'FRONTEND_URL': 'https://amardeep-portfolio-frontend.vercel.app',
            'RENDER': 'true'
        }
    
    def get_frontend_env_vars(self) -> Dict[str, str]:
        """Get frontend environment variables for production"""
        return {
            'NEXT_PUBLIC_DJANGO_API_URL': 'https://amardeep-portfolio-backend.onrender.com/api',
            'NEXT_PUBLIC_API_URL': 'https://amardeep-portfolio-backend.onrender.com',
            'NODE_ENV': 'production'
        }
    
    def _generate_secret_key(self) -> str:
        """Generate a secure Django secret key"""
        chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
        return ''.join(secrets.choice(chars) for _ in range(50))

class DeploymentValidator:
    """Single Responsibility: Validates deployment prerequisites"""
    
    def __init__(self, config: DeploymentConfig):
        self.config = config
    
    def validate_prerequisites(self) -> Tuple[bool, List[str]]:
        """Validate all deployment prerequisites"""
        errors = []
        
        # Check if required files exist
        required_files = [
            self.config.backend_path / "requirements.txt",
            self.config.backend_path / "manage.py",
            self.config.backend_path / "render.yaml",
            self.config.frontend_path / "package.json",
            self.config.frontend_path / "vercel.json"
        ]
        
        for file_path in required_files:
            if not file_path.exists():
                errors.append(f"Missing required file: {file_path}")
        
        # Check if Git repository is initialized
        if not (self.config.project_root / ".git").exists():
            errors.append("Git repository not initialized")
        
        # Check if environment variables are set
        required_env_vars = [
            'RAZORPAY_KEY_ID',
            'RAZORPAY_KEY_SECRET',
            'EMAIL_HOST_USER',
            'EMAIL_HOST_PASSWORD',
            'BREVO_API_KEY'
        ]
        
        missing_env_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_env_vars:
            errors.append(f"Missing environment variables: {', '.join(missing_env_vars)}")
        
        return len(errors) == 0, errors

class RenderDeployer:
    """Single Responsibility: Handles Render.com deployment"""
    
    def __init__(self, config: DeploymentConfig):
        self.config = config
    
    def prepare_backend_deployment(self) -> bool:
        """Prepare backend for Render.com deployment"""
        try:
            print("🔧 Preparing backend for Render.com deployment...")
            
            # Update render.yaml with current configuration
            self._update_render_config()
            
            # Create production environment file
            self._create_production_env_file()
            
            # Validate Django configuration
            self._validate_django_config()
            
            print("✅ Backend preparation completed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Backend preparation failed: {str(e)}")
            return False
    
    def _update_render_config(self):
        """Update render.yaml with current settings"""
        render_config = {
            "services": [{
                "type": "web",
                "name": "amardeep-portfolio-backend",
                "env": "python",
                "plan": "free",
                "buildCommand": "./build.sh",
                "startCommand": "gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT",
                "envVars": [
                    {"key": "DJANGO_SETTINGS_MODULE", "value": "backend.settings_production"},
                    {"key": "DEBUG", "value": "False"},
                    {"key": "ALLOWED_HOSTS", "value": ".onrender.com,localhost,127.0.0.1"},
                    {"key": "SECRET_KEY", "generateValue": True},
                    {"key": "DATABASE_URL", "fromDatabase": {"name": "portfolio-db", "property": "connectionString"}},
                    {"key": "RAZORPAY_KEY_ID", "sync": False},
                    {"key": "RAZORPAY_KEY_SECRET", "sync": False},
                    {"key": "RAZORPAY_WEBHOOK_SECRET", "sync": False},
                    {"key": "EMAIL_HOST_USER", "sync": False},
                    {"key": "EMAIL_HOST_PASSWORD", "sync": False},
                    {"key": "BREVO_API_KEY", "sync": False},
                    {"key": "FRONTEND_URL", "value": "https://amardeep-portfolio-frontend.vercel.app"},
                    {"key": "RENDER", "value": "true"}
                ],
                "healthCheckPath": "/api/health/"
            }],
            "databases": [{
                "name": "portfolio-db",
                "plan": "free"
            }]
        }
        
        # Write updated render.yaml
        import yaml
        with open(self.config.backend_path / "render.yaml", 'w') as f:
            yaml.dump(render_config, f, default_flow_style=False)
    
    def _create_production_env_file(self):
        """Create production environment file template"""
        env_content = """# Production Environment Variables for Render.com
# Set these in your Render.com dashboard

# Django Configuration
DJANGO_SETTINGS_MODULE=backend.settings_production
DEBUG=False
SECRET_KEY=<generate-secure-key>
ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1

# Database (automatically set by Render)
DATABASE_URL=<postgresql-connection-string>

# Razorpay Configuration
RAZORPAY_KEY_ID=<your-razorpay-key-id>
RAZORPAY_KEY_SECRET=<your-razorpay-key-secret>
RAZORPAY_WEBHOOK_SECRET=<your-razorpay-webhook-secret>

# Email Configuration (Brevo)
EMAIL_HOST_USER=<your-brevo-email>
EMAIL_HOST_PASSWORD=<your-brevo-smtp-password>
BREVO_API_KEY=<your-brevo-api-key>

# Frontend URL
FRONTEND_URL=https://amardeep-portfolio-frontend.vercel.app

# Production Flag
RENDER=true
"""
        
        with open(self.config.backend_path / ".env.production", 'w') as f:
            f.write(env_content)
    
    def _validate_django_config(self):
        """Validate Django configuration for production"""
        os.chdir(self.config.backend_path)
        
        # Set production environment
        os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings_production'
        os.environ['DEBUG'] = 'False'
        
        # Run Django checks
        result = subprocess.run([
            sys.executable, 'manage.py', 'check', '--deploy'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Django configuration validation failed: {result.stderr}")

class VercelDeployer:
    """Single Responsibility: Handles Vercel deployment"""
    
    def __init__(self, config: DeploymentConfig):
        self.config = config
    
    def prepare_frontend_deployment(self) -> bool:
        """Prepare frontend for Vercel deployment"""
        try:
            print("🔧 Preparing frontend for Vercel deployment...")
            
            # Update vercel.json configuration
            self._update_vercel_config()
            
            # Create production environment file
            self._create_production_env_file()
            
            # Validate Next.js configuration
            self._validate_nextjs_config()
            
            print("✅ Frontend preparation completed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Frontend preparation failed: {str(e)}")
            return False
    
    def _update_vercel_config(self):
        """Update vercel.json with optimized settings"""
        vercel_config = {
            "version": 2,
            "name": "amardeep-portfolio-frontend",
            "builds": [{
                "src": "package.json",
                "use": "@vercel/next"
            }],
            "routes": [{
                "src": "/(.*)",
                "dest": "/$1"
            }],
            "env": {
                "NEXT_PUBLIC_DJANGO_API_URL": "https://amardeep-portfolio-backend.onrender.com/api",
                "NEXT_PUBLIC_API_URL": "https://amardeep-portfolio-backend.onrender.com",
                "NODE_ENV": "production"
            },
            "functions": {
                "app/api/**/*.js": {
                    "maxDuration": 30
                }
            },
            "headers": [{
                "source": "/(.*)",
                "headers": [
                    {"key": "X-Content-Type-Options", "value": "nosniff"},
                    {"key": "X-Frame-Options", "value": "DENY"},
                    {"key": "X-XSS-Protection", "value": "1; mode=block"},
                    {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                    {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"}
                ]
            }],
            "redirects": [{
                "source": "/api/(.*)",
                "destination": "https://amardeep-portfolio-backend.onrender.com/api/$1",
                "permanent": False
            }]
        }
        
        with open(self.config.frontend_path / "vercel.json", 'w') as f:
            json.dump(vercel_config, f, indent=2)
    
    def _create_production_env_file(self):
        """Create production environment file for Vercel"""
        env_content = """# Production Environment Variables for Vercel
# Set these in your Vercel dashboard

# API Configuration
NEXT_PUBLIC_DJANGO_API_URL=https://amardeep-portfolio-backend.onrender.com/api
NEXT_PUBLIC_API_URL=https://amardeep-portfolio-backend.onrender.com

# Razorpay Configuration (Public Key Only)
NEXT_PUBLIC_RAZORPAY_KEY_ID=<your-razorpay-key-id>

# Environment
NODE_ENV=production
"""
        
        with open(self.config.frontend_path / ".env.production", 'w') as f:
            f.write(env_content)
    
    def _validate_nextjs_config(self):
        """Validate Next.js configuration"""
        os.chdir(self.config.frontend_path)
        
        # Check if package.json exists and has required scripts
        with open("package.json", 'r') as f:
            package_data = json.load(f)
        
        required_scripts = ['build', 'start']
        missing_scripts = [script for script in required_scripts if script not in package_data.get('scripts', {})]
        
        if missing_scripts:
            raise Exception(f"Missing required scripts in package.json: {missing_scripts}")

class DeploymentOrchestrator:
    """Single Responsibility: Orchestrates the entire deployment process"""
    
    def __init__(self):
        self.config = DeploymentConfig()
        self.validator = DeploymentValidator(self.config)
        self.render_deployer = RenderDeployer(self.config)
        self.vercel_deployer = VercelDeployer(self.config)
    
    def deploy(self) -> bool:
        """Execute complete deployment process"""
        print("🚀 Starting deployment process...")
        print("=" * 60)
        
        # Step 1: Validate prerequisites
        print("1️⃣ Validating prerequisites...")
        is_valid, errors = self.validator.validate_prerequisites()
        
        if not is_valid:
            print("❌ Prerequisites validation failed:")
            for error in errors:
                print(f"   • {error}")
            return False
        
        print("✅ Prerequisites validation passed")
        
        # Step 2: Prepare backend deployment
        print("\n2️⃣ Preparing backend deployment...")
        if not self.render_deployer.prepare_backend_deployment():
            return False
        
        # Step 3: Prepare frontend deployment
        print("\n3️⃣ Preparing frontend deployment...")
        if not self.vercel_deployer.prepare_frontend_deployment():
            return False
        
        # Step 4: Generate deployment instructions
        print("\n4️⃣ Generating deployment instructions...")
        self._generate_deployment_instructions()
        
        print("\n" + "=" * 60)
        print("🎉 Deployment preparation completed successfully!")
        print("📋 Check the generated deployment instructions for next steps.")
        
        return True
    
    def _generate_deployment_instructions(self):
        """Generate comprehensive deployment instructions"""
        instructions = """
# 🚀 Deployment Instructions

## Prerequisites Completed ✅
- Backend configuration prepared for Render.com
- Frontend configuration prepared for Vercel
- Environment files created
- Configuration files updated

## Next Steps:

### 1. Backend Deployment (Render.com)

1. **Create Database:**
   - Go to Render.com dashboard
   - Create new PostgreSQL database named 'portfolio-db'
   - Note the connection string

2. **Create Web Service:**
   - Create new Web Service
   - Connect your GitHub repository
   - Set root directory to 'portfolio_project/backend'
   - Build command: `./build.sh`
   - Start command: `gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`

3. **Set Environment Variables:**
   Copy from `.env.production` file and set in Render dashboard:
   - DJANGO_SETTINGS_MODULE=backend.settings_production
   - DEBUG=False
   - SECRET_KEY=(generate secure key)
   - DATABASE_URL=(auto-set by Render)
   - RAZORPAY_KEY_ID=your_key
   - RAZORPAY_KEY_SECRET=your_secret
   - EMAIL_HOST_USER=your_email
   - EMAIL_HOST_PASSWORD=your_password
   - BREVO_API_KEY=your_api_key
   - FRONTEND_URL=https://amardeep-portfolio-frontend.vercel.app

4. **Deploy:**
   - Connect PostgreSQL database to web service
   - Deploy the service
   - Test health endpoint: https://your-backend.onrender.com/api/health/

### 2. Frontend Deployment (Vercel)

1. **Import Project:**
   - Go to Vercel dashboard
   - Import from GitHub
   - Set root directory to 'portfolio_project/frontend'

2. **Set Environment Variables:**
   Copy from `.env.production` file and set in Vercel dashboard:
   - NEXT_PUBLIC_DJANGO_API_URL=https://your-backend.onrender.com/api
   - NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
   - NEXT_PUBLIC_RAZORPAY_KEY_ID=your_public_key

3. **Deploy:**
   - Deploy the project
   - Test the deployment
   - Verify API connectivity

### 3. Post-Deployment

1. **Update CORS Settings:**
   - Add your Vercel domain to CORS_ALLOWED_ORIGINS in Django settings

2. **Test Integration:**
   - Test frontend-backend communication
   - Test payment integration
   - Test email functionality

3. **Monitor:**
   - Check logs in both platforms
   - Monitor performance
   - Set up alerts

## 🔧 Troubleshooting

- **CORS Issues:** Ensure frontend domain is in CORS_ALLOWED_ORIGINS
- **Database Issues:** Check DATABASE_URL and migrations
- **Build Failures:** Check build logs and dependencies
- **API Issues:** Verify environment variables and endpoints

## 📞 Support

For deployment issues:
1. Check platform documentation (Render.com, Vercel)
2. Review application logs
3. Verify environment variables
4. Test endpoints individually

---
Generated by Amardeep Portfolio Deployment Script
"""
        
        with open(self.config.project_root / "DEPLOYMENT_INSTRUCTIONS.md", 'w') as f:
            f.write(instructions)

def main():
    """Main deployment function"""
    try:
        orchestrator = DeploymentOrchestrator()
        success = orchestrator.deploy()
        
        if success:
            print("\n🎯 Deployment preparation completed successfully!")
            print("📖 Read DEPLOYMENT_INSTRUCTIONS.md for next steps")
            sys.exit(0)
        else:
            print("\n💥 Deployment preparation failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()