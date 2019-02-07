from flask import Blueprint, request

from ..auth import admin_only, authenticate, get_current_user
from ..exceptions import ApiException
from ..models import Place, db
from ..result import ApiResult
from ..schemas import PlaceSchema


def resource_blueprint(Schema, Model, name):
    """This repurposes a lot of the code from the users endpoint to make an endpoint
    for another resource. There's probably a more object-oriented version of this
    approach that would be more effective."""
    bp = Blueprint(name, __name__)

    plural_schema = Schema(many=True)
    schema = Schema()

    @bp.route("/", methods=["GET"])
    def list_resources():
        resources = Model.query.all()
        records = plural_schema.dump(resources)
        return ApiResult(records)

    @bp.route("/<int:id>", methods=["GET"])
    def get(id):
        resource = Model.query.get_or_404(id)
        return ApiResult(schema.dump(resource))

    @bp.route("/<int:id>", methods=["POST", "PUT", "PATCH"])
    @authenticate
    def update(id):
        resource = Model.query.get_or_404(id)

        if not resource.belongs_to(get_current_user()):
            raise ApiException("You are not authorized to edit this resource.", 403)

        data = request.get_json()
        resource.update(**data)
        db.session.commit()

        return ApiResult(schema.dump(resource))

    @bp.route("/<int:id>", methods=["DELETE"])
    @admin_only
    def delete(id):
        resource = Model.query.get_or_404(id)

        db.session.delete(resource)
        db.session.commit()

        return ApiResult(status=204)

    @bp.route("/", methods=["POST"])
    @admin_only
    def new():
        data = request.get_json()
        resource = schema.load(data)

        db.session.add(resource)
        db.session.commit()

        return ApiResult(schema.dump(resource), 201)

    return bp


bp = resource_blueprint(PlaceSchema, Place, "places")
