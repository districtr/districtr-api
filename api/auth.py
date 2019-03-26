import functools

from flask import current_app, request
from itsdangerous import JSONWebSignatureSerializer, URLSafeTimedSerializer

from .exceptions import Unauthenticated, Unauthorized
from .models import User
from .schemas import UserSchema
from .utils import gcache

token_data_schema = UserSchema(only=("id", "first", "last", "email", "roles"))


def exchange_signin_token_for_bearer_token(signin_token):
    timed_serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

    user_id = timed_serializer.loads(signin_token, max_age=1800)
    user = User.query.get(user_id)
    return create_bearer_token(user)


def create_signin_token(user):
    """Creates a timed JWT. The user agent (e.g. front-end API client) can exchange
    this token for a Bearer token that doesn't expire. The user agent must store the
    Bearer token somewhere (e.g. localStorage)."""
    timed_serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

    return timed_serializer.dumps(user.id)


def create_bearer_token(user):
    serializer = JSONWebSignatureSerializer(current_app.config["SECRET_KEY"])

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


@gcache
def load_token_data(request):
    token = get_bearer_token(request.headers.get("Authorization"))
    if not token:
        return None

    serializer = JSONWebSignatureSerializer(current_app.config["SECRET_KEY"])
    token_data = serializer.loads(token)

    return token_data


@gcache
def get_current_user():
    user_data = load_token_data(request)
    user = None
    if user_data:
        user = User.query.get(user_data["id"])
    return user


@gcache
def get_current_user_roles():
    user_data = load_token_data(request)

    if user_data is None:
        return []
    else:
        return user_data["roles"]


def authenticate(controller):
    @functools.wraps(controller)
    def wrapper(*args, **kwargs):
        roles = get_current_user_roles()
        if not roles:
            raise Unauthenticated()
        return controller(*args, **kwargs)

    return wrapper


def requires(roles):
    def decorator(controller):
        @functools.wraps(controller)
        def wrapper(*args, **kwargs):
            user_roles = get_current_user_roles()
            if not user_roles:
                raise Unauthenticated()
            if any(role not in user_roles for role in roles):
                raise Unauthorized()
            return controller(*args, **kwargs)

        return wrapper

    return decorator

admin_only = requires(["admin"])
