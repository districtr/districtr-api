import os
import pathlib
import tempfile

import pytest

from api.config import (
    DefaultSecretWarning,
    database_uri,
    environment,
    get_database_uri_from_environment,
    secret,
)


class TestSecret:
    def test_secret_strips_whitespace(self):
        expected = "secret123490__--"
        with tempfile.TemporaryDirectory() as tempdir:
            with open(pathlib.Path(tempdir) / "my_test_secret", "w") as f:
                f.write(expected + "\n\n")

            value = secret("my_test_secret", secrets_path=tempdir)
            assert value == expected

    def test_secret_gives_default_when_missing(self):
        default = "my_default_secret"
        with pytest.warns(DefaultSecretWarning):
            value = secret("missing_secret", default=default, secrets_path="./")
        assert value == default

    def test_secret_warns_for_default(self):
        default = "my_default_secret"
        with pytest.warns(DefaultSecretWarning):
            secret("missing_secret", default=default, secrets_path="./")


class TestEnvironment:
    def test_environment(self):
        expected = "secret123490__--"
        os.environ["TEST_ENV_VAR"] = expected

        value = environment("TEST_ENV_VAR")

        assert value == expected

    def test_environment_gives_default_when_missing(self):
        assert (
            environment("MISSING_ENV_VAR", default="default_value") == "default_value"
        )


def test_database_uri():
    uri = database_uri("mggg", "mgggiskool", "gis", 5432, "gis")
    assert uri == "postgresql://mggg:mgggiskool@gis:5432/gis"


def test_get_database_uri_from_environment():
    os.environ["POSTGRES_HOST"] = "localhost"
    os.environ["POSTGRES_DB"] = "my_db"
    os.environ["POSTGRES_USER"] = "user"
    os.environ["POSTGRES_PASSWORD"] = "password123"
    os.environ["POSTGRES_PORT"] = "25432"
    uri = get_database_uri_from_environment()
    assert uri == "postgresql://user:password123@localhost:25432/my_db"
