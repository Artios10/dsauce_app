from django.db import transaction
from django.db.models import Case, F, IntegerField, Q, When
from django.utils import timezone

from apps.friendships.models import FriendRequest, FriendRequestStatus, Friendship


def _canonical_users(sender, receiver):
    first_id, second_id = Friendship.canonical_pair(sender.id, receiver.id)
    return first_id, second_id


def send_request(sender, receiver):
    return FriendRequest.objects.create(sender=sender, receiver=receiver)


@transaction.atomic
def accept_request(request_obj: FriendRequest):
    request_obj.status = FriendRequestStatus.ACCEPTED
    request_obj.responded_at = timezone.now()
    request_obj.save(update_fields=['status', 'responded_at'])

    first_id, second_id = _canonical_users(request_obj.sender, request_obj.receiver)
    Friendship.objects.get_or_create(requester_id=first_id, receiver_id=second_id)
    return request_obj


@transaction.atomic
def reject_request(request_obj: FriendRequest):
    request_obj.status = FriendRequestStatus.REJECTED
    request_obj.responded_at = timezone.now()
    request_obj.save(update_fields=['status', 'responded_at'])
    return request_obj


def remove_friend(user, friend_id):
    first_id, second_id = Friendship.canonical_pair(user.id, friend_id)
    Friendship.objects.filter(requester_id=first_id, receiver_id=second_id).delete()


def friend_ids(user):
    return Friendship.objects.filter(Q(requester=user) | Q(receiver=user)).values_list('requester_id', 'receiver_id')


def get_friend_id_set(user):
    return set(
        Friendship.objects.filter(Q(requester=user) | Q(receiver=user))
        .annotate(
            friend_id=Case(
                When(requester=user, then=F('receiver_id')),
                default=F('requester_id'),
                output_field=IntegerField(),
            )
        )
        .values_list('friend_id', flat=True)
    )
