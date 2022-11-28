from typing import Tuple, Generator

from etl_service.etl.data_structures.entities_meta import EntityMeta
from etl_service.etl.storage import State, RedisStorage
from etl_service.etl.postgres_extractor import PostgresExtractor


class Transformator:
    """Формирует тело для bulk запроса в elasticsearch"""
    def __init__(self, data_size: int = 1000):
        self.state = State(storage=RedisStorage)
        self.data_size = data_size

    async def transform_data(self, entity_meta: EntityMeta) -> Generator[Tuple[list, str], None, None]:
        last_modified = self.state.get_state(f"{entity_meta.index_data['index']}_last_modified")
        kwargs = {'last_modified': last_modified} if last_modified is not None else {}
        actions = list()
        modified = None

        async for data in PostgresExtractor(query=entity_meta.sql_query).get_data(**kwargs):
            data = data._asdict()
            modified = data.pop('modified')
            action = {"index": {"_index": entity_meta.index_data['index'], "_id": data["id"]}}
            doc = data
            actions.append(action)
            actions.append(doc)
            if len(actions) == self.data_size * 2:  # Т.к. мы записывает действие и дату =>
                # данных в списке в 2 раза больше
                yield actions, modified
                actions = list()
        if actions:
            yield actions, modified
