from django.contrib import admin
from django.utils import timezone
from .models import Mail, Inapp


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