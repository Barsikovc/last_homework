#!/bin/bash
set -e

echo "Применяем миграции..."
python manage.py migrate --noinput

echo "Запускаем сервер..."
exec "$@"
