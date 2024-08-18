#!/bin/sh

if [ "$DATABASE"="postgres" ]
then
    echo "Check id db is running..."

    while !nc -z $SQL_HOST "SQL_PORT"; do
      sleep 0.1
    done

    echo "The db is up and running!"
fi

python manage.py makemigrations
python manage.py migrate
exec "$@"