# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import random

# Indian Districts List (Major ones)
DISTRICT_CHOICES = [
    # Uttar Pradesh
    ('agra', 'Agra'), ('aligarh', 'Aligarh'), ('allahabad', 'Allahabad'), ('ambedkar_nagar', 'Ambedkar Nagar'),
    ('amethi', 'Amethi'), ('amroha', 'Amroha'), ('auraiya', 'Auraiya'), ('azamgarh', 'Azamgarh'),
    ('baghpat', 'Baghpat'), ('bahraich', 'Bahraich'), ('ballia', 'Ballia'), ('balrampur', 'Balrampur'),
    ('banda', 'Banda'), ('barabanki', 'Barabanki'), ('bareilly', 'Bareilly'), ('basti', 'Basti'),
    ('bhadohi', 'Bhadohi'), ('bijnor', 'Bijnor'), ('budaun', 'Budaun'), ('bulandshahr', 'Bulandshahr'),
    ('chandauli', 'Chandauli'), ('chitrakoot', 'Chitrakoot'), ('deoria', 'Deoria'), ('etah', 'Etah'),
    ('etawah', 'Etawah'), ('faizabad', 'Faizabad'), ('farrukhabad', 'Farrukhabad'), ('fatehpur', 'Fatehpur'),
    ('firozabad', 'Firozabad'), ('gautam_buddha_nagar', 'Gautam Buddha Nagar'), ('ghaziabad', 'Ghaziabad'),
    ('ghazipur', 'Ghazipur'), ('gonda', 'Gonda'), ('gorakhpur', 'Gorakhpur'), ('hamirpur', 'Hamirpur'),
    ('hapur', 'Hapur'), ('hardoi', 'Hardoi'), ('hathras', 'Hathras'), ('jalaun', 'Jalaun'),
    ('jaunpur', 'Jaunpur'), ('jhansi', 'Jhansi'), ('kannauj', 'Kannauj'), ('kanpur_dehat', 'Kanpur Dehat'),
    ('kanpur_nagar', 'Kanpur Nagar'), ('kasganj', 'Kasganj'), ('kaushambi', 'Kaushambi'), ('kheri', 'Kheri'),
    ('kushinagar', 'Kushinagar'), ('lalitpur', 'Lalitpur'), ('lucknow', 'Lucknow'), ('maharajganj', 'Maharajganj'),
    ('mahoba', 'Mahoba'), ('mainpuri', 'Mainpuri'), ('mathura', 'Mathura'), ('mau', 'Mau'),
    ('meerut', 'Meerut'), ('mirzapur', 'Mirzapur'), ('moradabad', 'Moradabad'), ('muzaffarnagar', 'Muzaffarnagar'),
    ('pilibhit', 'Pilibhit'), ('pratapgarh', 'Pratapgarh'), ('raebareli', 'Raebareli'), ('rampur', 'Rampur'),
    ('saharanpur', 'Saharanpur'), ('sambhal', 'Sambhal'), ('sant_kabir_nagar', 'Sant Kabir Nagar'),
    ('shahjahanpur', 'Shahjahanpur'), ('shamli', 'Shamli'), ('shravasti', 'Shravasti'), ('siddharthnagar', 'Siddharthnagar'),
    ('sitapur', 'Sitapur'), ('sonbhadra', 'Sonbhadra'), ('sultanpur', 'Sultanpur'), ('unnao', 'Unnao'),
    ('varanasi', 'Varanasi'),

    # Maharashtra
    ('mumbai', 'Mumbai'), ('pune', 'Pune'), ('nagpur', 'Nagpur'), ('thane', 'Thane'), ('nashik', 'Nashik'),
    ('aurangabad', 'Aurangabad'), ('solapur', 'Solapur'), ('kolhapur', 'Kolhapur'), ('amravati', 'Amravati'),

    # Delhi
    ('delhi', 'Delhi'), ('new_delhi', 'New Delhi'), ('north_delhi', 'North Delhi'), ('south_delhi', 'South Delhi'),
    ('east_delhi', 'East Delhi'), ('west_delhi', 'West Delhi'),

    # Karnataka
    ('bengaluru', 'Bengaluru'), ('mysuru', 'Mysuru'), ('hubli', 'Hubli'), ('mangaluru', 'Mangaluru'),

    # Tamil Nadu
    ('chennai', 'Chennai'), ('coimbatore', 'Coimbatore'), ('madurai', 'Madurai'), ('tiruchirappalli', 'Tiruchirappalli'),

    # West Bengal
    ('kolkata', 'Kolkata'), ('howrah', 'Howrah'), ('durgapur', 'Durgapur'), ('siliguri', 'Siliguri'),

    # Rajasthan
    ('jaipur', 'Jaipur'), ('jodhpur', 'Jodhpur'), ('kota', 'Kota'), ('udaipur', 'Udaipur'),

    # Gujarat
    ('ahmedabad', 'Ahmedabad'), ('surat', 'Surat'), ('vadodara', 'Vadodara'), ('rajkot', 'Rajkot'),
]

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number is required')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('provider', 'Service Provider'),
    )

    phone_regex = RegexValidator(
        regex=r'^[6-9]\d{9}$',
        message="Phone number must be 10 digits starting with 6-9"
    )

    phone_number = models.CharField(
        max_length=10,
        unique=True,
        primary_key=True,
        validators=[phone_regex]
    )
    name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name', 'user_type']

    def __str__(self):
        return f"{self.name} - {self.phone_number}"


