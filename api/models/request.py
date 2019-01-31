from datetime import datetime

from .db import db


class PlaceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    district_types = db.Column(db.String(160), nullable=False)
    information = db.Column(db.Text)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return "<PlaceRequest {}>".format(self.name)
