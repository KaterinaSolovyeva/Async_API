import uuid
from typing import List

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Depends
from fastapi.params import Query

from app.connections.elastic import get_es_connection
from app.connections.redis import get_redis
from app.serializers.query_params_classes import PaginationDataParams
from models.film import Film
from models.person import Person
from services.persons_toolkit import PersonsToolkit

router = APIRouter()


async def get_persons_toolkit(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_es_connection),
) -> PersonsToolkit:
    return PersonsToolkit(redis=redis, elastic=elastic)


@router.get("/search", response_model=List[Person])
async def get_filtered_persons(
    pagination_data: PaginationDataParams = Depends(PaginationDataParams),
    person_toolkit: PersonsToolkit = Depends(get_persons_toolkit),
    query: str = Query(None, description="Part of the person's data"),
) -> List[Person]:
    persons = await person_toolkit.persons_list(pagination_data=pagination_data, query=query)
    return persons


@router.get("/{person_uid}", response_model=Person)
async def person_get_api(
    person_uid: uuid.UUID,
    person_toolkit: PersonsToolkit = Depends(get_persons_toolkit)
) -> Person:
    person = await person_toolkit.get(pk=person_uid)
    return person


@router.get("/", response_model=List[Person])
async def persons_get_list_api(
    pagination_data: PaginationDataParams = Depends(PaginationDataParams),
    person_toolkit: PersonsToolkit = Depends(get_persons_toolkit)
) -> List[Person]:
    persons = await person_toolkit.list(pagination_data=pagination_data)
    return persons


@router.get("/{person_uid}/film", response_model=List[Film])
async def persons_get_films(
    person_uid: uuid.UUID,
    person_toolkit: PersonsToolkit = Depends(get_persons_toolkit)
) -> List[Film]:
    films = await person_toolkit.get_persons_films(pk=person_uid)
    return films
