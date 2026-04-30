import os

from alembic import command
from alembic.config import Config


from events.config.config import get_settings


def run_migrations():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    alembic_cfg.set_main_option("script_location", os.path.join(base_dir, "migrations"))


    settings = get_settings()
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    command.upgrade(alembic_cfg, "head")