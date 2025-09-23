# apps/analytics/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class RevenueReport(models.Model):
    """
    Model to store monthly revenue reports.
    """
    month = models.DateField(verbose_name=_('Month'), help_text=_('First day of the month for the report'))
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Total Revenue'))
    total_bookings = models.IntegerField(verbose_name=_('Total Bookings'))
    average_rating = models.FloatField(null=True, blank=True, verbose_name=_('Average Customer Rating'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Revenue Report')
        verbose_name_plural = _('Revenue Reports')
        ordering = ['-month']

    def __str__(self):
        return f"Revenue Report for {self.month.strftime('%Y-%m')}"

class StaffPerformance(models.Model):
    """
    Model to store staff performance metrics.
    """
    staff = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'STAFF'},
        verbose_name=_('Staff'),
        related_name='performance_reports'
    )
    month = models.DateField(verbose_name=_('Month'))
    completed_bookings = models.IntegerField(verbose_name=_('Completed Bookings'))
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Total Revenue Generated'))
    average_rating = models.FloatField(null=True, blank=True, verbose_name=_('Average Feedback Rating'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Staff Performance')
        verbose_name_plural = _('Staff Performances')
        ordering = ['-month', 'staff']

    def __str__(self):
        return f"Performance for {self.staff.get_full_name()} - {self.month.strftime('%Y-%m')}"