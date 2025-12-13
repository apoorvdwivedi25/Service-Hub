# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import User, ServiceProvider, Customer, Review, DISTRICT_CHOICES
from django.core.exceptions import ValidationError
from django.forms import formset_factory

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


# Forgot Password Flow Forms
class ForgotPasswordStep1Form(forms.Form):
    """Step 1: Enter phone number (and DOB for provider)"""
    phone_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': '10-digit phone number'
        })
    )
    # DOB will be added conditionally in the view
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.isdigit() or len(phone) != 10:
            raise ValidationError("Phone number must be exactly 10 digits")
        if phone[0] not in '6789':
            raise ValidationError("Phone number must start with 6, 7, 8, or 9")
        return phone


class ForgotPasswordStep2Form(forms.Form):
    """Step 2: Verify OTP"""
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full text-center text-2xl',
            'placeholder': '000000',
            'maxlength': '6'
        })
    )


class ForgotPasswordStep3Form(forms.Form):
    """Step 3: Reset Password"""
    new_password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'New Password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Confirm Password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError("Passwords don't match")
        return cleaned_data
class WorkPhotoForm(forms.Form):
    """Form for uploading work photos"""
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'file-input file-input-bordered w-full',
            'accept': 'image/*'
        })
    )
    title = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Photo title (optional)'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea textarea-bordered w-full',
            'rows': 2,
            'placeholder': 'Brief description (optional)'
        })
    )

