from models.mixin import BaseMixin
from pydantic import Field


class Person(BaseMixin):
    """Person information in the list."""
    uuid: str
    full_name: str


class ESFilmPerson(BaseMixin):
    """Person from ElasticSearch."""
    uuid: str = Field(..., alias='id')
    full_name: str = Field(..., alias='name')
