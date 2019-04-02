from .models import User, db
import click
from flask.cli import AppGroup

admin_cli = AppGroup("roles")


@admin_cli.command("add")
@click.option("--email")
@click.argument("role")
def add_role(role, email):
    user = User.by_email(email)
    if not user:
        click.echo("The specified user does not exist.")
        click.exit(1)
    try:
        user.add_role(role)
        db.session.commit()
    except ValueError:
        click.echo("The specified role is not defined.")
        click.exit(1)
    click.echo("User {} now has role {}.".format(email, role))
