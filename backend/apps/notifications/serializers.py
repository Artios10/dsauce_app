from rest_framework import serializers

from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'recipient',
            'actor',
            'actor_username',
            'notification_type',
            'title',
            'message',
            'metadata',
            'is_read',
            'created_at',
        ]
        read_only_fields = ['id', 'recipient', 'actor', 'created_at']
