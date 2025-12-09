ARG UV_VERSION=0.9.15
FROM --platform=linux/amd64 ghcr.io/astral-sh/uv:${UV_VERSION} AS uv_cli
FROM --platform=linux/amd64 python:3.12-slim-bookworm

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    build-essential pkg-config default-libmysqlclient-dev libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY --from=uv_cli /uv /uvx /bin/

RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app

ENV PYTHONPATH="${PYTHONPATH}:/app/app"
ENV UV_CACHE_DIR=/app/.cache/uv
ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./

RUN mkdir -p /app/.cache/uv && chown -R appuser:appuser /app
USER appuser


RUN uv sync --locked --no-install-project --no-dev

COPY --chown=appuser:appuser app /app/app
COPY --chown=appuser:appuser alembic /app/alembic
COPY --chown=appuser:appuser alembic.ini /app/alembic.ini
COPY --chown=appuser:appuser static_messages.json /app/static_messages.json

RUN uv sync --locked --no-dev
