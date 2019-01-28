from flask import Blueprint, current_app, request

from ..auth import create_signin_token
from ..email import send_email
from ..exceptions import ApiException
from ..models import User
from ..result import ApiResult
from ..schemas import UserSchema
from .users import create_user

bp = Blueprint("register", __name__)


registration_schema = UserSchema(only=("first", "last", "email"))
signin_schema = UserSchema(only=["email"])


def send_signin_email(email, token):
    base_url = current_app.config["FRONTEND_BASE_URL"]
    link = base_url + "/signin?token={}".format(token)
    template = current_app.jinja_env.get_template("signin_email.html")
    content = template.render(link=link)
    return send_email("signin@districtr.org", email, "Sign in to Districtr", content)


def send_registration_email(email, token):
    base_url = current_app.config["FRONTEND_BASE_URL"]
    link = base_url + "/signin?token={}".format(token)
    template = current_app.jinja_env.get_template("verify_email.html")
    content = template.render(link=link)
    return send_email(
        "signup@districtr.org", email, "Confirm your Districtr account", content
    )


@bp.route("/register/", methods=["POST"])
def register():
    """Register a new user."""
    user_data = registration_schema.load(request.get_json())

    user = User.query.filter_by(email=user_data["email"]).first()

    if user:
        send_signin_email(user.email, token=create_signin_token(user))
        return ApiResult(
            {
                "message": "This user already exists. A sign-in link has been sent"
                "to the provided email address."
            },
            status=201,
        )

    user = create_user(user_data)
    send_registration_email(user.email, token=create_signin_token(user))

    return ApiResult(
        {"message": "Confirmation link has been sent to the provided email address."},
        status=201,
    )


@bp.route("/signin/", methods=["POST"])
def signin():
    """Sign in via a magic link."""
    user_data = signin_schema.load(request.get_json())

    user = User.query.filter_by(email=user_data["email"]).first()
    if not user:
        raise ApiException("Specified user does not exist.", status=404)

    send_signin_email(user.email, token=create_signin_token(user))

    return ApiResult(
        {"message": "Sign-in link has been sent to the provided email address."},
        status=201,
    )
