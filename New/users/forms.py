from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import User, UserPreference


class NovarvoUserCreationForm(UserCreationForm):
    """Custom user registration form with additional fields"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )
    
    # Additional fields
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1234567890'
        })
    )
    preferred_currency = forms.ChoiceField(
        choices=User._meta.get_field('preferred_currency').choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Terms agreement
    agree_to_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='I agree to the Terms of Service and Privacy Policy'
    )
    marketing_emails = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Send me travel deals and promotional emails'
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 
                 'preferred_currency', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data.get('phone_number')
        user.preferred_currency = self.cleaned_data['preferred_currency']
        user.marketing_emails = self.cleaned_data.get('marketing_emails', True)
        
        if commit:
            user.save()
            # Create user preferences
            UserPreference.objects.get_or_create(user=user)
        return user


class NovarvoAuthenticationForm(AuthenticationForm):
    """Custom login form with styled inputs"""
    
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
            'autofocus': True
        }),
        label='Email Address'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Remember me for 30 days'
    )
    
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(
                self.request, 
                email=email, 
                password=password
            )
            if self.user_cache is None:
                raise ValidationError("Invalid email or password.")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile information"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 'date_of_birth',
            'bio', 'preferred_currency', 'preferred_language',
            'address_line_1', 'address_line_2', 'city', 'state',
            'postal_code', 'country', 'primary_travel_purpose',
            'email_notifications', 'sms_notifications', 'marketing_emails'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell us a bit about yourself...'
            }),
            'preferred_currency': forms.Select(attrs={'class': 'form-select'}),
            'preferred_language': forms.Select(attrs={'class': 'form-select'}),
            'address_line_1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street address'
            }),
            'address_line_2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apartment, suite, etc. (optional)'
            }),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province'
            }),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'primary_travel_purpose': forms.Select(attrs={'class': 'form-select'}),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sms_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'marketing_emails': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UserPreferenceForm(forms.ModelForm):
    """Form for editing user travel preferences"""
    
    class Meta:
        model = UserPreference
        fields = [
            'default_adults', 'default_children', 'default_rooms',
            'preferred_hotel_class', 'preferred_cabin_class',
            'preferred_seat_type', 'profile_visibility'
        ]
        
        widgets = {
            'default_adults': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10
            }),
            'default_children': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 10
            }),
            'default_rooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5
            }),
            'preferred_hotel_class': forms.Select(attrs={'class': 'form-select'}),
            'preferred_cabin_class': forms.Select(attrs={'class': 'form-select'}),
            'preferred_seat_type': forms.Select(attrs={'class': 'form-select'}),
            'profile_visibility': forms.Select(attrs={'class': 'form-select'}),
        }


class CustomPasswordResetForm(PasswordResetForm):
    """Custom password reset form with styling"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )


class ProfilePictureForm(forms.ModelForm):
    """Form for uploading profile picture"""
    
    class Meta:
        model = User
        fields = ['profile_picture']
        
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def clean_profile_picture(self):
        image = self.cleaned_data.get('profile_picture')
        if image:
            # Check file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Image file too large (max 5MB)")
            
            # Check file type
            if not image.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise ValidationError("Only PNG, JPG, JPEG, and GIF files are allowed")
        
        return image