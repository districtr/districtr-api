from datetime import datetime

from .db import db


class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey("place.id"))

    # The JSON string of the { unit id: district number } mapping.
    serialized = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Plan {}>".format(self.name)

    def update(self, name=None, serialized=None):
        if name is not None:
            self.name = name
        if serialized is not None:
            self.serialized = serialized
        self.modified_at = datetime.utcnow()
