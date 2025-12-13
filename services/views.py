# views.py - COMPLETE FILE WITH ALL FIXES
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import User, ServiceProvider, Customer, Review, DISTRICT_CHOICES, OTPVerification, ProviderWorkPhoto
from .forms import (ProviderRegistrationForm, CustomerRegistrationForm, LoginForm,
                   ProfileEditForm, ProviderProfileEditForm, CustomerProfileEditForm,
                   CustomPasswordChangeForm, ReviewForm, DistrictSelectionForm,
                   ForgotPasswordStep1Form, ForgotPasswordStep2Form, ForgotPasswordStep3Form, WorkPhotoForm)


# Simulated SMS sending (replace with actual SMS gateway in production)
def send_otp_sms(phone_number, otp):
    """
    Send OTP via SMS
    In production, integrate with SMS gateway
    """
    try:
        # For development: Print to console
        print(f"\n{'='*60}")
        print(f"📱 SMS SENT TO: {phone_number}")
        print(f"🔐 YOUR OTP IS: {otp}")
        print(f"⏰ Valid for 10 minutes")
        print(f"{'='*60}\n")
        
        # PRODUCTION: Uncomment this for real SMS via Fast2SMS
        """
        import requests
        api_key = "YOUR_FAST2SMS_API_KEY"
        url = "https://www.fast2sms.com/dev/bulkV2"
        
        payload = {
            "route": "v3",
            "sender_id": "TXTIND",
            "message": f"Your ServiceHub password reset OTP is {otp}. Valid for 10 minutes. Do not share.",
            "language": "english",
            "flash": 0,
            "numbers": phone_number,
        }
        
        headers = {
            "authorization": api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        response = requests.post(url, data=payload, headers=headers)
        return response.status_code == 200
        """
        
        return True
        
    except Exception as e:
        print(f"SMS Error: {e}")
        return False


def home(request):
    """Common home page before login"""
    return render(request, 'services/home.html')


def login_choice(request):
    """Page to choose login type"""
    return render(request, 'services/login_choice.html')


def login_view(request, user_type):
    """Handle login for both user types with error handling"""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            try:
                user = authenticate(request, username=phone_number, password=password)
                
                if user is not None:
                    # Check if user type matches
                    if user.user_type != user_type:
                        messages.error(request, f'This phone number is registered as {user.get_user_type_display()}, not as {user_type}. Please select the correct login type.')
                        return redirect('login', user_type=user_type)
                    
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.name}!')
                    
                    # Set district for customers
                    if user_type == 'customer':
                        try:
                            customer = user.customer_profile
                            request.session['selected_district'] = customer.district
                        except ObjectDoesNotExist:
                            messages.error(request, 'Profile error. Please contact support.')
                            return redirect('home')
                        return redirect('customer_home')
                    else:
                        return redirect('provider_home')
                else:
                    messages.error(request, 'Invalid phone number or password. Please try again.')
            except Exception as e:
                messages.error(request, 'An error occurred during login. Please try again.')
                print(f"Login error: {e}")
        else:
            messages.error(request, 'Invalid phone number or password.')
    else:
        form = LoginForm()
    
    return render(request, 'services/login.html', {
        'form': form,
        'user_type': user_type
    })


