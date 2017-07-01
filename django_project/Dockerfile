FROM python:2.7-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /project
WORKDIR /project

ADD REQUIREMENTS.txt /project/REQUIREMENTS.txt
ADD REQUIREMENTS-dev.txt /project/REQUIREMENTS-dev.txt

RUN echo http://nl.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories \
    && apk --no-cache add gdal libpq postgresql-dev build-base python-dev geos musl-dev linux-headers \
    && pip install --no-cache-dir -r /project/REQUIREMENTS-dev.txt \
    && apk --no-cache del postgresql-dev build-base python-dev musl-dev linux-headers

ADD . /project

RUN mkdir /project/static && python manage.py collectstatic -c --noinput
