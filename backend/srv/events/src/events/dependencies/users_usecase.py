from events.dependencies.unit_of_work import get_sqlalchemy_uow
from events.usecase.unit_of_work import AbstractUnitOfWork
from fastapi import Depends

from events.usecase.users.create_user import SignupUserUsecase


def get_signup_user_usecase(uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow)):
    return SignupUserUsecase(uow=uow)