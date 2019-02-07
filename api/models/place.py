from .db import db


class Column(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    key = db.Column(db.String(80), nullable=False)
    min = db.Column(db.Float())
    max = db.Column(db.Float())
    sum = db.Column(db.Float())
    # Optional election id for vote total columns:
    election_id = db.Column(db.Integer, db.ForeignKey("election.id"))


# class UnitType(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(80), nullable=False)


class Election(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    race = db.Column(db.String(80), nullable=False)
    vote_totals = db.relationship("Column", backref="election", lazy=True)
    year = db.Column(db.Integer(), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey("place.id"))


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)

    # id_column_id = db.Column(db.Integer, db.ForeignKey("column.id"))
    # unit_type_id = db.Column(db.Integer, db.ForeignKey("unit_type.id"))

    # columns = db.relationship("Column", backref="place", lazy=True)
    plans = db.relationship("Plan", backref="place")

    elections = db.relationship("Election", backref="place", lazy=True)

    def __repr__(self):
        return "<Place {}>".format(self.name)
