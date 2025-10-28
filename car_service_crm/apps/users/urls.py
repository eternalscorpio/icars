# apps/users/urls.py

from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from .views import (
    CustomLoginView,
    CustomLogoutView,
    UserRegistrationView,
    UserProfileView,
    UserUpdateView,
    RoleBasedRedirectView,
)

app_name = 'users'  # Namespace for URL reversing

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    
    # Profile Management
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserUpdateView.as_view(), name='update_profile'),
    
    # Role-based Redirect (e.g., for home after login)
    path('', RoleBasedRedirectView.as_view(), name='home'),
    
    # Password Reset URLs (using Django's built-in views)
    path('password_reset/', PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]