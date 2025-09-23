# apps/customers/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from .models import Vehicle
from .forms import VehicleForm
from apps.bookings.models import Booking,Feedback

class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'customers/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookings_count'] = Booking.objects.filter(customer=self.request.user).count()
        context['vehicles_count'] = Vehicle.objects.filter(customer=self.request.user).count()
        context['feedback_count'] = Feedback.objects.filter(booking__customer=self.request.user).count()
        context['recent_bookings'] = Booking.objects.filter(customer=self.request.user)[:5]
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_customer:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)
    
class VehicleListView(LoginRequiredMixin, ListView):
    """
    List all vehicles for the logged-in customer.
    """
    model = Vehicle
    template_name = 'customers/vehicle_list.html'
    context_object_name = 'vehicles'

    def get_queryset(self):
        return Vehicle.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_customer:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class VehicleCreateView(LoginRequiredMixin, CreateView):
    """
    Add a new vehicle for the logged-in customer.
    """
    model = Vehicle
    form_class = VehicleForm
    template_name = 'customers/vehicle_form.html'
    success_url = reverse_lazy('customers:vehicle_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_customer:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update an existing vehicle for the logged-in customer.
    """
    model = Vehicle
    form_class = VehicleForm
    template_name = 'customers/vehicle_form.html'
    success_url = reverse_lazy('customers:vehicle_list')

    def get_queryset(self):
        return Vehicle.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_customer:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)