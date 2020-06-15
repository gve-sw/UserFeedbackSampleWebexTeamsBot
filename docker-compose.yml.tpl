---
    version: "2"
    services:
        db:
            image: postgres:12.0-alpine
            environment:
                - POSTGRES_USER=
                - POSTGRES_PASSWORD=
                - POSTGRES_DB=
            expose:
                - "5432"
        web:
            image: mneiding/evy_light:latest
            command: gunicorn evy_light.wsgi:application --bind 0.0.0.0:8000
            ports:
                - 80:8000
            environment:
                - DJANGO_SECRET_KEY=
                - DJANGO_DEBUG=0
                - DJANGO_ALLOWED_HOSTS=*
                - DJANGO_DATABASE=postgres
                - DJANGO_SQL_ENGINE=django.db.backends.postgresql
                - DJANGO_SQL_HOST=db
                - DJANGO_SQL_PORT=5432
                - DJANGO_SUPER_USER=
                - DJANGO_SUPER_USER_PASS=
                - POSTGRES_USER=
                - POSTGRES_PASSWORD=
                - POSTGRES_DB=
                - WEBEX_ACCESS_TOKEN=
            links:
                - db:db
        notifier:
            image: mneiding/evy_light:latest
            command: python3 manage.py schedule_tasks && python3 manage.py process_tasks
            environment:
                - DJANGO_SECRET_KEY=
                - DJANGO_DEBUG=0
                - DJANGO_ALLOWED_HOSTS=*
                - DJANGO_DATABASE=postgres
                - DJANGO_SQL_ENGINE=django.db.backends.postgresql
                - DJANGO_SQL_HOST=db
                - DJANGO_SQL_PORT=5432
                - DJANGO_SUPER_USER=
                - DJANGO_SUPER_USER_PASS=
                - POSTGRES_USER=
                - POSTGRES_PASSWORD=
                - POSTGRES_DB=
                - WEBEX_ACCESS_TOKEN=
            links:
                - db:db