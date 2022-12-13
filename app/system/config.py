import os
from starlette.config import Config
from starlette.datastructures import Secret

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_CELERY_DB_INDEX = os.environ.get('REDIS_CELERY_DB_INDEX')
REDIS_STORE_DB_INDEX = os.environ.get('REDIS_STORE_DB_INDEX')

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
RABBITMQ_USERNAME = os.environ.get('RABBITMQ_USERNAME')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT')

BROKER_CONN_URI = f"amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}"
BACKEND_CONN_URI = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB_INDEX}"

REDIS_STORE_CONN_URI = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_STORE_DB_INDEX}"

config = Config("/usr/src/app/.env")

POSTGRES_USER = config("POSTGRES_USER", cast=str, default='POSTGRES_USER')
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret, default='POSTGRES_PASSWORD')
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="POSTGRES_SERVER", )
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str, default="POSTGRES_DB")
DATABASE_URL = config(
    "DATABASE_URL",
    cast=str,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

URL_EMPLOYEE_BY_USERNAME = config("URL_EMPLOYEE_BY_USERNAME", cast=str, default="URL_EMPLOYEE_BY_USERNAME")

ALGORITHM = config('ALGORITHM', cast=str, default='')
SECRET_KEY = config('SECRET_KEY_JWT', cast=str, default='')
EMAIL_ADMIN = config('EMAIL_ADMIN', cast=str, default='').split(',')

SMTP_SERVER = config('SMTP_SERVER', cast=str, default='')
EMAIL_PORT = config('EMAIL_PORT', cast=int, default='9000')
SENDER_EMAIL = config('SENDER_EMAIL', cast=str, default='')
EMAIL_PASSWORD = config('EMAIL_PASSWORD', cast=str, default='')

URL_WORKFLOW = config('URL_WORKFLOW', cast=str, default='')
