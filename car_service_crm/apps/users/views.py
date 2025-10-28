# apps/users/views.py

from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic.base import View
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import User


class CustomLoginView(LoginView):
    """
    Custom login view that redirects users based on their role after successful login.
    """
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_admin:
            return reverse_lazy('staff:admin_dashboard')  # Assuming admin dashboard URL
        elif user.is_staff_member:
            return reverse_lazy('staff:staff_dashboard')  # Assuming staff dashboard URL
        elif user.is_customer:
            return reverse_lazy('customers:customers_dashboard')  # Use correct namespace
        return reverse_lazy('home')  # Fallback


class CustomLogoutView(LogoutView):
    """
    Custom logout view that redirects to the login page after logout.
    """
    http_method_names = ['post']
    next_page = reverse_lazy('users:login')


class UserRegistrationView(CreateView):
    """
    View for customer registration. Admins create staff accounts separately.
    Only allows creation of Customer role users.
    """
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users/login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = User.ROLE_CUSTOMER  # Force customer role for self-registration
        user.save()
        login(self.request, user)  # Auto-login after registration
        return redirect(self.success_url)


class UserProfileView(LoginRequiredMixin, DetailView):
    """
    View to display user profile details.
    Accessible only by the user themselves or admins.
    """
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        return self.request.user  # Default to current user

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return self.handle_no_permission()
        # Admins can view any profile, others only their own
        if user.is_admin or self.get_object().pk == user.pk:
            return super().dispatch(request, *args, **kwargs)
        return redirect('home')  # Or raise permission denied


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    View to update user profile.
    Fields editable depend on role (via form).
    """
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/update_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user  # Only allow updating own profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass user to form for role-based fields
        return kwargs


class RoleBasedRedirectView(LoginRequiredMixin, View):
    """
    Redirect view after login or for dashboard access, based on role.
    Can be used as a home view.
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_admin:
            return reverse_lazy('staff:admin_dashboard')
        elif user.is_staff_member:  
            return reverse_lazy('staff:staff_dashboard')
        elif user.is_customer:
            return reverse_lazy('customers:customers_dashboard')
        return redirect('login')  #Fallback if no role