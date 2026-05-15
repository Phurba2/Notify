from django.contrib import admin
from .models import EmailHistory, BookingHistory


@admin.register(EmailHistory)
class EmailHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "email", "short_message", "notify_type", "status", "created_at")
    list_filter = ("notify_type", "status", "created_at")
    search_fields = ("user", "email", "message", "notify_type", "status")
    ordering = ("-created_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(notify_type="BOOKING")

    def short_message(self, obj):
        return obj.message[:60] + "..." if len(obj.message) > 60 else obj.message

    short_message.short_description = "Message"


@admin.register(BookingHistory)
class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "email", "short_message", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user", "email", "message", "status")
    ordering = ("-created_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(notify_type="BOOKING")

    def short_message(self, obj):
        return obj.message[:60] + "..." if len(obj.message) > 60 else obj.message

    short_message.short_description = "Message"