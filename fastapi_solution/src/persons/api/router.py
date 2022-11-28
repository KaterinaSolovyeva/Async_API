import uuid
from typing import List

from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Depends

from app.connections.elastic import get_es_connection
from app.serializers.query_params_classes import PaginationDataParams
from persons.models.person import Person
from persons.services.toolkit import PersonsToolkit

router = APIRouter()


@router.get("/get/{person_uid}", response_model=Person)
async def person_get_api(
    person_uid: uuid.UUID,
    elastic: AsyncElasticsearch = Depends(get_es_connection),

) -> Person:
    person = await PersonsToolkit(elastic=elastic).get(pk=person_uid)
    return person


@router.get("/get", response_model=List[Person])
async def persons_get_list_api(
    pagination_data: PaginationDataParams = Depends(PaginationDataParams),
    elastic: AsyncElasticsearch = Depends(get_es_connection),
) -> List[Person]:
    persons = await PersonsToolkit(elastic=elastic).list(pagination_data=pagination_data)
    return persons
