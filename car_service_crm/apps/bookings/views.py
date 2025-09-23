# apps/bookings/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.template import Template, Context
from .models import Booking, Feedback
from .forms import BookingForm, FeedbackForm
from apps.communication.models import NotificationTemplate, CommunicationLog

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_customer:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('bookings:booking_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.customer = self.request.user
        response = super().form_valid(form)
        # Send confirmation email
        template = NotificationTemplate.objects.filter(name='Booking Confirmation', is_active=True).first()
        if not template:
            template = NotificationTemplate.objects.create(
                name='Booking Confirmation',
                subject='Your iCars Booking Confirmation',
                message='Dear {customer}, your booking for {service} on {date} has been confirmed.',
                is_active=True
            )
        rendered_message = Template(template.message).render(Context({
            'customer': self.request.user.get_full_name(),
            'service': form.instance.service.name,
            'date': form.instance.scheduled_date.strftime('%Y-%m-%d %H:%M')
        }))
        try:
            send_mail(
                subject=template.subject,
                message=rendered_message,
                from_email='no-reply@icars.com',
                recipient_list=[self.request.user.email],
                fail_silently=False
            )
            CommunicationLog.objects.create(
                recipient=self.request.user,
                booking=form.instance,
                message_type='EMAIL',
                subject=template.subject,
                message=rendered_message,
                template=template,
                status='SENT'
            )
        except Exception as e:
            CommunicationLog.objects.create(
                recipient=self.request.user,
                booking=form.instance,
                message_type='EMAIL',
                subject=template.subject,
                message=rendered_message,
                template=template,
                status='FAILED'
            )
        return response

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_customer:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('bookings:booking_list')

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_customer:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_customer:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)
    

class FeedbackCreateView(LoginRequiredMixin, CreateView):
    """
    View for customers to submit feedback for a completed booking.
    """
    model = Feedback
    form_class = FeedbackForm
    template_name = 'bookings/feedback_form.html'

    def dispatch(self, request, *args, **kwargs):

        self.booking = get_object_or_404(Booking, pk=self.kwargs['pk'], customer=request.user)
        # Check if booking is completed and feedback not already submitted
        if self.booking.status != Booking.STATUS_COMPLETED or self.booking.feedback_submitted:
            return redirect('bookings:booking_detail', pk=self.booking.pk)
        if not request.user.is_customer:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.booking = self.booking
        response = super().form_valid(form)
        self.booking.feedback_submitted = True
        self.booking.save()
        return response

    def get_success_url(self):
        # Ensure pk is passed correctly
        return reverse_lazy('bookings:booking_detail', kwargs={'pk': self.booking.pk})

    def get_context_data(self, **kwargs):
        # Add booking to context for template
        context = super().get_context_data(**kwargs)
        context['booking'] = self.booking
        return context
    """
    View for customers to submit feedback for a completed booking.
    """
    model = Feedback
    form_class = FeedbackForm
    template_name = 'bookings/feedback_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.booking = get_object_or_404(Booking, pk=self.kwargs['pk'], customer=request.user)
        if self.booking.status != Booking.STATUS_COMPLETED or self.booking.feedback_submitted:
            return redirect('bookings:booking_detail', pk=self.booking.pk)
        if not request.user.is_customer:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.booking = self.booking
        response = super().form_valid(form)
        self.booking.feedback_submitted = True
        self.booking.save()
        return response

    def get_success_url(self):
        return reverse_lazy('bookings:booking_detail', kwargs={'pk': self.booking.pk}) 