
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from events.routes.events import events_v1_router
from events.routes.users import users_v1_router

from migrate import run_migrations


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield


app = FastAPI(lifespan=lifespan)

v1_api_router = APIRouter(prefix="")

@v1_api_router.get("/healthcheck")
def read_root():
    return {"message": "ok"}


v1_api_router.include_router(events_v1_router)
v1_api_router.include_router(users_v1_router)
app.include_router(v1_api_router)
