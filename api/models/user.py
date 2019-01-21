from .db import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


roles = db.Table(
    "roles",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(80), nullable=False)
    last = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    roles = db.relationship("Role", secondary=roles, lazy="subquery")

    plans = db.relationship("Plan", backref="user")

    def update(self, first=None, last=None, email=None, id=None):
        if first is not None:
            self.first = first

        if last is not None:
            self.last = last

        if email is not None:
            self.email = email

    def is_admin(self):
        return any(role.name == "admin" for role in self.roles)

    def belongs_to(self, user):
        return user.id == self.id or user.is_admin()
