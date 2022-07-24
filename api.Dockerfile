FROM python:3.8-slim-buster

COPY ./app /usr/src/app

copy ./test /usr/src/test

COPY ./requirements-api.txt /usr/src/

RUN apt-get update \
    && apt-get install -y curl \
    && pip3 install --upgrade pip \
    && pip3 install -r /usr/src/requirements-api.txt \
    && pip3 install api \
    && addgroup --system api && adduser --system --group api

USER api

WORKDIR /usr/src

CMD gunicorn --bind 0.0.0.0:5000 app.system.main:app -w 4 -k uvicorn.workers.UvicornWorker --access-logfile - --error-logfile - --log-level info
