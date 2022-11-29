from typing import Optional

from elasticsearch import AsyncElasticsearch

from app.core.config import settings
from etl_service.etl.helpers import backoff

es: Optional[AsyncElasticsearch] = None


@backoff(border_sleep_time=15)
async def get_es_connection():
    """Функция для установления соединения с es"""
    return AsyncElasticsearch(
        hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}']
    )
