"""
Module with CLI commands for arnold
The CLI is intended for development/testing purpose only. To run in a production setting please refer to documentation
for suggestions how.
"""

import logging
import click
import uvicorn

# Get version and doc decorator
from arnold import __version__
from arnold.settings import settings

LOG = logging.getLogger(__name__)


@click.version_option(__version__)
@click.group()
@click.pass_context
def cli(context: click.Context):
    """Main entry point"""
    logging.basicConfig(level=logging.INFO)
    context.obj = {}


@cli.command(name="serve")
@click.option(
    "--version", default="v1", type=click.Choice(["v1", "v2"]), show_default=True
)
@click.option("--reload", is_flag=True)
def serve_command(reload: bool, version: str):
    """Serve the arnold app for testing purpose."""

    app = f"arnold.api.api_{version}.api:app"
    LOG.info("Running on host:%s and port:%s", settings.host, settings.port)
    uvicorn.run(app=app, host=settings.host, port=settings.port, reload=reload)
