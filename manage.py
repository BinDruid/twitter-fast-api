from __future__ import annotations

import typer
import uvicorn

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
    log_level: str = 'debug',
    reload: bool = True,
):
    """Run the API development server(uvicorn)."""
    migrate_db()
    uvicorn.run(
        'api.main:api',
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )


if __name__ == '__main__':
    cli()
