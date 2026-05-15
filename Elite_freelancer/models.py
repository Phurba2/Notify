from django.db import models
from django.utils import timezone
from datetime import timedelta

class EmailHistory(models.Model):
    user = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    message = models.TextField()
    notify_type = models.CharField(max_length=50, default="MAIL")
    status = models.CharField(max_length=50, default="PENDING")

    project = models.CharField(max_length=50, default="ELITE")
    channel = models.CharField(max_length=50, default="EMAIL")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Email history"
        verbose_name_plural = "Email history"
        db_table = "Elite_mail_emailhistory"
        
    def __str__(self):
        return self.user

class BookingHistory(EmailHistory):
    class Meta:
        proxy = True
        verbose_name = "Booking"
        verbose_name_plural = "Booking"

class EliteInAppHistory(EmailHistory):
    class Meta:
        proxy = True
        verbose_name = "Inapp"
        verbose_name_plural = "Inapp"


class EliteMailHistory(EmailHistory):
    class Meta:
        proxy = True
        verbose_name = "Mail"
        verbose_name_plural = "Mail"
