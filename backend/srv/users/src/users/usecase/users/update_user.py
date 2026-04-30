import uuid

from users.domain.exceptions import EmailAlreadyTaken, UserNotFound
from users.schemas.users import UserResponse, UserUpdate
from users.usecase.unit_of_work import AbstractUnitOfWork


class UpdateUserUsecase:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(self, user_id: uuid.UUID, data: UserUpdate) -> UserResponse:
        async with self.uow as uow:
            user = await uow.users_repo.get(user_id)
            if user is None:
                raise UserNotFound(f"User {user_id} not found")

            if data.email is not None and data.email != user.email:
                conflict = await uow.users_repo.get_by_email(data.email)
                if conflict is not None:
                    raise EmailAlreadyTaken(f"Email {data.email} is already taken")

            user.update(
                name=data.name,
                email=data.email,
                birth_date=data.birth_date,
                role=data.role,
            )
            await uow.commit()
            return UserResponse.from_domain(user)
