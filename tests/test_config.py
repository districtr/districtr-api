import os
import pathlib
import tempfile

from api.config import environment, secret


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
        value = secret("missing_secret", default=default, secrets_path="./")
        assert value == default


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
