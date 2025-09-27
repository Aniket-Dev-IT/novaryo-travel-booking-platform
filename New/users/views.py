from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
import uuid
import hashlib

from .models import (
    User, UserPreference, SavedHotel, SavedSearch,
    UserLoginLog, EmailVerificationToken, PasswordResetToken
)
from .forms import (
    NovarvoUserCreationForm, NovarvoAuthenticationForm,
    UserProfileForm, UserPreferenceForm, ProfilePictureForm
)
from hotels.models import Hotel


class UserRegistrationView(CreateView):
    """User registration view"""
    model = User
    form_class = NovarvoUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:registration_success')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        
        # Create email verification token
        self.create_email_verification_token(user)
        
        # Log the registration
        messages.success(
            self.request, 
            'Registration successful! Please check your email to verify your account.'
        )
        
        return response
    
    def create_email_verification_token(self, user):
        """Create email verification token for user"""
        token = hashlib.sha256(f"{user.id}{uuid.uuid4()}".encode()).hexdigest()[:50]
        expires_at = timezone.now() + timedelta(hours=24)
        
        EmailVerificationToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        # TODO: Send verification email
        # This would typically use Celery for async email sending
        print(f"Verification email would be sent to {user.email} with token: {token}")


class UserLoginView(LoginView):
    """Custom login view"""
    form_class = NovarvoAuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('hotels:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Set session expiry based on remember me
        if form.cleaned_data.get('remember_me'):
            self.request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
        else:
            self.request.session.set_expiry(0)  # Session expires when browser closes
        
        # Log the login
        self.log_user_login(form.get_user(), True)
        
        messages.success(self.request, f'Welcome back, {form.get_user().first_name}!')
        return response
    
    def form_invalid(self, form):
        # Log failed login attempt
        email = form.cleaned_data.get('username')
        if email:
            try:
                user = User.objects.get(email=email)
                self.log_user_login(user, False)
            except User.DoesNotExist:
                pass
        
        return super().form_invalid(form)
    
    def log_user_login(self, user, successful):
        """Log user login attempt"""
        UserLoginLog.objects.create(
            user=user,
            ip_address=self.get_client_ip(),
            user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
            login_successful=successful,
            login_method='email'
        )
    
    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class UserLogoutView(LogoutView):
    """Custom logout view"""
    next_page = reverse_lazy('hotels:home')
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


class RegistrationSuccessView(TemplateView):
    """Registration success page"""
    template_name = 'users/registration_success.html'


@method_decorator(login_required, name='dispatch')
class UserDashboardView(TemplateView):
    """User dashboard with overview"""
    template_name = 'users/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context.update({
            'saved_hotels_count': user.saved_hotels.count(),
            'saved_searches_count': user.saved_searches.count(),
            'recent_saved_hotels': user.saved_hotels.all()[:3],
            'recent_login_logs': user.login_logs.filter(login_successful=True)[:5],
            'profile_completion': self.calculate_profile_completion(user),
        })
        
        return context
    
    def calculate_profile_completion(self, user):
        """Calculate profile completion percentage"""
        fields_to_check = [
            'first_name', 'last_name', 'phone_number', 'date_of_birth',
            'city', 'country', 'profile_picture'
        ]
        
        completed_fields = 0
        for field in fields_to_check:
            if getattr(user, field):
                completed_fields += 1
        
        return (completed_fields / len(fields_to_check)) * 100


@method_decorator(login_required, name='dispatch')
class UserProfileView(UpdateView):
    """User profile editing view"""
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['preference_form'] = UserPreferenceForm(
            instance=getattr(self.request.user, 'preferences', None)
        )
        context['picture_form'] = ProfilePictureForm(instance=self.request.user)
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class UserPreferencesView(UpdateView):
    """User preferences editing view"""
    model = UserPreference
    form_class = UserPreferenceForm
    template_name = 'users/preferences.html'
    success_url = reverse_lazy('users:preferences')
    
    def get_object(self):
        preferences, created = UserPreference.objects.get_or_create(
            user=self.request.user
        )
        return preferences
    
    def form_valid(self, form):
        messages.success(self.request, 'Preferences updated successfully!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class SavedHotelsView(TemplateView):
    """User's saved hotels view"""
    template_name = 'users/saved_hotels.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        saved_hotels = self.request.user.saved_hotels.select_related('hotel', 'hotel__city')
        paginator = Paginator(saved_hotels, 12)  # Show 12 hotels per page
        
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context.update({
            'saved_hotels': page_obj,
            'total_saved': saved_hotels.count(),
        })
        
        return context


@login_required
def toggle_saved_hotel(request, hotel_id):
    """Toggle hotel save status via AJAX"""
    if request.method == 'POST':
        hotel = get_object_or_404(Hotel, id=hotel_id, is_active=True)
        saved_hotel, created = SavedHotel.objects.get_or_create(
            user=request.user,
            hotel=hotel
        )
        
        if not created:
            saved_hotel.delete()
            saved = False
        else:
            saved = True
        
        return JsonResponse({
            'saved': saved,
            'message': 'Hotel saved!' if saved else 'Hotel removed from saved list.'
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def email_verification(request, token):
    """Email verification view"""
    try:
        verification_token = EmailVerificationToken.objects.get(
            token=token,
            is_used=False
        )
        
        if verification_token.is_expired:
            messages.error(request, 'Verification link has expired. Please request a new one.')
            return redirect('users:login')
        
        # Verify the user
        user = verification_token.user
        user.is_email_verified = True
        user.save()
        
        # Mark token as used
        verification_token.is_used = True
        verification_token.save()
        
        messages.success(
            request, 
            'Email verified successfully! You can now log in to your account.'
        )
        return redirect('users:login')
        
    except EmailVerificationToken.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('users:login')


@method_decorator(login_required, name='dispatch')
class AccountSecurityView(TemplateView):
    """Account security settings view"""
    template_name = 'users/security.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Recent login activity
        recent_logins = self.request.user.login_logs.all()[:10]
        
        context.update({
            'recent_logins': recent_logins,
            'is_email_verified': self.request.user.is_email_verified,
            'is_phone_verified': self.request.user.is_phone_verified,
        })
        
        return context
