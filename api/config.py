SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "postgresql://mggg:mgggiskool@localhost:5432/gis"

try:
    with open("/run/secrets/secret_key", "b") as f:
        SECRET_KEY = f.read()
except FileNotFoundError:
    SECRET_KEY = "my_secret_key"
