from django.contrib import admin
from .models import Alert, Fishery, PollutionReport, SafePlace, SMSSubscriber, NotificationLog

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'created_at', 'is_active')
    list_filter = ('severity', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    actions = ['send_notifications_to_all']

    def send_notifications_to_all(self, request, queryset):
        for alert in queryset:
            if alert.is_active:
                # This will trigger notifications to all active subscribers
                from .utils import send_alert_notifications
                send_alert_notifications(alert)
        self.message_user(request, f"Notifications sent for {queryset.count()} alerts")
    send_notifications_to_all.short_description = "Send notifications for selected alerts"

@admin.register(Fishery)
class FisheryAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'current_occupancy')
    list_filter = ('location',)
    search_fields = ('name', 'location')

@admin.register(PollutionReport)
class PollutionReportAdmin(admin.ModelAdmin):
    list_display = ('location', 'severity', 'reported_at', 'status')
    list_filter = ('severity', 'status', 'reported_at')
    search_fields = ('location', 'description')

@admin.register(SafePlace)
class SafePlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'contact_info')
    list_filter = ('location',)
    search_fields = ('name', 'location')

@admin.register(SMSSubscriber)
class SMSSubscriberAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'is_active', 'subscribed_at', 'last_notification_sent')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('phone_number',)
    actions = ['activate_subscribers', 'deactivate_subscribers']

    def activate_subscribers(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} subscribers activated")
    activate_subscribers.short_description = "Activate selected subscribers"

    def deactivate_subscribers(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} subscribers deactivated")
    deactivate_subscribers.short_description = "Deactivate selected subscribers"

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'alert', 'sent_at', 'status')
    list_filter = ('status', 'sent_at')
    search_fields = ('subscriber__phone_number', 'alert__title')
    readonly_fields = ('sent_at',)