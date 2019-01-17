from marshmallow import Schema, fields, post_load

from ..models import User


class UserSchema(Schema):
    id = fields.Int()
    first = fields.Str()
    last = fields.Str()
    email = fields.Email()

    @post_load
    def create_user(self, data):
        return User(**data)
