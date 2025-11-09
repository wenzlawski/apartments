#! /usr/bin/env bash
set -e
set -x

uv run python -m app.tests_pre_start

bash scripts/test.sh "$@"
