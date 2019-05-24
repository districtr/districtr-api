from flask import Blueprint, request

from ..auth import authenticate, get_current_user, admin_only
from ..exceptions import ApiException
from ..result import ApiResult
from ..models import Plan, db
from ..schemas import PlanSchema, PlanSchemaOut

bp = Blueprint("plans", __name__)

plans_schema = PlanSchema(
    only=(
        "id",
        "name",
        "created_at",
        "modified_at",
        "user",
        "units_id",
        "problem_id",
        "place_id",
    ),
    many=True,
)
plan_schema = PlanSchema()
plan_schema_out = PlanSchemaOut()


@bp.route("/", methods=["POST"])
@admin_only
def new_plan():
    data = plan_schema.load(request.get_json())

    name = data["name"]
    place_id = data["place_id"]
    problem_id = data["problem_id"]
    units_id = data["units_id"]
    parts = data.get("parts", None)
    serialized = data.get("serialized", None)

    plan = Plan(
        name=name,
        serialized=serialized,
        place_id=place_id,
        problem_id=problem_id,
        units_id=units_id,
        user=get_current_user(),
        parts=parts,
    )

    db.session.add(plan)
    db.session.commit()
    return ApiResult(plan_schema_out.dump(plan), 201)


@bp.route("/", methods=["GET"])
@admin_only
def list_plans():
    """List all plans."""
    plans = Plan.query.order_by(Plan.modified_at.desc())
    records = plans_schema.dump(plans)
    return ApiResult(records)


@authenticate
def list_my_plans():
    user = get_current_user()
    records = plans_schema.dump(
        Plan.query.with_parent(user).order_by(Plan.modified_at.desc())
    )
    return ApiResult(records)


@bp.route("/<int:id>", methods=["GET"])
@authenticate
def get_plan(id):
    plan = Plan.query.get_or_404(id)

    user = get_current_user()
    if not plan.belongs_to(user):
        raise ApiException("You are not authorized to view this resource.", 403)

    return ApiResult(plan_schema_out.dump(plan))


@bp.route("/<int:id>", methods=["PATCH", "PUT"])
@authenticate
def update_plan(id):
    plan = Plan.query.get_or_404(id)

    user = get_current_user()
    if not plan.belongs_to(user):
        raise ApiException("You are not authorized to edit this resource.", 403)

    data = request.get_json()

    plan.update(**data)
    db.session.commit()

    return "", 204


@bp.route("/<int:id>", methods=["DELETE"])
@authenticate
def delete_plan(id):
    plan = Plan.query.get_or_404(id)

    user = get_current_user()
    if not plan.belongs_to(user):
        raise ApiException("You are not authorized to delete this resource.", 403)

    db.session.delete(plan)
    db.session.commit()

    return "", 204
