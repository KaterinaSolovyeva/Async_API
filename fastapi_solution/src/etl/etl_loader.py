from elasticsearch import AsyncElasticsearch

from etl.transformators import Transformator
from app.core.config import settings
from etl.storage import State, JsonFileStorage
from etl.data_structures.entities_meta import entities_meta
from app.connections.elastic import get_es_connection


class ESLoader:
    def __init__(self, data_size: int = 1000):
        self.state = State(storage=JsonFileStorage(file_path=settings.STORAGE_FILE_PATH))
        self.data_size = data_size

    async def load_data(self, last_modified: str = None) -> None:
        """Устанавливает соединение с postgres и es и переносит данные из postgres в es"""
        es_connection: AsyncElasticsearch = await get_es_connection()
        for entity_meta in entities_meta:
            await self.create_index_if_not_exists(es=es_connection, index=entity_meta.index_data)
            if last_modified is not None:
                self.state.set_state(key=f'last_modified', value=last_modified)
            async for actions, modified in Transformator().transform_data(entity_meta=entity_meta):
                await es_connection.bulk(actions, index=entity_meta.index_data['index'])
                self.state.set_state(key='last_modified', value=str(modified))
        await es_connection.close()

    @staticmethod
    async def create_index_if_not_exists(es: AsyncElasticsearch, index: dict) -> None:
        index_name = index['index']
        if not await es.indices.exists(index=index_name):
            index_body = index['body']
            await es.indices.create(index=index_name, body=index_body)
