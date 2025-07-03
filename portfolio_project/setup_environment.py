#!/usr/bin/env python3
"""
Environment Setup Script for Amardeep Portfolio Project
Sets up development and production environments
Following SOLID principles for maintainable configuration

Author: Amardeep Asode
"""

import os
import sys
import json
import secrets
import string
from pathlib import Path
from typing import Dict, List, Optional
import subprocess

class EnvironmentConfig:
    """Single Responsibility: Manages environment configuration"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.backend_path = project_root / "backend"
        self.frontend_path = project_root / "frontend"
    
    def generate_secret_key(self, length: int = 50) -> str:
        """Generate a secure Django secret key"""
        chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    def get_development_backend_env(self) -> Dict[str, str]:
        """Get development environment variables for backend"""
        return {
            'DJANGO_SETTINGS_MODULE': 'backend.settings',
            'DEBUG': 'True',
            'SECRET_KEY': self.generate_secret_key(),
            'ALLOWED_HOSTS': 'localhost,127.0.0.1',
            'DATABASE_URL': 'sqlite:///./db.sqlite3',
            'FRONTEND_URL': 'http://localhost:3000',
            'EMAIL_HOST_USER': 'your-email@gmail.com',
            'EMAIL_HOST_PASSWORD': 'your-email-password',
            'BREVO_API_KEY': 'your-brevo-api-key',
            'RAZORPAY_KEY_ID': 'your-razorpay-key-id',
            'RAZORPAY_KEY_SECRET': 'your-razorpay-key-secret',
            'RAZORPAY_WEBHOOK_SECRET': 'your-razorpay-webhook-secret'
        }
    
    def get_production_backend_env(self) -> Dict[str, str]:
        """Get production environment variables for backend"""
        return {
            'DJANGO_SETTINGS_MODULE': 'backend.settings_production',
            'DEBUG': 'False',
            'SECRET_KEY': self.generate_secret_key(),
            'ALLOWED_HOSTS': '.onrender.com,localhost,127.0.0.1',
            'DATABASE_URL': 'postgresql://user:password@host:port/database',
            'FRONTEND_URL': 'https://amardeep-portfolio-frontend.vercel.app',
            'RENDER': 'true',
            'EMAIL_HOST_USER': 'your-email@gmail.com',
            'EMAIL_HOST_PASSWORD': 'your-email-password',
            'BREVO_API_KEY': 'your-brevo-api-key',
            'RAZORPAY_KEY_ID': 'your-razorpay-key-id',
            'RAZORPAY_KEY_SECRET': 'your-razorpay-key-secret',
            'RAZORPAY_WEBHOOK_SECRET': 'your-razorpay-webhook-secret'
        }
    
    def get_development_frontend_env(self) -> Dict[str, str]:
        """Get development environment variables for frontend"""
        return {
            'NEXT_PUBLIC_DJANGO_API_URL': 'http://localhost:8000/api',
            'NEXT_PUBLIC_API_URL': 'http://localhost:8000',
            'NEXT_PUBLIC_RAZORPAY_KEY_ID': 'your-razorpay-key-id',
            'NODE_ENV': 'development'
        }
    
    def get_production_frontend_env(self) -> Dict[str, str]:
        """Get production environment variables for frontend"""
        return {
            'NEXT_PUBLIC_DJANGO_API_URL': 'https://amardeep-portfolio-backend.onrender.com/api',
            'NEXT_PUBLIC_API_URL': 'https://amardeep-portfolio-backend.onrender.com',
            'NEXT_PUBLIC_RAZORPAY_KEY_ID': 'your-razorpay-key-id',
            'NODE_ENV': 'production'
        }

class EnvironmentFileManager:
    """Single Responsibility: Manages environment file creation and updates"""
    
    def __init__(self, config: EnvironmentConfig):
        self.config = config
    
    def create_env_file(self, file_path: Path, env_vars: Dict[str, str], 
                       description: str = "") -> bool:
        """Create environment file with variables"""
        try:
            content = []
            
            if description:
                content.append(f"# {description}")
                content.append("")
            
            for key, value in env_vars.items():
                content.append(f"{key}={value}")
            
            with open(file_path, 'w') as f:
                f.write('\n'.join(content))
            
            print(f"✅ Created {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create {file_path}: {str(e)}")
            return False
    
    def update_env_file(self, file_path: Path, updates: Dict[str, str]) -> bool:
        """Update existing environment file"""
        try:
            # Read existing content
            existing_vars = {}
            if file_path.exists():
                with open(file_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            existing_vars[key] = value
            
            # Update with new values
            existing_vars.update(updates)
            
            # Write updated content
            content = []
            for key, value in existing_vars.items():
                content.append(f"{key}={value}")
            
            with open(file_path, 'w') as f:
                f.write('\n'.join(content))
            
            print(f"✅ Updated {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update {file_path}: {str(e)}")
            return False

class DependencyManager:
    """Single Responsibility: Manages project dependencies"""
    
    def __init__(self, config: EnvironmentConfig):
        self.config = config
    
    def install_backend_dependencies(self) -> bool:
        """Install backend Python dependencies"""
        try:
            print("📦 Installing backend dependencies...")
            
            os.chdir(self.config.backend_path)
            
            # Create virtual environment if it doesn't exist
            venv_path = self.config.backend_path / "venv"
            if not venv_path.exists():
                print("Creating virtual environment...")
                subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            
            # Install dependencies
            if os.name == 'nt':  # Windows
                pip_path = venv_path / "Scripts" / "pip"
            else:  # Unix/Linux/macOS
                pip_path = venv_path / "bin" / "pip"
            
            subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
            
            print("✅ Backend dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install backend dependencies: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error installing backend dependencies: {str(e)}")
            return False
    
    def install_frontend_dependencies(self) -> bool:
        """Install frontend Node.js dependencies"""
        try:
            print("📦 Installing frontend dependencies...")
            
            os.chdir(self.config.frontend_path)
            
            # Check if npm is available
            subprocess.run(["npm", "--version"], check=True, capture_output=True)
            
            # Install dependencies
            subprocess.run(["npm", "install"], check=True)
            
            print("✅ Frontend dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install frontend dependencies: {str(e)}")
            return False
        except FileNotFoundError:
            print("❌ npm not found. Please install Node.js and npm")
            return False
        except Exception as e:
            print(f"❌ Unexpected error installing frontend dependencies: {str(e)}")
            return False

class DatabaseManager:
    """Single Responsibility: Manages database setup"""
    
    def __init__(self, config: EnvironmentConfig):
        self.config = config
    
    def setup_development_database(self) -> bool:
        """Set up development database"""
        try:
            print("🗄️ Setting up development database...")
            
            os.chdir(self.config.backend_path)
            
            # Set environment for Django
            os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
            
            # Run migrations
            subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
            
            # Create superuser if needed
            self._create_superuser()
            
            print("✅ Development database setup completed")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to setup database: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error setting up database: {str(e)}")
            return False
    
    def _create_superuser(self):
        """Create superuser for development"""
        try:
            # Check if superuser already exists
            check_script = """
