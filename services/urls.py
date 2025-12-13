# services/urls.py
from django.urls import path
from django.contrib import admin
from .views import health
from . import views

urlpatterns = [
    # Home and login/register choices
    path("health/", health),
    path('', views.home, name='home'),
    path('login-choice/', views.login_choice, name='login_choice'),
    path('register-choice/', views.register_choice, name='register_choice'),
    
    # Login
    path('login/<str:user_type>/', views.login_view, name='login'),
    
    # Forgot Password
    
    path('forgot-password/verify-otp/', views.forgot_password_step2, name='forgot_password_step2'),
    path('forgot-password/reset/', views.forgot_password_step3, name='forgot_password_step3'),
    path('forgot-password/<str:user_type>/', views.forgot_password_step1, name='forgot_password_step1'),
    
    # Registration
    path('register/provider/', views.register_provider, name='register_provider'),
    path('register/customer/', views.register_customer, name='register_customer'),
    
    # District selection (kept for profile editing, removed from UI)
    path('select-district/', views.select_district, name='select_district'),
    
    # Home pages after login
    path('provider/home/', views.provider_home, name='provider_home'),
    path('customer/home/', views.customer_home, name='customer_home'),
    
    # Service providers list
    path('service/<str:service_code>/providers/', views.service_providers_list, name='service_providers_list'),
    
    # Reviews
    path('review/add/<str:provider_phone>/', views.add_review, name='add_review'),
    
    # Profile management
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    
    # Logout
    path('logout/', views.logout_view, name='logout'),

    path('provider/work-photos/add/', views.add_work_photo, name='add_work_photo'),
    path('provider/work-photos/delete/<int:photo_id>/', views.delete_work_photo, name='delete_work_photo'),
    path('provider/work-gallery/<str:provider_phone>/', views.view_work_gallery, name='view_work_gallery'),
]