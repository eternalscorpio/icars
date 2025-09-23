# apps/services/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class Service(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Service Name'),
        help_text=_('e.g., Oil Change, Engine Repair')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Description'),
        help_text=_('Details about the service')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Price'),
        help_text=_('Cost of the service in USD')
    )
    duration = models.DurationField(
        verbose_name=_('Duration'),
        help_text=_('Estimated time to complete the service, e.g., 01:30:00 for 1.5 hours')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['name']

    def __str__(self):
        return self.name