from django.contrib import admin
from .models import NotificationHistory


@admin.register(NotificationHistory)
class NotificationHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "recipient_name", "notify_type", "status", "created_at")
    list_filter = ("notify_type", "status", "created_at")
    search_fields = ("recipient_name", "message")