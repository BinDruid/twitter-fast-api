import typer

cli = typer.Typer()


@cli.command('migrate-database')
def migrate_db():
    """Apply database migrations"""
    import subprocess

    subprocess.run(('alembic', 'upgrade', 'head'))  # noqa


@cli.command('runserver')
def runserver(
    port: int = 8000,
    host: str = 'localhost',
):
    """Run the API development server(uvicorn)."""
    import subprocess

    subprocess.run(('fastapi', 'dev', './twitter_api/main.py', '--reload', '--host', f'{host}', '--port', f'{port}'))  # noqa


if __name__ == '__main__':
    cli()
