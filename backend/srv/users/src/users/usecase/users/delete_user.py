import uuid

from users.domain.exceptions import UserNotFound
from users.usecase.unit_of_work import AbstractUnitOfWork


class DeleteUserUsecase:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(self, user_id: uuid.UUID) -> None:
        async with self.uow as uow:
            deleted = await uow.users_repo.delete(user_id)
            if not deleted:
                raise UserNotFound(f"User {user_id} not found")
            await uow.commit()
