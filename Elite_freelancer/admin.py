from django.contrib import admin

from .models import BookingHistory, EliteInAppHistory, EliteMailHistory

class BaseHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "email", "short_message", "notify_type", "status", "created_at")
    list_filter = ("notify_type", "status", "created_at")
    search_fields = ("user", "email", "message", "notify_type", "status")
    ordering = ("-created_at",)
    list_per_page = 25

    def short_message(self, obj):
        return obj.message[:60] + "..." if len(obj.message) > 60 else obj.message

    short_message.short_description = "Message"


@admin.register(BookingHistory)
class BookingHistoryAdmin(BaseHistoryAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(project="ELITE", notify_type="BOOKING")


@admin.register(EliteInAppHistory)
class EliteInAppHistoryAdmin(BaseHistoryAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(project="ELITE", channel="INAPP")


@admin.register(EliteMailHistory)
class EliteMailHistoryAdmin(BaseHistoryAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(project="ELITE", channel="EMAIL").exclude(notify_type="BOOKING")