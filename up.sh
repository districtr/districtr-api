#!/bin/sh
set -e

# Do the database migration. We do a retry loop in case we failed due to
# the database not being ready.
while true; do
    pipenv run flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo "Upgrade command failed, retrying in 5 secs..."
    sleep 5
done

exec pipenv run gunicorn -b :3000 --access-logfile - --error-logfile - "api:create_app()"