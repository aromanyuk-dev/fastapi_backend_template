from typing import Generator

import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import clear_mappers

from events.adapters.orm import metadata, start_mappers
from testcontainers.postgres import PostgresContainer

from events.dependencies.unit_of_work import get_sqlalchemy_uow
from events.main import app
from events.usecase.unit_of_work import SQLAlchemyUnitOfWork
from tests.utils.pg_container_helper import PostgresContainerHelper
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text





@pytest.fixture(scope="session", name="postgres_container")
def fixture_postgres_container() -> Generator[PostgresContainer, None, None]:
    print('ZZZ')
    container = PostgresContainer("postgres:16-alpine")
    container.start()
    yield container
    container.stop()


@pytest.fixture(scope="session", name="postgres_container_helper")
def fixture_postgres_container_helper(
    postgres_container,
) -> PostgresContainerHelper:
    helper = PostgresContainerHelper(postgres_container)
    helper.prepare_env()
    return helper



@pytest.fixture(scope='function')
async def session(postgres_container_helper):
    url = postgres_container_helper.get_connection_url()

    engine = create_async_engine(url, future=True, echo=False)


    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    start_mappers()
    Session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with Session() as sess:
        yield sess

    clear_mappers()
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def async_engine(postgres_container_helper):

    url = postgres_container_helper.get_connection_url()
    engine = create_async_engine(url, future=True, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    start_mappers()
    yield engine
    clear_mappers()

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
def async_session_maker(async_engine):
    return async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

@pytest_asyncio.fixture(scope="function", loop_scope='session', autouse=True)
async def truncate_tables(async_engine):

    yield
    print("\n--- TRUNCATING ALL TABLES ---")
    async with async_engine.begin() as conn:
        tables = ", ".join(f'"{table.name}"' for table in reversed(metadata.sorted_tables))
        if tables:
            await conn.execute(text(f"TRUNCATE TABLE {tables} RESTART IDENTITY CASCADE;"))

@pytest_asyncio.fixture(scope='session', name='async_client')
async def async_client_fixture(async_session_maker):

    def override_get_sqlalchemy_uow():
        return SQLAlchemyUnitOfWork(async_session_maker)

    app.dependency_overrides[get_sqlalchemy_uow] = override_get_sqlalchemy_uow

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        yield client

    app.dependency_overrides.clear()