from flask import json
from marshmallow import Schema, fields, post_dump, pre_load, pre_dump

from .user import UserSchema
from .place import DistrictingProblemSchema, UnitSetSchema, PlaceSchema


class PlanSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(default="Untitled")
    created_at = fields.Date(dump_only=True)
    modified_at = fields.Date(dump_only=True)

    user = fields.Nested(
        UserSchema(only=("id", "first", "last", "email")), dump_only=True
    )

    units_id = fields.Int()
    problem_id = fields.Int()
    place_id = fields.Int()

    parts = fields.Str()

    serialized = fields.Str()

    @post_dump
    def decode_assignment(self, data):
        if "serialized" in data:
            data["assignment"] = json.loads(data["serialized"])
            return {k: v for k, v in data.items() if k != "serialized"}
        return data

    @pre_load
    def encode_assignment_and_parts(self, data):
        if "parts" in data:
            data["parts"] = json.dumps(data["parts"])

        if "assignment" in data:
            if "serialized" not in data:
                data["serialized"] = json.dumps(data["assignment"])
            return {k: v for k, v in data.items() if k != "assignment"}
        return data


class PartSchema(Schema):
    id = fields.Int(validate=lambda n: n >= 0)
    displayNumber = fields.Int(validate=lambda n: n >= 1)
    name = fields.Str()
    description = fields.Str()


class PlanSchemaOut(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    place = fields.Nested(
        PlaceSchema(only=("id", "slug", "name", "state", "description"))
    )
    units = fields.Nested(UnitSetSchema)
    problem = fields.Nested(DistrictingProblemSchema)

    parts = fields.Nested(PartSchema, many=True)
    assignment = fields.Dict()

    created_at = fields.Date(dump_only=True)
    modified_at = fields.Date(dump_only=True)

    user = fields.Nested(
        UserSchema(only=("id", "first", "last", "email")), dump_only=True
    )

    @pre_dump
    def decode_parts(self, plan):
        data = {
            key: getattr(plan, key) if hasattr(plan, key) else None
            for key in self.fields
        }
        data = {key: value for key, value in data.items() if value is not None}
        if "parts" in data:
            data["parts"] = json.loads(data["parts"])
        data["assignment"] = json.loads(plan.serialized)
        return data
