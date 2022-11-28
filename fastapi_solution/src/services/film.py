from functools import lru_cache
from typing import Optional

from aioredis import Redis
from app.core.config import settings
from app.connections.elastic import get_es_connection
from app.connections.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.film import ESFilm, Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
    
    async def get_all_films_from_elastic(self, **params):
        page_size = params.get('page_size', settings.DEFAULT_PAGE_SIZE)
        page = params.get('page', settings.DEFAULT_PAGE_NUMBER)
        sort = params.get('sort', '')
        genre = params.get('genre', None)
        body = None
        if sort and str(sort)[0] == '-':
            sort = str(sort)[1:]+':desc'
        if genre:
            body = {
                'query': {
                    'nested': {
                        'path': "genres",
                        'query': {
                            'bool': {
                                'must': [
                                    {
                                        'match': {
                                            'genres.id': genre
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        films = await self.elastic.search(
            index='movies',
            body=body,
            params={
                'size': page_size,
                'from': page - 1,
                'sort': sort
            }
        )
        return [Film(uuid=doc['_id'], **doc['_source']).dict() for doc in films['hits']['hits']]

    async def get_by_id(self, film_id: str) -> Optional[ESFilm]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)
        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[ESFilm]:
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        return ESFilm(uuid=['_id'], **doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[ESFilm]:
        data = await self.redis.get(film_id)
        if not data:
            return None
        film = ESFilm.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: ESFilm):
        await self.redis.set(film.uuid, film.json(by_alias=True), expire=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_es_connection),
) -> FilmService:
    return FilmService(redis, elastic)
