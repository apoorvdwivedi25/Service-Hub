@echo off
echo 🚀 ServiceHub Quick Start
echo =========================

echo 📦 Creating virtual environment...
python -m venv venv

echo ✅ Activating virtual environment...
call venv\Scripts\activate

echo 📚 Installing dependencies...
pip install -r requirements.txt

echo 📁 Creating directories...
mkdir media\provider_photos
mkdir static

echo 🗄️  Running migrations...
python manage.py makemigrations
python manage.py migrate

echo 👤 Create your admin account:
python manage.py createsuperuser

echo 🎉 Starting development server...
python manage.py runserver
