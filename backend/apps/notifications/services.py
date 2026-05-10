from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from redis.exceptions import RedisError

from apps.notifications.models import Notification


def create_notification(recipient, actor, notification_type, title, message, metadata=None):
    notification = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        notification_type=notification_type,
        title=title,
        message=message,
        metadata=metadata or {},
    )

    channel_layer = get_channel_layer()
    if channel_layer:
        try:
            async_to_sync(channel_layer.group_send)(
                f'notifications_{recipient.id}',
                {
                    'type': 'notification_event',
                    'notification': {
                        'id': notification.id,
                        'notification_type': notification.notification_type,
                        'title': notification.title,
                        'message': notification.message,
                        'metadata': notification.metadata,
                        'created_at': notification.created_at.isoformat(),
                    },
                },
            )
        except RedisError:
            pass
    return notification
