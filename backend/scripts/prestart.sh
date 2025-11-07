#! /usr/bin/env bash

set -e
set -x

# Let the DB start
uv run python -m app.backend_pre_start

# Run migrations
uv run alembic upgrade head

# Create initial data in DB
uv run python -m app.initial_data
