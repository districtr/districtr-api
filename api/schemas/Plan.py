
from flask import json
from marshmallow import Schema
from marshmallow import fields
from marshmallow import pre_load

from .User import UserSchema


class PlanSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    user_id = fields.Int()
    user = fields.Nested(UserSchema)
    serialized = fields.Str()
    mapping = fields.Method("decode_mapping")
    created_at = fields.Date(dump_only=True)
    modified_at = fields.Date(dump_only=True)

    # TODO incorporate this somehow – it'll be useful for decoding, but doesn't
    # get used there as of now.
    def decode_mapping(self, plan):
        return json.loads(plan.serialized)

    # TODO change this method up a bit.
    @pre_load
    def encode_mapping(self, data):
        if "mapping" in data:
            if "serialized" not in data:
                data["serialized"] = json.dumps(data["mapping"])
            del data["mapping"]
        return data