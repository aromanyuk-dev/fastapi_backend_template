COMPOSE_FILE := deployment/local/docker-compose.yaml
COMPOSE      := docker compose -f $(COMPOSE_FILE)

.PHONY: help up up-build down stop restart build rebuild logs-users logs-db ps

help:
	@echo "Available targets:"
	@echo "  make up           - start all containers in background"
	@echo "  make up-build     - build and start all containers in background"
	@echo "  make down         - stop and remove containers, networks"
	@echo "  make stop         - stop containers without removing them"
	@echo "  make restart      - restart all containers"
	@echo "  make build        - build images"
	@echo "  make rebuild      - rebuild images without cache and restart"
	@echo "  make logs-users   - tail logs from users (app) service"
	@echo "  make logs-db      - tail logs from db service"
	@echo "  make ps           - list running containers"

up:
	$(COMPOSE) up -d

up-build:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

stop:
	$(COMPOSE) stop


restart:
	$(COMPOSE) restart

build:
	$(COMPOSE) build

rebuild:
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d

logs-users:
	$(COMPOSE) logs -f --tail=200 users

logs-db:
	$(COMPOSE) logs -f --tail=200 db

ps:
	$(COMPOSE) ps
