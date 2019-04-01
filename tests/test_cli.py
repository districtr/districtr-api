from api.models import User
from api.commands import make_admin


def test_make_admin(app):
    runner = app.test_cli_runner()

    runner.invoke(make_admin, ["person@example.com"])

    with app.app_context():
        user = User.by_email("person@example.com")
        assert user.has_role("admin")


def test_make_nonexistant_admin_tells_you_it_didnt_work(app):
    runner = app.test_cli_runner()

    result = runner.invoke(make_admin, ["missing@example.com"])
    assert "does not exist" in result.output
