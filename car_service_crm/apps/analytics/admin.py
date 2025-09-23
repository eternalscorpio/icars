# apps/analytics/admin.py
from django.contrib import admin
from .models import RevenueReport, StaffPerformance

@admin.register(RevenueReport)
class RevenueReportAdmin(admin.ModelAdmin):
    list_display = ('month', 'total_revenue', 'total_bookings', 'average_rating')
    list_filter = ('month',)
    ordering = ('-month',)

@admin.register(StaffPerformance)
class StaffPerformanceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'month', 'completed_bookings', 'total_revenue', 'average_rating')
    list_filter = ('month', 'staff')
    ordering = ('-month', 'staff')