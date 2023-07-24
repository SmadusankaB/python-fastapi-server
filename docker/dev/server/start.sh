#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# alembic upgrade head
# gunicorn project.asgi:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --chdir=/app
# python3 -m project.swagi.app

# uvicorn server.main:app --reload --reload-dir server  --host 0.0.0.0 --port 8080
uvicorn server.main:app --host 0.0.0.0 --port 8080