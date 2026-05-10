from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.friendships.models import FriendRequest, FriendRequestStatus, Friendship
from apps.friendships.serializers import FriendListSerializer, FriendRequestSerializer, MutualFriendSerializer, SendRequestSerializer
from apps.friendships.services import accept_request, reject_request, remove_friend, send_request

User = get_user_model()


class FriendRequestViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user)).select_related('sender', 'receiver')

    @action(detail=False, methods=['post'])
    def send(self, request):
        serializer = SendRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        receiver = User.objects.get(id=serializer.validated_data['receiver_id'])
        if receiver == request.user:
            return Response({'detail': 'Cannot send request to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        existing = FriendRequest.objects.filter(sender=request.user, receiver=receiver, status=FriendRequestStatus.PENDING).first()
        if existing:
            return Response(FriendRequestSerializer(existing).data, status=status.HTTP_200_OK)

        request_obj = send_request(request.user, receiver)
        return Response(FriendRequestSerializer(request_obj).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        request_obj = self.get_queryset().filter(id=pk, receiver=request.user).first()
        if not request_obj:
            return Response({'detail': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)
        accept_request(request_obj)
        return Response(FriendRequestSerializer(request_obj).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        request_obj = self.get_queryset().filter(id=pk, receiver=request.user).first()
        if not request_obj:
            return Response({'detail': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)
        reject_request(request_obj)
        return Response(FriendRequestSerializer(request_obj).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='remove/(?P<friend_id>[^/.]+)')
    def remove(self, request, friend_id=None):
        remove_friend(request.user, friend_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def friends(self, request):
        friends = FriendListSerializer.get_friends(request.user)
        return Response(MutualFriendSerializer(friends, many=True).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='mutual/(?P<user_id>[^/.]+)')
    def mutual(self, request, user_id=None):
        target = User.objects.filter(id=user_id).first()
        if not target:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        current_friend_ids = set()
        target_friend_ids = set()

        for requester_id, receiver_id in Friendship.objects.filter(Q(requester=request.user) | Q(receiver=request.user)).values_list('requester_id', 'receiver_id'):
            current_friend_ids.update([requester_id, receiver_id])
        current_friend_ids.discard(request.user.id)

        for requester_id, receiver_id in Friendship.objects.filter(Q(requester=target) | Q(receiver=target)).values_list('requester_id', 'receiver_id'):
            target_friend_ids.update([requester_id, receiver_id])
        target_friend_ids.discard(target.id)

        mutual_ids = current_friend_ids.intersection(target_friend_ids)
        users = User.objects.filter(id__in=mutual_ids)
        return Response(MutualFriendSerializer(users, many=True).data, status=status.HTTP_200_OK)
