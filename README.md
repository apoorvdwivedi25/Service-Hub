# 🛠️ ServiceHub - Modern Service Marketplace

A comprehensive Django-based service marketplace platform connecting customers with verified service providers across India. Built with modern UI/UX using Tailwind CSS and DaisyUI.

![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Integration](#api-integration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## ✨ Features

### 🔐 Authentication & Security
- **Dual User System**: Separate registration/login for Customers and Service Providers
- **Phone-based Authentication**: 10-digit Indian phone numbers as primary identifiers
- **OTP Verification**: Forgot password with SMS OTP (MSG91 integration ready)
- **Aadhar Verification**: Service providers verified using Aadhar numbers
- **Secure Password Management**: Built-in Django authentication with password change

### 👥 User Management
- **Customer Features**:
  - Browse services by district
  - Search and filter providers by name and rating
  - Add and edit reviews with star ratings
  - Profile management with district selection
  
- **Provider Features**:
  - Register with up to 3 services
  - Profile with photo upload
  - View reviews and ratings
  - District-based service area
  - Admin verification system

### 🎯 Service Categories
- Mason
- Painter
- Plumber
- Carpenter
- Electrician
- Tile/Marble Worker
- Steel Fabricator
- Glass Worker
- Gardener
- Driver

### 🔍 Advanced Filtering
- **Search by Name**: Real-time provider name search
- **Filter by Rating**: 2.0+, 3.0+, 3.5+, 4.0+, 4.5+ stars
- **Sort Options**: By rating, reviews, name, or date joined
- **District-based**: Automatic filtering by customer's district

### 🎨 Modern UI/UX
- **Dark Mode**: Sleek dark theme with glassmorphism effects
- **Responsive Design**: Mobile-first, works on all devices
- **Micro-animations**: Smooth transitions and hover effects
- **DaisyUI Components**: Modern, accessible UI components
- **Tailwind CSS**: Utility-first styling

### ⭐ Review System
- 5-star rating system
- Written reviews with comments
- Automatic provider rating calculation
- Edit your own reviews
- Review count display

### 📍 Location-based
- **75+ Indian Districts** covered across major states
- District selection during registration
- Automatic provider filtering by district
- Change district anytime from profile

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 4.2.7
- **Database**: SQLite (Development) / PostgreSQL (Production ready)
- **Authentication**: Django's built-in auth system
- **ORM**: Django ORM

### Frontend
- **CSS Framework**: Tailwind CSS 3.x
- **Component Library**: DaisyUI 4.x
- **Icons**: Font Awesome 6.x
- **Fonts**: Google Fonts (Inter)
- **JavaScript**: Vanilla JS (no framework)

### External Services
- **SMS Gateway**: MSG91 (OTP delivery)
- **Image Storage**: Local storage (Development) / AWS S3 ready

---

## 📸 Screenshots

### Landing Page
Modern hero section with gradient animations

### Service Cards
Interactive service selection with hover effects

### Provider Listings
Grid layout with filtering and sorting

### Profile Management
Clean profile editing interface

### Review System
Star ratings with detailed feedback

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- Git

### Step 1: Clone Repository
```bash
git clone <your-repository-url>
cd Application/service
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

Create a `.env` file in the project root:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Optional for Production)
DB_NAME=servicehub_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# MSG91 Configuration
MSG91_AUTH_KEY=your-msg91-auth-key
MSG91_TEMPLATE_ID=your-template-id
MSG91_SENDER_ID=SVCHUB
USE_REAL_SMS=False

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

### Step 5: Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
# Enter phone: 9999999999
# Enter name: Admin
# Choose user_type: customer
# Enter password: admin123
```

### Step 6: Create Media Directories
```bash
mkdir media
mkdir media/provider_photos
mkdir static
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## ⚙️ Configuration

### settings.py Key Configurations
```python
# Custom User Model
AUTH_USER_MODEL = 'services.User'

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# MSG91 SMS Configuration
MSG91_AUTH_KEY = os.environ.get('MSG91_AUTH_KEY')
MSG91_TEMPLATE_ID = os.environ.get('MSG91_TEMPLATE_ID')
MSG91_SENDER_ID = os.environ.get('MSG91_SENDER_ID', 'SVCHUB')
USE_REAL_SMS = os.environ.get('USE_REAL_SMS', 'False') == 'True'

# Time Zone
TIME_ZONE = 'Asia/Kolkata'
```

---

## 📱 Usage

### For Customers

1. **Register**: 
   - Click "Register" → "Customer"
   - Enter phone, name, district, password
   - Login with credentials

2. **Browse Services**:
   - Select your district (set during registration)
   - Choose a service from the cards
   - View verified providers in your district

3. **Filter Providers**:
   - Search by name
   - Filter by minimum rating
   - Sort by rating, reviews, or name

4. **Add Reviews**:
   - Click on a provider
   - Click "Add Review"
   - Rate 1-5 stars and add comments

5. **Manage Profile**:
   - View profile details
   - Edit name, address, district
   - Change password

### For Service Providers

1. **Register**:
   - Click "Register" → "Service Provider"
   - Enter all details including Aadhar
   - Upload photo (optional)
   - Select up to 3 services
   - Wait for admin verification

2. **After Verification**:
   - Login to view dashboard
   - See your rating and reviews
   - Edit profile information
   - View customer feedback

3. **Profile Management**:
   - Update services offered
   - Change district
   - Upload/change photo
   - Manage account settings

### For Admins

1. **Access Admin Panel**: `http://127.0.0.1:8000/admin/`

2. **Verify Providers**:
   - Go to Service Providers
   - Check "is_verified" for approved providers
   - Save changes

3. **Manage Users**:
   - View all customers and providers
   - Edit user details
   - Handle reported issues

---

## 📁 Project Structure
```
Application/
└── service/
    ├── venv/                          # Virtual environment
    ├── service/                       # Main project folder
    │   ├── __init__.py
    │   ├── settings.py               # Project settings
    │   ├── urls.py                   # Main URL configuration
    │   ├── wsgi.py
    │   └── asgi.py
    ├── services/                      # Main app
    │   ├── migrations/               # Database migrations
    │   ├── templates/
    │   │   └── services/             # HTML templates
    │   │       ├── base.html         # Base template
    │   │       ├── home.html         # Landing page
    │   │       ├── login.html        # Login page
    │   │       ├── customer_home.html
    │   │       ├── provider_home.html
    │   │       └── ...
    │   ├── __init__.py
    │   ├── admin.py                  # Admin configuration
    │   ├── models.py                 # Database models
    │   ├── forms.py                  # Django forms
    │   ├── views.py                  # View functions
    │   └── urls.py                   # App URL patterns
    ├── media/                         # User uploads
    │   └── provider_photos/
    ├── static/                        # Static files
    ├── db.sqlite3                     # Database (dev)
    ├── manage.py                      # Django management
    ├── requirements.txt               # Dependencies
    └── README.md                      # This file
```

---

## 🔌 API Integration

### MSG91 SMS Setup

1. **Sign up**: [MSG91.com](https://msg91.com/)

2. **Get Credentials**:
   - Auth Key from dashboard
   - Create OTP template
   - Get Template ID

3. **Configure**:
```python
   # In settings.py
   MSG91_AUTH_KEY = 'your-auth-key'
   MSG91_TEMPLATE_ID = 'your-template-id'
   USE_REAL_SMS = True  # Enable real SMS
```

4. **Template Format**:
```
   Your ServiceHub OTP is ##OTP##. Valid for 10 minutes. Do not share.
```

### Alternative SMS Providers

The system supports easy integration with:
- **Twilio**: International SMS
- **Fast2SMS**: Indian SMS service
- **AWS SNS**: Scalable SMS delivery
- **TextLocal**: Bulk SMS service

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] User registration (Customer & Provider)
- [ ] Login with correct/incorrect credentials
- [ ] Forgot password flow (OTP verification)
- [ ] District selection and filtering
- [ ] Service browsing and provider list
- [ ] Search and filter functionality
- [ ] Add/Edit reviews
- [ ] Profile editing
- [ ] Password change
- [ ] Admin verification of providers
- [ ] Responsive design on mobile

### Test Accounts
```
Customer:
Phone: 9876543210
Password: test123

Provider:
Phone: 9876543211
Password: test123

Admin:
Phone: 9999999999
Password: admin123
```

---

## 🚢 Deployment

### Production Checklist
```python
# settings.py changes for production:

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Use PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'servicehub_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Deployment Steps

1. **Collect Static Files**:
```bash
   python manage.py collectstatic
```

2. **Database Migration**:
```bash
   python manage.py migrate
```

3. **Create Superuser**:
```bash
   python manage.py createsuperuser
```

4. **Run with Gunicorn**:
```bash
   gunicorn service.wsgi:application --bind 0.0.0.0:8000
```

### Deployment Platforms

- **Heroku**: Easy deployment with PostgreSQL
- **DigitalOcean**: VPS with full control
- **AWS EC2**: Scalable cloud hosting
- **PythonAnywhere**: Beginner-friendly
- **Railway**: Modern deployment platform

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

### Code Standards

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Write docstrings for functions
- Test before committing

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🐛 Known Issues

- SMS OTP delivery depends on MSG91 service availability
- Profile photos are stored locally (not recommended for production)
- Review editing doesn't notify the provider
- No real-time notifications

---

## 🔮 Future Enhancements

### Planned Features
- [ ] Real-time chat between customer and provider
- [ ] Booking/appointment system
- [ ] Payment gateway integration
- [ ] Email notifications
- [ ] Provider availability calendar
- [ ] Service request history
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Provider verification documents upload
- [ ] Customer booking history
- [ ] Promotional offers/discounts
- [ ] Refer and earn program

---

## 📞 Support & Contact

### Getting Help

- **Issues**: [GitHub Issues](your-repo-url/issues)
- **Email**: your-email@example.com
- **Documentation**: [Wiki](your-repo-url/wiki)

### Developer

- **Name**: Your Name
- **Email**: your.email@example.com
- **GitHub**: [@yourusername](https://github.com/yourusername)
- **LinkedIn**: [Your Profile](https://linkedin.com/in/yourprofile)

---

## 🙏 Acknowledgments

- Django Documentation
- Tailwind CSS Team
- DaisyUI Contributors
- Font Awesome
- MSG91 SMS Service
- All open-source contributors

---

## 📊 Project Stats

- **Lines of Code**: ~5,000+
- **Templates**: 15+
- **Models**: 5
- **Views**: 20+
- **Districts Covered**: 75+
- **Services**: 10
- **Development Time**: 2-3 months

---

## 🔄 Version History

### v1.0.0 (Current)
- Initial release
- Customer and Provider registration
- Service browsing and filtering
- Review system
- Profile management
- OTP-based password reset
- Admin verification system
- District-based filtering

---

## 💡 Tips & Tricks

### Development
```bash
# Quick database reset
python manage.py flush

# Create test data
python manage.py shell
>>> from services.models import *
>>> # Create test users and providers
```

### Production
```bash
# Check deployment readiness
python manage.py check --deploy

# Create database backup
python manage.py dumpdata > backup.json

# Restore database
python manage.py loaddata backup.json
```

---

**Made with ❤️ using Django and Tailwind CSS**

---

**⭐ Star this repo if you find it helpful!**

---

*Last Updated: December 2025*
