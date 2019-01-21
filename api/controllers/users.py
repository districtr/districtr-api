from flask import Blueprint, jsonify, request

from ..auth import admin_only, authenticate, get_current_user
from ..exceptions import ApiException
from ..models import User, db
from ..schemas import UserSchema

bp = Blueprint("users", __name__)

users_schema = UserSchema(many=True)
user_schema = UserSchema()


@bp.route("/", methods=["GET"])
def list_users():
    users = User.query.all()
    records = users_schema.dump(users)
    return jsonify(records), 200


@bp.route("/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user_schema.dump(user)), 200


@bp.route("/<int:id>", methods=["POST", "PUT", "PATCH"])
@authenticate
def update_user(id):
    user = User.query.get_or_404(id)

    if not user.belongs_to(get_current_user()):
        raise ApiException("You are not authorized to edit this resource.", 403)

    data = request.get_json()
    user.update(**data)
    db.session.commit()

    return jsonify(user_schema.dump(user)), 200


@bp.route("/<int:id>", methods=["DELETE"])
@admin_only
def delete_user(id):
    user = User.query.get_or_404(id)

    if user.id == get_current_user().id:
        return ApiException("A user cannot delete itself.", 400)

    db.session.delete(user)
    db.session.commit()

    return "", 204


@bp.route("/", methods=["POST"])
@admin_only
def new_user():
    user_data = request.get_json()
    user = user_schema.load(user_data)

    db.session.add(user)
    db.session.commit()

    return jsonify(id=user.id), 201