class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    photo = models.ImageField(upload_to='provider_photos/', blank=True, null=True)
    address = models.TextField()
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES, default='lucknow')
    aadhar_regex = RegexValidator(
        regex=r'^\d{12}$',
        message="Aadhar number must be exactly 12 digits"
    )
    aadhar_number = models.CharField(
        max_length=12,
        unique=True,
        validators=[aadhar_regex]
    )
    date_of_birth = models.DateField()

    SERVICE_CHOICES = [
        ('mason', 'Mason'),
        ('painter', 'Painter'),
        ('plumber', 'Plumber'),
        ('carpenter', 'Carpenter'),
        ('electrician', 'Electrician'),
        ('tile_marble', 'Tile/Marble Worker'),
        ('steel_fabricator', 'Steel Fabricator'),
        ('glass_worker', 'Glass Worker'),
        ('gardener', 'Gardener'),
        ('driver', 'Driver'),
    ]

    service1 = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    service2 = models.CharField(max_length=20, choices=SERVICE_CHOICES, blank=True, null=True)
    service3 = models.CharField(max_length=20, choices=SERVICE_CHOICES, blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        services = [self.service1, self.service2, self.service3]
        services = [s for s in services if s]
        if len(services) != len(set(services)):
            raise ValidationError("Cannot select the same service multiple times")

    def get_services(self):
        services = []
        if self.service1:
            services.append(self.get_service1_display())
        if self.service2:
            services.append(self.get_service2_display())
        if self.service3:
            services.append(self.get_service3_display())
        return services

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            total = sum(review.rating for review in reviews)
            self.rating = round(total / reviews.count(), 2)
            self.total_reviews = reviews.count()
            self.save()

    def __str__(self):
        return f"{self.user.name} - Provider"

    class Meta:
        ordering = ['-rating', '-created_at']


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.TextField(blank=True)
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES, default='lucknow')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - Customer"


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='requests')
    provider = models.ForeignKey(ServiceProvider, on_delete=models.SET_NULL, null=True, blank=True)
    service_type = models.CharField(max_length=20)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.user.name} - {self.service_type}"

    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='given_reviews')
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'provider')
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.provider.update_rating()

    def __str__(self):
        return f"{self.customer.user.name} -> {self.provider.user.name} ({self.rating}/5)"


class OTPVerification(models.Model):
    phone_number = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_valid(self):
        from datetime import timedelta
        return timezone.now() < self.created_at + timedelta(minutes=10)

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    def __str__(self):
        return f"{self.phone_number} - {self.otp}"

    class Meta:
        ordering = ['-created_at']


#forms.py


# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import User, ServiceProvider, Customer, Review, DISTRICT_CHOICES
from django.core.exceptions import ValidationError

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Phone Number',
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter 10-digit phone number'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter password'
        })
    )


class ProviderRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Password'}),
        min_length=6
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Confirm Password'})
    )
    
    phone_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': '10-digit phone number'})
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Full Name'})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3, 'placeholder': 'Complete Address'})
    )
    district = forms.ChoiceField(
        choices=[('', 'Select District')] + DISTRICT_CHOICES,
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )
    aadhar_number = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': '12-digit Aadhar Number'})
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'})
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full'})
    )

    class Meta:
        model = ServiceProvider
        fields = ['service1', 'service2', 'service3']
        widgets = {
            'service1': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'service2': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'service3': forms.Select(attrs={'class': 'select select-bordered w-full'}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords don't match")
        return confirm_password

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone).exists():
            raise ValidationError("This phone number is already registered")
        if not phone.isdigit() or len(phone) != 10:
            raise ValidationError("Phone number must be exactly 10 digits")
        if phone[0] not in '6789':
            raise ValidationError("Phone number must start with 6, 7, 8, or 9")
        return phone

    def clean_aadhar_number(self):
        aadhar = self.cleaned_data.get('aadhar_number')
        if ServiceProvider.objects.filter(aadhar_number=aadhar).exists():
            raise ValidationError("This Aadhar number is already registered")
        if not aadhar.isdigit() or len(aadhar) != 12:
            raise ValidationError("Aadhar number must be exactly 12 digits")
        return aadhar


class CustomerRegistrationForm(forms.Form):
    phone_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': '10-digit phone number'})
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Full Name'})
    )
    district = forms.ChoiceField(
        choices=[('', 'Select District')] + DISTRICT_CHOICES,
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Password'}),
        min_length=6
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Confirm Password'})
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3, 'placeholder': 'Address (Optional)'})
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords don't match")
        return confirm_password

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone).exists():
            raise ValidationError("This phone number is already registered")
        if not phone.isdigit() or len(phone) != 10:
            raise ValidationError("Phone number must be exactly 10 digits")
        if phone[0] not in '6789':
            raise ValidationError("Phone number must start with 6, 7, 8, or 9")
        return phone


class ProfileEditForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'})
    )
    
    class Meta:
        model = User
        fields = ['name']


class ProviderProfileEditForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3})
    )
    district = forms.ChoiceField(
        choices=DISTRICT_CHOICES,
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full'})
    )
    
    class Meta:
        model = ServiceProvider
        fields = ['address', 'district', 'photo', 'service1', 'service2', 'service3']
        widgets = {
            'service1': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'service2': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'service3': forms.Select(attrs={'class': 'select select-bordered w-full'}),
        }


class CustomerProfileEditForm(forms.ModelForm):
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3})
    )
    district = forms.ChoiceField(
        choices=DISTRICT_CHOICES,
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )
    
    class Meta:
        model = Customer
        fields = ['address', 'district']


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Current Password'})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Confirm New Password'})
    )


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'radio radio-warning'})
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea textarea-bordered w-full',
            'rows': 4,
            'placeholder': 'Share your experience (optional)...'
        })
    )
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class DistrictSelectionForm(forms.Form):
    district = forms.ChoiceField(
        choices=[('', 'Select Your District')] + DISTRICT_CHOICES,
        widget=forms.Select(attrs={'class': 'select select-bordered select-lg w-full max-w-md'})
    )

#views.py

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, ServiceProvider, Customer, Review, DISTRICT_CHOICES
from .forms import (ProviderRegistrationForm, CustomerRegistrationForm, LoginForm,
                   ProfileEditForm, ProviderProfileEditForm, CustomerProfileEditForm,
                   CustomPasswordChangeForm, ReviewForm, DistrictSelectionForm)
from django.db.models import Q

def home(request):
    """Common home page before login"""
    return render(request, 'services/home.html')


def login_choice(request):
    """Page to choose login type"""
    return render(request, 'services/login_choice.html')


def login_view(request, user_type):
    """Handle login for both user types"""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=phone_number, password=password)
            
            if user is not None:
                if user.user_type != user_type:
                    messages.error(request, f'This account is not registered as {user_type}')
                    return redirect('login', user_type=user_type)
                
                login(request, user)
                messages.success(request, f'Welcome back, {user.name}!')
                
                if user_type == 'provider':
                    return redirect('provider_home')
                else:
                    # Set district from customer profile to session
                    customer = user.customer_profile
                    request.session['selected_district'] = customer.district
                    return redirect('customer_home')
            else:
                messages.error(request, 'Invalid phone number or password')
        else:
            messages.error(request, 'Invalid phone number or password')
    else:
        form = LoginForm()
    
    return render(request, 'services/login.html', {
        'form': form,
        'user_type': user_type
    })


