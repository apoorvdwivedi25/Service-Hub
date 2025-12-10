#FOR LINUX AND MAC

#!/bin/bash

echo "🚀 ServiceHub Quick Start"
echo "========================="

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create directories
echo "📁 Creating directories..."
mkdir -p media/provider_photos
mkdir -p static

# Run migrations
echo "🗄️  Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "👤 Create your admin account:"
python manage.py createsuperuser

# Run server
echo "🎉 Starting development server..."
python manage.py runserver
