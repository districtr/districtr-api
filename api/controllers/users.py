from flask import Blueprint, jsonify, request

from ..auth import admin_only
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
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.update(**data)
    db.session.commit()

    return jsonify(user_schema.dump(user)), 200


@bp.route("/<int:id>", methods=["DELETE"])
@admin_only
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return "", 200


@bp.route("/", methods=["POST"])
def new_user():
    user_data = request.get_json()
    user = user_schema.load(user_data)

    db.session.add(user)
    db.session.commit()

    return jsonify(id=user.id), 201
