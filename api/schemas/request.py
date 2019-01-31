from marshmallow import Schema, fields, pre_load

from .user import UserSchema


class PlaceRequestSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    created_at = fields.Date(dump_only=True)
    modified_at = fields.Date(dump_only=True)
    district_types = fields.Str(required=True)
    information = fields.Str()

    user = fields.Nested(UserSchema(only=("first", "last", "email", "organization")))

    @pre_load
    def camel_case_to_snake_case(self, data):
        if "districtTypes" in data:
            data["district_types"] = data["districtTypes"]
            del data["districtTypes"]
        return data
