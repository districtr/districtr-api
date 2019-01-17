from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int()
    first = fields.Str()
    last = fields.Str()
    email = fields.Email()
