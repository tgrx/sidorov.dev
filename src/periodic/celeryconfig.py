from multiprocessing import cpu_count
from os import getenv

from dynaconf import settings

_broker_url = settings.CELERY_BROKER_URL
_workers = cpu_count() * 2 + 1

if settings.ENV_FOR_DYNACONF == "heroku":
    _workers = int(getenv("WEB_CONCURRENCY", "2"))
    _broker_url = getenv("REDIS_URL")

_workers = 1

broker_url = _broker_url
imports = ["periodic.tasks"]
redbeat_redis_url = _broker_url
result_backend = _broker_url
result_persistent = False
worker_concurrency = _workers
