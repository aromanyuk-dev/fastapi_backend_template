from users.dependencies.session import async_session
from users.usecase.unit_of_work import SQLAlchemyUnitOfWork


def get_sqlalchemy_uow() -> SQLAlchemyUnitOfWork:
    return SQLAlchemyUnitOfWork(async_session)
