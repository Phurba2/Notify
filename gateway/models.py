from django.db import models

class NotificationHistory(models.Model):
    # Define the choices
    TYPE_CHOICES = [
        ('MAIL', 'Email Notification'),
        ('PUSH', 'Push Notification (Desktop)'),
        ('INAPP', 'In-App Notification'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
    ]

    recipient_name = models.CharField(max_length=100)
    message = models.TextField()
    # Apply the choices here
    notify_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient_name} | {self.notify_type} | {self.status}"