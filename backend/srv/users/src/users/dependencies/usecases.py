from fastapi import Depends

from users.dependencies.unit_of_work import get_sqlalchemy_uow
from users.usecase.unit_of_work import AbstractUnitOfWork
from users.usecase.users.create_user import CreateUserUsecase
from users.usecase.users.delete_user import DeleteUserUsecase
from users.usecase.users.get_user import GetUserUsecase
from users.usecase.users.list_users import ListUsersUsecase
from users.usecase.users.update_user import UpdateUserUsecase


def get_create_user_usecase(
    uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow),
) -> CreateUserUsecase:
    return CreateUserUsecase(uow=uow)


def get_get_user_usecase(
    uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow),
) -> GetUserUsecase:
    return GetUserUsecase(uow=uow)


def get_update_user_usecase(
    uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow),
) -> UpdateUserUsecase:
    return UpdateUserUsecase(uow=uow)


def get_delete_user_usecase(
    uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow),
) -> DeleteUserUsecase:
    return DeleteUserUsecase(uow=uow)


def get_list_users_usecase(
    uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow),
) -> ListUsersUsecase:
    return ListUsersUsecase(uow=uow)
