#!/usr/bin/env bash
# Build script for Render.com deployment
# Following SOLID principles for robust deployment

set -o errexit  # Exit on error

echo "🚀 Starting build process for Render.com..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Set environment variables for build
export DJANGO_SETTINGS_MODULE=backend.settings
export DEBUG=False

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist (optional)
echo "👤 Creating superuser if needed..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
EOF

# Test Django setup
echo "🧪 Testing Django setup..."
python manage.py check --deploy

echo "✅ Build completed successfully!"
echo "🌐 Application is ready for deployment"