def forgot_password_step1(request, user_type):
    """Step 1: Enter phone (and DOB for provider), then send OTP"""
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', '').strip()
        date_of_birth = request.POST.get('date_of_birth', '').strip() if user_type == 'provider' else None
        
        # Basic validation
        if not phone_number:
            messages.error(request, 'Please enter your phone number')
            return render(request, 'services/forgot_password_step1.html', {'user_type': user_type})
        
        if len(phone_number) != 10 or not phone_number.isdigit():
            messages.error(request, 'Please enter a valid 10-digit phone number')
            return render(request, 'services/forgot_password_step1.html', {'user_type': user_type})
        
        if phone_number[0] not in '6789':
            messages.error(request, 'Phone number must start with 6, 7, 8, or 9')
            return render(request, 'services/forgot_password_step1.html', {'user_type': user_type})
        
        try:
            # Check if user exists
            user = User.objects.get(phone_number=phone_number, user_type=user_type)
            
            # For provider, verify DOB
            if user_type == 'provider':
                if not date_of_birth:
                    messages.error(request, 'Please enter your date of birth')
                    return render(request, 'services/forgot_password_step1.html', {'user_type': user_type})
                
                try:
                    from datetime import datetime
                    dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                    provider = user.provider_profile
                    
                    if provider.date_of_birth != dob:
                        messages.error(request, 'Phone number and date of birth do not match')
                        return render(request, 'services/forgot_password_step1.html', {'user_type': user_type})
                except ValueError:
                    messages.error(request, 'Invalid date format')
                    return render(request, 'services/forgot_password_step1.html', {'user_type': user_type})
                except ObjectDoesNotExist:
                    messages.error(request, 'Provider profile not found')
                    return render(request, 'services/forgot_password_step1.html', {'user_type': user_type})
            
            # Delete old OTPs
            OTPVerification.objects.filter(
                phone_number=phone_number,
                is_verified=False
            ).delete()
            
            # Generate OTP
            otp = OTPVerification.generate_otp()
            otp_record = OTPVerification.objects.create(
                phone_number=phone_number,
                otp=otp
            )
            
            # Print OTP to console
            print(f"\n{'='*60}")
            print(f"📱 OTP FOR: {phone_number}")
            print(f"🔐 OTP CODE: {otp}")
            print(f"⏰ Valid for 10 minutes")
            print(f"{'='*60}\n")
            
            # Store in session
            request.session['reset_phone'] = phone_number
            request.session['reset_user_type'] = user_type
            
            # Success message and redirect
            messages.success(request, f'OTP sent successfully! Check your console/terminal.')
            return redirect('forgot_password_step2')
            
        except User.DoesNotExist:
            messages.error(request, f'No {user_type} account found with phone number {phone_number}')
            return render(request, 'services/forgot_password_step1.html', {'user_type': user_type})
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            print(f"Error: {e}")
            return render(request, 'services/forgot_password_step1.html', {'user_type': user_type})
    
    # GET request
    return render(request, 'services/forgot_password_step1.html', {'user_type': user_type})

def forgot_password_step2(request):
    """Step 2: Verify OTP"""
    phone_number = request.session.get('reset_phone')
    user_type = request.session.get('reset_user_type', 'customer')
    
    if not phone_number:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('forgot_password_step1', user_type=user_type)
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()
        
        if not entered_otp or len(entered_otp) != 6:
            messages.error(request, 'Please enter a valid 6-digit OTP')
            return render(request, 'services/forgot_password_step2.html', {
                'phone_number': phone_number,
                'user_type': user_type
            })
        
        try:
            # Get latest OTP for this phone
            otp_record = OTPVerification.objects.filter(
                phone_number=phone_number,
                is_verified=False
            ).order_by('-created_at').first()
            
            if not otp_record:
                messages.error(request, 'No OTP found. Please request a new one.')
                return redirect('forgot_password_step1', user_type=user_type)
            
            print(f"Stored OTP: {otp_record.otp}, Entered OTP: {entered_otp}")
            
            if not otp_record.is_valid():
                messages.error(request, 'OTP expired (10 min limit). Please request a new one.')
                return redirect('forgot_password_step1', user_type=user_type)
            
            if otp_record.otp == entered_otp:
                # Mark as verified
                otp_record.is_verified = True
                otp_record.save()
                
                messages.success(request, '✓ OTP verified successfully!')
                return redirect('forgot_password_step3')
            else:
                messages.error(request, 'Invalid OTP. Please check and try again.')
                return render(request, 'services/forgot_password_step2.html', {
                    'phone_number': phone_number,
                    'user_type': user_type
                })
                
        except Exception as e:
            messages.error(request, f'Verification failed: {str(e)}')
            print(f"OTP verification error: {e}")
            return render(request, 'services/forgot_password_step2.html', {
                'phone_number': phone_number,
                'user_type': user_type
            })
    
    # GET request
    return render(request, 'services/forgot_password_step2.html', {
        'phone_number': phone_number,
        'user_type': user_type
    })

