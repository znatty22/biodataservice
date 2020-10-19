#! /bin/sh

# Web container entrypoint

set -e

until PGPASSWORD=$PG_PASS psql -h "$PG_HOST" -U "$PG_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

/app/manage.py makemigrations
/app/manage.py migrate
exec /app/manage.py runserver 0.0.0.0:8000
