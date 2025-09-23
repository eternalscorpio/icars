# apps/bookings/forms.py
from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Booking,Feedback
from apps.customers.models import Vehicle
from apps.services.models import Service  # Add this import

class BookingForm(forms.ModelForm):
    """
    Form for creating/updating bookings by customers.
    """
    class Meta:
        model = Booking
        fields = ('vehicle', 'service', 'scheduled_date', 'notes')  # Updated service_type to service
        labels = {
            'vehicle': _('Vehicle'),
            'service': _('Service'),  # Updated label
            'scheduled_date': _('Scheduled Date and Time'),
            'notes': _('Additional Notes'),
        }
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Limit vehicle choices to those owned by the customer
            self.fields['vehicle'].queryset = Vehicle.objects.filter(owner=user)
        # Set service choices from Service model
        self.fields['service'].queryset = Service.objects.all()

    def clean_scheduled_date(self):
        scheduled_date = self.cleaned_data.get('scheduled_date')
        if scheduled_date < timezone.now():
            raise forms.ValidationError(_('Scheduled date cannot be in the past.'))
        return scheduled_date
    
class FeedbackForm(forms.ModelForm):
    """
    Form for customers to submit feedback on completed bookings.
    """
    class Meta:
        model = Feedback
        fields = ('rating', 'comments')
        labels = {
            'rating': _('Rating'),
            'comments': _('Comments'),
        }
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
        }