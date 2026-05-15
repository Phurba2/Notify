from django.db import models
from django.utils import timezone
from datetime import timedelta


class BaseNotification(models.Model):
    user = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    status = models.CharField(max_length=50, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Mail(BaseNotification):
    class Meta:
        db_table = 'elite_freelancer"."mail'
        verbose_name = "Mail"
        verbose_name_plural = "Mail"


class Inapp(BaseNotification):
    class Meta:
        db_table = 'elite_freelancer"."inapp'
        verbose_name = "Inapp"
        verbose_name_plural = "Inapp"


class Booking(BaseNotification):
    class Meta:
        db_table = 'elite_freelancer"."booking'
        verbose_name = "Booking"
        verbose_name_plural = "Booking"

class PushToken(models.Model):
    user = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    token = models.TextField(unique=True)
    platform = models.CharField(max_length=50, default="android")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'elite_freelancer"."push_token'
        verbose_name = "Push token"
        verbose_name_plural = "Push tokens"

    def __str__(self):
        return self.email or self.user or str(self.id)