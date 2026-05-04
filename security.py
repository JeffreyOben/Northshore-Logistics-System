import hashlib
import base64

# Password hashing (SHA-256)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Simple encryption (for sensitive data like addresses)
SECRET_KEY = "northshore_secret_key"


def xor_cipher(data):
    key = SECRET_KEY
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))


def encrypt(data):
    encrypted = xor_cipher(data)
    return base64.b64encode(encrypted.encode()).decode()


def decrypt(data):
    decoded = base64.b64decode(data).decode()
    return xor_cipher(decoded)