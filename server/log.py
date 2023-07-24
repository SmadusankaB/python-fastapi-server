from pydantic import BaseModel
from server.config import settings


# pydanthic does cls to dict casting
class LogConfig(BaseModel):
    """Logging configuration to be set"""

    LOGGER_NAME: str = settings.LOGGER_NAME
    LOG_FORMAT: str = "%(levelprefix)s %(asctime)s [%(filename)s %(lineno)d] %(message)s"
    LOG_LEVEL: str = settings.LOG_LEVEL
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }
