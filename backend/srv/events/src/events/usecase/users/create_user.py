
from events.domain.users.users import User
from events.schemas.users import SignupUser, UserResponse
from events.usecase.unit_of_work import AbstractUnitOfWork


class SignupUserUsecase:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow


    async def execute(self, signup_user: SignupUser) -> UserResponse:
        event = User.create_user(**signup_user.model_dump())
        async with self.uow as uow:
            event = await uow.users_repo.add(event)
            await uow.commit()
            print("User id", event.id)
        print("User id", event.id)
        return UserResponse.from_domain(event)