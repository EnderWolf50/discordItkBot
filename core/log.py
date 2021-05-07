import sys
import logging
import sentry_sdk
from pathlib import Path
from datetime import datetime
from logging import handlers

import coloredlogs
from sentry_sdk.integrations.logging import LoggingIntegration

from core import Log

__all__ = (
    'logging_setup',
    'sentry_setup',
)


def logging_setup() -> None:
    logging.TRACE = Log.log_level
    logging.addLevelName(Log.log_level, "TRACE")
    logging.Logger.trace = _logging_trace

    log_level = Log.log_level

    log_file = Path(
        Log.file_path,
        Log.file_name,
    )
    log_file.parent.mkdir(exist_ok=True)

    log_handler = handlers.RotatingFileHandler(
        filename=log_file,
        maxBytes=5242880,
        backupCount=10,
        encoding="UTF-8",
    )

    log_format = logging.Formatter(
        fmt=Log.log_format,
        datefmt=Log.date_format,
    )
    log_handler.setFormatter(log_format)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(log_handler)

    logging.getLogger("discord").setLevel(logging.ERROR)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.INFO)
    logging.getLogger("googleapiclient").setLevel(logging.WARNING)

    coloredlogs.DEFAULT_LEVEL_STYLES = {
        **coloredlogs.DEFAULT_LEVEL_STYLES,
        **Log.coloredlogs["styles"],
    }
    coloredlogs.DEFAULT_LOG_FORMAT = Log.log_format
    coloredlogs.DEFAULT_LOG_LEVEL = log_level
    coloredlogs.install(logger=root_logger, stream=sys.stdout)


def sentry_setup() -> None:
    sentry_logging = LoggingIntegration(
        level=logging.DEBUG,
        event_level=logging.WARNING,
    )

    sentry_sdk.init(
        dsn=Log.sentry_dsn,
        integrations=[
            sentry_logging,
        ],
    )


def _logging_trace(self: logging.Logger, msg: str, *args, **kwargs) -> None:
    if self.isEnabledFor(Log.log_level):
        self._log(Log.log_level, msg, args, **kwargs)
