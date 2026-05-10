from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.uploads.models import UploadedFile
from apps.uploads.serializers import UploadedFileSerializer
from apps.uploads.services import validate_upload


class FileUploadViewSet(viewsets.ModelViewSet):
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UploadedFile.objects.filter(owner=self.request.user)

    @action(detail=False, methods=['post'])
    def upload(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'detail': 'file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        file_type = validate_upload(file_obj)
        uploaded = UploadedFile.objects.create(
            owner=request.user,
            file=file_obj,
            file_type=file_type,
            original_name=file_obj.name,
            size=file_obj.size,
        )
        return Response(self.get_serializer(uploaded).data, status=status.HTTP_201_CREATED)
