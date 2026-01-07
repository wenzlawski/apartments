import logging
import multiprocessing

import typer
import uvicorn

logger = logging.getLogger(__name__)

app_cli = typer.Typer(help="Management CLI for the project")


@app_cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
):
    """
    Root command. Shows help if no subcommand is given.
    """
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@app_cli.command()
def start(
    reload: bool = typer.Option(False, help="Enable auto-reload (dev only)"),
):
    """
    Start the FastAPI server.
    """
    logger.info("Starting server")
    uvicorn.run(
        "app.main:app",  # or create_app() via factory, see note below
        reload=reload,
        factory=False,  # set True if you want to use create_app as a factory
    )


@app_cli.command()
def scrape_once():
    """
    Run the scraper once (blocking).
    """
    logger.info("Running scraper once via CLI")


def entrypoint():
    multiprocessing.freeze_support()
    app_cli()


if __name__ == "__main__":
    entrypoint()
