from flask import Blueprint, current_app, request

from ..auth import admin_only
from ..email import send_email
from ..exceptions import ApiException
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

    send_new_request_email(place_request)

    return ApiResult(request_schema.dump(place_request), 201)


def send_new_request_email(place_request):
    template = current_app.jinja_env.get_template("new_request_email.html")
    content = template.render(
        user=place_request.user,
        name=place_request.name,
        district_types=place_request.district_types,
        information=place_request.information,
    )
    try:
        send_email(
            "requests@districtr.org",
            "districtr@mggg.org",
            "New Districtr Request: {}".format(place_request.name),
            content,
        )
    except ApiException:
        current_app.logger.error("Unable to send email")
