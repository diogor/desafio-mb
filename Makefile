include .env
export $(shell sed 's/=.*//' .env)

port = 8000
host = 0.0.0.0

.PHONY: api migrate migration

migrate:
	alembic upgrade head

migration:
	alembic revision --autogenerate -m "$(name)"

api:
	uvicorn app.web.main:app --port $(port) --host $(host)
