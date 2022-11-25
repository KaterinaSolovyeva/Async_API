from datetime import datetime
from typing import Optional
from pydantic import Field
from models.genre import ESFilmGenre
from models.mixin import BaseMixin
from models.person import ESFilmPerson


class Film(BaseMixin):
    """Filmworks on the homepage and search."""
    uuid: str
    title: str
    imdb_rating: float


class FilmDetailed(Film):
    """All information about the filmwork"""
    description: Optional[str]
    genres: Optional[list[ESFilmGenre]]
    actors: Optional[list[ESFilmPerson]]
    writers: Optional[list[ESFilmPerson]]
    directors: Optional[list[ESFilmPerson]]


class ESFilm(BaseMixin):
    """Модель описывающая document в Elasticserch."""
    uuid: str = Field(..., alias='id')
    imdb_rating: Optional[float]
    genres: Optional[list[ESFilmGenre]]
    title: str
    description: Optional[str]
    director: Optional[list[str]]
    actors_names: Optional[list[str]]
    writers_names: Optional[list[str]]
    directors: Optional[list[ESFilmPerson]]
    actors: Optional[list[ESFilmPerson]]
    writers: Optional[list[ESFilmPerson]]
    modified: datetime
