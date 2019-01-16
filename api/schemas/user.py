from marshmallow import Schema
from marshmallow import fields


class userSchema(Schema):
    id = fields.Int()
    first = fields.Str()
    last = fields.Str()
    email = fields.Email()