def register_choice(request):
    """Page to choose registration type"""
    return render(request, 'services/register_choice.html')


def register_provider(request):
    """Service provider registration"""
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
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ProviderRegistrationForm()
    
    return render(request, 'services/register_provider.html', {'form': form})


def register_customer(request):
    """Customer registration"""
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
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
    if request.user.user_type != 'provider':
        messages.error(request, 'Access denied')
        return redirect('home')
    
    provider = request.user.provider_profile
    reviews = provider.reviews.all()[:5]  # Latest 5 reviews
    return render(request, 'services/provider_home.html', {
        'provider': provider,
        'reviews': reviews
    })


@login_required
def select_district(request):
    """District selection page for customers"""
    if request.user.user_type != 'customer':
        messages.error(request, 'Access denied')
        return redirect('home')
    
    if request.method == 'POST':
        form = DistrictSelectionForm(request.POST)
        if form.is_valid():
            district = form.cleaned_data['district']
            request.session['selected_district'] = district
            messages.success(request, f'District changed to {dict(DISTRICT_CHOICES).get(district)}')
            return redirect('customer_home')
        else:
            messages.error(request, 'Please select a valid district')
    else:
        # Pre-fill with current district
        current_district = request.session.get('selected_district', request.user.customer_profile.district)
        form = DistrictSelectionForm(initial={'district': current_district})
    
    return render(request, 'services/select_district.html', {'form': form})


@login_required
def customer_home(request):
    """Home page for customers - shows all services"""
    if request.user.user_type != 'customer':
        messages.error(request, 'Access denied')
        return redirect('home')
    
    # Get district from session or customer profile
    selected_district = request.session.get('selected_district')
    if not selected_district:
        # Set from customer profile
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


@login_required
def service_providers_list(request, service_code):
    """List all providers for a specific service in selected district"""
    if request.user.user_type != 'customer':
        messages.error(request, 'Access denied')
        return redirect('home')
    
    selected_district = request.session.get('selected_district')
    if not selected_district:
        selected_district = request.user.customer_profile.district
        request.session['selected_district'] = selected_district
    
    service_names = dict(ServiceProvider.SERVICE_CHOICES)
    service_name = service_names.get(service_code, 'Unknown Service')
    
    # Find all verified providers offering this service in the selected district
    providers = ServiceProvider.objects.filter(
        Q(service1=service_code) | Q(service2=service_code) | Q(service3=service_code)
    ).filter(is_verified=True, district=selected_district)
    
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
        'selected_district': selected_district_name
    })


@login_required
def add_review(request, provider_phone):
    """Add or update review for a provider"""
    if request.user.user_type != 'customer':
        messages.error(request, 'Only customers can add reviews')
        return redirect('home')
    
    provider = get_object_or_404(ServiceProvider, user__phone_number=provider_phone)
    customer = request.user.customer_profile
    
    # Check if review already exists
    existing_review = Review.objects.filter(customer=customer, provider=provider).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = customer
            review.provider = provider
            review.save()
            
            if existing_review:
                messages.success(request, 'Review updated successfully!')
            else:
                messages.success(request, 'Review added successfully!')
            
            return redirect('service_providers_list', service_code=provider.service1)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReviewForm(instance=existing_review)
    
    return render(request, 'services/add_review.html', {
        'form': form,
        'provider': provider,
        'existing_review': existing_review
    })


@login_required
def profile_view(request):
    """View profile"""
    if request.user.user_type == 'provider':
        return redirect('provider_home')
    else:
        customer = request.user.customer_profile
        return render(request, 'services/customer_profile.html', {'customer': customer})


