SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "postgresql://mggg:mgggiskool@localhost:5432/gis"

try:
    with open("/run/secrets/secret_key", "rb") as f:
        SECRET_KEY = f.read()
except FileNotFoundError:
    print("Using development secret key. Never do this in production!")
    SECRET_KEY = "my_secret_key"
