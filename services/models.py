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