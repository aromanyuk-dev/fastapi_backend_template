from users.schemas.users import UserResponse
from users.usecase.unit_of_work import AbstractUnitOfWork


class ListUsersUsecase:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(self, limit: int, offset: int) -> list[UserResponse]:
        async with self.uow as uow:
            users = await uow.users_repo.list(limit=limit, offset=offset)
            return [UserResponse.from_domain(u) for u in users]
