
from marshmallow import Schema
from marshmallow import fields


class UserSchema(Schema):
    id = fields.Int()
    first = fields.Str()
    last = fields.Str()
    email = fields.Email()
