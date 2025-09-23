# apps/customers/forms.py

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Vehicle

class VehicleForm(forms.ModelForm):
    """
    Form for creating/updating vehicle details.
    """
    class Meta:
        model = Vehicle
        fields = ('make', 'model', 'year', 'license_plate', 'vin')
        labels = {
            'make': _('Make'),
            'model': _('Model'),
            'year': _('Year'),
            'license_plate': _('License Plate'),
            'vin': _('VIN'),
        }

    def clean_vin(self):
        vin = self.cleaned_data.get('vin')
        if len(vin) != 17:
            raise forms.ValidationError(_('VIN must be exactly 17 characters.'))
        if Vehicle.objects.filter(vin=vin).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError(_('This VIN is already registered.'))
        return vin

    def clean_license_plate(self):
        license_plate = self.cleaned_data.get('license_plate')
        if Vehicle.objects.filter(license_plate=license_plate).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError(_('This license plate is already registered.'))
        return license_plate