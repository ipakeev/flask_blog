from werkzeug.security import generate_password_hash


def encrypt_password(password: str) -> str:
    return generate_password_hash(password, salt_length=32)
