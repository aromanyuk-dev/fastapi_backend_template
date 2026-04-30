from events.dependencies.session import async_session
from events.usecase.unit_of_work import SQLAlchemyUnitOfWork


def get_sqlalchemy_uow():
    return SQLAlchemyUnitOfWork(async_session)