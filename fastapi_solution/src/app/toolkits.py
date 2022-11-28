import uuid
from abc import ABC, abstractmethod
from typing import Type, Optional, Union

from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel

from app.serializers.query_params_classes import PaginationDataParams


class BaseToolkit(ABC):
    """Базовый тулкит для реализации базовых REST методов"""

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    @property
    @abstractmethod
    def entity_name(self) -> str:
        """Имя сущности, над которой будет работать тулкит"""
        pass

    @property
    @abstractmethod
    def pk_field_name(self) -> str:
        """Наименование ключевого атрибута сущности"""
        pass

    @property
    @abstractmethod
    def entity_model(self) -> Type[BaseModel]:
        """Модель сущности"""
        pass

    @property
    @abstractmethod
    def exc_does_not_exist(self) -> Exception:
        """Класс исключения, вызываемый при ошибке поиска экземпляра модели в get"""
        pass

    async def list(self, pagination_data: PaginationDataParams, body: Optional[dict] = None):
        if (sort := pagination_data.sort) and sort.startswith('-'):
            sort = sort.lstrip('-')+':desc'
        data = await self.elastic.search(
            index=self.entity_name,
            body=body,
            params={
                'size': pagination_data.page_size,
                'from': pagination_data.page - 1,
                'sort': sort
            }
        )
        return [self.entity_model(uuid=doc['_id'], **doc['_source']) for doc in data['hits']['hits']]

    async def get(self, pk: Union[str, uuid.UUID]):
        try:
            doc = await self.elastic.get(self.entity_name, pk)
        except NotFoundError:
            raise self.exc_does_not_exist
        return self.entity_model(uuid=doc['_id'], **doc['_source'])