from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<Place %r>" % self.name
