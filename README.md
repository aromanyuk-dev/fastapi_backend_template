# FastAPI Backend Template (Clean Architecture + DDD)

A microservice-ready FastAPI template. Ships with a single `users` service implementing a CRUD + list endpoint, ready to be cloned/renamed for new domains.

## Layout

```
backend/srv/users/         # service package (rename per service)
  src/users/
    domain/                # entities, value objects, domain rules
      users/user.py
      user_role.py
      exceptions.py
    usecase/               # application services (use-case classes)
      unit_of_work.py
      users/
        create_user.py
        get_user.py
        update_user.py
        delete_user.py
        list_users.py
    adapters/              # infra: SQLAlchemy ORM + repositories
      orm.py
      user_repo.py
    schemas/               # FastAPI/Pydantic DTOs
      users.py
    routes/                # HTTP layer
      users.py
    dependencies/          # FastAPI DI wiring
      session.py
      unit_of_work.py
      usecases.py
    config/config.py
    main.py
  migrations/              # Alembic
  tests/
deployment/
  Dockerfile               # multi-stage: builder / development / production
  local/docker-compose.yaml
```

## Run locally

```bash
make up-build            # build image, start db + users service
curl localhost:8000/healthcheck
make logs-users
make down
```

## Endpoints

| Method | Path                       | Description    |
|--------|----------------------------|----------------|
| GET    | `/healthcheck`             | health         |
| POST   | `/users/v1/users`          | create user    |
| GET    | `/users/v1/users`          | list users     |
| GET    | `/users/v1/users/{id}`     | get user       |
| PATCH  | `/users/v1/users/{id}`     | update user    |
| DELETE | `/users/v1/users/{id}`     | delete user    |

## Using as a template for a new service

1. Copy `backend/srv/users` to `backend/srv/<your-service>`.
2. Rename the inner `src/users` package to `src/<your-service>` and update imports.
3. Update `pyproject.toml` (`name`, `tool.poetry.packages`).
4. Replace the User domain/usecases/schemas/routes with your own.
5. Add a service entry to `deployment/local/docker-compose.yaml`.
