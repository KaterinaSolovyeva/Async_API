from typing import Type

from pydantic import BaseModel

from app.toolkits import BaseToolkit
from persons.models.person import Person, ESFilmPerson


class PersonsToolkit(BaseToolkit):
    @property
    def entity_name(self) -> str:
        """Имя сущности, над которой будет работать тулкит"""
        return 'persons'

    @property
    def pk_field_name(self) -> str:
        """Наименование ключевого атрибута сущности"""
        return 'id'

    @property
    def entity_model(self) -> Type[BaseModel]:
        """Модель сущности"""
        return Person

    @property
    def exc_does_not_exist(self) -> Exception:
        """Класс исключения, вызываемый при ошибке поиска экземпляра модели в get"""
        return Exception('Не удалось получить данные о человеке по указанным параметрам')
