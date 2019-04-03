from api.models import User
from api.commands import add_role


def test_add_role(app):
    runner = app.test_cli_runner()

    runner.invoke(add_role, ["admin", "--email", "person@example.com"])

    with app.app_context():
        user = User.by_email("person@example.com")
        assert user.has_role("admin")


def test_make_nonexistant_admin_tells_you_it_didnt_work(app):
    runner = app.test_cli_runner()

    result = runner.invoke(add_role, ["admin", "--email", "missing@example.com"])
    assert "does not exist" in result.output
    assert result.exit_code == 1


def test_add_nonexistent_role_exits_with_code_1(app):
    runner = app.test_cli_runner()

    result = runner.invoke(add_role, ["hamlet", "--email", "person@example.com"])
    assert result.exit_code == 1
