from marshmallow import Schema, fields, post_load

from ..models import Place


class PlaceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()

    @post_load
    def create_place(self, data):
        return Place(**data)
