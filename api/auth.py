import functools

from flask import current_app, g, request
from itsdangerous import (JSONWebSignatureSerializer,
                          TimedJSONWebSignatureSerializer)

from .exceptions import Unauthenticated, Unauthorized
from .models import User
from .schemas import UserSchema

token_data_schema = UserSchema(only=("id", "first", "last", "email"))

timed_serializer = TimedJSONWebSignatureSerializer(
    current_app.config["SECRET_KEY"], expires_in=1800
)
serializer = JSONWebSignatureSerializer(current_app.config["SECRET_KEY"])


def exchange_signin_token_for_bearer_token(signin_token):
    serialized_user = timed_serializer.loads(signin_token)
    return serializer.dumps(serialized_user)


def create_signin_token(user):
    """Creates a timed JWT. The user agent (e.g. front-end API client) can exchange
    this token for a Bearer token that doesn't expire. The user agent must store the
    Bearer token somewhere (e.g. localStorage)."""
    return timed_serializer.dumps(token_data_schema.dump(user))


def create_bearer_token(user):
    return serializer.dumps(token_data_schema.dump(user))


def get_bearer_token(header):
    """Extracts the token from a header of the form "Bearer {token}" or
    "JWT {token}"
    """
    if not header:
        return None
    header_parts = header.split(" ")
    if len(header_parts) < 2:
        return None
    token = header.split(" ")[1]
    return token


def get_current_user_from_request(request):
    token = get_bearer_token(request.headers.get("Authorization"))
    if not token:
        return None

    token_data = serializer.loads(token)

    return User.query.get(token_data["id"])


def get_current_user():
    user = getattr(g, "user", None)
    if user is None:
        user = get_current_user_from_request(request)
        g.user = user
    return user


def authenticate(controller):
    @functools.wraps(controller)
    def wrapper(*args, **kwargs):
        if get_current_user() is None:
            raise Unauthenticated()
        return controller(*args, **kwargs)

    return wrapper


def admin_only(controller):
    @functools.wraps(controller)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if user is None or not user.is_admin():
            raise Unauthorized()
        return controller(*args, **kwargs)

    return wrapper
