from flask import Blueprint, json, jsonify, request

from .models import Plan, db
from .schemas import PlanSchema

bp = Blueprint("plan", __name__)

plans_schema = PlanSchema(only=("id", "name", "user"), many=True)
plan_schema = PlanSchema(only=("id", "name", "user", "mapping"))


@bp.route("/", methods=["POST"])
def new_plan():
    data = request.get_json()
    name = data["name"]
    serialized = json.dumps(data["mapping"])

    plan = Plan(name=name, serialized=serialized)

    db.session.add(plan)
    db.session.commit()
    return jsonify(id=plan.id), 201


@bp.route("/", methods=["GET"])
def get_plans():
    plans = Plan.query.all()
    records = plans_schema.dump(plans)
    return jsonify(records)


@bp.route("/<int:id>", methods=["GET"])
def get_plan(id):
    plan = Plan.query.filter_by(id=id).first_or_404()
    return jsonify(plan_schema.dump(plan))


@bp.route("/<int:id>", methods=["PATCH"])
def update_plan(id):
    plan = Plan.query.filter_by(id=id).first_or_404()

    data = request.get_json()
    plan.update(name=data.get("name", None), serialized=data.get("serialized", None))
    db.session.commit()

    return "", 204


@bp.route("/<int:id>", methods=["PUT"])
def overwrite_plan(id):
    plan = Plan.query.filter_by(id=id).first_or_404()

    data = request.get_json()
    plan.update(name=data["name"], serialized=data["serialized"])
    db.session.commit()

    return "", 204
