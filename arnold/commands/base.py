#!/usr/bin/env python
import click
import yaml

from arnold import options

# commands
from arnold.commands.serve import serve_command


@click.group(invoke_without_command=True)
@options.config()
@click.pass_context
def cli(ctx, config):
    with open(config) as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)

    ctx.ensure_object(dict)
    ctx.obj["host"] = config_data.get("ARNOLD_HOST")
    ctx.obj["port"] = config_data.get("ARNOLD_PORT")
    ctx.obj["db_uri"] = config_data.get("DB_URI")
    ctx.obj["db_name"] = config_data.get("DB_NAME")


cli.add_command(serve_command)
