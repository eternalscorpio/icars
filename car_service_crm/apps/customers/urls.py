# apps/customers/urls.py

from django.urls import path
from .views import (
    CustomerDashboardView,
    VehicleListView,
    VehicleCreateView,
    VehicleUpdateView,
)

app_name = 'customers'

urlpatterns = [
    path('dashboard/', CustomerDashboardView.as_view(), name='customers_dashboard'),
    path('vehicles/', VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/add/', VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/edit/', VehicleUpdateView.as_view(), name='vehicle_update'),
]