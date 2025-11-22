import secrets
from .settings import CHARSET, CODE_LENGTH


def generate_short_code(length: int = CODE_LENGTH):
    return "".join(secrets.choice(CHARSET) for _ in range(length))

