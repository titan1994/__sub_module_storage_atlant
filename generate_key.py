"""
Помошник по генерации секретного ключа
"""

from cryptography.fernet import Fernet

def create_access_token():
    left = Fernet.generate_key().decode()
    right = Fernet.generate_key().decode()
    return left+right

print(create_access_token())