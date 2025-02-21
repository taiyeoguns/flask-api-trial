from logging.config import dictConfig
from pathlib import Path

from decouple import config
from sqlalchemy.engine.url import URL

BASEDIR = Path.cwd()

LOG_LEVEL = config("LOG_LEVEL", default="debug").upper()
LOG_DIR = BASEDIR / "logs"


dictConfig(
    dict(
        version=1,
        formatters={
            "default": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
            },
            "rich": {"datefmt": "[%X]"},
        },
        handlers={
            "console": {
                "class": "rich.logging.RichHandler",
                "formatter": "rich",
                "level": "DEBUG",
                "rich_tracebacks": True,
            },
            "file": {
                "level": "DEBUG",
                "formatter": "default",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": LOG_DIR / "app.log",
                "when": "D",
                "interval": 1,
                "backupCount": 7,
            },
        },
        root={"handlers": ["console"], "level": "DEBUG"},
        loggers={
            "app": {
                "level": LOG_LEVEL,
                "handlers": ["console", "file"],
                "propagate": False,
            }
        },
    )
)


class Config:
    SECRET_KEY = config("SECRET_KEY", default="s3cRe7-kE4")
    DEBUG = False
    API_VERSION = "v1"
    FLASK_RUN_PORT = config("FLASK_RUN_PORT", default=5000, cast=int)
    API_KEY = config("API_KEY")
    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="postgresql",
        username=config("POSTGRES_USER"),
        password=config("POSTGRES_PASSWORD"),
        host=config("POSTGRES_HOST"),
        port=config("POSTGRES_PORT", default=5432, cast=int),
        database=config("POSTGRES_DB"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
