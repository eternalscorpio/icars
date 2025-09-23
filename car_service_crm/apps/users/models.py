
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Includes role-based access control for Admin, Staff, and Customer.
    """
    
    # Role choices
    ROLE_ADMIN = 'ADMIN'
    ROLE_STAFF = 'STAFF'
    ROLE_CUSTOMER = 'CUSTOMER'

    
    ROLE_CHOICES = [
        (ROLE_ADMIN, _('Admin/Owner/Manager')),
        (ROLE_STAFF, _('Staff/Mechanic/Service Advisor')),
        (ROLE_CUSTOMER, _('Customer')),
    ]
    
    # Additional fields
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_CUSTOMER,
        verbose_name=_('User Role'),
        help_text=_('Defines the user\'s role and permissions in the system.')
    )
    
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_('Phone Number'),
        help_text=_('Contact phone number for the user.')
    )
    
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Address'),
        help_text=_('Physical address of the user.')
    )
    
    # For staff-specific fields (can be null for other roles)
    specialization = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Specialization'),
        help_text=_('Staff expertise, e.g., Engine Repair, AC Service (for Staff role only).')
    )
    
    # Override email to make it required if needed
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required for account verification and notifications.')
    )
    
    # Make username optional if using email as primary identifier
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Optional. If not provided, email will be used for login.')
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','username']  # username is not required
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
    
    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN
    
    @property
    def is_staff_member(self):
        return self.role == self.ROLE_STAFF
    
    @property
    def is_customer(self):
        return self.role == self.ROLE_CUSTOMER
    
    # Additional methods can be added for role-specific logic if needed