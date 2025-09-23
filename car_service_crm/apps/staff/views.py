# apps/staff/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Avg, Count
from django.db.models.functions import TruncMonth
from datetime import datetime
from apps.users.models import User
from apps.customers.models import Vehicle
from apps.bookings.models import Booking
from apps.services.models import Service
from apps.analytics.models import RevenueReport, StaffPerformance
from apps.communication.models import CommunicationLog, NotificationTemplate
from django.template import Template, Context
from  django.core.mail import send_mail
from django.forms import forms

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    """
    Admin dashboard showing key metrics and quick access to management tasks.
    """
    template_name = 'staff/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_admin:
            context['total_customers'] = User.objects.filter(role=User.ROLE_CUSTOMER).count()
            context['total_staff'] = User.objects.filter(role=User.ROLE_STAFF).count()
            context['total_vehicles'] = Vehicle.objects.count()
            context['pending_bookings'] = Booking.objects.filter(status=Booking.STATUS_PENDING).count()
            context['recent_bookings'] = Booking.objects.order_by('-created_at')[:5]
            context['total_services'] = Service.objects.count()  # Added
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class CustomerListView(LoginRequiredMixin, ListView):
    """
    List all customers for Admin management.
    """
    model = User
    template_name = 'staff/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return User.objects.filter(role=User.ROLE_CUSTOMER)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class StaffListView(LoginRequiredMixin, ListView):
    """
    List all staff for Admin management.
    """
    model = User
    template_name = 'staff/staff_list.html'
    context_object_name = 'staff'

    def get_queryset(self):
        return User.objects.filter(role=User.ROLE_STAFF)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class BookingManagementView(LoginRequiredMixin, ListView):
    """
    List all bookings for Admin oversight and management.
    """
    model = Booking
    template_name = 'staff/booking_management.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class BookingAssignStaffView(LoginRequiredMixin, UpdateView):
    """
    Assign staff to a booking.
    """
    model = Booking
    fields = ('assigned_staff',)
    template_name = 'staff/booking_assign.html'
    success_url = reverse_lazy('staff:booking_management')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['assigned_staff'].queryset = User.objects.filter(role=User.ROLE_STAFF)
        return form

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class StaffDashboardView(LoginRequiredMixin, TemplateView):
    """
    Staff dashboard showing assigned bookings and workload.
    """
    template_name = 'staff/staff_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff_member:
            context['assigned_bookings'] = Booking.objects.filter(
                assigned_staff=self.request.user,
                status__in=[Booking.STATUS_PENDING, Booking.STATUS_IN_PROGRESS]
            ).order_by('scheduled_date')[:5]
            context['completed_bookings'] = Booking.objects.filter(
                assigned_staff=self.request.user,
                status=Booking.STATUS_COMPLETED
            ).count()
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff_member:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class StaffBookingListView(LoginRequiredMixin, ListView):
    """
    List all bookings assigned to the logged-in staff member.
    """
    model = Booking
    template_name = 'staff/staff_booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(assigned_staff=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff_member:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class StaffBookingUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update booking status and notes for assigned bookings.
    """
    model = Booking
    fields = ('status', 'notes')
    template_name = 'staff/staff_booking_update.html'
    success_url = reverse_lazy('staff:staff_booking_list')

    def get_queryset(self):
        return Booking.objects.filter(assigned_staff=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Restrict status choices to relevant options
        form.fields['status'].choices = [
            (Booking.STATUS_PENDING, _('Pending')),
            (Booking.STATUS_IN_PROGRESS, _('In Progress')),
            (Booking.STATUS_COMPLETED, _('Completed')),
        ]
        return form

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff_member:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class ServiceListView(LoginRequiredMixin, ListView):
    """
    List all services for Admin management.
    """
    model = Service
    template_name = 'staff/service_list.html'
    context_object_name = 'services'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class ServiceCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new service.
    """
    model = Service
    fields = ('name', 'description', 'price', 'duration')
    template_name = 'staff/service_form.html'
    success_url = reverse_lazy('staff:service_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update an existing service.
    """
    model = Service
    fields = ('name', 'description', 'price', 'duration')
    template_name = 'staff/service_form.html'
    success_url = reverse_lazy('staff:service_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)
    
class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    """
    Analytics dashboard for Admins to view reports.
    """
    template_name = 'staff/analytics_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_admin:
            context['revenue_reports'] = RevenueReport.objects.all()[:12]  # Last 12 months
            context['staff_performances'] = StaffPerformance.objects.all()[:10]  # Last 10
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class GenerateReportsView(LoginRequiredMixin, FormView):
    """
    View for Admins to generate new reports.
    """
    template_name = 'staff/generate_reports.html'
    form_class = forms.Form  # Placeholder; use a custom form for month selection if needed
    success_url = reverse_lazy('staff:analytics_dashboard')

    def form_valid(self, form):
        # Generate revenue report for the current month
        current_month = datetime.now().replace(day=1)
        completed_bookings = Booking.objects.filter(status=Booking.STATUS_COMPLETED, created_at__month=current_month.month, created_at__year=current_month.year)
        total_revenue = completed_bookings.aggregate(Sum('service__price'))['service__price__sum'] or 0
        total_bookings = completed_bookings.count()
        average_rating = completed_bookings.aggregate(Avg('feedback__rating'))['feedback__rating__avg'] or 0

        RevenueReport.objects.update_or_create(
            month=current_month,
            defaults={
                'total_revenue': total_revenue,
                'total_bookings': total_bookings,
                'average_rating': average_rating,
            }
        )

        # Generate staff performance
        staff_members = User.objects.filter(role=User.ROLE_STAFF)
        for staff in staff_members:
            staff_bookings = completed_bookings.filter(assigned_staff=staff)
            staff_revenue = staff_bookings.aggregate(Sum('service__price'))['service__price__sum'] or 0
            staff_completed = staff_bookings.count()
            staff_rating = staff_bookings.aggregate(Avg('feedback__rating'))['feedback__rating__avg'] or 0

            StaffPerformance.objects.update_or_create(
                staff=staff,
                month=current_month,
                defaults={
                    'completed_bookings': staff_completed,
                    'total_revenue': staff_revenue,
                    'average_rating': staff_rating,
                }
            )

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)
    
class CommunicationDashboardView(LoginRequiredMixin, ListView):
    """
    Dashboard for Admins to view and manage communication templates and logs.
    """
    model = NotificationTemplate
    template_name = 'staff/communication_dashboard.html'
    context_object_name = 'templates'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = CommunicationLog.objects.all()[:10]  # Last 10 logs
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class NotificationTemplateCreateView(LoginRequiredMixin, CreateView):
    """
    View for Admins to create new notification templates.
    """
    model = NotificationTemplate
    fields = ['name', 'subject', 'message', 'is_active']
    template_name = 'staff/notification_template_form.html'
    success_url = reverse_lazy('staff:communication_dashboard')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class SendBroadcastView(LoginRequiredMixin, FormView):
    """
    View for Admins to send broadcast messages to all customers.
    """
    template_name = 'staff/send_broadcast.html'
    form_class = forms.Form  # Placeholder; can extend with template selection
    success_url = reverse_lazy('staff:communication_dashboard')

    def form_valid(self, form):
        customers = User.objects.filter(role=User.ROLE_CUSTOMER)
        template = NotificationTemplate.objects.filter(name='Broadcast Message', is_active=True).first()
        if not template:
            template = NotificationTemplate.objects.create(
                name='Broadcast Message',
                subject='Important Update from iCars',
                message='Dear {customer}, we have an important update: {message}',
                is_active=True
            )

        message = self.request.POST.get('message', 'No message provided.')
        for customer in customers:
            rendered_message = Template(template.message).render(Context({
                'customer': customer.get_full_name(),
                'message': message
            }))
            try:
                send_mail(
                    subject=template.subject,
                    message=rendered_message,
                    from_email='no-reply@icars.com',
                    recipient_list=[customer.email],
                    fail_silently=False
                )
                CommunicationLog.objects.create(
                    recipient=customer,
                    message_type='EMAIL',
                    subject=template.subject,
                    message=rendered_message,
                    template=template,
                    status='SENT'
                )
            except Exception as e:
                CommunicationLog.objects.create(
                    recipient=customer,
                    message_type='EMAIL',
                    subject=template.subject,
                    message=rendered_message,
                    template=template,
                    status='FAILED'
                )

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)