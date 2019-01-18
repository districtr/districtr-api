import os

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@{host}:{port}/{db}".format(
    user=os.environ.get("POSTGRES_USER", "mggg"),
    password=os.environ.get("POSTGRES_PASSWORD", "mgggiskool"),
    db=os.environ.get("POSTGRES_DB", "gis"),
    port=os.environ.get("POSTGRES_PORT", 5432),
    host=os.environ.get("POSTGRES_HOST", "localhost"),
)

try:
    with open("/run/secrets/secret_key", "rb") as f:
        SECRET_KEY = f.read()
except FileNotFoundError:
    print("Using development secret key. Never do this in production!")
    SECRET_KEY = "my_secret_key"
