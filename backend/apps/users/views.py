from django.contrib.auth import get_user_model
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.permissions import IsSelfOrReadOnly
from apps.users.serializers import UserProfileSerializer, UserSearchSerializer
from apps.users.services import user_suggestions_for

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrReadOnly]
    search_fields = ['username', 'email', 'bio']
    ordering_fields = ['created_at', 'username']

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSearchSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def update_profile(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def upload_profile_image(self, request):
        if 'profile_picture' not in request.FILES:
            return Response({'detail': 'profile_picture file is required.'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.profile_picture = request.FILES['profile_picture']
        request.user.save(update_fields=['profile_picture'])
        return Response(UserProfileSerializer(request.user).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def suggestions(self, request):
        users = user_suggestions_for(request.user)
        serializer = UserSearchSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
