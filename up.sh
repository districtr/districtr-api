#!/bin/sh
set -e

# Try to do database migrations, with a longer and longer timeout for each
# time we fail.
retries=0
timeout=10
until [ $retries -ge 10 ]
do
    pipenv run flask db upgrade && break
    retries=$[$retries+1]
    sleep $timeout
    timeout=$[$timeout*2]
done

pipenv run flask roles add admin --email max.hully@gmail.com

exec pipenv run gunicorn -b :5000 -w 4 --access-logfile - --error-logfile - "api:create_app()"