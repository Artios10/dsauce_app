from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Count
from django.utils import timezone

from apps.messaging.models import Conversation, ConversationParticipant, Message

User = get_user_model()


@transaction.atomic
def get_or_create_conversation(creator, participant_ids):
    participant_ids = sorted(set([creator.id, *participant_ids]))
    candidates = (
        Conversation.objects.annotate(total_participants=Count('participants'))
        .filter(total_participants=len(participant_ids), participants__id=participant_ids[0])
        .prefetch_related('participants')
    )

    for conversation in candidates:
        existing_ids = sorted(conversation.participants.values_list('id', flat=True))
        if existing_ids == participant_ids:
            return conversation, False

    conversation = Conversation.objects.create()
    users = User.objects.filter(id__in=participant_ids)
    ConversationParticipant.objects.bulk_create([
        ConversationParticipant(conversation=conversation, user=user) for user in users
    ])
    return conversation, True


def mark_messages_read(conversation, user):
    return Message.objects.filter(conversation=conversation, is_read=False).exclude(sender=user).update(is_read=True, read_at=timezone.now())
