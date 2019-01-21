from marshmallow import Schema, fields, post_dump, post_load
from marshmallow.validate import OneOf

from ..models import User


class RoleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=OneOf(("user", "admin")))

    @post_dump
    def just_return_name(self, data):
        return data["name"]


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first = fields.Str()
    last = fields.Str()
    email = fields.Email()
    roles = fields.Nested(RoleSchema, many=True)

    @post_load
    def create_user(self, data):
        return User(**data)
