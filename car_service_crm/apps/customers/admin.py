# apps/customers/admin.py
from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """
    Admin interface for Vehicle model.
    """
    list_display = ('license_plate', 'make', 'model', 'year', 'owner', 'created_at')
    list_filter = ('make', 'year', 'owner')
    search_fields = ('license_plate', 'vin', 'make', 'model', 'owner__email')
    ordering = ('-created_at',)
    raw_id_fields = ('owner',)  # Improves performance for large user bases