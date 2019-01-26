from marshmallow import Schema, fields, post_dump, pre_load
from marshmallow.validate import OneOf


class RoleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=OneOf({"user", "admin"}))

    @post_dump
    def just_return_name(self, data):
        return data["name"]


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first = fields.Str()
    last = fields.Str()
    email = fields.Email(required=True)
    roles = fields.Nested(RoleSchema, many=True)

    @pre_load
    def turn_strings_into_roles(self, data):
        if self.only is not None and "roles" not in self.only:
            return data

        if "roles" not in data:
            data["roles"] = ["user"]

        data["roles"] = [{"name": role} for role in data["roles"]]
        return data
