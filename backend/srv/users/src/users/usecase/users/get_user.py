import uuid

from users.domain.exceptions import UserNotFound
from users.schemas.users import UserResponse
from users.usecase.unit_of_work import AbstractUnitOfWork


class GetUserUsecase:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(self, user_id: uuid.UUID) -> UserResponse:
        async with self.uow as uow:
            user = await uow.users_repo.get(user_id)
            if user is None:
                raise UserNotFound(f"User {user_id} not found")
            return UserResponse.from_domain(user)
