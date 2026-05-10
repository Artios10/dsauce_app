from django.contrib.auth import get_user_model
from django.db.models import Count, F, Q

from apps.friendships.services import get_friend_id_set

User = get_user_model()


def user_suggestions_for(user, limit=10):
    current_friend_ids = get_friend_id_set(user)
    excluded_ids = {user.id, *current_friend_ids}
    return (
        User.objects.exclude(id__in=excluded_ids)
        .annotate(
            mutual_from_requested=Count(
                'requested_friendships',
                filter=Q(requested_friendships__receiver_id__in=current_friend_ids),
                distinct=True,
            ),
            mutual_from_received=Count(
                'received_friendships',
                filter=Q(received_friendships__requester_id__in=current_friend_ids),
                distinct=True,
            ),
        )
        .annotate(mutual_connections=F('mutual_from_requested') + F('mutual_from_received'))
        .order_by('-mutual_connections', '-created_at')[:limit]
    )
