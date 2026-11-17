# Deploy and Host FastAPI on Railway

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template/fastapi-starter?referralCode=sLjDXb&utm_medium=integration&utm_source=button&utm_campaign=fastapi-starter)

A current [FastAPI](https://fastapi.tiangolo.com) starter for Python APIs, live on its own Railway domain a minute after you click deploy. It runs on Uvicorn and comes with interactive docs at `/docs`, a `/health` route Railway checks before every switch-over, an example CRUD router with Pydantic models, settings from variables, JSON logs and a pytest suite. Eject it and the repo is yours.

## About Hosting FastAPI

FastAPI is a Python web framework for building APIs with type hints: request bodies, query parameters and responses are validated by Pydantic, and the OpenAPI schema and docs pages are generated from your code.

- One small service, no database, no required variables: it boots on the 0.5 GB plan with room to spare.
- Railway builds it from the `Dockerfile` (Python 3.13 slim), runs it as a non-root user, and only routes traffic to a new deploy once `/health` answers.
- A typo in a variable (`LOG_LEVEL=loud`, `WEB_CONCURRENCY=two`) logs a warning and falls back to the default instead of crashing the deploy.

## Common Use Cases

- A backend API for a web or mobile app
- A webhook receiver or integration service
- An API in front of an AI model, a database or a scraper
- Learning FastAPI with a working deploy from minute one

## Dependencies for FastAPI Hosting

- Nothing to set up first. Every variable has a working default.

### Deployment Dependencies

- [FastAPI documentation](https://fastapi.tiangolo.com)
- [Uvicorn](https://uvicorn.dev)
- [Pydantic](https://docs.pydantic.dev)

### Implementation Details

**First use:** open the service's domain. `/` says it is running, `/docs` is the interactive Swagger UI (try `POST /items` there) and `/redoc` is the reference view.

**Project layout:**

| Path | What it is |
| --- | --- |
| `app/main.py` | The app: middleware, `/` and `/health`, router includes |
| `app/routers/items.py` | Example resource with Pydantic models; copy it for your own |
| `app/config.py` | Settings read from variables, with safe defaults |
| `app/log_config.py` | JSON log lines (Railway filters on `level`, `path`, `status`, `ms`) |
| `tests/` | pytest suite using FastAPI's `TestClient` |
| `Dockerfile` | Build steps; FastAPI and Uvicorn versions are pinned here |
| `start.sh` | Start command: host, port and worker count |

**Make it yours:** eject the template in the service's settings to get your own copy of the repo. Add routers under `app/routers/`, include them in `app/main.py`, put new packages in `requirements.txt`, and push: every push redeploys.

**Run it locally:**

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload    # http://127.0.0.1:8000/docs
pytest
```

**Variables:**

| Variable | Default | What it does |
| --- | --- | --- |
| `APP_NAME` | `FastAPI` | Title in `/docs` and in `/` |
| `LOG_LEVEL` | `INFO` | `DEBUG` to `CRITICAL` |
| `CORS_ORIGINS` | empty | Comma-separated browser origins allowed to call the API, or `*` |
| `DOCS_ENABLED` | `true` | `false` hides `/docs`, `/redoc` and `/openapi.json` |
| `WEB_CONCURRENCY` | `1` | Uvicorn workers; raise it on plans with more memory |
| `HOST` | `0.0.0.0` | Set `::` in an older project whose private network is IPv6-only |

**Add a database:** add Railway's PostgreSQL to the project, reference `DATABASE_URL` in this service's variables, and open the connection pool in the `lifespan` function in `app/main.py`. Keep startup tolerant of a database that is still starting, or a crash there fails the deploy.

Notes and limits:

- The example items live in memory and are cleared on every redeploy.
- Keep `/health` fast and free of external calls: Railway waits up to 2 minutes for it on each deploy.

## Why Deploy FastAPI on Railway?

Railway is a singular platform to deploy your infrastructure stack. Railway will host your infrastructure so you don't have to deal with configuration, while allowing you to vertically and horizontally scale it.

By deploying FastAPI on Railway, you are one step closer to supporting a complete full-stack application with minimal burden. Host your servers, databases, AI agents, and more on Railway.