@login_required
def edit_profile(request):
    """Edit profile"""
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
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = ProfileEditForm(instance=user)
        
        if user.user_type == 'provider':
            profile_form = ProviderProfileEditForm(instance=user.provider_profile)
        else:
            profile_form = CustomerProfileEditForm(instance=user.customer_profile)
    
    return render(request, 'services/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def change_password(request):
    """Change password"""
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


@login_required
def logout_view(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')

# services/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Home and login/register choices
    path('', views.home, name='home'),
    path('login-choice/', views.login_choice, name='login_choice'),
    path('register-choice/', views.register_choice, name='register_choice'),
    
    # Login
    path('login/<str:user_type>/', views.login_view, name='login'),
    
    # Registration
    path('register/provider/', views.register_provider, name='register_provider'),
    path('register/customer/', views.register_customer, name='register_customer'),
    
    # District selection
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
]


#admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ServiceProvider, Customer, ServiceRequest

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('phone_number', 'name', 'user_type', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('phone_number', 'name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('name', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'name', 'user_type', 'password1', 'password2'),
        }),
    )

class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('user', 'aadhar_number', 'is_verified', 'rating', 'total_reviews', 'created_at')
    list_filter = ('is_verified', 'service1', 'service2', 'service3', 'created_at')
    search_fields = ('user__name', 'user__phone_number', 'aadhar_number')
    readonly_fields = ('created_at',)
    list_editable = ('is_verified',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Personal Details', {
            'fields': ('photo', 'address', 'aadhar_number', 'date_of_birth')
        }),
        ('Services', {
            'fields': ('service1', 'service2', 'service3')
        }),
        ('Status & Ratings', {
            'fields': ('is_verified', 'rating', 'total_reviews')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'created_at')
    search_fields = ('user__name', 'user__phone_number')
    readonly_fields = ('created_at',)

class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('customer', 'provider', 'service_type', 'status', 'created_at')
    list_filter = ('status', 'service_type', 'created_at')
    search_fields = ('customer__user__name', 'provider__user__name')
    readonly_fields = ('created_at',)
    list_editable = ('status',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(ServiceProvider, ServiceProviderAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(ServiceRequest, ServiceRequestAdmin)

# Customize admin site headers
admin.site.site_header = "ServiceHub Administration"
admin.site.site_title = "ServiceHub Admin"
admin.site.index_title = "Welcome to ServiceHub Administration"


#login.html

{% extends 'services/base.html' %}

{% block title %}Login - {{ user_type|title }}{% endblock %}

{% block content %}
<div class="hero min-h-[70vh]">
    <div class="hero-content">
        <div class="card glass-effect w-full max-w-md">
            <div class="card-body">
                <div class="text-center mb-6">
                    <div class="w-20 h-20 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center mx-auto mb-4">
                        <i class="fas {% if user_type == 'provider' %}fa-briefcase{% else %}fa-user{% endif %} text-4xl text-white"></i>
                    </div>
                    <h2 class="text-3xl font-bold">{{ user_type|title }} Login</h2>
                    <p class="text-base-content/70 mt-2">Enter your credentials to continue</p>
                </div>
                
                <form method="POST">
                    {% csrf_token %}
                    
                    <div class="form-control">
                        <label class="label">
                            <span class="label-text">Phone Number</span>
                        </label>
                        {{ form.username }}
                    </div>
                    
                    <div class="form-control mt-4">
                        <label class="label">
                            <span class="label-text">Password</span>
                        </label>
                        {{ form.password }}
                    </div>
                    
                    <div class="form-control mt-6">
                        <button type="submit" class="btn btn-primary btn-block hover-lift">
                            <i class="fas fa-sign-in-alt mr-2"></i> Login
                        </button>
                    </div>
                </form>
                
                <div class="divider">OR</div>
                
                <div class="text-center">
                    <p class="text-base-content/70">
                        Don't have an account?
                        <a href="{% if user_type == 'provider' %}{% url 'register_provider' %}{% else %}{% url 'register_customer' %}{% endif %}" 
                           class="link link-primary font-semibold">Register here</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

#customer_home.html

{% extends 'services/base.html' %}

{% block title %}Services - ServiceHub{% endblock %}

{% block content %}
<div class="mb-8">
    <div class="flex justify-between items-center flex-wrap gap-4">
        <div>
            <h1 class="text-4xl font-bold mb-2">Welcome, {{ user.name }}! 👋</h1>
            <p class="text-xl text-base-content/70">
                <i class="fas fa-map-marker-alt text-primary mr-2"></i>
                Showing services in: <span class="badge badge-primary badge-lg">{{ selected_district }}</span>
            </p>
        </div>
        <a href="{% url 'select_district' %}" class="btn btn-outline btn-primary">
            <i class="fas fa-map-marked-alt mr-2"></i>
            Change District
        </a>
    </div>
</div>

<div class="divider"></div>

<h2 class="text-3xl font-bold mb-6">Choose a Service</h2>

<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
    {% for service in services %}
    <a href="{% url 'service_providers_list' service_code=service.code %}" 
       class="card glass-effect hover-lift card-shine cursor-pointer group">
        <div class="card-body items-center text-center p-8">
            <div class="w-24 h-24 rounded-full bg-gradient-to-br {{ service.gradient }} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <i class="fas fa-{{ service.icon }} text-5xl text-white animate-icon"></i>
            </div>
            <h3 class="card-title text-2xl">{{ service.name }}</h3>
            <div class="badge badge-ghost">Find Providers</div>
        </div>
    </a>
    {% endfor %}
</div>

<div class="card glass-effect mt-12">
    <div class="card-body">
        <h3 class="card-title text-2xl mb-4">
            <i class="fas fa-info-circle text-info mr-2"></i>
            How It Works
        </h3>
        <div class="steps steps-vertical lg:steps-horizontal w-full">
            <div class="step step-primary">
                <div class="text-left">
                    <p class="font-bold">Select Service</p>
                    <p class="text-sm opacity-70">Choose from available services</p>
                </div>
            </div>
            <div class="step step-primary">
                <div class="text-left">
                    <p class="font-bold">Browse Providers</p>
                    <p class="text-sm opacity-70">View verified professionals</p>
                </div>
            </div>
            <div class="step step-primary">
                <div class="text-left">
                    <p class="font-bold">Check Reviews</p>
                    <p class="text-sm opacity-70">Read customer feedback</p>
                </div>
            </div>
            <div class="step step-primary">
                <div class="text-left">
                    <p class="font-bold">Contact & Hire</p>
                    <p class="text-sm opacity-70">Get in touch directly</p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}


#providers list.html

{% extends 'services/base.html' %}

{% block title %}{{ service_name }} Providers - ServiceHub{% endblock %}

{% block content %}
<div class="mb-8">
    <a href="{% url 'customer_home' %}" class="btn btn-ghost mb-4">
        <i class="fas fa-arrow-left mr-2"></i> Back to Services
    </a>
    
    <div class="card glass-effect">
        <div class="card-body text-center">
            <h1 class="text-4xl font-bold mb-2">
                <i class="fas fa-users text-primary mr-3"></i>
                {{ service_name }} Service Providers
            </h1>
            <p class="text-xl text-base-content/70">
                <i class="fas fa-map-marker-alt text-success mr-2"></i>
                Showing providers in: <span class="badge badge-primary badge-lg">{{ selected_district }}</span>
            </p>
            <div class="badge badge-info badge-lg mt-4">
                {{ providers.count }} Verified Provider{{ providers.count|pluralize }} Found
            </div>
            <p class="text-sm text-base-content/60 mt-2">
                <i class="fas fa-info-circle mr-1"></i>
                To search in another district, update your district in Profile → Edit Profile
            </p>
        </div>
    </div>
</div>

{% if providers %}
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    {% for provider in providers %}
    <div class="card glass-effect hover-lift card-shine">
        <div class="card-body">
            <!-- Provider Header -->
            <div class="flex items-start gap-4 pb-4 border-b border-base-300">
                <div class="avatar placeholder">
                    <div class="w-20 h-20 rounded-full {% if provider.photo %}{% else %}bg-gradient-to-br from-primary to-secondary{% endif %}">
                        {% if provider.photo %}
                        <img src="{{ provider.photo.url }}" alt="{{ provider.user.name }}">
                        {% else %}
                        <span class="text-3xl text-white">{{ provider.user.name|first|upper }}</span>
                        {% endif %}
                    </div>
                </div>
                
                <div class="flex-1">
                    <h3 class="text-2xl font-bold">{{ provider.user.name }}</h3>
                    <p class="text-base-content/70">
                        <i class="fas fa-phone text-primary mr-2"></i>
                        {{ provider.user.phone_number }}
                    </p>
                    {% if provider.is_verified %}
                    <div class="badge badge-success gap-2 mt-2">
                        <i class="fas fa-check-circle"></i>
                        Verified Provider
                    </div>
                    {% endif %}
                </div>
            </div>
            
            <!-- Provider Details -->
            <div class="space-y-3 my-4">
                <div class="flex items-start gap-3">
                    <i class="fas fa-map-marker-alt text-primary mt-1"></i>
                    <div class="flex-1">
                        <p class="text-sm text-base-content/60">Address</p>
                        <p>{{ provider.address }}</p>
                    </div>
                </div>
                
                <div class="flex items-start gap-3">
                    <i class="fas fa-map text-success mt-1"></i>
                    <div class="flex-1">
                        <p class="text-sm text-base-content/60">District</p>
                        <p>{{ provider.get_district_display }}</p>
                    </div>
                </div>
                
                <div class="flex items-start gap-3">
                    <i class="fas fa-calendar text-info mt-1"></i>
                    <div class="flex-1">
                        <p class="text-sm text-base-content/60">Member Since</p>
                        <p>{{ provider.created_at|date:"d M, Y" }}</p>
                    </div>
                </div>
            </div>
            
            <!-- Services Offered -->
            <div class="card bg-base-200">
                <div class="card-body p-4">
                    <h4 class="font-semibold mb-2">
                        <i class="fas fa-tools text-primary mr-2"></i>
                        Services Offered
                    </h4>
                    <div class="flex flex-wrap gap-2">
                        {% for service in provider.get_services %}
                        <div class="badge badge-primary">{{ service }}</div>
                        {% endfor %}
                    </div>
                </div>
            </div>
            
            <!-- Rating Display -->
            <div class="card bg-gradient-to-br from-amber-500 to-orange-500 text-white mt-4">
                <div class="card-body p-4 flex-row items-center justify-between">
                    <div>
                        <div class="flex gap-1 text-2xl mb-1">
                            {% for i in "12345" %}
                                {% if forloop.counter <= provider.rating %}
                                    <i class="fas fa-star"></i>
                                {% else %}
                                    <i class="far fa-star"></i>
                                {% endif %}
                            {% endfor %}
                        </div>
                        <p class="text-sm opacity-90">{{ provider.total_reviews }} review{{ provider.total_reviews|pluralize }}</p>
                    </div>
                    <div class="text-5xl font-bold">{{ provider.rating }}</div>
                </div>
            </div>
            
            <!-- Action Buttons -->
            <div class="card-actions justify-end mt-4">
                {% if provider.user_has_reviewed %}
                <a href="{% url 'add_review' provider_phone=provider.user.phone_number %}" class="btn btn-outline btn-warning">
                    <i class="fas fa-edit mr-2"></i>
                    Edit Review
                </a>
                {% else %}
                <a href="{% url 'add_review' provider_phone=provider.user.phone_number %}" class="btn btn-primary">
                    <i class="fas fa-star mr-2"></i>
                    Add Review
                </a>
                {% endif %}
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% else %}
<div class="card glass-effect">
    <div class="card-body text-center py-20">
        <div class="text-8xl mb-6">
            <i class="fas fa-exclamation-circle text-warning animate-icon"></i>
        </div>
        <h3 class="text-3xl font-bold mb-4">No Providers Available</h3>
        <p class="text-xl text-base-content/70 mb-2">
            No verified {{ service_name }} providers found in {{ selected_district }}.
        </p>
        <p class="text-base-content/60 mb-6">
            Try checking another service or update your district in your profile.
        </p>
        <div class="flex gap-4 justify-center flex-wrap">
            <a href="{% url 'customer_home' %}" class="btn btn-primary">
                <i class="fas fa-arrow-left mr-2"></i>
                Browse Other Services
            </a>
        </div>
    </div>
</div>
{% endif %}
{% endblock %}


#service provider list old function

@login_required
def service_providers_list(request, service_code):
    """List all providers for a specific service in selected district"""
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
        
        # Find all verified providers offering this service in the selected district
        providers = ServiceProvider.objects.filter(
            Q(service1=service_code) | Q(service2=service_code) | Q(service3=service_code)
        ).filter(is_verified=True, district=selected_district)
        
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
            'selected_district': selected_district_name
        })
    except Exception as e:
        messages.error(request, 'An error occurred. Please try again.')
        print(f"Providers list error: {e}")
        return redirect('customer_home')



        