def forgot_password_step3(request):
    """Step 3: Reset Password"""
    phone_number = request.session.get('reset_phone')
    user_type = request.session.get('reset_user_type', 'customer')
    
    if not phone_number:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('login_choice')
    
    # Verify OTP was verified
    otp_verified = OTPVerification.objects.filter(
        phone_number=phone_number,
        is_verified=True
    ).order_by('-created_at').first()
    
    if not otp_verified or not otp_verified.is_valid():
        messages.error(request, 'Verification expired. Please start again.')
        return redirect('forgot_password_step1', user_type=user_type)
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        # Validation
        if not new_password or len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
            return render(request, 'services/forgot_password_step3.html')
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'services/forgot_password_step3.html')
        
        try:
            user = User.objects.get(phone_number=phone_number)
            user.set_password(new_password)
            user.save()
            
            # Clear session
            if 'reset_phone' in request.session:
                del request.session['reset_phone']
            if 'reset_user_type' in request.session:
                del request.session['reset_user_type']
            
            messages.success(request, '✓ Password reset successfully! Please login with your new password.')
            return redirect('login', user_type=user.user_type)
            
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('login_choice')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            print(f"Password reset error: {e}")
            return render(request, 'services/forgot_password_step3.html')
    
    # GET request
    return render(request, 'services/forgot_password_step3.html')


def register_choice(request):
    """Page to choose registration type"""
    return render(request, 'services/register_choice.html')


