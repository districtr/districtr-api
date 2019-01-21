from marshmallow import Schema, fields, post_load

from ..models import Place
from ..models.place import Column


class ColumnSchema(Schema):
    name = fields.Str(required=True)
    key = fields.Str(required=True)
    min = fields.Float()
    max = fields.Float()
    sum = fields.Float()
    is_id = fields.Boolean(default=False)

    @post_load
    def create_column(self, data):
        return Column(**data)


class PlaceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()

    @post_load
    def create_place(self, data):
        return Place(**data)
