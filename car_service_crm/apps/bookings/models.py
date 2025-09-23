# apps/bookings/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from apps.customers.models import Vehicle
from apps.services.models import Service

class Booking(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_CANCELLED = 'CANCELLED'

    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_IN_PROGRESS, _('In Progress')),
        (STATUS_COMPLETED, _('Completed')),
        (STATUS_CANCELLED, _('Cancelled')),
    ]

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.ROLE_CUSTOMER},
        verbose_name=_('Customer'),
        related_name='bookings'
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        verbose_name=_('Vehicle'),
        related_name='bookings'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        verbose_name=_('Service'),
        related_name='bookings'
    )
    scheduled_date = models.DateTimeField(
        verbose_name=_('Scheduled Date'),
        help_text=_('Date and time of the appointment.')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name=_('Status')
    )
    assigned_staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        limit_choices_to={'role': User.ROLE_STAFF},
        null=True,
        blank=True,
        verbose_name=_('Assigned Staff'),
        related_name='assigned_bookings'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Notes'),
        help_text=_('Additional notes or customer requests.')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    feedback_submitted = models.BooleanField(default=False, verbose_name=_('Feedback Submitted'))

    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')
        ordering = ['-scheduled_date']

    def __str__(self):
        return f"{self.service.name} for {self.vehicle} on {self.scheduled_date}"
    
class Feedback(models.Model):
    """
    Model to store customer feedback for completed bookings.
    """
    RATING_CHOICES = [
        (1, '1 Star - Poor'),
        (2, '2 Stars - Fair'),
        (3, '3 Stars - Average'),
        (4, '4 Stars - Good'),
        (5, '5 Stars - Excellent'),
    ]

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        verbose_name=_('Booking'),
        related_name='feedback'
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name=_('Rating')
    )
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Comments'),
        help_text=_('Optional feedback comments')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback for Booking #{self.booking.id}"