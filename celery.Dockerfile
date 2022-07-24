FROM python:3.8-slim-buster

COPY ./app/celery /usr/src/app/celery

COPY ./app/__init__.py /usr/src/app/

COPY ./app/system/config.py /usr/src/app/system/

COPY ./app/.env /usr/src/app/

COPY ./requirements-celery.txt /usr/src/

RUN pip3 install --upgrade pip \
    && pip3 install -r /usr/src/requirements-celery.txt \
    && addgroup --system celery && adduser --system --group celery

USER celery

WORKDIR /usr/src

CMD celery -A app.celery.worker.app worker --loglevel=INFO -E
