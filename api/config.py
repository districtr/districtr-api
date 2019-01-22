import os
import pathlib
import warnings


def secret(name, default=None, mode="r", secrets_path="/run/secrets/"):
    try:
        with open(pathlib.Path(secrets_path) / name, mode) as f:
            return f.read().strip()
    except FileNotFoundError:
        warnings.warn(
            "Using default for secret {}. Never do this in production!".format(name),
            DefaultSecretWarning,
        )
        return default


def environment(name, default=None):
    return os.environ.get(name, default)


def database_uri(user, password, db, port, host, driver="postgresql"):
    return f"{driver}://{user}:{password}@{host}:{port}/{db}"


def get_database_uri_from_environment():
    return database_uri(
        user=secret("gis_user", environment("POSTGRES_USER", "mggg")),
        password=secret("gis_password", environment("POSTGRES_PASSWORD", "mgggiskool")),
        db=environment("POSTGRES_DB", "gis"),
        port=environment("POSTGRES_PORT", 5432),
        host=environment("POSTGRES_HOST", "localhost"),
    )


class DefaultSecretWarning(Warning):
    pass


SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = get_database_uri_from_environment()
SECRET_KEY = secret("secret_key", default="my_secret_key", mode="rb")
