from users.domain.exceptions import EmailAlreadyTaken
from users.domain.users.user import User
from users.schemas.users import UserCreate, UserResponse
from users.usecase.unit_of_work import AbstractUnitOfWork


class CreateUserUsecase:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(self, data: UserCreate) -> UserResponse:
        async with self.uow as uow:
            existing = await uow.users_repo.get_by_email(data.email)
            if existing is not None:
                raise EmailAlreadyTaken(f"Email {data.email} is already taken")

            user = User.create(
                name=data.name,
                email=data.email,
                birth_date=data.birth_date,
                role=data.role,
            )
            user = await uow.users_repo.add(user)
            await uow.commit()
            return UserResponse.from_domain(user)
