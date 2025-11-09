#! /usr/bin/env bash
set -e
set -x

uv run python -m app.fake_initial_data
