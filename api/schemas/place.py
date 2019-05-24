import re
import json

from marshmallow import Schema, fields, post_load, pre_dump, pre_load
from marshmallow.validate import OneOf, Regexp
from us import states

from ..models import Place
from ..models.place import Column, ColumnSet, DistrictingProblem, Tileset, UnitSet


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
    number_of_parts = fields.Int()
    name = fields.Str(required=True)
    plural_noun = fields.Str(default="Districts", required=True)
    type = fields.Str(
        validate=OneOf(["districts", "community", "multimember"]), default="districts"
    )
    units = fields.List(fields.Str())

    @post_load
    def create_districting_problem(self, data):
        if "units" in data:
            data["units"] = json.dumps(data["units"])
        return DistrictingProblem(**data)

    @pre_dump
    def decode_units(self, data):
        if data.units:
            data = {key: getattr(data, key) for key in self.fields}
            data["units"] = json.loads(data["units"])
            return data
        return data


class ColumnSetSchema(Schema):
    name = fields.String(required=True)
    type = fields.String(required=True)
    subgroups = fields.Nested(ColumnSchema, many=True)
    total = fields.Nested(ColumnSchema)

    @post_load
    def create_model(self, data):
        return ColumnSet(**data)


class UnitSetSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    slug = fields.Str(required=True, validate=Regexp(re.compile("^[a-zA-Z0-9_]*$")))
    name = fields.String(required=True)
    unit_type = fields.String(required=True)
    id_column = fields.Nested(ColumnSchema, required=True)
    name_column = fields.Nested(ColumnSchema, required=False)
    tilesets = fields.Nested(TilesetSchema, many=True, required=True)
    column_sets = fields.Nested(ColumnSetSchema, many=True)
    bounds = fields.List(fields.List(fields.Float()), required=True)

    @pre_dump
    def translate_bounds(self, data):
        data = {
            "id": data.id,
            "slug": data.slug,
            "name": data.name,
            "unit_type": data.unit_type,
            "id_column": data.id_column,
            "name_column": data.name_column,
            "tilesets": data.tilesets,
            "column_sets": data.column_sets,
            "bounds": json.loads(data.bounds),
        }
        return data

    @post_load
    def create_unit_set(self, data):
        if not isinstance(data["bounds"], str):
            data["bounds"] = json.dumps(data["bounds"])
        return UnitSet(**data)


class PlaceSchema(Schema):
    id = fields.Int(dump_only=True)
    slug = fields.Str(required=True, validate=Regexp(re.compile("^[a-zA-Z0-9_]*$")))
    name = fields.Str(required=True)
    state = fields.Str(required=True)
    description = fields.Str()
    landmarks = fields.Dict()

    units = fields.Nested(UnitSetSchema, many=True)
    districting_problems = fields.Nested(DistrictingProblemSchema, many=True)

    @pre_load
    def lookup_state(self, data):
        state = states.lookup(data["state"])
        data["state"] = state.name
        return data

    @post_load
    def create_place(self, data):
        if "landmarks" in data:
            data["landmarks"] = json.dumps(data["landmarks"])
        return Place(**data)

    @pre_dump
    def decode_landmarks(self, data):
        if hasattr(data, "landmarks"):
            data = {key: getattr(data, key) for key in self.fields}
            data["landmarks"] = json.loads(data["landmarks"])
            return data
        return data
