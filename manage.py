from __future__ import annotations

import httpx
import typer
import uvicorn

from src.core.config import settings

cli = typer.Typer()


@cli.command('migrate-database')
def migrate_db():
    """Apply database migrations"""
    import subprocess

    subprocess.run(('migrations', 'upgrade', 'head'))


@cli.command('runserver')
def runserver(
    port: int = 8000,
    host: str = 'localhost',
    log_level: str = 'debug',
    reload: bool = True,
):
    """Run the API development server(uvicorn)."""
    # migrate_db()
    uvicorn.run(
        'src.main:api',
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )


@cli.command()
def info():
    """Show project health and settings."""
    with httpx.Client(base_url=settings.SERVER_HOST) as client:
        try:
            resp = client.get('/health', follow_redirects=True)
        except httpx.ConnectError:
            app_health = typer.style('❌ API is not responding', fg=typer.colors.RED, bold=True)
        else:
            app_health = '\n'.join([f'{key.upper()}={value}' for key, value in resp.json().items()])

    envs = '\n'.join([f'{key}={value}' for key, value in settings.dict().items()])
    title = typer.style('===> APP INFO <==============\n', fg=typer.colors.BLUE)
    typer.secho(title + app_health + '\n' + envs)


if __name__ == '__main__':
    cli()
