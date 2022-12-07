import time

from settings import test_settings
from tests.functional.settings import Redis

if __name__ == '__main__':
    redis_db = Redis(**test_settings.REDIS_DSN.dict())
    while True:
        if redis_db.ping():
            break
        time.sleep(1)
