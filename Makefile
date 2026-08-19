DC := docker compose
# ── Help ──────────────────────────────────────────────────────────────────────

.PHONY: help
help:
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "  make app <app_name>                 Create a new FastAPI app"
	@echo "  make revision \"message\"              Generate Alembic migration"
	@echo "  make migrate                         Apply migrations"
	@echo "  make downgrade                       Rollback last migration"
	@echo "  make current                         Show current migration"
	@echo "  make history                         Show migration history"
	@echo ""
	@echo "Docker:"
	@echo "  make build                           Build Docker images"
	@echo "  make up                              Start containers"
	@echo "  make down                            Stop containers"
	@echo "  make restart                         Restart containers"
	@echo "  make logs                            Follow container logs"
	@echo "Management Command:"
	@echo "  make permission                      Create permissions and category"
	@echo "  make flush                           Flush all data"
	@echo "  make superuser                       Create superuser"
	@echo ""

# ── apps ───────────────────────────────────────────────────────────────
.PHONY: app
app:
	@if [ -z "$(word 2,$(MAKECMDGOALS))" ]; then \
		echo "Usage: make app <app_name>"; \
		exit 1; \
	fi
	@mkdir -p apps/$(word 2,$(MAKECMDGOALS))
	@touch apps/$(word 2,$(MAKECMDGOALS))/__init__.py
	@touch apps/$(word 2,$(MAKECMDGOALS))/models.py
	@touch apps/$(word 2,$(MAKECMDGOALS))/schemas.py
	@touch apps/$(word 2,$(MAKECMDGOALS))/route.py
	@touch apps/$(word 2,$(MAKECMDGOALS))/utils.py
	@echo "Created FastAPI app: apps/$(word 2,$(MAKECMDGOALS))"


# ── Alembic ───────────────────────────────────────────────────────────────────

.PHONY: revision
revision:
	@if [ -z "$(word 2,$(MAKECMDGOALS))" ]; then \
		echo 'Usage: make revision "your message"'; \
		exit 1; \
	fi
	$(DC) exec web alembic revision --autogenerate -m "$(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))"

.PHONY: migrate
migrate:
	$(DC) exec web alembic upgrade head


# ── Docker ────────────────────────────────────────────────────────────────────

.PHONY: logs
logs:
	$(DC) logs -f


.PHONY: build
build:
	$(DC) build


.PHONY: up
up:
	$(DC) up -d


.PHONY: down
down:
	$(DC) down

.PHONY: remove
remove:
	$(DC) down -v


.PHONY: restart
restart:
	$(DC) restart

# ───────────────── Management command-------------------------
.PHONY: permission
permission:
	$(DC) exec web python manage.py seed_permissions


.PHONY: flush
flush:
	$(DC) exec web python manage.py flush_data


.PHONY: superuser
superuser:
	$(DC) exec web python manage.py createsuperuser

# ── Positional Arguments ──────────────────────────────────────────────────────

%:
	@: