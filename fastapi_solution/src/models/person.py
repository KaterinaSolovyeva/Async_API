from pydantic import Field

from app.models import BaseMixin


class Person(BaseMixin):
    """Person information in the list."""
    uuid: str = Field(..., alias='id')
    full_name: str = Field(..., alias='name')


class ESFilmPerson(BaseMixin):
    """Person from ElasticSearch."""
    uuid: str = Field(..., alias='id')
    full_name: str = Field(..., alias='name')
