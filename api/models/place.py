from .db import db


class Column(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    key = db.Column(db.String(80), nullable=False)
    min = db.Column(db.Float())
    max = db.Column(db.Float())
    sum = db.Column(db.Float())
    is_id_column = db.Column(db.Boolean(), default=False)


class UnitType(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)

    id_column_id = db.Column(db.Integer, db.ForeignKey("column.id"))
    unit_type_id = db.Column(db.Integer, db.ForeignKey("unit_type.id"))

    columns = db.relationship("Column", backref="place", lazy=True)
    plans = db.relationship("Plan", backref="place")

    def __repr__(self):
        return "<Place {}>".format(self.name)
