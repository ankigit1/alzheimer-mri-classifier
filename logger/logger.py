import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

_LOGGERS = {}


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        return True


def get_logger(name="app", log_file="inference.log"):
    cache_key = f"{name}:{log_file}"
    if cache_key in _LOGGERS:
        return _LOGGERS[cache_key]

    root = Path(__file__).resolve().parents[1]
    logs_dir = root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / log_file

    logger = logging.getLogger(cache_key)
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(request_id)s | "
        "%(filename)s:%(lineno)d | %(message)s"
    )

    file_handler = TimedRotatingFileHandler(
        log_path, when="midnight", interval=1, backupCount=14, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.addFilter(RequestIdFilter())

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(RequestIdFilter())

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.propagate = False

    _LOGGERS[cache_key] = logger
    return logger
