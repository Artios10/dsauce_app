from rest_framework import serializers

from apps.uploads.models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'owner', 'file', 'file_type', 'original_name', 'size', 'created_at']
        read_only_fields = ['id', 'owner', 'file_type', 'original_name', 'size', 'created_at']
