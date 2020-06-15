#!/bin/sh

if [ "$DJANGO_DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DJANGO_SQL_HOST $DJANGO_SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

mkdir -p staticfiles
mkdir -p static
python manage.py collectstatic --no-input
python manage.py makemigrations --no-input
python manage.py migrate --no-input
# Create superuser 
./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('$DJANGO_SUPER_USER', 'admin@example.com', '$DJANGO_SUPER_USER_PASS')"

exec "$@"