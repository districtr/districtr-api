import os

SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = (
    "postgresql+psycopg2://"
    "{user}:{password}@{url}/{db}".format(
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        url=os.environ["POSTGRES_URL"],
        db=os.environ["POSTGRES_DB"],
    )
)
