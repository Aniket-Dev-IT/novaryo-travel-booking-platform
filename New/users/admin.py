from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserPreference


class UserPreferenceInline(admin.StackedInline):
    model = UserPreference
    can_delete = False
    verbose_name_plural = 'Preferences'
    fields = (
        ('default_adults', 'default_children', 'default_rooms'),
        ('preferred_hotel_class', 'preferred_cabin_class', 'preferred_seat_type'),
        ('profile_visibility',)
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'email', 'first_name', 'last_name', 'preferred_currency', 
        'is_email_verified', 'is_active', 'is_staff', 'date_joined'
    ]
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 'is_email_verified', 
        'preferred_currency', 'preferred_language', 'primary_travel_purpose'
    ]
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Authentication', {
            'fields': ('email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth', 'profile_picture', 'bio')
        }),
        ('Address', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country'),
            'classes': ('collapse',)
        }),
        ('Preferences', {
            'fields': ('preferred_currency', 'preferred_language', 'primary_travel_purpose'),
        }),
        ('Travel Profile', {
            'fields': ('frequent_traveler',),
        }),
        ('Notifications', {
            'fields': ('email_notifications', 'sms_notifications', 'marketing_emails'),
            'classes': ('collapse',)
        }),
        ('Verification Status', {
            'fields': ('is_email_verified', 'is_phone_verified')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', 'last_login_ip'),
            'classes': ('collapse',)
        })
    )
    
    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login']
    inlines = [UserPreferenceInline]
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'default_adults', 'default_children', 'preferred_hotel_class', 
        'preferred_cabin_class', 'profile_visibility'
    ]
    list_filter = ['preferred_hotel_class', 'preferred_cabin_class', 'profile_visibility']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
