from .sa import CustomSQLAlchemy as SQLAlchemy

# Initialize database.
db = SQLAlchemy()

# This is a postgis built-in table that we need to define, or else Alembic will try
# to remove it during every database migration.
spatial_ref_sys = db.Table(
    "spatial_ref_sys",
    db.Column("srid", db.INTEGER(), autoincrement=False, nullable=False),
    db.Column("auth_name", db.VARCHAR(length=256), autoincrement=False, nullable=True),
    db.Column("auth_srid", db.INTEGER(), autoincrement=False, nullable=True),
    db.Column("srtext", db.VARCHAR(length=2048), autoincrement=False, nullable=True),
    db.Column("proj4text", db.VARCHAR(length=2048), autoincrement=False, nullable=True),
    db.CheckConstraint(
        "(srid > 0) AND (srid <= 998999)", name="spatial_ref_sys_srid_check"
    ),
    db.PrimaryKeyConstraint("srid", name="spatial_ref_sys_pkey"),
)
