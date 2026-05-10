from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.messaging.models import Conversation, ConversationParticipant, Message

User = get_user_model()


class ConversationParticipantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ConversationParticipant
        fields = ['id', 'user', 'username', 'joined_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants_data = ConversationParticipantSerializer(source='conversation_participants', many=True, read_only=True)
    unread_messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants_data', 'created_at', 'updated_at', 'unread_messages']

    def get_unread_messages(self, obj):
        user = self.context['request'].user
        return obj.messages.exclude(sender=user).filter(is_read=False).count()


class ConversationCreateSerializer(serializers.Serializer):
    participant_ids = serializers.ListField(child=serializers.IntegerField(), min_length=1)


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_username', 'content', 'attachment', 'is_read', 'created_at', 'read_at']
        read_only_fields = ['id', 'sender', 'is_read', 'created_at', 'read_at']
