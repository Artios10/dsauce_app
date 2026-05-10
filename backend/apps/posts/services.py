from apps.friendships.models import Friendship
from apps.posts.models import Post, PostLike


def toggle_post_like(post: Post, user):
    existing = PostLike.objects.filter(post=post, user=user).first()
    if existing:
        existing.delete()
        return False
    PostLike.objects.create(post=post, user=user)
    return True


def feed_queryset(user):
    friendship_ids = Friendship.objects.filter(requester=user).values_list('receiver_id', flat=True)
    reverse_friendship_ids = Friendship.objects.filter(receiver=user).values_list('requester_id', flat=True)
    return Post.objects.filter(user_id__in=[user.id, *friendship_ids, *reverse_friendship_ids]).select_related('user').prefetch_related('likes', 'comments')
