from pathlib import Path

from rest_framework.exceptions import ValidationError

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
ALLOWED_DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt'}
MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024


def validate_upload(file_obj):
    extension = Path(file_obj.name).suffix.lower()
    if extension in ALLOWED_IMAGE_EXTENSIONS:
        if file_obj.size > MAX_IMAGE_SIZE:
            raise ValidationError('Image file exceeds 5MB.')
        return 'image'

    if extension in ALLOWED_DOCUMENT_EXTENSIONS:
        if file_obj.size > MAX_DOCUMENT_SIZE:
            raise ValidationError('Document file exceeds 10MB.')
        return 'document'

    raise ValidationError('Unsupported file type.')
