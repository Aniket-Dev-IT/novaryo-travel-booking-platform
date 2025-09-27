from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomPasswordResetForm

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('registration-success/', views.RegistrationSuccessView.as_view(), name='registration_success'),
    
    # Email verification
    path('verify-email/<str:token>/', views.email_verification, name='verify_email'),
    
    # Password reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html',
             form_class=CustomPasswordResetForm,
             success_url='/users/password-reset/done/',
             email_template_name='users/password_reset_email.html',
         ), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             success_url='/users/password-reset-complete/'
         ), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    
    # User dashboard and profile
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('preferences/', views.UserPreferencesView.as_view(), name='preferences'),
    path('security/', views.AccountSecurityView.as_view(), name='security'),
    
    # Saved items
    path('saved-hotels/', views.SavedHotelsView.as_view(), name='saved_hotels'),
    path('api/toggle-saved-hotel/<int:hotel_id>/', views.toggle_saved_hotel, name='toggle_saved_hotel'),
]
