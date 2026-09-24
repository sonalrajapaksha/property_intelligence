.PHONY: up down test migrate seed
up:
	docker compose up --build
down:
	docker compose down
test:
	docker compose run --rm api pytest
	mkdir -p frontend/node_modules && cd frontend && npm test -- --run
migrate:
	docker compose run --rm api alembic upgrade head
seed:
	docker compose run --rm api python -m app.seed
