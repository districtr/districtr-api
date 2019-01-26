from .db import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    @classmethod
    def by_name(cls, name):
        if name not in {"user", "admin"}:
            raise ValueError
        role = Role.query.filter_by(name=name).first()
        if not role:
            role = Role(name=name)
        return role


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

    def email_already_exists(self):
        existing = User.query.filter_by(email=self.email).first()
        return bool(existing)

    @classmethod
    def from_schema_load(cls, data):
        if "roles" not in data:
            data["roles"] = [{"name": "user"}]
        roles = [Role.by_name(role["name"]) for role in data["roles"]]
        user = cls(first=data["first"], last=data["last"], email=data["email"])
        user.roles = roles
        return user