def register_provider(request):
    """Service provider registration with error handling"""
    if request.method == 'POST':
        form = ProviderRegistrationForm(request.POST, request.FILES)
        phone_number = request.POST.get('phone_number')
        name = request.POST.get('name')
        password = request.POST.get('password')
        address = request.POST.get('address')
        district = request.POST.get('district')
        aadhar_number = request.POST.get('aadhar_number')
        date_of_birth = request.POST.get('date_of_birth')
        
        if form.is_valid():
            try:
                # Create user
                user = User.objects.create_user(
                    phone_number=phone_number,
                    password=password,
                    name=name,
                    user_type='provider'
                )
                
                # Create provider profile
                provider = form.save(commit=False)
                provider.user = user
                provider.address = address
                provider.district = district
                provider.aadhar_number = aadhar_number
                provider.date_of_birth = date_of_birth
                if request.FILES.get('photo'):
                    provider.photo = request.FILES['photo']
                provider.save()
                
                messages.success(request, 'Registration successful! Please login.')
                return redirect('login', user_type='provider')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
                print(f"Registration error: {e}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ProviderRegistrationForm()
    
    return render(request, 'services/register_provider.html', {'form': form})


def register_customer(request):
    """Customer registration with error handling"""
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create user
                user = User.objects.create_user(
                    phone_number=form.cleaned_data['phone_number'],
                    password=form.cleaned_data['password'],
                    name=form.cleaned_data['name'],
                    user_type='customer'
                )
                
                # Create customer profile
                Customer.objects.create(
                    user=user,
                    address=form.cleaned_data.get('address', ''),
                    district=form.cleaned_data['district']
                )
                
                messages.success(request, 'Registration successful! Please login.')
                return redirect('login', user_type='customer')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
                print(f"Registration error: {e}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'services/register_customer.html', {'form': form})


@login_required
def provider_home(request):
    """Home page for service providers"""
    try:
        if request.user.user_type != 'provider':
            messages.error(request, 'Access denied. Please login with a provider account.')
            logout(request)
            return redirect('login_choice')
        
        provider = request.user.provider_profile
        reviews = provider.reviews.all()[:5]
        return render(request, 'services/provider_home.html', {
            'provider': provider,
            'reviews': reviews
        })
    except ObjectDoesNotExist:
        messages.error(request, 'Provider profile not found. Please contact support.')
        logout(request)
        return redirect('home')
    except Exception as e:
        messages.error(request, 'An error occurred. Please login again.')
        print(f"Provider home error: {e}")
        logout(request)
        return redirect('home')


@login_required
def select_district(request):
    """District selection page for customers - REMOVED FROM UI"""
    try:
        if request.user.user_type != 'customer':
            messages.error(request, 'Access denied')
            return redirect('home')
        
        if request.method == 'POST':
            form = DistrictSelectionForm(request.POST)
            if form.is_valid():
                district = form.cleaned_data['district']
                request.session['selected_district'] = district
                
                # Update customer profile district
                customer = request.user.customer_profile
                customer.district = district
                customer.save()
                
                messages.success(request, f'District updated successfully')
                return redirect('customer_home')
        else:
            current_district = request.session.get('selected_district', request.user.customer_profile.district)
            form = DistrictSelectionForm(initial={'district': current_district})
        
        return render(request, 'services/select_district.html', {'form': form})
    except Exception as e:
        messages.error(request, 'An error occurred. Please try again.')
        print(f"Select district error: {e}")
        return redirect('customer_home')


@login_required
def customer_home(request):
    """Home page for customers - shows all services"""
    try:
        if request.user.user_type != 'customer':
            messages.error(request, 'Access denied. Please login with a customer account.')
            logout(request)
            return redirect('login_choice')
        
        # Get district from session or customer profile
        selected_district = request.session.get('selected_district')
        if not selected_district:
            selected_district = request.user.customer_profile.district
            request.session['selected_district'] = selected_district
        
        # Get district name for display
        selected_district_name = dict(DISTRICT_CHOICES).get(selected_district, selected_district)
        
        services = [
            {'code': 'mason', 'name': 'Mason', 'icon': 'hard-hat', 'gradient': 'from-red-500 to-pink-500'},
            {'code': 'painter', 'name': 'Painter', 'icon': 'paint-roller', 'gradient': 'from-cyan-500 to-blue-500'},
            {'code': 'plumber', 'name': 'Plumber', 'icon': 'wrench', 'gradient': 'from-blue-500 to-indigo-500'},
            {'code': 'carpenter', 'name': 'Carpenter', 'icon': 'hammer', 'gradient': 'from-amber-500 to-orange-500'},
            {'code': 'electrician', 'name': 'Electrician', 'icon': 'bolt', 'gradient': 'from-yellow-400 to-yellow-600'},
            {'code': 'tile_marble', 'name': 'Tile/Marble Worker', 'icon': 'th', 'gradient': 'from-slate-400 to-slate-600'},
            {'code': 'steel_fabricator', 'name': 'Steel Fabricator', 'icon': 'industry', 'gradient': 'from-gray-500 to-gray-700'},
            {'code': 'glass_worker', 'name': 'Glass Worker', 'icon': 'wine-glass', 'gradient': 'from-purple-500 to-indigo-500'},
            {'code': 'gardener', 'name': 'Gardener', 'icon': 'leaf', 'gradient': 'from-green-400 to-emerald-600'},
            {'code': 'driver', 'name': 'Driver', 'icon': 'car', 'gradient': 'from-pink-500 to-rose-500'},
        ]
        
        return render(request, 'services/customer_home.html', {
            'services': services,
            'selected_district': selected_district_name
        })
    except ObjectDoesNotExist:
        messages.error(request, 'Customer profile not found. Please contact support.')
        logout(request)
        return redirect('home')
    except Exception as e:
        messages.error(request, 'An error occurred. Please login again.')
        print(f"Customer home error: {e}")
        logout(request)
        return redirect('home')


@login_required
def service_providers_list(request, service_code):
    """List all providers for a specific service in selected district with filtering"""
    try:
        if request.user.user_type != 'customer':
            messages.error(request, 'Access denied')
            return redirect('home')
        
        selected_district = request.session.get('selected_district')
        if not selected_district:
            selected_district = request.user.customer_profile.district
            request.session['selected_district'] = selected_district
        
        service_names = dict(ServiceProvider.SERVICE_CHOICES)
        service_name = service_names.get(service_code, 'Unknown Service')
        
        # Base query - Find all verified providers offering this service in the selected district
        providers = ServiceProvider.objects.filter(
            Q(service1=service_code) | Q(service2=service_code) | Q(service3=service_code)
        ).filter(is_verified=True, district=selected_district)
        
        # Get filter parameters from request
        search_name = request.GET.get('search', '').strip()
        rating_filter = request.GET.get('rating', '').strip()
        sort_by = request.GET.get('sort', 'rating')  # Default sort by rating
        
        # Apply name search filter
        if search_name:
            providers = providers.filter(user__name__icontains=search_name)
        
        # Apply rating filter
        if rating_filter:
            try:
                min_rating = float(rating_filter)
                providers = providers.filter(rating__gte=min_rating)
            except ValueError:
                pass  # Invalid rating value, ignore filter
        
        # Apply sorting
        if sort_by == 'rating':
            providers = providers.order_by('-rating', '-total_reviews')
        elif sort_by == 'name':
            providers = providers.order_by('user__name')
        elif sort_by == 'reviews':
            providers = providers.order_by('-total_reviews', '-rating')
        elif sort_by == 'newest':
            providers = providers.order_by('-created_at')
        else:
            providers = providers.order_by('-rating', '-total_reviews')
        
        # Check if customer has reviewed each provider
        customer = request.user.customer_profile
        for provider in providers:
            provider.user_has_reviewed = Review.objects.filter(
                customer=customer, provider=provider
            ).exists()
        
        selected_district_name = dict(DISTRICT_CHOICES).get(selected_district, selected_district)
        
        return render(request, 'services/providers_list.html', {
            'service_code': service_code,
            'service_name': service_name,
            'providers': providers,
            'selected_district': selected_district_name,
            'search_name': search_name,
            'rating_filter': rating_filter,
            'sort_by': sort_by,
        })
    except Exception as e:
        messages.error(request, 'An error occurred. Please try again.')
        print(f"Providers list error: {e}")
        return redirect('customer_home')


@login_required
def add_review(request, provider_phone):
    """Add or update review for a provider"""
    try:
        if request.user.user_type != 'customer':
            messages.error(request, 'Only customers can add reviews')
            return redirect('home')
        
        provider = get_object_or_404(ServiceProvider, user__phone_number=provider_phone)
        customer = request.user.customer_profile
        
        existing_review = Review.objects.filter(customer=customer, provider=provider).first()
        
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=existing_review)
            if form.is_valid():
                review = form.save(commit=False)
                review.customer = customer
                review.provider = provider
                review.save()
                
                messages.success(request, 'Review submitted successfully!' if not existing_review else 'Review updated successfully!')
                return redirect('service_providers_list', service_code=provider.service1)
        else:
            form = ReviewForm(instance=existing_review)
        
        return render(request, 'services/add_review.html', {
            'form': form,
            'provider': provider,
            'existing_review': existing_review
        })
    except Exception as e:
        messages.error(request, 'An error occurred. Please try again.')
        print(f"Add review error: {e}")
        return redirect('customer_home')


@login_required
def profile_view(request):
    """View profile"""
    try:
        if request.user.user_type == 'provider':
            return redirect('provider_home')
        else:
            customer = request.user.customer_profile
            return render(request, 'services/customer_profile.html', {'customer': customer})
    except Exception as e:
        messages.error(request, 'An error occurred. Please login again.')
        print(f"Profile view error: {e}")
        logout(request)
        return redirect('home')


@login_required
def edit_profile(request):
    """Edit profile with work photos for providers"""
    try:
        user = request.user
        
        if request.method == 'POST':
            user_form = ProfileEditForm(request.POST, instance=user)
            
            if user.user_type == 'provider':
                profile_form = ProviderProfileEditForm(
                    request.POST, request.FILES, instance=user.provider_profile
                )
            else:
                profile_form = CustomerProfileEditForm(
                    request.POST, instance=user.customer_profile
                )
            
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                
                # Update session district if customer changed it
                if user.user_type == 'customer':
                    request.session['selected_district'] = user.customer_profile.district
                
                messages.success(request, 'Profile updated successfully!')
                
                if user.user_type == 'provider':
                    return redirect('provider_home')
                else:
                    return redirect('customer_home')
        else:
            user_form = ProfileEditForm(instance=user)
            
            if user.user_type == 'provider':
                profile_form = ProviderProfileEditForm(instance=user.provider_profile)
                # Get work photos for provider
                work_photos = user.provider_profile.work_photos.all()
            else:
                profile_form = CustomerProfileEditForm(instance=user.customer_profile)
                work_photos = None
        
        return render(request, 'services/edit_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'work_photos': work_photos,
        })
    except Exception as e:
        messages.error(request, 'An error occurred. Please try again.')
        print(f"Edit profile error: {e}")
        if request.user.user_type == 'provider':
            return redirect('provider_home')
        else:
            return redirect('customer_home')


