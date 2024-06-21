import datetime
import secrets
import string

import jwt
from django.conf import settings


def generate_token(length=5) -> string:
    numbers = string.digits
    token = ""
    while len(token) < length:
        token += "".join(secrets.choice(numbers))
    return token


def get_random(length):
    return "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )


def get_access_token(payload):
    return jwt.encode(
        {"exp": datetime.datetime.now() + datetime.timedelta(days=7), **payload},
        settings.SECRET_KEY,
        algorithm="HS256",
    )


def get_refresh_token():
    return jwt.encode(
        {
            "exp": datetime.datetime.now() + datetime.timedelta(days=21),
            "ref_key": get_random(20),
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )


def verify_token(token):
    # decode the token
    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return None

    # check if token as exipired
    exp = decoded_data["exp"]

    if datetime.datetime.now().timestamp() > exp:
        return None

    return decoded_data


def generate_random_string(length: int = 8):
    chars = string.ascii_letters + string.digits
    random_string = "".join(secrets.choice(chars) for _ in range(length))
    return random_string
