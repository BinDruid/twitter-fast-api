import logging

import sentry_sdk
from rich.logging import RichHandler
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.atexit import AtexitIntegration
from sentry_sdk.integrations.dedupe import DedupeIntegration
from sentry_sdk.integrations.excepthook import ExcepthookIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.modules import ModulesIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.stdlib import StdlibIntegration

from .config import settings

logger = logging.getLogger(__name__)

handler = RichHandler()

logger.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)

handler.setFormatter(logging.Formatter('%(message)s'))

logger.addHandler(handler)


sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)


def configure_sentry():
    logger.debug('Configuring Sentry')
    if settings.SENTRY_ENABLED:
        sentry_sdk.init(
            dsn=str(settings.SENTRY_ENABLED),
            integrations=[
                AioHttpIntegration(),
                AtexitIntegration(),
                DedupeIntegration(),
                ExcepthookIntegration(),
                ModulesIntegration(),
                SqlalchemyIntegration(),
                StdlibIntegration(),
                sentry_logging,
            ],
            environment=settings.ENVIRONMENT,
            auto_enabling_integrations=False,
        )
