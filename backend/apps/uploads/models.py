from django.conf import settings
from django.db import models
from django.utils import timezone


class UploadedFile(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_files')
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=20)
    original_name = models.CharField(max_length=255)
    size = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
