import os
from django.core.exceptions import ValidationError

def images_path(instance, filename):
    user_id = instanceç.user.id
    return f"user_{user_id}_profiles/{filename}"