@login_required
def add_work_photo(request):
    """Add work photo to provider's gallery"""
    try:
        if request.user.user_type != 'provider':
            messages.error(request, 'Only providers can add work photos')
            return redirect('home')
        
        provider = request.user.provider_profile
        
        # Check if provider already has 10 photos
        current_count = provider.work_photos.count()
        if current_count >= 10:
            messages.error(request, 'Maximum 10 work photos allowed. Please delete some photos first.')
            return redirect('edit_profile')
        
        if request.method == 'POST':
            # Manual form handling for better debugging
            photo_file = request.FILES.get('photo')
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            
            if photo_file:
                try:
                    # Create the work photo
                    work_photo = ProviderWorkPhoto.objects.create(
                        provider=provider,
                        photo=photo_file,
                        title=title,
                        description=description
                    )
                    messages.success(request, 'Work photo added successfully!')
                    return redirect('edit_profile')
                except Exception as e:
                    messages.error(request, f'Error saving photo: {str(e)}')
                    print(f"Photo save error: {e}")
            else:
                messages.error(request, 'Please select a photo to upload')
        
        # For GET request
        current_count = provider.work_photos.count()
        return render(request, 'services/add_work_photo.html', {
            'current_count': current_count,
            'max_photos': 10
        })
        
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        print(f"Add work photo error: {e}")
        import traceback
        traceback.print_exc()
        return redirect('edit_profile')

