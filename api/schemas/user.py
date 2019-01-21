from marshmallow import Schema, fields, post_dump, post_load, pre_load
from marshmallow.validate import OneOf

from ..models import Role, User


class RoleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=OneOf({"user", "admin"}))

    @post_dump
    def just_return_name(self, data):
        return data["name"]

    @post_load
    def find_role(self, data):
        return Role.query.filter_by(name=data["name"]).first()


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first = fields.Str()
    last = fields.Str()
    email = fields.Email()
    roles = fields.Nested(RoleSchema, many=True)

    @pre_load
    def turn_strings_into_roles(self, data):
        data["roles"] = [{"name": role} for role in data["roles"]]
        return data

    @post_load
    def create_user(self, data):
        return User(**data)
