from logging.handlers import RotatingFileHandler
import sys

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    ADMIN: int
    MODERATOR: int
    DBPASS: SecretStr = "postgres"
    DBNAME: str = "postgres"
    DBUSER: str = "postgres"
    DBHOST: str = "localhost"
    DBPORT: int = 5432
    echo: bool = False

    @property
    def postgres_db_url(self) -> str:
        return f'postgresql+asyncpg://{self.DBUSER}:{self.DBPASS.get_secret_value()}@{self.DBHOST}:{self.DBPORT}/{self.DBNAME}'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=False)


settings = Settings()


def get_logging_config(app_name: str):
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "main": {
                "format": "%(asctime)s.%(msecs)03d [%(levelname)8s] [%(module)s:%(funcName)s:%(lineno)d] %(message)s",
                "datefmt": "%d.%m.%Y %H:%M:%S%z",
            },
            "errors": {
                "format": "%(asctime)s.%(msecs)03d [%(levelname)8s] [%(module)s:%(funcName)s:%(lineno)d] %(message)s",
                "datefmt": "%d.%m.%Y %H:%M:%S%z",
            },
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "main",
                "stream": sys.stdout,
            },
            "stderr": {
                "class": "logging.StreamHandler",
                "level": "WARNING",
                "formatter": "errors",
                "stream": sys.stderr,
            },
            "file_info": {
                "()": RotatingFileHandler,
                "level": "INFO",
                "formatter": "main",
                "filename": f"logs/{app_name}.log",
                "maxBytes": 5000000,
                "backupCount": 3,
                "encoding": "utf-8",
            },
            "file_debug": {
                "()": RotatingFileHandler,
                "level": "DEBUG",
                "formatter": "main",
                "filename": f"logs/{app_name}_debug.log",
                "maxBytes": 5000000,
                "backupCount": 3,
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "root": {
                "level": "DEBUG",
                "handlers": ["stdout", "stderr", "file_info", "file_debug"],
            },
        },
    }
