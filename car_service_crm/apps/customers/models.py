# apps/customers/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User

class Vehicle(models.Model):
    """
    Model to store customer vehicle details.
    Linked to a User with CUSTOMER role.
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.ROLE_CUSTOMER},
        verbose_name=_('Owner'),
        related_name='vehicles'
    )
    make = models.CharField(
        max_length=50,
        verbose_name=_('Make'),
        help_text=_('Vehicle manufacturer, e.g., Toyota, Ford.')
    )
    model = models.CharField(
        max_length=50,
        verbose_name=_('Model'),
        help_text=_('Vehicle model, e.g., Corolla, Mustang.')
    )
    year = models.PositiveIntegerField(
        verbose_name=_('Year'),
        help_text=_('Manufacturing year, e.g., 2020.')
    )
    license_plate = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('License Plate'),
        help_text=_('Unique license plate number.')
    )
    vin = models.CharField(
        max_length=17,
        unique=True,
        verbose_name=_('VIN'),
        help_text=_('Vehicle Identification Number.')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"