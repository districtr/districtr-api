from flask import Blueprint, current_app, request

from ..auth import create_signin_token
from ..email import send_email
from ..result import ApiResult
from ..schemas import UserSchema
from .users import create_user

bp = Blueprint("register", __name__)


registration_schema = UserSchema(only=("first", "last", "email"))


def send_sign_in_email(email, token):
    base_url = current_app.config["FRONTEND_BASE_URL"]
    link = base_url + "/signin?token={}".format(token)
    template = current_app.jinja_env.get_template("verify_email.html")
    content = template.render(link=link)
    return send_email(
        "registration@districtr.org", email, "Confirm your Districtr account", content
    )


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
