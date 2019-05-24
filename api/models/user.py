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

    organization = db.Column(db.String(160), nullable=True)

    roles = db.relationship("Role", secondary=roles, lazy="subquery")
    place_requests = db.relationship("PlaceRequest", backref="user")
    plans = db.relationship("Plan", backref="user", lazy=True)

    def update(
        self, first=None, last=None, email=None, organization=None, roles=None, **kwargs
    ):
        if first is not None:
            self.first = first
        if last is not None:
            self.last = last
        if email is not None:
            self.email = email
        if organization is not None:
            self.organization = organization
        if roles is not None:
            for role in roles:
                self.add_role(role)

    def belongs_to(self, user):
        return user.id == self.id or user.has_role("admin")

    def email_already_exists(self):
        existing = User.query.filter_by(email=self.email).first()
        return bool(existing)

    def add_role(self, role_name):
        if not self.has_role(role_name):
            role = Role.by_name(role_name)
            self.roles.append(role)

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)

    @classmethod
    def by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def from_schema_load(cls, data):
        if "roles" not in data:
            data["roles"] = [{"name": "user"}]
        roles = [Role.by_name(role["name"]) for role in data["roles"]]
        user = cls(
            first=data["first"],
            last=data["last"],
            email=data["email"],
            organization=data.get("organization", None),
        )
        user.roles = roles
        return user
