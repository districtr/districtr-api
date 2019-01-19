import os
import warnings


def secret(name, default=None, mode="r"):
    try:
        with open("/run/secrets/{}".format(name), mode) as f:
            return f.read()
    except FileNotFoundError:
        warnings.warn(
            "Using default for secret {}. Never do this in production!".format(name)
        )
        return default


def environment(name, default=None):
    return (os.environ.get(name, default),)


SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@{host}:{port}/{db}".format(
    user=secret("gis_user", environment("POSTGRES_USER", "mggg")),
    password=secret("gis_password", environment("POSTGRES_PASSWORD", "mgggiskool")),
    db=environment("POSTGRES_DB", "gis"),
    port=environment("POSTGRES_PORT", 5432),
    host=environment("POSTGRES_HOST", "localhost"),
)
SECRET_KEY = secret("secret_key", default="my_secret_key", mode="rb")
