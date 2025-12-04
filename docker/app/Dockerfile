ARG UV_VERSION=0.9.15
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv_cli

# ARG PYTHON_VERSION=3.12-slim-trixie
# FROM python:${PYTHON_VERSION}
FROM python:3.12-slim-trixie

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential pkg-config default-libmysqlclient-dev libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=uv_cli /uv /uvx /bin/

# 3. FIX: Create the user (This was missing!)
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# 4. ENV setup
ENV PYTHONPATH="${PYTHONPATH}:/app/app"
ENV UV_CACHE_DIR=/app/.cache/uv

# 5. FIX: Optimized Caching & Permissions
# First, copy ONLY dependency files
COPY pyproject.toml uv.lock ./

# Give ownership to appuser BEFORE syncing
RUN mkdir -p /app/.cache/uv && chown -R appuser:appuser /app

USER appuser

COPY --chown=appuser:appuser . /app

RUN uv sync --locked --no-dev
COPY --chown=appuser:appuser docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]