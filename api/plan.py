from flask import Blueprint, jsonify, request

from .models import Plan, db

bp = Blueprint("plan", __name__)


@bp.route("/", methods=["POST"])
def new_plan():
    if "name" in request.form:
        data = request.form
    else:
        data = request.get_json()
    name = data["name"]
    serialized = data["serialized"]
    plan = Plan(name=name, serialized=serialized)
    db.session.add(plan)
    db.session.commit()
    return jsonify(id=plan.id)


@bp.route("/", methods=["GET"])
def get_plans():
    plans = Plan.query.all()
    print(plans)
    response = [{"id": plan.id, "name": plan.name} for plan in plans]
    return jsonify(response)
