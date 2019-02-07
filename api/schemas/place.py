from datetime import datetime

from marshmallow import Schema, fields, post_load, validate

from ..models import Place
from ..models.place import Column, Election


class ColumnSchema(Schema):
    name = fields.Str(required=True)
    key = fields.Str(required=True)
    min = fields.Float()
    max = fields.Float()
    sum = fields.Float()

    @post_load
    def create_column(self, data):
        return Column(**data)


class ElectionSchema(Schema):
    year = fields.Integer(
        validate=validate.Range(min=1776, max=datetime.now().year), required=True
    )
    race = fields.String(required=True)
    vote_totals = fields.Nested(ColumnSchema, many=True)

    @post_load
    def create_election(self, data):
        return Election(**data)


class PlaceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    elections = fields.Nested(ElectionSchema, many=True)

    @post_load
    def create_place(self, data):
        return Place(**data)
