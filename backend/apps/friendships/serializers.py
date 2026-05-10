from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from apps.friendships.models import FriendRequest, Friendship

User = get_user_model()


class FriendRequestSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = FriendRequest
        fields = [
            'id',
            'sender',
            'receiver',
            'sender_username',
            'receiver_username',
            'status',
            'created_at',
            'responded_at',
        ]
        read_only_fields = ['id', 'sender', 'status', 'created_at', 'responded_at']


class FriendshipSerializer(serializers.ModelSerializer):
    requester_username = serializers.CharField(source='requester.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'requester', 'receiver', 'requester_username', 'receiver_username', 'created_at']


class MutualFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_picture']


class SendRequestSerializer(serializers.Serializer):
    receiver_id = serializers.IntegerField()

    def validate_receiver_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError('Receiver does not exist.')
        return value


class FriendListSerializer(serializers.Serializer):
    @staticmethod
    def get_friends(user):
        friendships = Friendship.objects.filter(Q(requester=user) | Q(receiver=user)).select_related('requester', 'receiver')
        friends = []
        for friendship in friendships:
            friend = friendship.receiver if friendship.requester_id == user.id else friendship.requester
            friends.append(friend)
        return friends
