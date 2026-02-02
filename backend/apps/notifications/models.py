import hashid_field
from django.conf import settings
from django.db import models
from django.utils import timezone

from . import managers


class Notification(models.Model):
    id: hashid_field.HashidAutoField = hashid_field.HashidAutoField(primary_key=True)
    user: models.ForeignKey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type: models.CharField = models.CharField(max_length=64)

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    read_at: models.DateTimeField = models.DateTimeField(null=True, blank=True)

    data: models.JSONField = models.JSONField(default=dict)

    issuer: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="notifications_issued"
    )

    objects = managers.NotificationManager()

    def __str__(self) -> str:
        return str(self.id)

    @property
    def is_read(self) -> bool:
        return self.read_at is not None

    @is_read.setter
    def is_read(self, val: bool):
        self.read_at = timezone.now() if val else None


class ScheduledNotification(models.Model):
    """Model for scheduled notifications to be sent at a future time."""

    id: hashid_field.HashidAutoField = hashid_field.HashidAutoField(primary_key=True)
    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="scheduled_notifications"
    )
    type: models.CharField = models.CharField(max_length=64)
    data: models.JSONField = models.JSONField(default=dict)

    scheduled_for: models.DateTimeField = models.DateTimeField()
    sent: models.BooleanField = models.BooleanField(default=False)
    sent_at: models.DateTimeField = models.DateTimeField(null=True, blank=True)

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["scheduled_for"]
        indexes = [
            models.Index(fields=["scheduled_for", "sent"]),
        ]

    def __str__(self) -> str:
        return f"Scheduled: {self.type} for {self.user} at {self.scheduled_for}"


class NotificationPreference(models.Model):
    """User notification preferences."""

    CHANNEL_CHOICES = [
        ("email", "Email"),
        ("push", "Push Notification"),
        ("in_app", "In-App"),
    ]

    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notification_preferences"
    )
    notification_type: models.CharField = models.CharField(max_length=64)
    channel: models.CharField = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    enabled: models.BooleanField = models.BooleanField(default=True)

    class Meta:
        unique_together = ["user", "notification_type", "channel"]

    def __str__(self) -> str:
        status = "enabled" if self.enabled else "disabled"
        return f"{self.user}: {self.notification_type} via {self.channel} ({status})"
