import os
import sys

from redis import Redis
from helpers import backoff

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from settings import test_settings  # noqa


@backoff()
def wait_for_redis():
    redis_db = Redis(**test_settings.REDIS_DSN.dict())
    if not redis_db.ping():
        raise Exception


if __name__ == '__main__':
    wait_for_redis()
