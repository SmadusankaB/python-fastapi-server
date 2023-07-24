#!/bin/bash

set -o errexit
set -o nounset
exec celery -A server.celery:celery_app worker --loglevel=${LOG_LEVEL}