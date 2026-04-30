from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "postgres"
    DB_USER: str = "user"
    DB_PASSWORD: str = "user"


@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()
