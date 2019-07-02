#!/usr/bin/env bash

echo "Waiting for database..."
until psql -h postgres -p 5432 -U postgres -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
echo "Connected to database."

#python3 manage.py migrate --noinput
#if [ $? -ne 0 ]; then
#    echo "Migration failed." >&2
#    exit 1
#fi

echo 'Creating admins'
cat admin_creator.py | ./manage.py shell

echo 'Trying to add initial data to the Database'
cat approved_words_adder.py | ./manage.py shell

exec gunicorn --env DJANGO_SETTINGS_MODULE=TahrirBackend.settings TahrirBackend.wsgi \
    --name tahrir-gunicorn \
    --bind 0.0.0.0:5555 \
    --workers 3 \
    --timeout 10 \
    --log-level=info \
    --graceful-timeout 15 \
    --reload
