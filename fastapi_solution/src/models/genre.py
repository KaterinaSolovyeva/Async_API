from pydantic import Field
from models.mixin import BaseMixin


class Genre(BaseMixin):
    """Genres in the list."""
    uuid: str
    name: str


class ESFilmGenre(BaseMixin):
    """Genre from ElasticSearch"""
    uuid: str = Field(..., alias='id')
    name: str
