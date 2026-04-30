import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status, Request

from users.dependencies.usecases import (
    get_create_user_usecase,
    get_delete_user_usecase,
    get_get_user_usecase,
    get_list_users_usecase,
    get_update_user_usecase,
)
from users.domain.exceptions import EmailAlreadyTaken, UserNotFound
from users.schemas.users import UserCreate, UserResponse, UserUpdate
from users.usecase.users.create_user import CreateUserUsecase
from users.usecase.users.delete_user import DeleteUserUsecase
from users.usecase.users.get_user import GetUserUsecase
from users.usecase.users.list_users import ListUsersUsecase
from users.usecase.users.update_user import UpdateUserUsecase

users_v1_router = APIRouter(prefix="/users/v1", tags=["users"])


@users_v1_router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    data: UserCreate,
    usecase: CreateUserUsecase = Depends(get_create_user_usecase),
) -> UserResponse:
    try:
        return await usecase.execute(data)
    except EmailAlreadyTaken as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@users_v1_router.get(
    "/users",
    response_model=list[UserResponse],
)
async def list_users(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    usecase: ListUsersUsecase = Depends(get_list_users_usecase),
) -> list[UserResponse]:
    return await usecase.execute(limit=limit, offset=offset)


@users_v1_router.get(
    "/users/{user_id}",
    response_model=UserResponse,
)
async def get_user(
    user_id: uuid.UUID,
    usecase: GetUserUsecase = Depends(get_get_user_usecase),
) -> UserResponse:
    try:
        return await usecase.execute(user_id)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@users_v1_router.patch(
    "/users/{user_id}",
    response_model=UserResponse,
)
async def update_user(
    user_id: uuid.UUID,
    data: UserUpdate,
    usecase: UpdateUserUsecase = Depends(get_update_user_usecase),
) -> UserResponse:
    try:
        return await usecase.execute(user_id, data)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except EmailAlreadyTaken as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@users_v1_router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: uuid.UUID,
    usecase: DeleteUserUsecase = Depends(get_delete_user_usecase),
) -> None:
    try:
        await usecase.execute(user_id)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
