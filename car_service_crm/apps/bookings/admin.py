# apps/bookings/admin.py
from django.contrib import admin
from .models import Booking, Feedback

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('get_service_name', 'customer', 'vehicle', 'scheduled_date', 'status', 'assigned_staff', 'feedback_submitted')  # Added
    list_filter = ('status', 'scheduled_date', 'service')
    search_fields = ('customer__email', 'vehicle__license_plate', 'service__name')
    ordering = ('-scheduled_date',)

    def get_service_name(self, obj):
        return obj.service.name
    get_service_name.short_description = 'Service'

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('booking__id', 'comments')
    ordering = ('-created_at',)