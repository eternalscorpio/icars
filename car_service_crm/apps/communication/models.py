# apps/communication/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from apps.bookings.models import Booking

class NotificationTemplate(models.Model):
    """
    Model to store reusable notification templates for email/SMS.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Template Name'),
        help_text=_('e.g., Booking Confirmation, Service Reminder')
    )
    subject = models.CharField(
        max_length=200,
        verbose_name=_('Email Subject'),
        help_text=_('Subject line for emails')
    )
    message = models.TextField(
        verbose_name=_('Message Body'),
        help_text=_('Use {customer}, {booking}, {service} for dynamic content')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active'),
        help_text=_('Enable/disable this template')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Notification Template')
        verbose_name_plural = _('Notification Templates')
        ordering = ['name']

    def __str__(self):
        return self.name

class CommunicationLog(models.Model):
    """
    Model to store logs of sent notifications.
    """
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Recipient'),
        related_name='communication_logs'
    )
    booking = models.ForeignKey(
        Booking,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Booking'),
        related_name='communication_logs'
    )
    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Template Used')
    )
    message_type = models.CharField(
        max_length=20,
        choices=[('EMAIL', 'Email'), ('SMS', 'SMS')],
        verbose_name=_('Message Type')
    )
    subject = models.CharField(
        max_length=200,
        verbose_name=_('Subject'),
        blank=True
    )
    message = models.TextField(verbose_name=_('Message Content'))
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('SENT', 'Sent'), ('FAILED', 'Failed')],
        default='SENT',
        verbose_name=_('Status')
    )

    class Meta:
        verbose_name = _('Communication Log')
        verbose_name_plural = _('Communication Logs')
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.message_type} to {self.recipient} on {self.sent_at}"