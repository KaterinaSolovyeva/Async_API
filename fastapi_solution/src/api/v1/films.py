from http import HTTPStatus
from typing import Optional

from core.config import DEFAULT_PAGE_NUMBER, DEFAULT_PAGE_SIZE
from fastapi import APIRouter, Depends, HTTPException, Query
from models.film import ESFilm, Film, FilmDetailed
from pydantic import BaseModel
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    '/',
    response_model=list[Film],
    summary='All movies',
    description='Returns all filmworks'
)
async def get_all_filmworks(
    film_service: FilmService = Depends(get_film_service),
    sort: str = Query('', description='Sorting'),
    genre: str = Query(None, description='Filter by genre uuid', alias='filter[genre]'),
    page_size: int = Query(DEFAULT_PAGE_SIZE, description='Number of filmworks on page', alias='page[size]'),
    page: int = Query(DEFAULT_PAGE_NUMBER, description='Page number', alias='page[number]')
):
    """Returns all filmworks."""
    films = await film_service.get_all_films_from_elastic(
        page_size=page_size,
        page=page,
        sort=sort,
        genre=genre
    )
    return films

@router.get(
    '/{film_id}',
    response_model=FilmDetailed,
    summary='Information about the film',
    description='Returns information about a movie by its id',
)
async def film_details(
    film_id: str,
    film_service: FilmService = Depends(get_film_service)
) -> FilmDetailed:
    """Returns filmwork's detailed description."""
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Film not found')
    return FilmDetailed(uuid=film_id, **film.dict(by_alias=True))
