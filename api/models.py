from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return "<Place {}>".format(self.name)


class DistrictingProblem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey("place.id"))
    place = db.relationship("Place", backref=db.backref("problems", lazy="dynamic"))
    number_of_parts = db.Column(db.Integer, nullable=False)


class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("plans", lazy="dynamic"))
    serialized = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<Plan {}>".format(self.name)

    def update(self, name=None, serialized=None):
        if name is not None:
            self.name = name
        if serialized is not None:
            self.serialized = serialized
        self.modified_at = datetime.utcnow()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(80), nullable=False)
    last = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), nullable=False)
