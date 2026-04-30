import os

from testcontainers.postgres import PostgresContainer

class PostgresContainerHelper:
    def __init__(self, container: PostgresContainer) -> None:
        self.container = container

    def get_connection_url(self) -> str:
        url = self.container.get_connection_url()
        return url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")

    def prepare_env(self):
        url = self.get_connection_url()

        os.environ["DB_HOST"] = self.container.get_container_host_ip()
        os.environ["DB_PORT"] = str(self.container.get_exposed_port(
            self.container.port
        ))
        os.environ["DB_NAME"] = self.container.dbname
        os.environ["DB_USER"] = self.container.username
        os.environ["DB_PASSWORD"] = self.container.password

        os.environ["DB_URL"] = url