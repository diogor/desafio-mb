port = 8000
host = 0.0.0.0

.PHONY: run

run:
	granian --interface asgi app.web.main:app --port $(port) --host $(host)
