from django.conf import settings
from django.db import models
from django.utils import timezone


class FriendRequestStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'


class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(max_length=20, choices=FriendRequestStatus.choices, default=FriendRequestStatus.PENDING)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    responded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sender', 'receiver'], name='unique_friend_request_pair'),
            models.CheckConstraint(condition=~models.Q(sender=models.F('receiver')), name='no_self_friend_request'),
        ]
        indexes = [models.Index(fields=['status', 'created_at'])]


class Friendship(models.Model):
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requested_friendships')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_friendships')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['requester', 'receiver'], name='unique_friendship_pair'),
            models.CheckConstraint(condition=~models.Q(requester=models.F('receiver')), name='no_self_friendship'),
        ]
        indexes = [models.Index(fields=['created_at'])]

    @staticmethod
    def canonical_pair(user_a_id, user_b_id):
        return (min(user_a_id, user_b_id), max(user_a_id, user_b_id))
