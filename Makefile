port = 8000
host = 0.0.0.0

.PHONY: api

api:
	uvicorn app.web.main:app --port $(port) --host $(host)
