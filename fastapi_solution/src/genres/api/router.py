import uuid
from typing import List

from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Depends

from app.connections.elastic import get_es_connection
from app.serializers.query_params_classes import PaginationDataParams
from genres.models.genre import Genre
from genres.services.toolkit import GenresToolkit

router = APIRouter()


@router.get("/get/{genre_uid}", response_model=Genre)
async def genre_get_api(
    genre_uid: uuid.UUID,
    elastic: AsyncElasticsearch = Depends(get_es_connection),

) -> Genre:
    person = await GenresToolkit(elastic=elastic).get(pk=genre_uid)
    return person


@router.get("/get", response_model=List[Genre])
async def genres_get_list_api(
    pagination_data: PaginationDataParams = Depends(PaginationDataParams),
    elastic: AsyncElasticsearch = Depends(get_es_connection),
) -> List[Genre]:
    persons = await GenresToolkit(elastic=elastic).list(pagination_data=pagination_data)
    return persons
