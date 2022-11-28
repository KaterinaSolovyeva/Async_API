from elasticsearch import AsyncElasticsearch

from app.core.config import settings
from etl.helpers import backoff


@backoff(border_sleep_time=15)
async def get_es_connection():
    """Функция для установления соединения с es"""
    return AsyncElasticsearch(
        hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}']
    )