from django.contrib.auth import get_user_model
User = get_user_model()
if User.objects.filter(username='admin').exists():
    print('Superuser already exists')
else:
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
"""
            
            subprocess.run([
                sys.executable, "manage.py", "shell", "-c", check_script
            ], check=True)
            
        except Exception as e:
            print(f"Warning: Could not create superuser: {str(e)}")

class EnvironmentSetup:
    """Single Responsibility: Orchestrates environment setup"""
    
    def __init__(self, project_root: Optional[Path] = None):
        if project_root is None:
            project_root = Path(__file__).parent
        
        self.config = EnvironmentConfig(project_root)
        self.file_manager = EnvironmentFileManager(self.config)
        self.dependency_manager = DependencyManager(self.config)
        self.database_manager = DatabaseManager(self.config)
    
    def setup_development_environment(self) -> bool:
        """Set up complete development environment"""
        print("🚀 Setting up development environment...")
        print("=" * 60)
        
        success = True
        
        # Create environment files
        print("\n1️⃣ Creating environment files...")
        
        # Backend .env
        backend_env = self.config.get_development_backend_env()
        if not self.file_manager.create_env_file(
            self.config.backend_path / ".env",
            backend_env,
            "Development Environment Variables for Django Backend"
        ):
            success = False
        
        # Frontend .env.local
        frontend_env = self.config.get_development_frontend_env()
        if not self.file_manager.create_env_file(
            self.config.frontend_path / ".env.local",
            frontend_env,
            "Development Environment Variables for Next.js Frontend"
        ):
            success = False
        
        # Install dependencies
        print("\n2️⃣ Installing dependencies...")
        if not self.dependency_manager.install_backend_dependencies():
            success = False
        
        if not self.dependency_manager.install_frontend_dependencies():
            success = False
        
        # Setup database
        print("\n3️⃣ Setting up database...")
        if not self.database_manager.setup_development_database():
            success = False
        
        # Generate instructions
        print("\n4️⃣ Generating setup instructions...")
        self._generate_development_instructions()
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 Development environment setup completed successfully!")
            print("📖 Check DEVELOPMENT_SETUP.md for next steps")
        else:
            print("�� Development environment setup completed with errors!")
            print("Please check the error messages above and resolve them")
        
        return success
    
    def setup_production_environment(self) -> bool:
        """Set up production environment files"""
        print("🚀 Setting up production environment files...")
        print("=" * 60)
        
        success = True
        
        # Create production environment files
        print("\n1️⃣ Creating production environment files...")
        
        # Backend production .env
        backend_env = self.config.get_production_backend_env()
        if not self.file_manager.create_env_file(
            self.config.backend_path / ".env.production",
            backend_env,
            "Production Environment Variables for Django Backend (Render.com)"
        ):
            success = False
        
        # Frontend production .env
        frontend_env = self.config.get_production_frontend_env()
        if not self.file_manager.create_env_file(
            self.config.frontend_path / ".env.production",
            frontend_env,
            "Production Environment Variables for Next.js Frontend (Vercel)"
        ):
            success = False
        
        # Generate instructions
        print("\n2️⃣ Generating production setup instructions...")
        self._generate_production_instructions()
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 Production environment files created successfully!")
            print("📖 Check PRODUCTION_SETUP.md for deployment instructions")
        else:
            print("💥 Production environment setup completed with errors!")
        
        return success
    
    def _generate_development_instructions(self):
        """Generate development setup instructions"""
        instructions = """
