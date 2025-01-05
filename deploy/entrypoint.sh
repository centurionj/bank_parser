#!/bin/sh

cmd="$@"

# the official postgres image uses 'postgres' as default user if not set explicitly.
if [ -z "$POSTGRES_USER" ]; then
    export POSTGRES_USER=postgres
fi

postgres_ready() {
python << END
import os
import sys

import psycopg2

try:
    conn = psycopg2.connect(
        dbname=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        port=os.environ['POSTGRES_PORT'],
        host=os.environ['POSTGRES_HOST'],
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres ${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB} is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."

export PYTHONPATH=${PYTHONPATH}:${PROJECT_ROOT}

echo Run command ${cmd}
exec ${cmd}