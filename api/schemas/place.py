from datetime import datetime

from marshmallow import Schema, fields, post_load, pre_dump, validate
from marshmallow.validate import OneOf

from ..models import Place
from ..models.place import Column, Election, Tileset


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


class SourceSchema(Schema):
    url = fields.Str(
        validate=lambda url: url.split("://")[0] == "mapbox", required=True
    )
    type = fields.Str(validate=OneOf(["vector"]), required=True)


class TilesetSchema(Schema):
    source = fields.Nested(SourceSchema, required=True)
    type = fields.Str(validate=OneOf(["circle", "fill"]), required=True)
    sourceLayer = fields.Str(required=True)

    @post_load
    def create_tileset(self, data):
        return Tileset(
            source_url=data["source"]["url"],
            type=data["type"],
            source_type=data["source"]["type"],
            source_layer=data["sourceLayer"],
        )

    @pre_dump
    def unflatten_record(self, tileset):
        data = {
            "type": tileset.type,
            "source": {"type": tileset.source_type, "url": tileset.source_url},
            "sourceLayer": tileset.source_layer,
        }
        return data


class DistrictingProblemSchema(Schema):
    id = fields.Int(dump_only=True)
    numberOfParts = fields.Int(required=True)
    name = fields.Str(required=True)
    pluralNoun = fields.Str(required=True)


class PlaceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    elections = fields.Nested(ElectionSchema, many=True)
    tilesets = fields.Nested(TilesetSchema, many=True)

    @post_load
    def create_place(self, data):
        return Place(**data)
