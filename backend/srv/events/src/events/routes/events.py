import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from events.dependencies.usecases import get_create_event_usecase, get_signup_to_event_usecase, get_get_event_usecase, \
    get_list_user_events_usecase
from events.domain.exceptions import EventError, UserCantCreateEvents, UserDoesntExist, EventTimeConflictError
from events.schemas.events import EventCreate, EventResponse, EventSignupRequestSchema
from events.usecase.create_event import CreateEventUsecase
from events.usecase.get_event import GetEventUsecase
from events.usecase.list_user_events import ListUserEventsUsecase
from events.usecase.signup_to_event import SignupToEventUsecase

events_v1_router = APIRouter(prefix="/events/v1", tags=["events"])

@events_v1_router.post("/events",
                    response_model=EventResponse,
                    status_code=201)
async def create_event(
        user_id: uuid.UUID,
        event: EventCreate,
        create_event_usecase: CreateEventUsecase = Depends(get_create_event_usecase)) -> EventResponse | JSONResponse:
    try:
        res = await create_event_usecase.execute(event, user_id)
        return res

    except UserDoesntExist:
        return JSONResponse(content={"msg": "Bad Request"}, status_code=400)
    except EventTimeConflictError:
        return JSONResponse(content={"msg": "You already have events which is overlapped"}, status_code=400)
    except UserCantCreateEvents:
        return JSONResponse(content={"msg": "Your status doesn't allow create events"}, status_code=400)



@events_v1_router.post("/events/{event_id}",
                    response_model=EventResponse,
                    responses={400: {"msg": "error message"}},
                    status_code=201)
async def signup_to_event(
        event_id: int,
        signup_request: EventSignupRequestSchema,
        signup_to_event_usecase: SignupToEventUsecase = Depends(get_signup_to_event_usecase)) -> EventResponse | JSONResponse:
    try:
        res = await signup_to_event_usecase.execute(event_id, signup_request)
        return res
    except EventError as e:
        return JSONResponse(content={"msg": e.message}, status_code=400)


@events_v1_router.get("/events/{event_id}",
                    response_model=EventResponse,
                    status_code=200)
async def get_event(
        event_id: int,
        get_event_usecase: GetEventUsecase = Depends(get_get_event_usecase)) -> EventResponse:
    return await get_event_usecase.execute(event_id)


@events_v1_router.get('/events')
async def list_my_events(
        user_id: int,
        list_user_events_usecase: ListUserEventsUsecase = Depends(get_list_user_events_usecase)
        ) -> list[EventResponse]:
    return await list_user_events_usecase.execute(user_id)
