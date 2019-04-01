from .models import User, db
import click
from flask.cli import AppGroup

admin_cli = AppGroup("admin")


@admin_cli.command("create")
@click.argument("email")
def make_admin(email):
    user = User.by_email(email)
    if not user:
        click.echo("The specified user does not exist.")
        return
    if not user.has_role("admin"):
        user.add_role("admin")
        db.session.commit()
