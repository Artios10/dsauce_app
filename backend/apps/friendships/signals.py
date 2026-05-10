from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.friendships.models import FriendRequest, FriendRequestStatus
from apps.notifications.services import create_notification


@receiver(post_save, sender=FriendRequest)
def notify_friend_request(sender, instance, created, **kwargs):
    if created:
        create_notification(
            recipient=instance.receiver,
            actor=instance.sender,
            notification_type='friend_request',
            title='New friend request',
            message=f'{instance.sender.username} sent you a friend request.',
        )
    elif instance.status == FriendRequestStatus.ACCEPTED:
        create_notification(
            recipient=instance.sender,
            actor=instance.receiver,
            notification_type='friend_accept',
            title='Friend request accepted',
            message=f'{instance.receiver.username} accepted your friend request.',
        )
