from django.db import models
from django.utils import timezone
from datetime import timedelta

class NotificationHistory(models.Model):
    recipient_name = models.CharField(max_length=255)
    message = models.TextField()
    notify_type = models.CharField(max_length=50, default="MAIL")
    status = models.CharField(max_length=50, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recipient_name


class ProfessionalOTP(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    expertise = models.CharField(max_length=255, blank=True, null=True)
    otp_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.name} - {self.email}"