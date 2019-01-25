from flask import Blueprint, request

from ..auth import (
    create_bearer_token,
    exchange_signin_token_for_bearer_token,
    get_current_user,
)
from ..result import ApiResult

bp = Blueprint("tokens", __name__)


@bp.route("/", methods=["POST"])
def new_token():
    """Create a new bearer token by providing one of:
    1. a sign-in token in the body of the request
    2. a valid bearer token in the Authorization header.
    """
    user = get_current_user()
    if user:
        bearer_token = create_bearer_token(user)
    else:
        token = request.get_json().get("token", None)
        bearer_token = exchange_signin_token_for_bearer_token(token)
    return ApiResult({"token": bearer_token.decode("utf-8")}, status=201)
