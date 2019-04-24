from marshmallow import Schema, fields, post_load, pre_dump
from marshmallow.validate import OneOf

from ..models import Place
from ..models.place import Column, UnitSet, ColumnSet, DistrictingProblem, Tileset
from ..utils import camel_to_snake


class ColumnSchema(Schema):
    name = fields.Str(required=True)
    key = fields.Str(required=True)
    min = fields.Float()
    max = fields.Float()
    sum = fields.Float()

    @post_load
    def create_column(self, data):
        return Column(**data)


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
    pluralNoun = fields.Str(default="Districts", required=True)

    @post_load
    @camel_to_snake
    def create_districting_problem(self, data):
        return DistrictingProblem(**data)


class ColumnSetSchema(Schema):
    name = fields.String(required=True)
    type = fields.String(required=True)
    columns = fields.Nested(ColumnSchema, many=True)

    @post_load
    @camel_to_snake
    def create_model(self, data):
        return ColumnSet(**data)


class UnitSetSchema(Schema):
    unitType = fields.String(required=True)
    idColumn = fields.Nested(ColumnSchema, required=True)
    tilesets = fields.Nested(TilesetSchema, many=True, required=True)
    columnSets = fields.Nested(ColumnSetSchema, many=True)

    @post_load
    @camel_to_snake
    def create_unit_set(self, data):
        data["id_column_key"] = data["id_column"].key
        del data["id_column"]
        return UnitSet(**data)


class PlaceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    units = fields.Nested(UnitSetSchema, many=True)
    districtingProblems = fields.Nested(DistrictingProblemSchema, many=True)

    @post_load
    @camel_to_snake
    def create_place(self, data):
        return Place(**data)

    @pre_dump
    def dump_place(self, place):
        return {
            "id": place.id,
            "name": place.name,
            "description": place.description,
            "units": place.units,
            "districtingProblems": place.districting_problems,
        }
