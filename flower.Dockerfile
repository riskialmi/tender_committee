FROM python:3.8-slim-buster

COPY ./app/celery /usr/src/app/celery

COPY ./app/__init__.py /usr/src/app/

COPY ./app/system/config.py /usr/src/app/system/

COPY ./app/.env /usr/src/app/

COPY ./requirements-celery.txt /usr/src/

RUN apt-get update \
    && apt-get install -y curl \
    && pip3 install --upgrade pip \
    && pip3 install -r /usr/src/requirements-celery.txt \
    && pip3 install flower \
    && addgroup --system flower && adduser --system --group flower

USER flower

WORKDIR /usr/src

CMD celery -A app.celery.tasks --broker=amqp://${RABBITMQ_USERNAME}:${RABBITMQ_PASSWORD}@${RABBITMQ_HOST}:${RABBITMQ_PORT}// flower --port=5566