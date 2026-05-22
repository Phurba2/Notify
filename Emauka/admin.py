from django.contrib import admin
from .models import Mail, Inapp


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "email", "short_message", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user", "email", "message", "status")
    ordering = ("-created_at",)
    list_per_page = 25

    def short_message(self, obj):
        return obj.message[:60]


admin.site.register(Mail, NotificationAdmin)
admin.site.register(Inapp, NotificationAdmin)