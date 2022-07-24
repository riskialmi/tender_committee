import redis

from .worker import app
from app.system.config import REDIS_STORE_CONN_URI

redis_store = redis.Redis.from_url(REDIS_STORE_CONN_URI)


