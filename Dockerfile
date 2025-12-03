FROM python:3.12-slim-trixie

# 1. Install Build Deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential pkg-config default-libmysqlclient-dev libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Setup UV
COPY --from=ghcr.io/astral-sh/uv:0.9.15 /uv /uvx /bin/

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

# Switch to user NOW so uv sync creates files owned by appuser
USER appuser

# Install dependencies (This layer is now cached unless lockfile changes)


# 6. Copy the rest of the application code
# use --chown to ensure the new files belong to appuser
COPY --chown=appuser:appuser . /app

RUN uv sync --locked --no-dev

# 7. Setup Entrypoint
# (We need to switch back to root briefly to chmod if copying from Windows, 
# but usually --chown above handles ownership)
COPY --chown=appuser:appuser docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# 8. Define Entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]