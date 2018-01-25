FROM python:2.7-alpine
COPY requirements.txt /requirements.txt

COPY . /app/
WORKDIR /app/

ENV DJANGO_SETTINGS_MODULE=statuspage.settings
ENV UWSGI_WSGI_FILE=statuspage/wsgi.py UWSGI_MASTER=1 UWSGI_WORKERS=2 UWSGI_THREADS=8 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add \
gcc make libc-dev musl-dev linux-headers pcre-dev build-base gettext vim openssl-dev libffi-dev postgresql-client \
postgresql-dev jpeg-dev zlib-dev python python-dev py-openssl

RUN pip install -r /requirements.txt && pip install uwsgi

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN mkdir /db
ENV DATABASE_URL='sqlite:////db/statuspage.db'
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput
RUN echo "User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell_plus
RUN python manage.py loaddata initial_data

EXPOSE 8000

CMD uwsgi --http 0.0.0.0:8000

# Start uWSGI
#CMD ["gunicorn", "mspdna.wsgi:application"]
#CMD ["uwsgi", "--http-auto-chunked" "--http-keepalive"]
