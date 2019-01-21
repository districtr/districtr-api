from .db import db


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)

    plans = db.relationship("Plan", backref="place")

    def __repr__(self):
        return "<Place {}>".format(self.name)
