from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""
    
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """Create and return a regular user with an email and password"""
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        """Create and return a superuser with an email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, first_name, last_name, password, **extra_fields)
class User(AbstractUser):
    """Custom User model for Novaryo with additional fields"""
    
    # Remove username, use email as the unique identifier
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    objects = UserManager()
    
    # Personal Information
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    phone_number = PhoneNumberField(_('phone number'), blank=True, null=True)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    
    # Profile Information
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True,
        help_text='Upload your profile picture'
    )
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    
    # Preferences
    preferred_currency = models.CharField(
        max_length=3, 
        default='USD',
        choices=[
            ('USD', 'US Dollar'),
            ('EUR', 'Euro'),
            ('GBP', 'British Pound'),
            ('INR', 'Indian Rupee'),
            ('JPY', 'Japanese Yen'),
            ('AUD', 'Australian Dollar'),
            ('CAD', 'Canadian Dollar'),
        ]
    )
    preferred_language = models.CharField(
        max_length=10,
        default='en',
        choices=[
            ('en', 'English'),
            ('es', 'Spanish'),
            ('fr', 'French'),
            ('de', 'German'),
            ('it', 'Italian'),
            ('pt', 'Portuguese'),
            ('ru', 'Russian'),
            ('ja', 'Japanese'),
            ('ko', 'Korean'),
            ('zh', 'Chinese'),
            ('ar', 'Arabic'),
            ('hi', 'Hindi'),
        ]
    )
    
    # Address Information
    address_line_1 = models.CharField(_('address line 1'), max_length=255, blank=True)
    address_line_2 = models.CharField(_('address line 2'), max_length=255, blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    state = models.CharField(_('state/province'), max_length=100, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=20, blank=True)
    country = models.CharField(_('country'), max_length=100, blank=True)
    
    # Travel Preferences
    frequent_traveler = models.BooleanField(default=False)
    travel_purpose_choices = [
        ('leisure', 'Leisure'),
        ('business', 'Business'),
        ('both', 'Both'),
    ]
    primary_travel_purpose = models.CharField(
        max_length=20, 
        choices=travel_purpose_choices,
        default='leisure'
    )
    
    # Notification Preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    marketing_emails = models.BooleanField(default=True)
    
    # Account Status
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'novaryo_users'
    
    def __str__(self):
        return f"{self.email} - {self.get_full_name()}"
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    
    @property
    def full_address(self):
        """Return formatted full address"""
        address_parts = []
        if self.address_line_1:
            address_parts.append(self.address_line_1)
        if self.address_line_2:
            address_parts.append(self.address_line_2)
        if self.city:
            address_parts.append(self.city)
        if self.state:
            address_parts.append(self.state)
        if self.postal_code:
            address_parts.append(self.postal_code)
        if self.country:
            address_parts.append(self.country)
        return ', '.join(address_parts)


class UserPreference(models.Model):
    """Additional user preferences that can be extended"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    
    # Search Preferences
    default_adults = models.PositiveIntegerField(default=1)
    default_children = models.PositiveIntegerField(default=0)
    default_rooms = models.PositiveIntegerField(default=1)
    
    # Hotel Preferences
    preferred_hotel_class = models.CharField(
        max_length=20,
        choices=[
            ('budget', 'Budget (1-2 stars)'),
            ('mid-range', 'Mid-range (3 stars)'),
            ('upscale', 'Upscale (4 stars)'),
            ('luxury', 'Luxury (5+ stars)'),
        ],
        blank=True
    )
    
    # Flight Preferences
    preferred_cabin_class = models.CharField(
        max_length=20,
        choices=[
            ('economy', 'Economy'),
            ('premium_economy', 'Premium Economy'),
            ('business', 'Business'),
            ('first', 'First'),
        ],
        default='economy'
    )
    preferred_seat_type = models.CharField(
        max_length=20,
        choices=[
            ('any', 'Any'),
            ('aisle', 'Aisle'),
            ('window', 'Window'),
        ],
        default='any'
    )
    
    # Privacy Settings
    profile_visibility = models.CharField(
        max_length=20,
        choices=[
            ('public', 'Public'),
            ('friends', 'Friends Only'),
            ('private', 'Private'),
        ],
        default='public'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Preferences for {self.user.email}"


class SavedHotel(models.Model):
    """Hotels saved by users as favorites/wishlist"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_hotels')
    hotel = models.ForeignKey('hotels.Hotel', on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Personal notes about this hotel")
    
    class Meta:
        unique_together = ('user', 'hotel')
        ordering = ['-saved_at']
    
    def __str__(self):
        return f"{self.user.email} saved {self.hotel.name}"


class SavedSearch(models.Model):
    """User's saved search queries for future use"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_searches')
    search_name = models.CharField(max_length=100, help_text="User-defined name for this search")
    
    # Search Parameters
    location = models.CharField(max_length=255, blank=True)
    checkin_offset = models.PositiveIntegerField(default=7, help_text="Days from today for check-in")
    checkout_offset = models.PositiveIntegerField(default=8, help_text="Days from today for check-out")
    adults = models.PositiveIntegerField(default=2)
    children = models.PositiveIntegerField(default=0)
    rooms = models.PositiveIntegerField(default=1)
    
    # Filters
    min_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    min_stars = models.PositiveIntegerField(blank=True, null=True)
    max_stars = models.PositiveIntegerField(blank=True, null=True)
    
    # Price alerts
    price_alert_enabled = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_used']
    
    def __str__(self):
        return f"{self.user.email} - {self.search_name}"


class UserLoginLog(models.Model):
    """Track user login attempts and history for security"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_logs')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    login_successful = models.BooleanField()
    login_method = models.CharField(
        max_length=20,
        choices=[
            ('email', 'Email/Password'),
            ('google', 'Google'),
            ('facebook', 'Facebook'),
            ('apple', 'Apple'),
        ],
        default='email'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        status = 'Success' if self.login_successful else 'Failed'
        return f"{self.user.email} - {status} ({self.timestamp})"


class EmailVerificationToken(models.Model):
    """Email verification tokens for new registrations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_tokens')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Email verification token for {self.user.email}"
    
    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at


class PasswordResetToken(models.Model):
    """Password reset tokens"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Password reset token for {self.user.email}"
    
    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at
