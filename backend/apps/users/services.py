from django.contrib.auth import get_user_model
from django.db.models import Count, Q

from apps.friendships.models import Friendship

User = get_user_model()


def user_suggestions_for(user, limit=10):
    friend_ids = Friendship.objects.filter(
        Q(requester=user) | Q(receiver=user)
    ).values_list('requester_id', 'receiver_id')
    excluded_ids = {user.id}
    for requester_id, receiver_id in friend_ids:
        excluded_ids.add(requester_id)
        excluded_ids.add(receiver_id)

    return (
        User.objects.exclude(id__in=excluded_ids)
        .annotate(mutual_connections=Count('requested_friendships'))
        .order_by('-mutual_connections', '-created_at')[:limit]
    )
