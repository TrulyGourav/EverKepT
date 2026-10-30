.PHONY: install check test up down run

install:
	uv sync --extra dev

check:
	uv run ruff check . && uv run ruff format --check . && uv run mypy

test:
	uv run pytest

up:
	docker compose up -d

down:
	docker compose down

run:
	uv run uvicorn everkept.api:create_app --factory --reload
