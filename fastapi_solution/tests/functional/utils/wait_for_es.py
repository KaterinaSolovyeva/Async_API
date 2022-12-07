import time

from elasticsearch import Elasticsearch
from tests.functional.settings import test_settings

if __name__ == '__main__':
    es_client = Elasticsearch(**test_settings.ELASTIC_DSN.dict())
    while True:
        if es_client.ping():
            break
        time.sleep(1)
