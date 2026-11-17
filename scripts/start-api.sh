#!/bin/sh
# Container entrypoint for the API: bring the schema up to date, then serve.
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
