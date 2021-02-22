import os
import logging
import sentry_sdk
from datetime import datetime as dt
from sentry_sdk.integrations.logging import LoggingIntegration

LOGGING_FORMAT = '%(asctime)s %(levelname)-8s: %(message)s'
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=f'./logs/discord.log',
                              mode='a',
                              encoding='UTF8')
handler.setFormatter(logging.Formatter(fmt=LOGGING_FORMAT,
                                       datefmt=DATE_FORMAT))
logger.addHandler(handler)

sentry_logging = LoggingIntegration(level=logging.INFO,
                                    event_level=logging.ERROR)
sentry_sdk.init(dsn=os.getenv('SENTRY_DSN'), integrations=[sentry_logging])


def get_logger():
    return logger