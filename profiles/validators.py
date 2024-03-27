import os
from django.core.exceptions import ValidationError

def images_path(instance, filename):
    user_id = instance.profile.user.id
    return f"user_{user_id}_profiles/{filename}"