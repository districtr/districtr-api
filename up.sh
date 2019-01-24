#!/bin/sh
set -e

pipenv run flask db upgrade

exec pipenv run gunicorn -b :5000 --access-logfile - --error-logfile - "api:create_app()"