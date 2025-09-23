# apps/staff/urls.py
from django.urls import path
from .views import (
    AdminDashboardView,
    CustomerListView,
    StaffListView,
    BookingManagementView,
    BookingAssignStaffView,
    StaffDashboardView,
    StaffBookingListView,
    StaffBookingUpdateView,
    ServiceListView,
    ServiceCreateView,
    ServiceUpdateView,
    AnalyticsDashboardView,
    GenerateReportsView,
    CommunicationDashboardView,
    NotificationTemplateCreateView,
    SendBroadcastView,
)

app_name = 'staff'

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('customers/', CustomerListView.as_view(), name='customer_management'),
    path('staff/', StaffListView.as_view(), name='staff_management'),
    path('bookings/', BookingManagementView.as_view(), name='booking_management'),
    path('bookings/<int:pk>/assign/', BookingAssignStaffView.as_view(), name='booking_assign'),
    path('staff-dashboard/', StaffDashboardView.as_view(), name='staff_dashboard'),
    path('staff-bookings/', StaffBookingListView.as_view(), name='staff_booking_list'),
    path('staff-bookings/<int:pk>/update/', StaffBookingUpdateView.as_view(), name='staff_booking_update'),
    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/add/', ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/edit/', ServiceUpdateView.as_view(), name='service_update'),
    path('analytics/', AnalyticsDashboardView.as_view(), name='analytics_dashboard'),
    path('analytics/generate/', GenerateReportsView.as_view(), name='generate_reports'),
    path('communication/', CommunicationDashboardView.as_view(), name='communication_dashboard'),
    path('communication/template/add/', NotificationTemplateCreateView.as_view(), name='notification_template_create'),
    path('communication/broadcast/', SendBroadcastView.as_view(), name='send_broadcast'),
]