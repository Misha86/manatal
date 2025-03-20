# Makefile

# Define variables
MAIN_PATH = src.main

# Define targets
.PHONY: run migrate makemigrations

# Run local server
run:
	uvicorn ${MAIN_PATH}:app --host 0.0.0.0 --port 8000 --reload

migrate:
	alembic upgrade head

makemigrations:
	alembic revision --autogenerate -m '$(name)'