FROM python:2.7-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /project

WORKDIR /project
ADD . /project

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev build-essential gdal-bin netcat \
    && pip install --no-cache-dir -r /project/REQUIREMENTS-dev.txt \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /project/static && python manage.py collectstatic -c --noinput
