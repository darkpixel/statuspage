FROM docker.io/python:3.8.10-alpine

RUN mkdir /app/
WORKDIR /app/
ADD . /app/

ENV DJANGO_SETTINGS_MODULE=statuspage.settings
ENV UWSGI_WSGI_FILE=statuspage/wsgi.py UWSGI_MASTER=1 UWSGI_WORKERS=2 UWSGI_THREADS=8 UWSGI_UID=1000 UWSGI_GID=2000 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy
ENV PYTHONUNBUFFERED 1

RUN apk update; apk add python3-dev postgresql-dev libpq gcc libjpeg jpeg-dev zlib zlib-dev g++
RUN pip install -r /app/requirements.txt

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
#RUN DATABASE_URL='' python manage.py collectstatic --noinput

EXPOSE 5000

CMD ["uwsgi", "--http", ":5000", "--wsgi-file", "statuspage/wsgi.py"]
