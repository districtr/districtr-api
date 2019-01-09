from flask import json
from marshmallow import Schema, ValidationError, fields, pre_load


class UserSchema(Schema):
    id = fields.Int()
    first = fields.Str()
    last = fields.Str()
    email = fields.Email()

def not_blank(data):
    if not data:
        raise ValidationError("Provided data is blank.")


class PlanSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    user_id = fields.Int()
    user = fields.Nested(UserSchema)
    serialized = fields.Str()
    mapping = fields.Method("decode_mapping")
    created_at = fields.Date(dump_only=True)
    modified_at = fields.Date(dump_only=True)

    def decode_mapping(self, plan):
        return json.loads(plan.serialized)

    @pre_load
    def encode_mapping(self, data):
        if "mapping" in data:
            if "serialized" not in data:
                data["serialized"] = json.dumps(data["mapping"])
            del data["mapping"]
        return data
