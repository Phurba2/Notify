from django.contrib import admin
from django.utils import timezone
from .models import Mail, Inapp, Booking, PushToken


class BaseNotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "email", "short_message", "status", "formatted_created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user", "email", "message", "status")
    ordering = ("-created_at",)
    list_per_page = 25

    def short_message(self, obj):
        return obj.message[:60] + "..." if len(obj.message) > 60 else obj.message

    short_message.short_description = "Message"

    def formatted_created_at(self, obj):
        local_time = timezone.localtime(obj.created_at)
        return local_time.strftime("%Y %-d %B %-I:%M %p").lower()

    formatted_created_at.short_description = "Created At"


@admin.register(Mail)
class MailAdmin(BaseNotificationAdmin):
    pass


@admin.register(Inapp)
class InappAdmin(BaseNotificationAdmin):
    pass


@admin.register(Booking)
class BookingAdmin(BaseNotificationAdmin):
    pass


@admin.register(PushToken)
class PushTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "email", "platform", "short_token", "formatted_created_at")
    list_filter = ("platform", "created_at")
    search_fields = ("user", "email", "token", "platform")
    ordering = ("-created_at",)
    list_per_page = 25

    def short_token(self, obj):
        if not obj.token:
            return ""
        return obj.token[:35] + "..." if len(obj.token) > 35 else obj.token

    short_token.short_description = "Token"

    def formatted_created_at(self, obj):
        local_time = timezone.localtime(obj.created_at)
        return local_time.strftime("%Y %-d %B %-I:%M %p").lower()

    formatted_created_at.short_description = "Created At"