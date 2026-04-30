from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from events.dependencies.users_usecase import get_signup_user_usecase
from events.schemas.users import SignupUser, UserResponse
from events.usecase.users.create_user import SignupUserUsecase

users_v1_router = APIRouter(prefix="/users/v1", tags=['users'])

@users_v1_router.post("/users",
                    response_model=UserResponse,
                    status_code=201)
async def create_user(
        user_data: SignupUser,
        signup_user_usecase: SignupUserUsecase = Depends(get_signup_user_usecase)) -> UserResponse | JSONResponse:
    try:
        res = await signup_user_usecase.execute(user_data)
        return res
    except ValueError as e:
        return JSONResponse(content={"msg": str(e)}, status_code=400)