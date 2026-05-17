from django.db import models


class BaseNotification(models.Model):
    user = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Mail(BaseNotification):
    class Meta:
        db_table = 'emauka"."mail'
        verbose_name = "Mail"
        verbose_name_plural = "Mail"


class Inapp(BaseNotification):
    class Meta:
        db_table = 'emauka"."inapp'
        verbose_name = "Inapp"
        verbose_name_plural = "Inapp"