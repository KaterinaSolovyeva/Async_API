import logging

import aioredis
import uvicorn as uvicorn
from api.v1 import films
from app.core.config import settings
from app.core.logger import LOGGING
from app.connections import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from app.core.router_v1 import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool(
        settings.REDIS_URL,
        minsize=10,
        maxsize=20
    )
    elastic.es = AsyncElasticsearch(hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}'])


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()

app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