# Development Environment Setup

## Environment Setup Completed ✅

The development environment has been configured with the following:

### Backend (Django)
- Virtual environment created in `backend/venv/`
- Dependencies installed from `requirements.txt`
- Environment variables configured in `backend/.env`
- SQLite database initialized
- Superuser created: `admin` / `admin123`

### Frontend (Next.js)
- Dependencies installed from `package.json`
- Environment variables configured in `frontend/.env.local`

## Next Steps

### 1. Start Backend Server
```bash
cd backend
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
python manage.py runserver
```

### 2. Start Frontend Server
```bash
cd frontend
npm run dev
```

### 3. Access Applications
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/
- Django Admin: http://localhost:8000/admin/

### 4. Configure Services

#### Email Service (Brevo)
1. Sign up at https://www.brevo.com/
2. Get your API key and SMTP credentials
3. Update `.env` file with your credentials

#### Payment Gateway (Razorpay)
1. Sign up at https://razorpay.com/
2. Get your test API keys
3. Update `.env` and `.env.local` files

### 5. Test the Application
- Register a new user
- Test authentication
- Test payment integration (use test mode)
- Test email functionality

## Troubleshooting

### Common Issues
1. **Port already in use**: Change ports in the start commands
2. **Database errors**: Run `python manage.py migrate`
3. **Permission errors**: Check file permissions
4. **Module not found**: Ensure virtual environment is activated

### Getting Help
- Check Django logs for backend issues
- Check browser console for frontend issues
- Review environment variable configuration

