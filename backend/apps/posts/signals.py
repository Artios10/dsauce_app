from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notifications.services import create_notification
from apps.posts.models import Comment, PostLike


@receiver(post_save, sender=PostLike)
def notify_post_like(sender, instance, created, **kwargs):
    if created and instance.post.user_id != instance.user_id:
        create_notification(
            recipient=instance.post.user,
            actor=instance.user,
            notification_type='post_like',
            title='Your post was liked',
            message=f'{instance.user.username} liked your post.',
            metadata={'post_id': instance.post_id},
        )


@receiver(post_save, sender=Comment)
def notify_post_comment(sender, instance, created, **kwargs):
    if created and instance.post.user_id != instance.user_id:
        create_notification(
            recipient=instance.post.user,
            actor=instance.user,
            notification_type='post_comment',
            title='New comment on your post',
            message=f'{instance.user.username} commented on your post.',
            metadata={'post_id': instance.post_id, 'comment_id': instance.id},
        )
