from .db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(80), nullable=False)
    last = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), nullable=False)

    plans = db.relationship("Plan", backref="user")

    def update(self, first=None, last=None, email=None, id=None):
        if first is not None:
            self.first = first

        if last is not None:
            self.last = last

        if email is not None:
            self.email = email