---
Generated by Environment Setup Script
"""
        
        with open(self.config.project_root / "DEVELOPMENT_SETUP.md", 'w') as f:
            f.write(instructions)
    
    def _generate_production_instructions(self):
        """Generate production setup instructions"""
        instructions = """
# Production Environment Setup

## Environment Files Created ✅

Production environment files have been created:
- `backend/.env.production` - Backend environment variables
- `frontend/.env.production` - Frontend environment variables

## Deployment Instructions

### 1. Backend Deployment (Render.com)

#### Prerequisites
- GitHub repository with your code
- Render.com account
- PostgreSQL database on Render

#### Steps
1. **Create PostgreSQL Database**
   - Go to Render.com dashboard
   - Create new PostgreSQL database
   - Name: `portfolio-db`
   - Plan: Free or paid

2. **Create Web Service**
   - Create new Web Service
   - Connect GitHub repository
   - Root directory: `portfolio_project/backend`
   - Build command: `./build.sh`
   - Start command: `gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`

3. **Set Environment Variables**
   Copy from `.env.production` and set in Render dashboard:
   ```
   DJANGO_SETTINGS_MODULE=backend.settings_production
   DEBUG=False
   SECRET_KEY=<generate-secure-key>
   DATABASE_URL=<auto-set-by-render>
   RAZORPAY_KEY_ID=<your-key>
   RAZORPAY_KEY_SECRET=<your-secret>
   EMAIL_HOST_USER=<your-email>
   EMAIL_HOST_PASSWORD=<your-password>
   BREVO_API_KEY=<your-api-key>
   FRONTEND_URL=https://amardeep-portfolio-frontend.vercel.app
   ```

4. **Deploy**
   - Connect PostgreSQL database
   - Deploy the service
   - Test: https://your-backend.onrender.com/api/health/

### 2. Frontend Deployment (Vercel)

#### Prerequisites
- Vercel account
- GitHub repository

#### Steps
1. **Import Project**
   - Go to Vercel dashboard
   - Import from GitHub
   - Root directory: `portfolio_project/frontend`

2. **Set Environment Variables**
   Copy from `.env.production` and set in Vercel dashboard:
   ```
   NEXT_PUBLIC_DJANGO_API_URL=https://your-backend.onrender.com/api
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
   NEXT_PUBLIC_RAZORPAY_KEY_ID=<your-public-key>
   ```

3. **Deploy**
   - Deploy the project
   - Test the deployment

### 3. Post-Deployment

#### Update CORS Settings
Add your Vercel domain to Django CORS settings:
```python
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend.vercel.app",
    # ... other domains
]
```

#### Test Integration
- Test frontend-backend communication
- Test payment flow
- Test email functionality
- Monitor logs for errors

## Security Checklist

- [ ] All environment variables are set correctly
- [ ] Secret keys are generated and secure
- [ ] CORS is configured properly
- [ ] HTTPS is enabled on both services
- [ ] Database credentials are secure
- [ ] API keys are not exposed in frontend

## Monitoring

Use the monitoring script to check deployment health:
```bash
python monitor_deployment.py --mode check
```

---
Generated by Environment Setup Script
"""
        
        with open(self.config.project_root / "PRODUCTION_SETUP.md", 'w') as f:
            f.write(instructions)

def main():
    """Main setup function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup Amardeep Portfolio Environment')
    parser.add_argument('--mode', choices=['dev', 'prod', 'both'], 
                       default='dev', help='Setup mode')
    parser.add_argument('--project-root', type=Path, 
                       help='Project root directory')
    
    args = parser.parse_args()
    
    try:
        setup = EnvironmentSetup(args.project_root)
        
        if args.mode == 'dev':
            success = setup.setup_development_environment()
        elif args.mode == 'prod':
            success = setup.setup_production_environment()
        elif args.mode == 'both':
            dev_success = setup.setup_development_environment()
            prod_success = setup.setup_production_environment()
            success = dev_success and prod_success
        
        if success:
            print("\n🎯 Environment setup completed successfully!")
            sys.exit(0)
        else:
            print("\n💥 Environment setup completed with errors!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()