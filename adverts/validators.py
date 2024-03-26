import os
from django.core.exceptions import ValidationError


def validate_icon(value):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != '.svg':
        raise ValidationError('Only SVG files are allowed.')


def images_path(instance, filename):
    user_id = instance.profile.user.id
    return f"user_{user_id}_images/{filename}"