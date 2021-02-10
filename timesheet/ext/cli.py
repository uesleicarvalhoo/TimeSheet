import click
from flask import Flask

from timesheet.ext.db import create_all, drop_db
from timesheet.ext.db.models.users import User


def init_app(app: Flask) -> None:
    app.cli.add_command(app.cli.command()(create_user))
    app.cli.add_command(app.cli.command()(create_all))
    app.cli.add_command(app.cli.command()(drop_db))


@click.option("--username", "-u")
@click.option("--passwd", "-p")
@click.option("--workload", "-w")
@click.option("--name", "-n", default="")
@click.option("--admin", "-a", is_flag=True, default=True)
def create_user(username: str, passwd: str, name: str, workload: int, admin: bool) -> None:
    user = User.create(username, passwd, name, workload, admin, save=False)
    response = user.save()

    if response["success"]:
        click.echo('Usuario "%s" criado com sucesso!' % user)

    else:
        click.echo("Erro ao criar usuario\nDescrição: %s" % response["message"])
