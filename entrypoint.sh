#!/bin/sh

# Wait for the database to be available
while ! nc -z db 5432; do
  echo "Waiting for the database..."
  sleep 3
done

# Run Django migrations and start the server
python manage.py migrate
exec "$@"
