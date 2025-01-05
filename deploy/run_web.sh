#!/bin/sh

# Применение миграций Django
echo "Applying database migrations..."
if ! python src/manage.py migrate; then
    echo "Django migrations failed. Exiting."
    exit 1
fi
echo "Migrations applied successfully."

# Применяем фикстуры users
echo "Applying users fixtures..."
if ! python src/manage.py loaddata "src/server/fixtures/users_fixture.json"; then
    echo "User fixtures failed. Exiting."
    exit 1
fi
echo "User fixtures applied successfully."

# Сбор статики
echo "Collecting static..."
if ! python src/manage.py collectstatic --noinput; then
    echo "Collecting static failed. Exiting."
    exit 1
fi
echo "Collecting static successfully."

# Запуск Gunicorn с exec для передачи сигналов
exec gunicorn -c deploy/gunicorn.conf.py src.server.wsgi:application
