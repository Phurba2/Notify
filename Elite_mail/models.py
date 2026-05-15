from django.db import models
from django.utils import timezone
from datetime import timedelta

class EmailHistory(models.Model):
    user = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    message = models.TextField()
    notify_type = models.CharField(max_length=50, default="MAIL")
    status = models.CharField(max_length=50, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Email history"
        verbose_name_plural = "Email histories"
        db_table = "Elite_mail_emailhistory"

    def __str__(self):
        return self.user

class BookingHistory(EmailHistory):
    class Meta:
        proxy = True
        verbose_name = "Booking history"
        verbose_name_plural = "Booking histories"