from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.posts.models import Comment, Post
from apps.posts.serializers import CommentSerializer, PostSerializer
from apps.posts.services import feed_queryset, toggle_post_like


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.select_related('user').prefetch_related('likes', 'comments').all()
    filterset_fields = ['user']
    search_fields = ['content', 'user__username']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        liked = toggle_post_like(post, request.user)
        return Response({'liked': liked}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def feed(self, request):
        queryset = feed_queryset(request.user)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.select_related('user', 'post').all()
    filterset_fields = ['post', 'user']
    search_fields = ['content']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
