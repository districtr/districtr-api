from flask import Blueprint, request

from ..auth import create_signin_token
from ..result import ApiResult
from ..schemas import UserSchema
from .users import create_user

bp = Blueprint("register", __name__)


registration_schema = UserSchema(only=("first", "last", "email"))


def send_sign_in_email(email, token):
    return


@bp.route("/", methods=["POST"])
def register():
    """Register a new user."""
    user_data = registration_schema.load(request.get_json())

    user = create_user(user_data)

    send_sign_in_email(user.email, token=create_signin_token(user))

    return ApiResult(
        {"message": "Sign-in link has been sent to the provided email address."},
        status=201,
    )
