import random
import requests
from rest_framework import status
from rest_framework.response import Response
from django.core.cache import cache

def generate_code(phone_number):
     # Check if a code already exists for the given phone number
    existing_code = cache.get(f'imdb:{phone_number}')
    if existing_code is not None:
        return existing_code  # Return the existing code if one is found
    
    # Generate a 4-digit random code
    code = random.randint(1000, 9999)
    
    # Set the key-value pair in the Django cache with a timeout of 1 minute
    cache.set(f'imdb:{phone_number}', code, 60)
    print(code)
    return code


def validate_code(phone_number, entered_code):
    # Retrieve the stored code from the cache
    stored_code = cache.get(f'imdb:{phone_number}')

    # Check if the stored code exists and matches the entered code
    if stored_code is not None and str(stored_code) == str(entered_code):
        # Code is valid, remove it from the cache (optional) and return True
        cache.delete(f'imdb:{phone_number}')
        return True

    # Code is invalid
    return False


def make_call(phone_number, verification_code):
    
    flashcall_data = {
        'msisdn': str(phone_number),
        'verification_code': verification_code,
    }

    flashcall_url = 'https://authenticalls.com/api/flashcall/'

    token = '8ad1141e0b9cef6dc54ae730faf289199a67e7f55c32d9b001a75713154662ea'
    headers = {
        'Authorization': f'Bearer {token}',
    }

    response = requests.post(
        flashcall_url,
        json = flashcall_data,
        headers = headers
    )

    if response.status_code == 200:
        return True
    return False