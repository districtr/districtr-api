from flask import Blueprint, request

from ..auth import admin_only
from ..models import PlaceRequest, User, db
from ..result import ApiResult
from ..schemas import PlaceRequestSchema

bp = Blueprint("requests", __name__)

request_schema = PlaceRequestSchema()
requests_schema = PlaceRequestSchema(many=True)


@bp.route("/", methods=["GET"])
@admin_only
def list_requests():
    place_requests = PlaceRequest.query.all()
    return ApiResult(requests_schema.dump(place_requests), 200)


@bp.route("/", methods=["POST"])
def new_request():
    data = request.get_json()
    place_request_data = request_schema.load(data)
    # Don't create a new user if they already exist
    user = User.by_email(place_request_data["user"]["email"])
    if not user:
        user = User(**place_request_data["user"])
    place_request_data["user"] = user
    place_request = PlaceRequest(**place_request_data)
    db.session.add(place_request)
    db.session.commit()
    return ApiResult(request_schema.dump(place_request), 201)
