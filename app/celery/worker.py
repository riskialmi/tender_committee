from celery import Celery
from app.system.config import BACKEND_CONN_URI, BROKER_CONN_URI


app = Celery('BRE-V1',
             broker=BROKER_CONN_URI,
             backend=BACKEND_CONN_URI,
             include=['app.celery.tasks'])

app.conf.update(
    result_expires=3600,
)
