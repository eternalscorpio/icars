# apps/users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new user, used for customer self-registration.
    Uses email as the primary identifier instead of username.
    Includes additional fields like phone_number and address.
    """
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'password1',
            'password2',
        )
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'email': _('Email Address'),
            'phone_number': _('Phone Number'),
            'address': _('Address'),
        }
        help_texts = {
            'email': _('Required for account verification and notifications.'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make username not required, as email is used
        if 'username' in self.fields:
            self.fields.pop('username')
        # Set email field attributes
        self.fields['email'].widget.attrs.update({'autofocus': True})


class CustomUserUpdateForm(UserChangeForm):
    """
    Form for updating user profile.
    Dynamically shows/hides fields based on user's role.
    Password is not editable here; use separate password change view if needed.
    """
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'specialization',
        )
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'email': _('Email Address'),
            'phone_number': _('Phone Number'),
            'address': _('Address'),
            'specialization': _('Specialization'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Remove password field as it's not for updating here
        self.fields.pop('password', None)
        
        # Make username not editable if present
        if 'username' in self.fields:
            self.fields['username'].disabled = True
        
        # Role-based field visibility
        if user:
            if not (user.is_staff_member or user.is_admin):
                # Hide specialization for customers
                self.fields.pop('specialization', None)
        else:
            # Default: include all, but in practice, user is passed
            pass

    def clean_email(self):
        """
        Ensure email uniqueness, excluding the current user.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_('This email address is already in use.'))
        return email