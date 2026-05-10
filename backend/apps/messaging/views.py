from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.messaging.models import Conversation, Message
from apps.messaging.permissions import IsConversationParticipant
from apps.messaging.serializers import ConversationCreateSerializer, ConversationSerializer, MessageSerializer
from apps.messaging.services import get_or_create_conversation, mark_messages_read


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).prefetch_related('conversation_participants__user', 'participants')

    def create(self, request, *args, **kwargs):
        serializer = ConversationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation, created = get_or_create_conversation(request.user, serializer.validated_data['participant_ids'])
        output = self.get_serializer(conversation)
        return Response(output.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsConversationParticipant]
    queryset = Message.objects.select_related('conversation', 'sender').all()
    filterset_fields = ['conversation', 'sender', 'is_read']
    search_fields = ['content']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return self.queryset.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if not conversation.participants.filter(id=self.request.user.id).exists():
            raise permissions.PermissionDenied('You are not a participant of this conversation.')
        serializer.save(sender=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_read(self, request):
        conversation_id = request.data.get('conversation_id')
        conversation = Conversation.objects.filter(id=conversation_id, participants=request.user).first()
        if not conversation:
            return Response({'detail': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)
        count = mark_messages_read(conversation, request.user)
        return Response({'updated': count}, status=status.HTTP_200_OK)
