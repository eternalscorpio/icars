# apps/communication/admin.py
from django.contrib import admin
from .models import NotificationTemplate, CommunicationLog

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'subject', 'message')
    ordering = ('name',)

@admin.register(CommunicationLog)
class CommunicationLogAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'booking', 'message_type', 'status', 'sent_at')
    list_filter = ('message_type', 'status', 'sent_at')
    search_fields = ('recipient__email', 'subject', 'message')
    ordering = ('-sent_at',)