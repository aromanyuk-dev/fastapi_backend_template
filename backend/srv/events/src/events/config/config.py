from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: str = '5432'
    DB_NAME: str = 'db_name'
    DB_USER: str = 'db_user'
    DB_PASSWORD: str = 'db_pass'
    model_config = SettingsConfigDict(env_prefix="GWM_")


@lru_cache()
def get_settings():
    return AppSettings()