from django.conf import settings
from django.db import models
from django.utils import timezone


class NotificationType(models.TextChoices):
    FRIEND_REQUEST = 'friend_request', 'Friend Request'
    FRIEND_ACCEPT = 'friend_accept', 'Friend Accepted'
    MESSAGE = 'message', 'Message'
    POST_LIKE = 'post_like', 'Post Like'
    POST_COMMENT = 'post_comment', 'Post Comment'
    COURSE_UPDATE = 'course_update', 'Course Update'


class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='actor_notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=40, choices=NotificationType.choices)
    title = models.CharField(max_length=255)
    message = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['recipient', 'is_read', '-created_at'])]
