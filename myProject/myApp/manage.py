import click
from flask.cli import with_appcontext


@click.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from myApp.extensions import db
    from myApp.models import User

    click.echo("create user")
    user = User(username="admin", email="rocketwalker@gmail.com", password="password", active=True)
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")
