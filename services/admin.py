from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ServiceProvider, Customer, ServiceRequest, Review, OTPVerification

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

class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'otp', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('phone_number',)
    readonly_fields = ('created_at',)

admin.site.register(OTPVerification, OTPVerificationAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(ServiceProvider, ServiceProviderAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(ServiceRequest, ServiceRequestAdmin)

# Customize admin site headers
admin.site.site_header = "ServiceHub Administration"
admin.site.site_title = "ServiceHub Admin"
admin.site.index_title = "Welcome to ServiceHub Administration"