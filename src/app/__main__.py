import click
from .app import run_app


@click.command()
@click.option("--local", is_flag=True, help="Run in local mode.")
@click.option("--server", is_flag=True, help="Run in server mode.")
@click.option(
    "--host", default="0.0.0.0", help="Host address for server mode."
)
@click.option(
    "--port", default=8050, type=int, help="Port number for server mode."
)
def main(local, server, host, port):
    if local and server:
        click.echo("Error: Cannot use both --local and --server.")
        return

    if local:
        run_app(local=True)
    elif server:
        run_app(local=False, host=host, port=port)
    else:
        click.echo("Error: Must specify either --local or --server.")


if __name__ == "__main__":
    main()
