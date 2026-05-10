from django.contrib import admin

from apps.uploads.models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'file_type', 'original_name', 'size', 'created_at')
    search_fields = ('owner__username', 'original_name')
