import functools

from flask import current_app, g, request
from itsdangerous import JSONWebSignatureSerializer

from .exceptions import ApiException
from .models import User
from .schemas import UserSchema

token_data_schema = UserSchema(only=("id", "first", "last", "email"))


def create_bearer_token(user):
    serializer = JSONWebSignatureSerializer(current_app.config["SECRET_KEY"])
    print(token_data_schema.dump(user))
    return serializer.dumps(token_data_schema.dump(user))


def get_bearer_token(header):
    # The header will be of the form "Bearer {token}" or "JWT {token}"
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

    serializer = JSONWebSignatureSerializer(current_app.config["SECRET_KEY"])
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
            raise ApiException("This action requires authentication.", 403)
        return controller(*args, **kwargs)

    return wrapper


def admin_only(controller):
    @functools.wraps(controller)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if user is None or not user.is_admin():
            raise ApiException("This action requires a more privileged role.", 403)
        return controller(*args, **kwargs)

    return wrapper
