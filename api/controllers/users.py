from flask import Blueprint, jsonify, request

from ..models import User, db
from ..schemas import UserSchema

bp = Blueprint("users", __name__)

users_schema = UserSchema()
user_schema = UserSchema()


@bp.route("/", methods=["GET"])
def list_users():
    users = User.query.all()
    records = users_schema.dump(users)
    return jsonify(records)


@bp.route("/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user_schema.dump(user).data)


@bp.route("/", methods=["POST"])
def new_user():
    user_raw_json = request.get_json()
    user_data = user_schema.load(user_raw_json)
    user = User(**user_data.data)

    db.session.add(user)
    db.session.commit()

    return jsonify(id=user.id), 201
