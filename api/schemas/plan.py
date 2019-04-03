from flask import json
from marshmallow import Schema, fields, post_dump, post_load, pre_load

from ..models import Plan
from .user import UserSchema


class PlanSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    created_at = fields.Date(dump_only=True)
    modified_at = fields.Date(dump_only=True)

    user = fields.Nested(
        UserSchema(only=("id", "first", "last", "email")), dump_only=True
    )

    place_id = fields.Int()

    serialized = fields.Str()

    @post_dump
    def decode_assignment(self, data):
        if "serialized" in data:
            data["assignment"] = json.loads(data["serialized"])
            return {k: v for k, v in data.items() if k != "serialized"}
        return data

    @pre_load
    def encode_assignment(self, data):
        if "assignment" in data:
            if "serialized" not in data:
                data["serialized"] = json.dumps(data["assignment"])
            return {k: v for k, v in data.items() if k != "assignment"}
        return data

    @post_load
    def create_plan(self, data):
        return Plan(**data)
