from .db import db


class Column(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    key = db.Column(db.String(80), nullable=False)
    min = db.Column(db.Float())
    max = db.Column(db.Float())
    sum = db.Column(db.Float())
    column_set_id = db.Column(db.Integer, db.ForeignKey("column_set.id"))


class ColumnSet(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    columns = db.relationship("Column", backref="column_set", lazy=False)
    unit_set_id = db.Column(db.Integer, db.ForeignKey("unit_set.id"), nullable=False)


class UnitSet(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    unit_type = db.Column(db.String(80), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey("place.id"))
    id_column_key = db.Column(db.String(80))
    tilesets = db.relationship("Tileset", backref="unit_set", lazy=False)
    column_sets = db.relationship("ColumnSet", backref="unit_set", lazy=False)


class Tileset(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.String(80), nullable=False)
    source_url = db.Column(db.String(256), nullable=False)
    source_type = db.Column(db.String(80), nullable=False)
    source_layer = db.Column(db.String(80), nullable=False)
    unit_set_id = db.Column(db.Integer, db.ForeignKey("unit_set.id"))


class DistrictingProblem(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    number_of_parts = db.Column(db.Integer(), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    plural_noun = db.Column(db.String(256), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey("place.id"))


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), nullable=False, unique=True, index=True)
    name = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)

    plans = db.relationship("Plan", backref="place", lazy=True)

    # units = db.relationship("UnitSet", backref="place", lazy=False)
    # districting_problems = db.relationship(
    # "DistrictingProblem", backref="place", lazy=False
    # )

    @classmethod
    def by_slug(cls, slug):
        return cls.query.filter_by(slug=slug).first_or_404()

    def __repr__(self):
        return "<Place {}>".format(self.name)
