from typing import Optional

from elasticsearch import AsyncElasticsearch

from app.core.config import settings

es: Optional[AsyncElasticsearch] = None


async def get_es_connection():
    """Функция для установления соединения с es"""
    return AsyncElasticsearch(
        hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}']
    )
