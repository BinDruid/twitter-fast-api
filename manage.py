from __future__ import annotations

from functools import partial
from itertools import chain

import httpx
import typer
import uvicorn
from tortoise import Tortoise, connections

from app.core.config import settings
from app.database.config import TORTOISE_ORM

cli = typer.Typer()


@cli.command('migrate-database')
def migrate_db():
    """Apply database migrations"""
    import subprocess

    subprocess.run(('aerich', 'upgrade'))


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
        'app.main:app',
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )


@cli.command()
def shell():
    """Opens an interactive shell with objects auto imported"""
    try:
        from IPython import start_ipython
        from traitlets.config import Config
    except ImportError:
        typer.secho(
            'Install iPython using `poetry add ipython` to use this feature.',
            fg=typer.colors.RED,
        )
        raise typer.Exit()

    def teardown_shell():
        import asyncio

        print('closing tortoise connections....')
        asyncio.run(connections.close_all())

    tortoise_init = partial(Tortoise.init, config=TORTOISE_ORM)
    modules = list(chain(*[app.get('models') for app in TORTOISE_ORM.get('apps').values()]))
    auto_imports = [
        'from tortoise.expressions import Q, F, Subquery',
        'from tortoise.query_utils import Prefetch',
    ] + [f'from {module} import *' for module in modules]
    shell_setup = [
        'import atexit',
        '_ = atexit.register(teardown_shell)',
        'await tortoise_init()',
    ]
    typer.secho('Auto Imports\n' + '\n'.join(auto_imports), fg=typer.colors.GREEN)
    c = Config()
    c.InteractiveShell.autoawait = True
    c.InteractiveShellApp.exec_lines = auto_imports + shell_setup
    start_ipython(
        argv=[],
        user_ns={'teardown_shell': teardown_shell, 'tortoise_init': tortoise_init},
        config=c,
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
