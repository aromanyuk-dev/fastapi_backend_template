import asyncio
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from migrate import run_migrations
from users.adapters.orm import start_mappers
from users.routes.users import users_v1_router

start_mappers()


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield


app = FastAPI(lifespan=lifespan, title="Users service")

v1_api_router = APIRouter(prefix="")


@v1_api_router.get("/healthcheck")
def healthcheck():
    return {"message": "ok"}


v1_api_router.include_router(users_v1_router)
app.include_router(v1_api_router)
