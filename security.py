import hashlib
import secrets

def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    derived = hashlib.scrypt(password.encode('utf-8'), salt=salt, n=2**14, r=8, p=1, dklen=64)
    return f'scrypt${salt.hex()}${derived.hex()}'
