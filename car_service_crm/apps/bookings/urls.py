# apps/bookings/urls.py
from django.urls import path
from .views import (
    BookingListView,
    BookingCreateView,
    BookingUpdateView,
    BookingDetailView,
    FeedbackCreateView,
)

app_name = 'bookings'

urlpatterns = [
    path('', BookingListView.as_view(), name='booking_list'),
    path('add/', BookingCreateView.as_view(), name='booking_create'),
    path('<int:pk>/edit/', BookingUpdateView.as_view(), name='booking_update'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('<int:pk>/feedback/', FeedbackCreateView.as_view(), name='feedback_create'),
]