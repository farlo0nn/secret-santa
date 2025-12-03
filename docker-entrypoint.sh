#!/bin/bash
set -e

# 1. Run Migrations
echo "Running Database Migrations..."
uv run alembic upgrade head

# 2. Start the Application
echo "Starting Application..."
exec uv run bot