@login_required
def delete_work_photo(request, photo_id):
    """Delete a work photo"""
    try:
        if request.user.user_type != 'provider':
            messages.error(request, 'Access denied')
            return redirect('home')
        
        photo = get_object_or_404(ProviderWorkPhoto, id=photo_id, provider=request.user.provider_profile)
        photo.delete()
        
        messages.success(request, 'Work photo deleted successfully!')
        return redirect('edit_profile')
    except Exception as e:
        messages.error(request, 'An error occurred. Please try again.')
        print(f"Delete work photo error: {e}")
        return redirect('edit_profile')


@login_required
def view_work_gallery(request, provider_phone):
    """View provider's work gallery"""
    try:
        provider = get_object_or_404(ServiceProvider, user__phone_number=provider_phone)
        work_photos = provider.work_photos.all()
        
        return render(request, 'services/work_gallery.html', {
            'provider': provider,
            'work_photos': work_photos
        })
    except Exception as e:
        messages.error(request, 'An error occurred. Please try again.')
        print(f"View gallery error: {e}")
        return redirect('customer_home')


@login_required
def change_password(request):
    """Change password"""
    try:
        if request.method == 'POST':
            form = CustomPasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully!')
                
                if request.user.user_type == 'provider':
                    return redirect('provider_home')
                else:
                    return redirect('customer_home')
            else:
                for error in form.errors.values():
                    messages.error(request, error)
        else:
            form = CustomPasswordChangeForm(request.user)
        
        return render(request, 'services/change_password.html', {'form': form})
    except Exception as e:
        messages.error(request, 'An error occurred. Please try again.')
        print(f"Change password error: {e}")
        if request.user.user_type == 'provider':
            return redirect('provider_home')
        else:
            return redirect('customer_home')


@login_required
def logout_view(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')

def health(request):
    # Simple, fast response with no DB queries
    return JsonResponse({"status": "ok"}, status=200)